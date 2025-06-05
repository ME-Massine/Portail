from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.db.models.functions import TruncMonth
from django.shortcuts import render, redirect
from django.utils import timezone

from prof.models import Note
from .services import get_student_dashboard_data


# Create your views here.
@login_required(login_url='login_view')
def dashboard(request):
    context = get_student_dashboard_data(request.user)
    return render(request, 'etudiant/dashboard.html', context)

def schedule_view(request):
    pass

def notes_view(request):
    grades = Note.objects.filter(
        etudiant=request.user
    ).select_related('matiere').order_by('-date_attribution')

    # Calculate statistics
    average = grades.aggregate(avg=Avg('valeur'))['avg']

    # Prepare data for charts
    grade_distribution = {
        '16-20': grades.filter(valeur__gte=16).count(),
        '12-15': grades.filter(valeur__gte=12, valeur__lt=16).count(),
        '8-11': grades.filter(valeur__gte=8, valeur__lt=12).count(),
        '0-7': grades.filter(valeur__lt=8).count()
    }

    # Prepare trend data (last 6 months)
    six_months_ago = timezone.now() - timedelta(days=180)
    monthly_trends = (
        grades.filter(date_attribution__gte=six_months_ago)
        .annotate(month=TruncMonth('date_attribution'))
        .values('month')
        .annotate(avg_grade=Avg('valeur'))
        .order_by('month')
    )

    context = {
        'grades': grades,
        'average_grade': round(average, 2) if average else None,
        'grade_distribution': grade_distribution,
        'monthly_trends': list(monthly_trends),
    }
    return render(request, "etudiant/notes.html", context)

def assignments_view(request):
    pass

def submit_assignment(request):
    pass

def add_event(request):
    pass