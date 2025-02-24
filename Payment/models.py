from django.db import models
from users.models import User
from courses.models import Course

# Create your models here.

class Payment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="payments")
    course=models.ForeignKey(Course,on_delete=models.CASCADE,related_name="payments")
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    transaction_id=models.CharField(max_length=100,unique=True)
    payment_status=models.CharField(max_length=50,choices=[("Pending", "Pending"), ("Completed", "Completed"), ("Failed", "Failed")])
    payment_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} -> {self.course.title} -> {self.payment_status}"
