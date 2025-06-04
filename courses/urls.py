from django.urls import path
from . import views

# URL patterns for course and lesson management in BeriS LMS
urlpatterns = [
    # Lesson routes
    path('lessons/', views.lesson_list, name='lesson_list'),  # List all lessons (view-only for regular users)
    path('lessons/create/', views.create_lesson, name='create_lesson'),  # Create a new lesson (admin-only)
    path('lessons/<int:lesson_id>/view/', views.view_lesson, name='view_lesson'),  # View lesson content (all users)
    path('lessons/<int:lesson_id>/edit/', views.edit_lesson, name='edit_lesson'),  # Edit a lesson (admin-only)
    path('lessons/<int:lesson_id>/delete/', views.delete_lesson, name='delete_lesson'),  # Delete a lesson (admin-only)

    # Course routes
    path('courses/create/', views.create_course, name='create_course'),  # Create a new course (admin-only)

    # Placeholder for future course management routes
    # path('courses/<int:course_id>/edit/', views.edit_course, name='edit_course'),
    # path('courses/<int:course_id>/delete/', views.delete_course, name='delete_course'),
]