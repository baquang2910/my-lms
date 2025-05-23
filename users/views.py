from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
import logging

# Set up logging
logger = logging.getLogger(__name__)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            logger.info("User %s authenticated, redirecting to dashboard", username)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
            logger.warning("Authentication failed for username: %s", username)
    return render(request, 'users/login.html')