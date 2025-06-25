from django.db.models import Avg
from django.utils import timezone
from core.models import Utilisateur, Matiere, EmploiDuTemps, Inscription, Message
from etudiant.models import Absence, AssignmentSubmission
from prof.models import Note, LectureMaterial, Assignment


def get_student_dashboard_data(student):
    # Get all courses the student is enrolled in
    courses = Matiere.objects.filter(
        inscription__etudiant=student
    ).distinct()

    # Calculate average grade
    nb_Absence = Absence.objects.filter(
        etudiant=student
    ).count()

    # Get current weekday in your format (3-letter uppercase)
    today = timezone.now()
    # French weekday mapping
    weekday_map = {
        'MON': 'LUN',
        'TUE': 'MAR',
        'WED': 'MER',
        'THU': 'JEU',
        'FRI': 'VEN',
        'SAT': 'SAM',
    }

    weekday = weekday_map[today.strftime('%a').upper()]

    # Alternative approach - get courses first, then schedules
    student_course_ids = student.inscriptions.values_list('matiere_id', flat=True)
    todays_classes = EmploiDuTemps.objects.filter(
        matiere_id__in=student_course_ids,
        jour=weekday
    ).order_by('heure_debut')

    # Get pending assignments (submissions not yet made)
    pending_assignments = []
    for inscription in student.inscriptions.select_related('matiere'):
        assignments = Assignment.objects.filter(matiere=inscription.matiere)
        for assignment in assignments:
            has_submitted = AssignmentSubmission.objects.filter(
                assignment=assignment,
                inscription=inscription
            ).exists()
            if not has_submitted:
                pending_assignments.append({
                    'title': assignment.title,
                    'matiere': inscription.matiere,
                    'due_date': assignment.due_date,
                    'description': assignment.description,
                })

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
        'nb_Absence': nb_Absence,
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