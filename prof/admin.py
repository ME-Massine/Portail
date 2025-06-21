from django.contrib import admin

from prof.models import Note, LectureMaterial, Assignment

# Register your models here.
admin.site.register(Note)
admin.site.register(LectureMaterial)
admin.site.register(Assignment)
