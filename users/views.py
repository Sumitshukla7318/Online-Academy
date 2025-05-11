from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from .models import User
from django.contrib.auth.hashers import make_password
from django.views import View
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import check_password
from SuperAdmin.models import AdminVerification,InstructorVerification
from courses.models import Course
from django.utils.timezone import now, timedelta
from analytics.models import UserStreak,UserGoal
import re

class SignupView(View):
    def get(self, request):
        return render(request, "users/signup.html")

    def post(self, request):
        full_name = request.POST.get('full_name', '').strip()
        username = request.POST.get("username", '').strip()
        email = request.POST.get("email", '').strip()
        password = request.POST.get("password", '').strip()
        profile_pic = request.FILES.get("profile_pic")

        errors = []

        # Full Name Validation
        if not full_name:
            errors.append("Full Name is required.")
        elif not re.match(r"^[A-Za-z ]+$", full_name):
            errors.append("Full Name should only contain letters.")

        # Username Validation
        if not username:
            errors.append("Username is required.")
        elif not re.match(r"^[A-Za-z0-9_]+$", username):
            errors.append("Username can only contain letters, numbers, and underscores.")
        elif User.objects.filter(username=username).exists():
            errors.append("Username already exists! Choose another one.")

        # Email Validation
        try:
            validate_email(email)
        except ValidationError:
            errors.append("Invalid email format.")
        if User.objects.filter(email=email).exists():
            errors.append("Email is already registered!")

        # Password Validation
        if len(password) < 8:
            errors.append("Password must be at least 8 characters long.")
        elif not re.search(r"[A-Za-z]", password) or not re.search(r"[0-9]", password):
            errors.append("Password must contain both letters and numbers.")

        # Profile Picture Validation
        if profile_pic and not profile_pic.content_type.startswith("image/"):
            errors.append("Profile picture must be an image file.")

        # If there are validation errors, show them
        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect("signup")

        # Create and save user
        user = User.objects.create(
            full_name=full_name,
            username=username,
            email=email,
            password=make_password(password),
        )

        # Save profile picture if uploaded
        if profile_pic:
            user.profile_pic = profile_pic
            user.save()
        
    
        messages.success(request, "Account created successfully! Please log in.")

        return redirect("login")


class LoginView(View):
    def get(self, request):
        return render(request, "users/login.html")

    def post(self, request):
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        if not username or not password:
            messages.error(request, "Both fields are required!")
            return render(request, "users/login.html")

        # # Superadmin direct login (Hardcoded for now)
        # if username == "" and password == "superadmin":
        #     request.session["user_role"] = "superadmin"
        #     return redirect("superadmin_dashboard")

        try:
            user = User.objects.get(username=username)

            if user.is_banned:
                messages.error(request, "Your account has been banned!")
                return render(request, "users/login.html")

            if user.is_instructor:
                if user.status.lower() == "pending":
                    messages.error(request, "Your account is under review. Please wait for admin approval.")
                    return render(request, "users/login.html")
                elif user.status.lower() == "rejected":
                    messages.error(request, "Your application has been rejected.")
                    return render(request, "users/login.html")

            if check_password(password, user.password):
                request.session["user_id"] = user.id
                request.session["user_role"] = user.role 
                messages.success(request, "Login successful!")

                if user.role=='superadmin':
                    return redirect('superadmin_dashboard')

                return redirect("profile")  # Redirect to profile/dashboard
            else:
                print("incorrect password")

        except User.DoesNotExist:
            messages.error(request, "Invalid username or password!")

        return render(request, "users/login.html")



class ProfileView(View):
    def get(self, request):
        user_id = request.session.get('user_id')

        if not user_id:
            messages.error(request, "You need to login first!")
            return redirect("login")

        user = User.objects.get(id=user_id)

        streak,created= UserStreak.objects.get_or_create(user=user)

    
        if streak.last_active_date:
            days_since_last_active = (now().date() - streak.last_active_date).days


            if days_since_last_active == 1:
                streak.current_streak += 1  # Increase streak if logged in on the next day
            elif days_since_last_active > 1:
                streak.longest_streak=streak.current_streak
                streak.current_streak = 1  # Reset streak if missed a day
                

       
        streak.last_active_date = now()
        streak.save()
        print(streak.last_active_date)

        active_goal = UserGoal.objects.filter(user=user, status="pending").order_by("-start_date").first()


        return render(request, "users/profile.html", {"user": user, "streak": streak,"active_goal": active_goal})


    def post(self, request):
        user_id = request.session.get('user_id')

        if not user_id:
            messages.error(request, "You need to login first!")
            return redirect("login")

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            messages.error(request, "User not found!")
            return redirect("login")

        # Handling profile picture update
        profile_pic = request.FILES.get('profile_pic')
        if profile_pic:
            user.profile_pic = profile_pic
            user.save()
            messages.success(request, "Profile picture updated successfully!")

        return redirect("profile")



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
        course_count=courses.count()

        return render(request, "Instructor/instructor_dashboard.html", 
                      {
                          "courses": courses,
                          'course_count':course_count,                   
                      })
    
    def post(self,request):
        pass


class StudentDetail(View):
    def get(self,request,id):
        pass
    def post(self,request,id):
        pass


class RequestInstructorship(View):
    def get(self, request):
        user_id = request.session.get('user_id')
        if not user_id:
            messages.error(request, "You need to log in first!")
            return redirect('login')
        
        user = get_object_or_404(User, id=user_id)

        existing_request = InstructorVerification.objects.filter(instructor=user, status="pending").first()
        if existing_request:
            messages.warning(request, "Your Instructor request is already under review.")
            return redirect("profile")

        return render(request,"superadmin/request_instructorship.html")

    def post(self, request):
        user_id = request.session.get('user_id')
        if not user_id:
            messages.error(request, "You need to log in first!")
            return redirect("login")
        
        user = get_object_or_404(User, id=user_id)

        aadhar_number = request.POST.get("aadhar_number", "").strip()
        pan_number = request.POST.get("pan_number", "").strip()
        account_number = request.POST.get("account_number", "").strip()

        
        if len(aadhar_number) != 12 or not aadhar_number.isdigit():
            messages.error(request, "Please enter a valid 12-digit Aadhar Number.")
            return redirect("request_instructorship")
        
    
        if len(pan_number) != 10 or not pan_number.isalnum():
            messages.error(request, "Please enter a valid 10-character PAN Number.")
            return redirect("request_instructorship")


        if not account_number.isdigit() or len(account_number) < 8:
            messages.error(request, "Please enter a valid bank account number.")
            return redirect("request_instructorship")


        instructor_request= InstructorVerification.objects.create(
            instructor=user,  
            aadhar_number=aadhar_number,
            pan_number=pan_number,
            account_number=account_number,
            status="pending"
        )
        instructor_request.save()

        messages.success(request, "Your Instructorship request has been sent to the SuperAdmin.")
        return redirect("profile")



class RequestAdminship(View):
    def get(self, request):
        user_id = request.session.get("user_id")
        if not user_id:
            messages.error(request, "You need to log in first!")
            return redirect("login")

        user = get_object_or_404(User, id=user_id)

       
        if hasattr(user, "admin_request"):
            if AdminVerification.objects.get(user=user).admin_status.lower()=='pending':
                messages.warning(request, "Your admin request is already under review!")
                return redirect("profile")

        return render(request, "superadmin/request_admin.html", {"user": user})

    def post(self, request):
        user_id = request.session.get("user_id")
        if not user_id:
            messages.error(request, "You need to log in first!")
            return redirect("login")

        user = get_object_or_404(User, id=user_id)
        aadhar_number = request.POST.get("aadhar_number", "").strip()

        # Validation
        if len(aadhar_number) != 12 or not aadhar_number.isdigit():
            messages.error(request, "Please enter a valid 12-digit Aadhar Number.")
            return redirect("request_admin")

        
        admin_request=AdminVerification.objects.filter(user=user).first()
        if admin_request:
            admin_request.admin_status="pending"
            admin_request.save()
        else:    
            AdminVerification.objects.create(
                user=user,
                aadhar_number=aadhar_number,
                admin_status='pending',
            )   

        messages.success(request, "Your adminship request has been sent to SuperAdmin.")
        return redirect("profile")



