from django.db import models
from django.utils import timezone

from core.models import Utilisateur, Matiere


# Create your models here.
class Note(models.Model):
    inscription = models.ForeignKey('core.Inscription', on_delete=models.CASCADE)
    etudiant = models.ForeignKey(
        'core.Utilisateur',
        on_delete=models.CASCADE,
        related_name='notes',
        limit_choices_to={'role': 'etudiant'}
    )
    matiere = models.ForeignKey('core.Matiere', on_delete=models.CASCADE)
    valeur = models.FloatField()
    commentaire = models.TextField(blank=True)
    date_attribution = models.DateTimeField(default=timezone.now)
    attribue_par = models.ForeignKey(
        'core.Utilisateur',
        on_delete=models.SET_NULL,
        null=True,
        related_name='notes_attribuees',
        limit_choices_to={'role': 'professeur'}
    )

    class Meta:
        verbose_name = "Note"
        verbose_name_plural = "Notes"
        ordering = ['-date_attribution']

    def __str__(self):
        return f"{self.valeur}/20 - {self.etudiant} ({self.matiere})"

class LectureMaterial(models.Model):
    matiere = models.ForeignKey('core.Matiere', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='lectures/%Y/%m/%d/')
    upload_date = models.DateTimeField(auto_now_add=True)
    is_visible = models.BooleanField(default=True)

    class Meta:
        ordering = ['-upload_date']