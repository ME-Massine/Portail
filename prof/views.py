from datetime import timedelta, datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone

from core.models import EmploiDuTemps, Inscription
from etudiant.models import AssignmentSubmission


# Create your views here.
@login_required(login_url='login_view')
def dashboard(request):

    profInfo=request.user
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

    cours= EmploiDuTemps.objects.filter(
        jour=today_jour,
        matiere__professeurs=profInfo
    )

    nb_cours = cours.count()

    matiere = cours.values_list('matiere__id', flat=True).distinct()

    nb_etudiants = Inscription.objects.filter(
        matiere__id__in=matiere
    ).values('etudiant').distinct().count()

    matiere_ids = cours.values_list('matiere__id', flat=True).distinct()

    # Get inscriptions in these matieres
    prof_matieres = profInfo.matieres_enseignees.all()

    # Get inscriptions for those subjects
    inscriptions = Inscription.objects.filter(matiere__in=prof_matieres)

    # Count all submissions related to those inscriptions
    nb_submissions = AssignmentSubmission.objects.filter(inscription__in=inscriptions).count()

    nb_matieres = profInfo.matieres_enseignees.count()



    prof_courses = EmploiDuTemps.objects.filter(matiere__professeurs=profInfo)

    total_duration = timedelta()
    for cours in prof_courses:
        duration = datetime.combine(timezone.now(), cours.heure_fin) - datetime.combine(timezone.now(),cours.heure_debut)
        total_duration += duration

    total_seconds = total_duration.total_seconds()
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    total_hours_formatted = f"{hours}h{minutes}min"

    return render(request, 'prof/dashboard.html', {'profInfo':profInfo ,
                                                   'nb_cours':nb_cours,
                                                   'nb_etudiants':nb_etudiants,
                                                   'nb_submissions':nb_submissions,
                                                   'nb_matieres':nb_matieres,
                                                   'total_hours_formatted':total_hours_formatted})