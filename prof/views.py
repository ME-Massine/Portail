from collections import defaultdict
from datetime import timedelta, datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from core.models import EmploiDuTemps, Inscription, Matiere, Utilisateur
from etudiant.models import AssignmentSubmission
from prof.forms import LectureMaterialForm
from prof.models import Note


# Create your views here.
@login_required(login_url='login_view')
def dashboard(request):
    profInfo = request.user
    today = timezone.now().date()

    weekday_map = {
        0: 'LUN',
        1: 'MAR',
        2: 'MER',
        3: 'JEU',
        4: 'VEN',
        5: 'SAM',
        6: 'DIM',
    }
    today_jour = weekday_map[today.weekday()]

    cours = EmploiDuTemps.objects.filter(
        jour=today_jour,
        matiere__professeurs=profInfo
    )

    nb_cours = cours.count()

    matiere = cours.values_list('matiere__id', flat=True).distinct()

    nb_etudiants = Inscription.objects.filter(
        matiere__id__in=matiere
    ).values('etudiant').distinct().count()

    # Get inscriptions in these matieres
    prof_matieres = profInfo.matieres_enseignees.all()

    # Get inscriptions for those subjects
    inscriptions = Inscription.objects.filter(matiere__in=prof_matieres)

    # Count all submissions related to those inscriptions
    nb_submissions = AssignmentSubmission.objects.filter(inscription__in=inscriptions).count()

    nb_matieres = profInfo.matieres_enseignees.count()

    prof_courses = EmploiDuTemps.objects.filter(matiere__professeurs=profInfo)

    total_duration = timedelta()
    for course in prof_courses:
        duration = datetime.combine(timezone.now(), course.heure_fin) - datetime.combine(timezone.now(),
                                                                                         course.heure_debut)
        total_duration += duration

    total_seconds = total_duration.total_seconds()
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    total_hours_formatted = f"{hours}h{minutes}min"

    return render(request, 'prof/dashboard.html', {'profInfo': profInfo,
                                                   'nb_cours': nb_cours,
                                                   'nb_etudiants': nb_etudiants,
                                                   'nb_submissions': nb_submissions,
                                                   'nb_matieres': nb_matieres,
                                                   'total_hours_formatted': total_hours_formatted,
                                                   'cours': cours})


def matiere(request):
    matieres_enseignees = request.user.matieres_enseignees.all()

    return render(request, 'prof/matiere.html', {'matieres_enseignees': matieres_enseignees})


@login_required
def ajouter_materiel(request, matiere_id):
    matiere = get_object_or_404(Matiere, id=matiere_id, professeurs=request.user)

    if request.method == 'POST':
        form = LectureMaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.matiere = matiere
            material.save()
            return redirect('prof:matiere')  # Replace with your actual URL name
    else:
        form = LectureMaterialForm()

    return render(request, 'prof/ajouter_materiel.html', {'form': form, 'matiere': matiere})


def settings(request):
    return render(request, 'prof/settings.html')


def emploi(request):
    user = request.user



    # Récupérer les matières enseignées par ce professeur
    matieres = user.matieres_enseignees.all()

    # Récupérer les cours associés à ses matières
    entries = EmploiDuTemps.objects.filter(matiere__in=matieres).select_related('matiere').order_by('jour',
                                                                                                    'heure_debut')

    # Organiser dans une structure à deux niveaux : [jour][heure]
    timetable = defaultdict(dict)
    for entry in entries:
        heure_str = entry.heure_debut.strftime("%H:%M")
        timetable[entry.jour][heure_str] = entry

    # Aplatir les clés pour le template
    flat_timetable = {}
    for jour, slots in timetable.items():
        for heure, slot in slots.items():
            key = f"{jour},{heure}"
            flat_timetable[key] = slot

    jours = ['LUN', 'MAR', 'MER', 'JEU', 'VEN', 'SAM']
    heures = [f"{h:02d}:00" for h in range(8, 19)]

    context = {
        'flat_timetable': flat_timetable,
        'jours': jours,
        'heures': heures
    }
    return render(request, 'prof/emploi.html', context)

@login_required
def notes(request):
    # Only show matieres taught by this prof
    matieres = request.user.matieres_enseignees.all().order_by('nom')

    # For each matiere, get enrolled students
    matiere_etudiants = {}
    for matiere in matieres:
        inscriptions = Inscription.objects.filter(matiere=matiere)
        matiere_etudiants[matiere.id] = [
            {
                'id': insc.etudiant.id,
                'name': f"{insc.etudiant.first_name} {insc.etudiant.last_name}"
            }
            for insc in inscriptions
        ]

    if request.method == 'POST':
        etudiant_id = request.POST.get('etudiant')
        matiere_id = request.POST.get('matiere')
        valeur = request.POST.get('valeur')
        commentaire = request.POST.get('commentaire', '')
        date_attribution = request.POST.get('date_attribution')
        type_note = request.POST.get('type_note')

        erreurs = []

        # Validation simple
        try:
            valeur = float(valeur)
            if not (0 <= valeur <= 20):
                erreurs.append("La note doit être comprise entre 0 et 20.")
        except (ValueError, TypeError):
            erreurs.append("Valeur de note invalide.")

        if not etudiant_id or not matiere_id or not type_note or not date_attribution:
            erreurs.append("Tous les champs obligatoires doivent être remplis.")

        # Récupérer objets liés
        try:
            etudiant = Utilisateur.objects.get(id=etudiant_id, role='etudiant')
        except Utilisateur.DoesNotExist:
            erreurs.append("Étudiant invalide.")

        try:
            matiere = Matiere.objects.get(id=matiere_id)
        except Matiere.DoesNotExist:
            erreurs.append("Matière invalide.")

        if erreurs:
            recent_notes = Note.objects.filter(attribue_par=request.user).order_by('-date_attribution')[:10]
            context = {
                'matieres': matieres,
                'matiere_etudiants': matiere_etudiants,
                'erreurs': erreurs,
                'recent_notes': recent_notes,
                'form_values': request.POST,
            }
            return render(request, 'prof/notation.html', context)

        # Créer et sauvegarder la note (plus de matiere_enseignee)
        note = Note.objects.create(
            etudiant=etudiant,
            matiere=matiere,
            valeur=valeur,
            commentaire=commentaire,
            date_attribution=date_attribution,
            attribue_par=request.user,
            type_note=type_note
        )

        return redirect('prof:notes')

    # GET: afficher formulaire et notes récentes
    recent_notes = Note.objects.filter(attribue_par=request.user).order_by('-date_attribution')[:10]

    context = {
        'matieres': matieres,
        'matiere_etudiants': matiere_etudiants,
        'recent_notes': recent_notes,
    }
    return render(request, 'prof/notation.html', context)

