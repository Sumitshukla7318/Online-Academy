from django.db import models
from courses.models import Course
from django.contrib.postgres.fields import JSONField  # For PostgreSQL

class Lesson(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=255)
    content = models.TextField()
    video_url = models.URLField(blank=True, null=True)
    pdf_files = models.JSONField(default=list, blank=True, null=True)  # Store multiple PDFs
    images = models.JSONField(default=list, blank=True, null=True)  # Store multiple images
    extra_sections = models.JSONField(default=list, blank=True, null=True)  # Store additional text sections
    order = models.PositiveIntegerField()

    def __str__(self):
        return self.title
