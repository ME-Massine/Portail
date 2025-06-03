from django.urls import path
from core import views

urlpatterns = [
    path('logout/', views.logout_view, name='logout'),

]
