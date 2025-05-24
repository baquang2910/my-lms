from django.urls import path
from . import views

urlpatterns = [
    path('lessons/', views.lesson_list, name='lesson_list'),
    path('create_lesson/', views.create_lesson, name='create_lesson'),
    path('create_course/', views.create_course, name='create_course'),
    path('lessons/<int:lesson_id>/edit/', views.edit_lesson, name='edit_lesson'),
]