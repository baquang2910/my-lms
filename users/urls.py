from django.urls import path
from . import views

# URL patterns for user authentication and dashboards
# Note: Root URL ('') is likely defined in my_lms/urls.py (e.g., for landing page)
urlpatterns = [
    # Authentication routes
    path('login/', views.login_view, name='login'),  # User login page
    path('register/', views.register_view, name='register'),  # User registration page
    path('logout/', views.logout_view, name='logout'),  # User logout (POST-only, redirects to landing)

    # Dashboard routes
    path('dashboard/', views.dashboard, name='dashboard'),  # General dashboard (redirects to admin/user based on role)
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),  # Admin-only dashboard (superusers)
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),  # User dashboard (non-superusers)

    # Add future routes here (e.g., profile, password reset)
]