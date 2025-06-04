from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
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
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        try:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}! Logged in successfully.')
                logger.info("User %s authenticated from IP %s", username, request.META.get('REMOTE_ADDR', 'unknown'))
                if user.is_superuser:
                    return redirect('admin_dashboard')
                return redirect('user_dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
                logger.warning("Authentication failed for username: %s from IP %s", username, request.META.get('REMOTE_ADDR', 'unknown'))
        except Exception as e:
            messages.error(request, 'An error occurred during login. Please try again.')
            logger.error("Login error for username: %s from IP %s - %s", username, request.META.get('REMOTE_ADDR', 'unknown'), str(e))
    return render(request, 'users/login.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        try:
            if form.is_valid():
                user = form.save()
                messages.success(request, f'Registration successful for {user.username}! Please log in.')
                logger.info("User %s registered from IP %s", user.username, request.META.get('REMOTE_ADDR', 'unknown'))
                return redirect('login')
            else:
                messages.error(request, 'Please correct the errors below.')
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
        except Exception as e:
            messages.error(request, 'An error occurred during registration. Please try again.')
            logger.error("Registration error from IP %s - %s", request.META.get('REMOTE_ADDR', 'unknown'), str(e))
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            username = request.user.username
            ip_address = request.META.get('REMOTE_ADDR', 'unknown')
            logout(request)
            messages.success(request, f'{username}, you have logged out successfully.')
            logger.info("User %s logged out from IP %s", username, ip_address)
        else:
            messages.info(request, 'You are already logged out.')
        return redirect('landing')
    else:
        messages.error(request, 'Please use the logout button to log out.')
        return redirect('dashboard')

@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        messages.warning(request, 'Access denied. Admin privileges required.')
        return redirect('user_dashboard')
    return render(request, 'admin_dashboard.html', {'user': request.user})

@login_required
def user_dashboard(request):
    if request.user.is_superuser:
        return redirect('admin_dashboard')
    return render(request, 'user_dashboard.html', {'user': request.user})

@login_required
def dashboard(request):
    if request.user.is_superuser:
        return redirect('admin_dashboard')
    return redirect('user_dashboard')