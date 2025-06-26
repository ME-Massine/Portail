from django.urls import path
from django.contrib.auth import views as auth_views
from etudiant.views import CustomPasswordChangeView
from prof import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('matiere/', views.matiere, name='matiere'),
    path('matiere/<int:matiere_id>/ajouter-materiel/', views.ajouter_materiel, name='ajouter_materiel'),
    path('settings/', views.settings, name='settings'),
    path('emploi/', views.emploi, name='emploi'),
    path('notes/', views.notes, name='notes'),
    path('materiaux/', views.voir_materiaux, name='voir_materiaux'),
    path('devoir/', views.devoir, name='devoir'),
    path('messages/', views.messages_view, name='messages'),
    path('messages/<int:student_id>/', views.chat_with_student, name='chat_with_student'),
    path('password-change/',
         CustomPasswordChangeView.as_view(),
         name='password_change'),

    path('password-change/done/',
         auth_views.PasswordChangeDoneView.as_view(
             template_name='prof/password_change_done.html'
         ),
         name='password_change_done'),
]
