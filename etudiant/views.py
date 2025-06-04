from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .services import get_student_dashboard_data


# Create your views here.
@login_required(login_url='login_view')
def dashboard(request):
    context = get_student_dashboard_data(request.user)
    return render(request, 'etudiant/dashboard.html', context)

def schedule_view(request):
    pass

def grades_view(request):
    pass

def assignments_view(request):
    pass

def submit_assignment(request):
    pass

def add_event(request):
    pass