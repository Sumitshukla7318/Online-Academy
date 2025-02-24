from django.db import models
from users.models import User

# Create your models here.
class Course(models.Model):
    id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=255)
    description=models.TextField()
    instructor=models.ForeignKey(User,on_delete=models.CASCADE,related_name="course")
    category=models.CharField(max_length=100)
    price=models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
    level=models.CharField(max_length=50,choices=[("Beginner", "Beginner"), ("Intermediate", "Intermediate"), ("Advanced", "Advanced")])
    thumbnail=models.ImageField(upload_to="course_thumbnails/")
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

#COurse Enrollment Model

class Enrollment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='enrollments')
    course=models.ForeignKey(Course,on_delete=models.CASCADE,related_name="enrolled_students")
    progress=models.FloatField(default=0.0)
    enrolled_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together=('user','course')
    
    def __str__(self):
        return f"{self.user.username} - {self.course.title}"