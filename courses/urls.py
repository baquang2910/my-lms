from django.urls import path
from . import views

urlpatterns = [
    path('create_lesson/', views.create_lesson, name='create_lesson'),
    path('lessons/', views.lesson_list, name='lesson_list'),
]