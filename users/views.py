from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
import logging

# Set up logging
logger = logging.getLogger(__name__)

def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_dashboard')
        return redirect('user_dashboard')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            logger.info("User %s authenticated", username)
            if user.is_superuser:
                return redirect('admin_dashboard')
            return redirect('user_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
            logger.warning("Authentication failed for username: %s", username)
    return render(request, 'users/login.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            username = request.user.username
            logout(request)
            messages.success(request, 'Logged out successfully!')
            logger.info("User %s logged out", username)
        else:
            messages.info(request, 'You are already logged out.')
        return redirect('landing')
    else:
        messages.error(request, 'Please use the logout button to log out.')
        return redirect('dashboard')

def admin_dashboard(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('user_dashboard')
    return render(request, 'admin_dashboard.html')

def user_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.is_superuser:
        return redirect('admin_dashboard')
    return render(request, 'user_dashboard.html')

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.is_superuser:
        return redirect('admin_dashboard')
    return redirect('user_dashboard')