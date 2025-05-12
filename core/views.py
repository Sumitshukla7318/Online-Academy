from django.shortcuts import render
from django.views import View
from courses.models import Course
from users.models import User
from analytics.models import UserStreak
from django.contrib.auth.hashers import make_password

# Create your views here.

class Home(View):
    def get(self,request):
        # user=User.objects.get(email="naveen123@gmail.com")
        # user.role="student"
        # # # user.username="Sumit1432"
        # # # user.password=make_password("Sumit1432")
        # user.save()
        courses=Course.objects.all()
        return render(request, "core/home.html",{"courses":courses})
     

class About(View):
    def get(self,request):
        return render(request,"about/about_page.html")
        

class Contact(View):
    def get(self,request):
        return render(request,"Contact/contact_us.html")