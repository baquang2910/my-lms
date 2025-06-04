from django.urls import path
from . import views

# URL patterns for course and lesson management in BeriS LMS
# Note: These paths are likely included under /courses/ in my_lms/urls.py
urlpatterns = [
    # Lesson routes
    path('lessons/', views.lesson_list, name='course_list'),  # List all lessons (view-only for non-admins, all for superusers)
    path('lessons/create/', views.create_lesson, name='create_lesson'),  # Create a new lesson (superuser-only)
    path('lessons/<int:lesson_id>/view/', views.view_lesson, name='view_lesson'),  # View lesson content (authenticated users, public courses for non-admins)
    path('lessons/<int:lesson_id>/edit/', views.edit_lesson, name='edit_lesson'),  # Edit lesson content (superuser-only)
    path('lessons/<int:lesson_id>/delete/', views.delete_lesson, name='delete_lesson'),  # Delete a lesson (superuser-only)

    # Course routes
    path('courses/create/', views.create_course, name='create_course'),  # Create a new course (superuser-only)

    # Add future routes here (e.g., course edit, course deletion)
]