from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from django.db.models.functions import TruncMonth
from django.shortcuts import render, redirect
from django.utils import timezone
import json

from .models import AssignmentSubmission
from core.models import Matiere, Inscription
from prof.models import Note, LectureMaterial
from .services import get_student_dashboard_data


# Create your views here.
@login_required(login_url='login_view')
def dashboard(request):
    context = get_student_dashboard_data(request.user)
    return render(request, 'etudiant/dashboard.html', context)


def schedule_view(request):
    pass


def cours_view(request):
    user = request.user

    # Get all course inscriptions for the logged-in student
    inscriptions = Inscription.objects.filter(etudiant=user).select_related('matiere')
    matieres = [inscription.matiere for inscription in inscriptions]

    # Fetch lecture material and assignment counts per subject
    course_data = []
    for matiere in matieres:
        profs = matiere.professeurs.all()
        materials_count = LectureMaterial.objects.filter(matiere=matiere, is_visible=True).count()
        submissions_count = AssignmentSubmission.objects.filter(
            inscription__etudiant=user, inscription__matiere=matiere
        ).count()

        course_data.append({
            'matiere': matiere,
            'professeurs': profs,
            'materials_count': materials_count,
            'submissions_count': submissions_count,
            'inscription_date': inscriptions.get(matiere=matiere).date_inscription,
        })

    # Basic stats
    total_courses = len(course_data)
    total_materials = sum(item['materials_count'] for item in course_data)
    total_submissions = sum(item['submissions_count'] for item in course_data)

    # Distribution of course enrollment over past 6 months
    six_months_ago = timezone.now() - timedelta(days=180)
    monthly_distribution = (
        Inscription.objects.filter(etudiant=user, date_inscription__gte=six_months_ago)
        .annotate(month=TruncMonth('date_inscription'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    chart_dates = [entry['month'].strftime('%b %Y') for entry in monthly_distribution]
    chart_values = [entry['count'] for entry in monthly_distribution]

    context = {
        'course_data': course_data,
        'total_courses': total_courses,
        'total_materials': total_materials,
        'total_submissions': total_submissions,
        'chart_dates': json.dumps(chart_dates),
        'chart_values': json.dumps(chart_values),
    }

    return render(request, "etudiant/cours.html", context)


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
