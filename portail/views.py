from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages


# Create your views here.
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            user_group = request.user.groups.first()
            if user_group:
                if user_group.name == 'prof':
                    return redirect('prof:dashboard')
                if user_group.name == 'etudiant':
                    return redirect('etudiant:dashboard')
                if user_group.name == 'admin':
                    return redirect('admin:dashboard')

        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')
