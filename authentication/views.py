from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from home.models import Tourist
from django.contrib.auth.models import Group
# Create your views here.


def auth_page(request):

    if request.method == "POST":
        email = request.POST['login']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)

            if user.groups.filter(name='staff').exists():
                return redirect('dashboard')
            elif user.groups.filter(name='manager').exists():
                return redirect('user_accomodation')
            else:
                return redirect('index')
        else:
            messages.error(request, "Invalid email or password.")
    
    return render(request, 'authentication/auth.html')

def custom_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('auth-page')  


def register(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']

        # Check if the email or username already exists
        if User.objects.filter(username=email).exists():
            messages.error(request, "Email is already taken.")
            return render(request, 'authentication/register.html')
        if User.objects.filter(email=email).exists():
            messages.error(request, "An account with this email already exists.")
            return render(request, 'authentication/register.html')
        
        # Create the user
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password, 
            first_name=firstname, 
            last_name=lastname
        )
        user.save()

        tourist = Tourist.objects.create(
            user = user,
        )

        tourist.save()

        # Send confirmation email
        subject = 'Welcome to PangasinanExpo!'
        message = f'Hello {firstname},\n\nThank you for registering at PangasinanExpo. Your account has been successfully created.'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        # Add a success message
        messages.success(request, "Registration successful! You can now log in.")

        return redirect('auth-page')

    return render(request, 'authentication/register.html')