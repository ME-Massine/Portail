from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class Utilisateur(AbstractUser):
    ROLE_CHOICES = (
        ('school_admin', 'Administrateur'),
        ('professeur', 'Professeur'),
        ('etudiant', 'Étudiant'),
    )
    FILLIERE_CHOICES = (
        ('Informatique', 'Informatique'),
        ('Finance', 'Finance'),
        ('Industruelle', 'Industruelle'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    date_naissance = models.DateField(null=True, blank=True)
    telephone = models.CharField(max_length=20, blank=True)
    adresse = models.TextField(blank=True)
    date_inscription = models.DateTimeField(auto_now_add=True)
    filliere=models.CharField(max_length=20,choices=FILLIERE_CHOICES,blank=True)


    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"

    def moyenne_generale(self):
        """Calculate student's overall average"""
        if self.role == 'etudiant':
            notes = self.notes.all()
            if notes.exists():
                total = sum(note.valeur * note.matiere.coefficient for note in notes)
                total_coeff = sum(note.matiere.coefficient for note in notes)
                return total / total_coeff
        return 0

class Matiere(models.Model):
    code = models.CharField(max_length=20, unique=True)
    nom = models.CharField(max_length=100)
    coefficient = models.IntegerField(default=1)
    professeurs = models.ManyToManyField(
        Utilisateur,
        related_name='matieres_enseignees',
        limit_choices_to={'role': 'professeur'}
    )

    class Meta:
        verbose_name = "Matière"
        verbose_name_plural = "Matières"
        ordering = ['nom']

    def __str__(self):
        return f"{self.code} - {self.nom}"

    def calculer_moyenne(self):
        """Calculate average grade for this subject"""
        notes = self.note_set.all()
        if notes.exists():
            total = sum(note.valeur for note in notes)
            return total / len(notes)
        return 0

class EmploiDuTemps(models.Model):
    JOURS_SEMAINE = (
        ('LUN', 'Lundi'),
        ('MAR', 'Mardi'),
        ('MER', 'Mercredi'),
        ('JEU', 'Jeudi'),
        ('VEN', 'Vendredi'),
        ('SAM', 'Samedi'),
    )

    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    jour = models.CharField(max_length=3, choices=JOURS_SEMAINE)
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    salle = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Emploi du temps"
        verbose_name_plural = "Emplois du temps"
        ordering = ['jour', 'heure_debut']
        constraints = [
            models.UniqueConstraint(
                fields=['jour', 'heure_debut', 'salle'],
                name='unique_schedule_slot'
            ),
            models.UniqueConstraint(
                fields=['matiere', 'jour', 'heure_debut'],
                name='unique_subject_schedule'
            )
        ]

    def __str__(self):
        return f"{self.matiere} - {self.get_jour_display()} {self.heure_debut}-{self.heure_fin}"

class Message(models.Model):
    expediteur = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='messages_envoyes'
    )
    destinataire = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='messages_recus'
    )
    contenu = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    lu = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ['-date_envoi']

    def __str__(self):
        return f"De {self.expediteur} à {self.destinataire} ({self.date_envoi})"

class Inscription(models.Model):
    etudiant = models.ForeignKey(
        'core.Utilisateur',
        on_delete=models.CASCADE,
        related_name='inscriptions',
        limit_choices_to={'role': 'etudiant'}
    )
    matiere = models.ForeignKey('core.Matiere', on_delete=models.CASCADE)
    date_inscription = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('etudiant', 'matiere')
        verbose_name = "Inscription"
        verbose_name_plural = "Inscriptions"

    def __str__(self):
        return f"{self.etudiant} inscrit à {self.matiere}"

class StudentProxy(Utilisateur):
    class Meta:
        proxy = True
        verbose_name = "Étudiant"
        verbose_name_plural = "Étudiants"

    def get_absences(self):
        return self.absences.all()