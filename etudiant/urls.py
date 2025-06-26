from django.urls import path
from etudiant import views
from django.contrib.auth import views as auth_views
from etudiant.views import CustomPasswordChangeView

app_name = 'etudiant'
urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('courses/', views.cours_view, name='courses'),
    path('emploi/', views.emploi_du_temps, name='emploi'),
    path('Notes/', views.notes_view, name='notes'),
    path('devoirs/', views.devoirs_view, name='devoirs'),
    path('materiaux/', views.voir_materiaux, name='voir_materiaux'),
    path('settings/', views.settings, name='settings'),
    path('messages/', views.messages_view, name='messages'),
    path('messages/<int:professor_id>/', views.chat_with_professor, name='chat_with_professor'),
    path('password-change/',
         CustomPasswordChangeView.as_view(),
         name='password_change'),

    path('password-change/done/',
         auth_views.PasswordChangeDoneView.as_view(
             template_name='etudiant/password_change_done.html'
         ),
         name='password_change_done'),
]
