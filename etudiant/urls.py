from django.urls import path
from etudiant import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),

]
