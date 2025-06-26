from django.urls import path
from prof import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('matiere/', views.matiere, name='matiere'),
    path('matiere/<int:matiere_id>/ajouter-materiel/', views.ajouter_materiel, name='ajouter_materiel'),
    path('settings/', views.settings, name='settings'),
    path('emploi/', views.emploi, name='emploi'),
    path('notes/', views.notes, name='notes'),
    path('materiaux/',views.voir_materiaux,name='voir_materiaux'),
    path('devoir/',views.devoir,name='devoir'),
]
