from django import forms
from .models import Lesson, Course

class LessonForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), required=True)
    
    class Meta:
        model = Lesson
        fields = ['title', 'content', 'file', 'course']