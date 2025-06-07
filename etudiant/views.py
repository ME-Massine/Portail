from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from django.db.models.functions import TruncMonth
from django.shortcuts import render, redirect
from django.utils import timezone
import json

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
    best_grade = grades.order_by('-valeur').first()
    worst_grade = grades.order_by('valeur').first()
    total_grades = grades.count()

    # Prepare data for evolution chart
    six_months_ago = timezone.now() - timedelta(days=180)
    monthly_trends = (
        grades.filter(date_attribution__gte=six_months_ago)
        .annotate(month=TruncMonth('date_attribution'))
        .values('month')
        .annotate(avg_grade=Avg('valeur'))
        .order_by('month')
    )

    dates = [trend['month'].strftime('%b %Y') for trend in monthly_trends]
    values = [float(trend['avg_grade']) for trend in monthly_trends]

    # Prepare data for distribution chart
    distribution = [
        grades.filter(valeur__gte=16).count(),  # A grades
        grades.filter(valeur__gte=12, valeur__lt=16).count(),  # B grades
        grades.filter(valeur__lt=12).count(),  # C grades
    ]

    context = {
        'grades': grades,
        'average_grade': round(average, 2) if average else None,
        'best_grade': best_grade,
        'worst_grade': worst_grade,
        'total_grades': total_grades,
        'dates': json.dumps(dates),
        'values': json.dumps(values),
        'distribution': json.dumps(distribution),
    }
    return render(request, "etudiant/notes.html", context)

def assignments_view(request):
    pass

def submit_assignment(request):
    pass

def add_event(request):
    pass