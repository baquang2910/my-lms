from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def landing_view(request):
    """Render the public landing page for BeriS LMS."""
    return render(request, 'landing.html')

@login_required
def dashboard_view(request):
    """Render the general dashboard, redirecting to admin or user dashboard based on role."""
    return render(request, 'dashboard.html', {'user': request.user})