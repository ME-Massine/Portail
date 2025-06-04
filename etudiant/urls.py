from django.urls import path
from etudiant import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('schedule/', views.schedule_view, name='schedule'),
    path('grades/', views.grades_view, name='grades'),
    path('assignments/', views.assignments_view, name='assignments'),
    path('submit-assignment/', views.submit_assignment, name='submit_assignment'),
    path('add_event/', views.add_event, name='add_event'),
    # etc.

]
