from django.utils import timezone
from django.db import models

from core.models import Utilisateur, Matiere


# Create your models here.
class AssignmentSubmission(models.Model):
    inscription = models.ForeignKey('core.Inscription', on_delete=models.CASCADE)
    file = models.FileField(upload_to='submissions/%Y/%m/%d/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    assignment_title = models.CharField(max_length=200)
    is_late = models.BooleanField(default=False)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = "Devoir rendu"
        verbose_name_plural = "Devoirs rendus"

class Absence(models.Model):
    etudiant = models.ForeignKey(
        'core.Utilisateur',
        on_delete=models.CASCADE,
        related_name='absences',
        limit_choices_to={'role': 'etudiant'}
    )
    matiere = models.ForeignKey('core.Matiere', on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(default=timezone.now)
    justifiee = models.BooleanField(default=False)
    commentaire = models.TextField(blank=True)

    class Meta:
        verbose_name = "Absence"
        verbose_name_plural = "Absences"
        ordering = ['-date']

    def __str__(self):
        status = "Justifiée" if self.justifiee else "Non justifiée"
        return f"Absence de {self.etudiant} le {self.date} ({status})"
