from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import logging

# Set up logging
logger = logging.getLogger(__name__)

def login_view(request):
    """Handle user login and redirect based on role."""
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        try:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                logger.info("User %s logged in from IP %s", username, request.META.get('REMOTE_ADDR', 'unknown'))
                if user.is_superuser:
                    logger.info("User %s redirected to admin_dashboard", username)
                    return redirect('admin_dashboard')
                logger.info("User %s redirected to user_dashboard", username)
                return redirect('user_dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
                logger.warning("Authentication failed for username: %s from IP %s", username, request.META.get('REMOTE_ADDR', 'unknown'))
        except Exception as e:
            messages.error(request, 'An error occurred during login.')
            logger.error("Login error for username: %s from IP %s: %s", username, request.META.get('REMOTE_ADDR', 'unknown'), str(e))
    return render(request, 'users/login.html')

def register_view(request):
    """Handle user registration and redirect to login."""
    if request.user.is_authenticated:
        logger.info("Authenticated user %s attempted to access register page from IP %s", 
                    request.user.username, request.META.get('REMOTE_ADDR', 'unknown'))
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
                for error in form.non_field_errors():
                    messages.error(request, error)
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field.capitalize()}: {error}")
                logger.warning("Registration form errors from IP %s: %s", 
                              request.META.get('REMOTE_ADDR', 'unknown'), form.errors)
        except Exception as e:
            messages.error(request, 'An error occurred during registration.')
            logger.error("Registration error from IP %s: %s", request.META.get('REMOTE_ADDR', 'unknown'), str(e))
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def logout_view(request):
    """Handle user logout (POST only)."""
    if request.method == 'POST':
        if request.user.is_authenticated:
            username = request.user.username
            ip_address = request.META.get('REMOTE_ADDR', 'unknown')
            logout(request)
            messages.success(request, f'{username}, you have logged out successfully.')
            logger.info("User %s logged out from IP %s", username, ip_address)
        return redirect('landing')
    messages.error(request, 'Please use the logout button to log out.')
    return redirect('dashboard')

@login_required
def admin_dashboard(request):
    """Render admin dashboard for superusers only."""
    if not request.user.is_superuser:
        messages.warning(request, 'Access denied. Admin privileges required.')
        logger.warning("Non-superuser %s attempted to access admin_dashboard from IP %s", 
                       request.user.username, request.META.get('REMOTE_ADDR', 'unknown'))
        return redirect('user_dashboard')
    logger.info("Superuser %s accessed admin_dashboard from IP %s", 
                request.user.username, request.META.get('REMOTE_ADDR', 'unknown'))
    return render(request, 'admin_dashboard.html', {'user': request.user})

@login_required
def user_dashboard(request):
    """Render user dashboard for non-superusers."""
    if request.user.is_superuser:
        logger.info("Superuser %s redirected from user_dashboard to admin_dashboard from IP %s", 
                    request.user.username, request.META.get('REMOTE_ADDR', 'unknown'))
        return redirect('admin_dashboard')
    logger.info("User %s accessed user_dashboard from IP %s", 
                request.user.username, request.META.get('REMOTE_ADDR', 'unknown'))
    return render(request, 'user_dashboard.html', {'user': request.user})

@login_required
def dashboard(request):
    """Redirect to appropriate dashboard based on user role."""
    if request.user.is_superuser:
        logger.info("Superuser %s redirected to admin_dashboard from dashboard from IP %s", 
                    request.user.username, request.META.get('REMOTE_ADDR', 'unknown'))
        return redirect('admin_dashboard')
    logger.info("User %s redirected to user_dashboard from dashboard from IP %s", 
                request.user.username, request.META.get('REMOTE_ADDR', 'unknown'))
    return redirect('user_dashboard')