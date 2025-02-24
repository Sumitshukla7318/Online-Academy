from django.shortcuts import render
from django.views import View
from courses.models import Course

# Create your views here.

class Home(View):
    def get(self,request):
        courses=Course.objects.all()
        return render(request, "core/home.html",{"courses":courses})
     
    def post(self,request):
        pass

class About(View):
    def get(self,request):
        return render(request,"about/about_page.html")
        

class Contact(View):
    def get(self,request):
        return render(request,"contact/contact_us.html")