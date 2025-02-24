from django.shortcuts import render,redirect
from django.contrib import messages
from .models import User
from django.contrib.auth.hashers import make_password
from django.views import View
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import check_password

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.views import View
from .models import User
from courses.models import Course

class SignupView(View):
    def get(self, request):
        return render(request, "users/signup.html")

    def post(self, request):
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        profile_pic = request.FILES.get("profile_pic")  
        is_instructor = request.POST.get("is_instructor") == "on"  

      
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Invalid email format.")
            return redirect("signup")  

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect("signup")

        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect("signup")


        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password), 
            is_instructor=is_instructor  
        )

        if profile_pic:
            user.profile_pic = profile_pic  
            user.save()

        messages.success(request, "Account created successfully! Please login.")
        return redirect("login")        


class LoginView(View):
    def get(self, request):
        return render(request, "users/login.html")

    def post(self, request):

        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)  
            print(password==user.password)
            if check_password(password,user.password): 
                request.session["user_id"] = user.id  
                messages.success(request, "Login successful!")
                return redirect("profile") 
            else:
                messages.error(request, "Invalid credentials!")
        except User.DoesNotExist:
            messages.error(request, "Invalid credentials!")

        return render(request, "users/login.html")


class ProfileView(View):
    def get(self,request):
        user_id=request.session.get('user_id')

        if not user_id:
            messages.error(request,"you need to login first!")
            return redirect("login")
        user=User.objects.get(id=user_id)
        return render(request,"users/profile.html",{"user":user})

    def post(self,request):
        pass

class LogoutView(View):
    def get(self,request):
        request.session.flush()
        messages.success(request,"logged out successfully!")
        return redirect("login")

    def post(self,request):
        pass

class InstructorDashboard(View):
    def get(self,request):
        user_id = request.session.get('user_id')
        if not user_id:  
            return redirect('login') 
        user = User.objects.get(id=user_id)
        courses = Course.objects.filter(instructor=user)
        return render(request, "Instructor/instructor_dashboard.html", {"courses": courses})
    
    def post(self,request):
        pass

class InstructorCourses(View):
    def get(self, request):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('login') 
        
        user = User.objects.get(id=user_id)
        courses = Course.objects.filter(instructor=user) 
        
        return render(request, "Instructor/instructor_courses.html", {"courses": courses})



    def post(self,request):
        pass


class InstructorCourseDetail(View):
    def get(self,request):
        pass
    def post(self,request):
        pass


class EditCourse(View):
    pass


class DeleteCourse(View):
    pass
