from django.urls import path
from . import views

app_name = 'courses'  # Namespace for URL names

urlpatterns = [
    path('lessons/', views.lesson_list, name='lesson_list'),
    path('lessons/create/', views.create_lesson, name='create_lesson'),
    path('lessons/<int:id>/edit/', views.edit_lesson, name='edit_lesson'),
    path('lessons/<int:id>/delete/', views.delete_lesson, name='delete_lesson'),
    path('create_course/', views.create_course, name='create_course'),
]