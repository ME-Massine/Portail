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
        context.update({
            "total_students": Utilisateur.objects.filter(role="etudiant").count(),
            "total_professors": Utilisateur.objects.filter(role="professeur").count(),
            "recent_users": Utilisateur.objects.order_by("-date_joined")[:5],
            "professors": Utilisateur.objects.filter(role="professeur"),  # For course modal
        })
        return context


def add_user(request):
    if request.method == 'POST':
        User = get_user_model()
        email = request.POST.get('email')
        role = request.POST.get('role')
        full_name = request.POST.get('full_name')

        # Create user (simplified example)
        user = Utilisateur.objects.create_user(
            email=email,
            role=role,
            first_name=full_name.split()[0],
            last_name=full_name.split()[-1],
            password="defaultpassword"  # Force password reset later
        )
        return redirect('school_admin:dashboard')
    return render(request, 'school_admin/dashboard.html')




def add_course(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        name = request.POST.get('name')
        professor_id = request.POST.get('professor')

        Matiere.objects.create(
            code=code,
            name=name,
            professeur_id=professor_id
        )
        return redirect('school_admin:dashboard')
    return render(request, 'school_admin/dashboard.html')




def add_absence(request):
    if request.method == 'POST':
        student_id = request.POST.get('student')
        date = request.POST.get('date')
        reason = request.POST.get('reason')

        Absence.objects.create(
            etudiant_id=student_id,
            date=date,
            raison=reason
        )
        return redirect('school_admin:dashboard')

    students = Utilisateur.objects.filter(role='ETUDIANT')
    return render(request, 'school_admin/add_absence.html', {'students': students})