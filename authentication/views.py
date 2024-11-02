from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
# Create your views here.


def auth_page(request):
    if request.method == "POST":
        email = request.POST['login']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('index') 
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, 'authentication/auth.html')


def custom_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('auth-page')  


def register(request):
    return render(request, 'authentication/register.html')