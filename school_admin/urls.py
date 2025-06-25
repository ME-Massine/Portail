from django.contrib import admin
from django.urls import path, include

from school_admin import views
from django.conf import settings

urlpatterns = [
    path('', views.AdminDashboardView.as_view(), name='dashboard'),
    path('add-user/', views.add_user, name='add_user'),
    path('add-course/', views.add_course, name='add_course'),
    path('add-absence/', views.add_absence, name='add_absence'), ]
