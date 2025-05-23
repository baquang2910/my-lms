from django import forms
from .models import Lesson

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'content', 'file']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'ckeditor'}),
        }