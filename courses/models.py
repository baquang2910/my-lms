from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

class Course(models.Model):
    title = models.CharField(max_length=200)  # Course title
    description = RichTextField()  # Rich text description of the course
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')  # Course creator
    is_public = models.BooleanField(default=True)  # Indicates if the course is accessible to all users
    created_at = models.DateTimeField(auto_now_add=True)  # Creation timestamp

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']  # Newest courses first

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')  # Parent course
    title = models.CharField(max_length=200)  # Lesson title
    content = RichTextField()  # Rich text lesson content
    file = models.FileField(upload_to='lessons/%Y/%m/%d/', blank=True, null=True)  # Optional lesson file
    created_at = models.DateTimeField(auto_now_add=True)  # Creation timestamp

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']  # Newest lessons first