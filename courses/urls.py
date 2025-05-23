from django.urls import path
from . import views

urlpatterns = [
    path('lessons/', views.lesson_list, name='lesson_list'),
    path('create_lesson/', views.create_lesson, name='create_lesson'),
    path('create_course/', views.create_course, name='create_course'),
    # Removed or commented out the edit_lesson path to fix AttributeError
    # path('lessons/<int:id>/edit/', views.edit_lesson, name='edit_lesson'),
]