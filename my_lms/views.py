# my_lms/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_view(request):
    if request.user.is_superuser:
        # Admin dashboard
        return render(request, 'admin_dashboard.html', {'user': request.user})
    else:
        # Regular user dashboard
        return render(request, 'user_dashboard.html', {'user': request.user})