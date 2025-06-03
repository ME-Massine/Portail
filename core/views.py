from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


# Create your views here.
@login_required(login_url='login_view')
def logout_view(request):
    logout(request)
    return redirect('login_view')