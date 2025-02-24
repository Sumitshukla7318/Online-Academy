from django.db import models

# Create your models here.

class User(models.Model):
    id=models.AutoField(primary_key=True)
    username=models.CharField(max_length=100,unique=True)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=255)
    profile_pic=models.ImageField(upload_to='profile_pics/',null=True,blank=True)
    is_instructor=models.BooleanField(default=False)
    date_joined=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username