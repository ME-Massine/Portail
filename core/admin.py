from django.contrib import admin

from core.models import Utilisateur, Matiere, EmploiDuTemps, Message, Inscription, StudentProxy

# Register your models here.
admin.site.register(Utilisateur)
admin.site.register(Matiere)
admin.site.register(EmploiDuTemps)
admin.site.register(Message)
admin.site.register(Inscription)
