from django.urls import path
from prof import views

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
]
