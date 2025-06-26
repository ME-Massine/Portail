from django import forms
from etudiant.models import AssignmentSubmission
from prof.models import Assignment
from core.models import Inscription
from prof.models import LectureMaterial


class LectureMaterialForm(forms.ModelForm):
    class Meta:
        model = LectureMaterial
        fields = ['title', 'file', 'is_visible']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_visible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class AssignmentCreateForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['matiere', 'title', 'description', 'due_date','file']
        widgets = {
            'matiere': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['matiere'].queryset = user.matieres_enseignees.all()