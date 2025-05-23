from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Lesson, Course
from .forms import LessonForm, CourseForm

@login_required
def create_lesson(request):
    # Check if any courses exist
    courses = Course.objects.all()
    if not courses:
        messages.error(request, 'No courses available. Please create a course first.')
        return redirect('create_course')  # Redirect to create_course view

    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid():
            lesson = form.save()
            messages.success(request, f'Lesson "{lesson.title}" created successfully!')
            return redirect('lesson_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LessonForm()
    return render(request, 'courses/create_lesson.html', {'form': form})

@login_required
def lesson_list(request):
    lessons = Lesson.objects.all().order_by('-created_at')  # Sort by creation date
    paginator = Paginator(lessons, 10)  # 10 lessons per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'courses/lesson_list.html', {'page_obj': page_obj, 'paginator': paginator})

@login_required
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)  # Create instance without saving
            course.instructor = request.user  # Set instructor to current user
            course.save()  # Save the course
            messages.success(request, f'Course "{course.title}" created successfully!')
            return redirect('create_lesson')  # Redirect back to create_lesson
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CourseForm()
    return render(request, 'courses/create_course.html', {'form': form})