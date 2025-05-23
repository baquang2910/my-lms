from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Lesson, Course  # Assuming Course model exists
from .forms import LessonForm
from django.contrib import messages
from django.core.paginator import Paginator

@login_required
def create_lesson(request):
    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid():
            lesson = form.save()  # Assumes course is set via form
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
    return render(request, 'courses/lesson_list.html', {'page_obj': page_obj})