from django.urls import path
from . import views

# URL patterns for user authentication and dashboards
urlpatterns = [
    # Authentication routes
    path('login/', views.login_view, name='login'),  # User login
    path('register/', views.register_view, name='register'),  # User registration
    path('logout/', views.logout_view, name='logout'),  # User logout (POST-only)

    # Dashboard routes
    path('dashboard/', views.dashboard, name='dashboard'),  # General dashboard (redirects based on role)
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),  # Admin-only dashboard
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),  # User dashboard for non-admins

    # Placeholder for future routes (e.g., profile, password reset)
    # path('profile/', views.profile_view, name='profile'),
]