from django.contrib import admin

from etudiant.models import AssignmentSubmission, Absence

# Register your models here.
admin.site.register(AssignmentSubmission)
admin.site.register(Absence)
