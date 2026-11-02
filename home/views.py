from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .models import *
# Create your views here.

def dash(request):
    return render(request, "home/dash.html")

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.info(request, 'Passwords do not match')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.info(request, 'Email already taken')
            return redirect('register')

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
        )
        user.set_password(password)
        user.set_password(confirm_password)
        user.save()
        messages.info(request, 'Account created successfully')

        return redirect('register')
    
    return render(request, "home/register.html", context={'title': 'Register', 'favicon': 'media/register.png'})

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not User.objects.filter(email=email).exists():
            messages.info(request, 'Email Invalid!')
            return redirect('login')

        user_obj = User.objects.get(email=email)
        user = authenticate(request, username=user_obj.username, password=password)
        if user:
            auth_login(request, user)
            return redirect('dash')
        else:
            messages.info(request, 'Invalid email or password!')
            return redirect('login')
    return render(request, "home/login.html", context={'title': 'Login', 'favicon': 'media/login.png'})

def logout_view(request):
    auth_logout(request)
    return redirect('dash')