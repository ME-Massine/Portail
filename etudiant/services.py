from django.db.models import Avg
from django.utils import timezone
from core.models import Utilisateur, Matiere, EmploiDuTemps, Inscription, Message
from etudiant.models import Absence, AssignmentSubmission
from prof.models import Note


def get_student_dashboard_data(student):
    today = timezone.now().date()
    weekday = today.strftime('%a').upper()[:3]  # Get weekday abbreviation (LUN, MAR, etc.)

    # Get all courses the student is enrolled in
    courses = Matiere.objects.filter(
        inscription__etudiant=student
    ).distinct()

    # Calculate average grade
    average_grade = Note.objects.filter(
        etudiant=student
    ).aggregate(avg_grade=Avg('valeur'))['avg_grade'] or 0

    # Get today's schedule
    todays_classes = EmploiDuTemps.objects.filter(
        matiere__inscription__etudiant=student,
        jour=weekday
    ).order_by('heure_debut').select_related('matiere')

    # Get pending assignments (submissions not yet made)
    pending_assignments = []
    for inscription in student.inscriptions.all():
        # Get all assignment titles that exist in submissions for this course
        submitted_titles = AssignmentSubmission.objects.filter(
            inscription=inscription
        ).values_list('assignment_title', flat=True)

        # Get recent assignment titles that haven't been submitted
        pending_assignments.extend([
            {'title': title, 'matiere': inscription.matiere}
            for title in get_recent_assignment_titles(inscription.matiere)
            if title not in submitted_titles
        ])

    # Calculate attendance stats
    total_classes = EmploiDuTemps.objects.filter(
        matiere__inscription__etudiant=student
    ).count()
    absences = Absence.objects.filter(etudiant=student).count()
    attendance_rate = ((total_classes - absences) / total_classes * 100) if total_classes else 100

    return {
        'courses': courses,
        'recent_grades': Note.objects.filter(
            etudiant=student
        ).select_related('matiere').order_by('-date_attribution')[:5],
        'average_grade': average_grade,
        'todays_classes': todays_classes,
        'pending_assignments': pending_assignments,
        'attendance_stats': {
            'total_classes': total_classes,
            'absences': absences,
            'attendance_rate': attendance_rate
        },
        'unread_messages': Message.objects.filter(
            destinataire=student,
            lu=False
        ).count()
    }


def get_recent_assignment_titles(matiere):
    """Helper function to get recent assignment titles for a course"""
    return [
        'Projet Final',
        'Examen Partiel',
        'TP 1',
        'TP 2',
        'Rapport de Recherche'
]