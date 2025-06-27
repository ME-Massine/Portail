from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from core.models import Matiere, Utilisateur
from etudiant.models import Absence


# Create your views here.
class AdminDashboardView(TemplateView):
    template_name = "school_admin/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        role = request.GET.get('role')
        recent_users_qs = Utilisateur.objects.all()
        if role in ['etudiant', 'professeur', 'administrateur']:
            recent_users_qs = recent_users_qs.filter(role=role)
        recent_users = recent_users_qs.order_by('-date_joined')[:10]
        context.update({
            "total_students": Utilisateur.objects.filter(role="etudiant").count(),
            "total_professors": Utilisateur.objects.filter(role="professeur").count(),
            "total_courses": Matiere.objects.count(),
            "total_absences": Absence.objects.count(),
            "recent_users": recent_users,
            "professors": Utilisateur.objects.filter(role="professeur"),  # For course modal
            "filières": Utilisateur.FILLIERE_CHOICES,  # Add filière choices for the modal
            "students": Utilisateur.objects.filter(role="etudiant"),  # For absence modal
            "courses": Matiere.objects.all(),  # For absence modal
        })
        return context


def add_user(request):
    if request.method == 'POST':
        User = get_user_model()
        email = request.POST.get('email')
        role = request.POST.get('role')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        filliere = request.POST.get('filière', '')

        # Generate a username from the email (before the @)
        username = email.split('@')[0]

        user = Utilisateur.objects.create_user(
            username=username,
            email=email,
            role=role,
            first_name=first_name,
            last_name=last_name,
            password="defaultpassword",
            filliere=filliere
        )
        return redirect('school_admin:dashboard')
    return render(request, 'school_admin/dashboard.html')




def add_course(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        nom = request.POST.get('name')
        coefficient = request.POST.get('coefficient', 1)
        professor_id = request.POST.get('professor')

        matiere = Matiere.objects.create(
            code=code,
            nom=nom,
            coefficient=coefficient
        )
        if professor_id:
            matiere.professeurs.add(professor_id)
        return redirect('school_admin:dashboard')
    return render(request, 'school_admin/dashboard.html')




def add_absence(request):
    if request.method == 'POST':
        student_id = request.POST.get('student')
        date = request.POST.get('date')
        reason = request.POST.get('reason')
        course_id = request.POST.get('course')
        justifiee = bool(request.POST.get('justifiee'))

        absence_kwargs = {
            'etudiant_id': student_id,
            'date': date,
            'commentaire': reason,
            'justifiee': justifiee
        }
        if course_id:
            absence_kwargs['matiere_id'] = course_id

        Absence.objects.create(**absence_kwargs)
        return redirect('school_admin:dashboard')

    students = Utilisateur.objects.filter(role='ETUDIANT')
    return render(request, 'school_admin/add_absence.html', {'students': students})