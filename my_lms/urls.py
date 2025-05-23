# my_lms/urls.py
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('courses/', include('courses.urls')),
    path('', views.landing_view, name='landing'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
]