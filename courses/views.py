from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Lesson
from .forms import LessonForm
from django.contrib import messages

@login_required
def create_lesson(request):
    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course_id = 1  # Temporary; use your first course’s ID
            lesson.save()
            messages.success(request, 'Lesson created successfully!')
            return redirect('lesson_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LessonForm()
    return render(request, 'courses/create_lesson.html', {'form': form})

def lesson_list(request):
    lessons = Lesson.objects.all()
    return render(request, 'courses/lesson_list.html', {'lessons': lessons})