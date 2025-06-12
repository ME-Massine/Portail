from django.urls import path
from prof import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('matiere/', views.matiere, name='matiere'),
    path('matiere/<int:matiere_id>/ajouter-materiel/', views.ajouter_materiel, name='ajouter_materiel'),
    path('settings/', views.settings, name='settings'),
]
