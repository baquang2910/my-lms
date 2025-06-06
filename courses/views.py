from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage
from .models import Lesson, Course
from .forms import LessonForm, CourseForm
import logging

# Set up logging
logger = logging.getLogger(__name__)

def is_admin(user):
    """Check if user is an authenticated admin (superuser)."""
    return user.is_authenticated and user.is_superuser

@login_required
@user_passes_test(is_admin)
def create_lesson(request):
    """Create a new lesson (admin-only)."""
    courses = Course.objects.all()
    if not courses:
        messages.error(request, 'No courses available. Please create a course first.')
        logger.warning("No courses available for lesson creation by user %s from IP %s",
                      request.user.username, request.META.get('REMOTE_ADDR', 'unknown'))
        return redirect('create_course')

    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES)
        try:
            if form.is_valid():
                lesson = form.save()
                messages.success(request, f'Lesson "{lesson.title}" created successfully!')
                logger.info("Lesson %s (ID: %s) created by user %s from IP %s",
                           lesson.title, lesson.id, request.user.username, request.META.get('REMOTE_ADDR', 'unknown'))
                return redirect('lesson_list')
            else:
                messages.error(request, 'Please correct the errors below.')
        except Exception as e:
            messages.error(request, 'An error occurred while creating the lesson.')
            logger.error("Error creating lesson by user %s from IP %s: %s",
                        request.user.username, request.META.get('REMOTE_ADDR', 'unknown'), str(e))
    else:
        form = LessonForm()
    return render(request, 'courses/create_lesson.html', {'form': form})

@login_required
def lesson_list(request):
    """List all lessons (view-only for regular users, management for admins)."""
    if request.user.is_superuser:
        lessons = Lesson.objects.all().order_by('-created_at')
    else:
        # Non-admins see only lessons from public courses
        lessons = Lesson.objects.filter(course__is_public=True).order_by('-created_at')
        logger.info("Non-admin user %s accessed public lessons from IP %s",
                    request.user.username, request.META.get('REMOTE_ADDR', 'unknown'))
    
    paginator = Paginator(lessons, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)
    return render(request, 'courses/lesson_list.html', {'page_obj': page_obj, 'paginator': paginator})

@login_required
@user_passes_test(is_admin)
def create_course(request):
    """Create a new course (admin-only)."""
    if request.method == 'POST':
        form = CourseForm(request.POST)
        try:
            if form.is_valid():
                course = form.save()
                messages.success(request, f'Course "{course.title}" created successfully!')
                logger.info("Course %s (ID: %s) created by user %s from IP %s",
                           course.title, course.id, request.user.username, request.META.get('REMOTE_ADDR', 'unknown'))
                return redirect('lesson_list')
            else:
                messages.error(request, 'Please correct the errors below.')
        except Exception as e:
            messages.error(request, 'An error occurred while creating the course.')
            logger.error("Error creating course by user %s from IP %s: %s",
                        request.user.username, request.META.get('REMOTE_ADDR', 'unknown'), str(e))
    else:
        form = CourseForm()
    return render(request, 'courses/create_course.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def edit_lesson(request, lesson_id):
    """Edit an existing lesson (admin-only)."""
    lesson = get_object_or_404(Lesson, id=lesson_id)
    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES, instance=lesson)
        try:
            if form.is_valid():
                form.save()
                messages.success(request, f'Lesson "{lesson.title}" updated successfully!')
                logger.info("Lesson %s (ID: %s) updated by user %s from IP %s",
                           lesson.title, lesson.id, request.user.username, request.META.get('REMOTE_ADDR', 'unknown'))
                return redirect('lesson_list')
            else:
                messages.error(request, 'Please correct the errors below.')
        except Exception as e:
            messages.error(request, 'An error occurred while updating the lesson.')
            logger.error("Error updating lesson %s (ID: %s) by user %s from IP %s: %s",
                        lesson.title, lesson.id, request.user.username, request.META.get('REMOTE_ADDR', 'unknown'), str(e))
    else:
        form = LessonForm(instance=lesson)
    return render(request, 'courses/edit_lesson.html', {'form': form, 'lesson': lesson})

@login_required
@user_passes_test(is_admin)
def delete_lesson(request, lesson_id):
    """Delete a lesson (admin-only)."""
    lesson = get_object_or_404(Lesson, id=lesson_id)
    if request.method == 'POST':
        try:
            lesson_title = lesson.title
            lesson_id = lesson.id
            lesson.delete()
            messages.success(request, f'Lesson "{lesson_title}" deleted successfully!')
            logger.info("Lesson %s (ID: %s) deleted by user %s from IP %s",
                       lesson_title, lesson_id, request.user.username, request.META.get('REMOTE_ADDR', 'unknown'))
            return redirect('lesson_list')
        except Exception as e:
            messages.error(request, 'An error occurred while deleting the lesson.')
            logger.error("Error deleting lesson %s (ID: %s) by user %s from IP %s: %s",
                        lesson.title, lesson.id, request.user.username, request.META.get('REMOTE_ADDR', 'unknown'), str(e))
    return render(request, 'courses/delete_lesson.html', {'lesson': lesson})

@login_required
def view_lesson(request, lesson_id):
    """View a lesson's content (available to all authenticated users)."""
    lesson = get_object_or_404(Lesson, id=lesson_id)
    # Non-admins can only view lessons from public courses
    if not lesson.course.is_public and not request.user.is_superuser:
        messages.error(request, 'You do not have access to this lesson.')
        logger.warning("User %s attempted to access lesson %s (ID: %s) without permission from IP %s",
                      request.user.username, lesson.title, lesson.id, request.META.get('REMOTE_ADDR', 'unknown'))
        return redirect('lesson_list')
    logger.info("User %s viewed lesson %s (ID: %s) from IP %s",
                request.user.username, lesson.title, lesson.id, request.META.get('REMOTE_ADDR', 'unknown'))
    return render(request, 'courses/view_lesson.html', {'lesson': lesson})