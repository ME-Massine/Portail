from django import forms

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