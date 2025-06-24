from django import forms
from etudiant.models import AssignmentSubmission
from prof.models import Assignment
from core.models import Inscription

class AssignmentSubmissionForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmission
        fields = ['assignment', 'file']
        widgets = {
            'assignment': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # Only show assignments for the student's courses
            inscriptions = Inscription.objects.filter(etudiant=user)
            matieres = [insc.matiere for insc in inscriptions]
            assignments = Assignment.objects.filter(matiere__in=matieres)
            # Exclude assignments already submitted by this student
            submitted_assignment_ids = AssignmentSubmission.objects.filter(
                inscription__etudiant=user
            ).values_list('assignment_id', flat=True)
            self.fields['assignment'].queryset = assignments.exclude(id__in=submitted_assignment_ids)