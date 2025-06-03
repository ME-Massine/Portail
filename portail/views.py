from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages


# Create your views here.
def login_view(request):
    form = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, 'Both username and password are required.')
            return render(request, 'login.html')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)

                if user.role is not None:
                    if user.role == 'professeur':
                        return redirect('prof:dashboard')
                    elif user.role == 'etudiant':
                        return redirect('etudiant:dashboard')
                    elif user.role == 'administrateur':
                        return redirect('school_admin:dashboard')
                    else:
                        messages.warning(request, 'Your account has no assigned role. Please contact support.')
                        return render(request, 'login.html')
                else:
                    messages.warning(request, 'Your account is not assigned to any role. Please contact support.')
                    return render(request, 'login.html')
            else:
                # Account is inactive
                messages.error(request, 'Your account is inactive. Please contact support.')
                return render(request, 'login.html')
        else:
            # Authentication failed
            messages.error(request, 'Invalid username or password.')
            return render(request, 'login.html')

    return render(request, 'login.html')
