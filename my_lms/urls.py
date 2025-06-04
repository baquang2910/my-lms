from django.contrib import admin
from django.urls import path, include
from . import views

# Root URL patterns for BeriS LMS
urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),  # Django admin interface
    path('users/', include('users.urls')),  # User authentication and dashboard routes
    path('courses/', include('courses.urls')),  # Course and lesson management routes
    path('', views.landing_view, name='landing'),  # Landing page (root URL)
    path('dashboard/', views.dashboard_view, name='dashboard'),  # General dashboard (renders dashboard.html)
]