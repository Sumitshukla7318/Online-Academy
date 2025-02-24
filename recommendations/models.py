from django.db import models
from users.models import User
from courses.models import Course

# Create your models here.
class CourseRecommendation(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="recommendations")
    recommended_course=models.ForeignKey(Course,on_delete=models.CASCADE)
    score=models.FloatField()

    def __str__(self):
        return f"{self.user.username} -> {self.recommended_course.title}"