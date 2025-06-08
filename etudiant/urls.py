from django.urls import path
from etudiant import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('courses/', views.cours_view, name='courses'),
    path('emploi/', views.emploi_du_temps, name='emploi'),
    path('Notes/', views.notes_view, name='notes'),
    path('devoirs/', views.devoirs_view, name='devoirs'),
    path('submit-assignment/', views.submit_assignment, name='submit_assignment'),
    path('add_event/', views.add_event, name='add_event'),
    path('materiaux/', views.voir_materiaux, name='voir_materiaux'),

]
