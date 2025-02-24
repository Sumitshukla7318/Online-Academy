from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from . models import Course,Enrollment
from users.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from Payment.models import Payment
from django.db.models import Sum,Q,Count
from django.contrib.auth.hashers import check_password, make_password

class AddCourse(View):
    def get(self,request):
        return render(request,"courses/add_course.html")
    
    def post(self, request):
        if not request.session['user_id']:
            return redirect('login')
        
        title = request.POST.get('title')
        description = request.POST.get('description')
        category = request.POST.get('category')
        price = request.POST.get('price')
        level = request.POST.get('level')
        thumbnail = request.FILES.get('thumbnail')

        if not title or not description or not category or not price or not level:
            return render(request, "courses/add_course.html", {"error": "All fields are required!"})

        user = User.objects.get(id=request.session['user_id'])
        
        course = Course(
            title=title,
            description=description,
            category=category,
            price=price,
            level=level,
            instructor=user, 
            thumbnail=thumbnail
        )
        course.save()

        return redirect('Instructor_dashboard') 
    

class CourseDetail(View):
    def get(self, request, id):
        course = get_object_or_404(Course, id=id)
        is_enrolled = False  
        
        user=User.objects.get(id=request.session['user_id'])

        print("yes authenticated")
        is_enrolled = Enrollment.objects.filter(user=user, course=course).exists()
        print(is_enrolled,"nnnnnnnnnnnnnn")

        return render(request, "courses/course_detail.html", {
            "course": course,
            "is_enrolled": is_enrolled
        })

    
    def post(self, request, id):
        if not request.session['user_id']:
            redirect('login')
        course = get_object_or_404(Course, id=id)

        user=User.objects.get(id=request.session['user_id'])

        if user==course.instructor:
            messages.error(request,"Instructor cannot enroll in their own courses ! ")
            return redirect('course_detail',id=course.id)

        if not Enrollment.objects.filter(user=user, course=course).exists():
            Enrollment.objects.create(user=user, course=course)
            print("enrolled sucess")

        return redirect('course_detail', id=course.id)

class Courses(View):
    def get(self,request):
        courses=Course.objects.all()
        return render(request,"courses/course_list.html",{"courses":courses})
    
class MyCourses(View):
    def get(self,request):
        if not request.session['user_id']:
            return redirect('login')
        user=User.objects.get(id=request.session['user_id'])
        enrolled_courses = Enrollment.objects.filter(user=user).select_related('course')
        return render(request, 'courses/my_courses.html', {'enrolled_courses': enrolled_courses})
    

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
    def get(self, request, id):
        course = get_object_or_404(Course, id=id)
        lessons = course.lessons.all()
        quizzes = course.quizzes.all()
        students = Enrollment.objects.filter(course=course) 

        context = {
            "course": course,
            "lessons": lessons,
            "quizzes": quizzes,
            "students": students,
        }
        return render(request, "Instructor/instructor_course_detail.html", context)

    def post(self,request,id):
        pass


class EditCourse(View):
    def get(self,request,id):
        pass
    def post(self,request,id):
        pass


class DeleteCourse(View):
    def get(self,request,id):
        pass
    def post(self,request,id):
        pass

class StudentsEnrolledInCourse(View):
    def get(self,request):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('login') 

        instructor = User.objects.get(id=user_id)
        courses = Course.objects.filter(instructor=instructor).prefetch_related('enrolled_students__user')

        return render(request, "Instructor/students_enrolled.html", {"courses": courses})

    def post(self,request):
        pass

class StudentDetail(View):
    def get(self,request):
        pass
    def post(self,request):
        pass

class Earning(View):
    def get(self, request):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('login')

        instructor = User.objects.get(id=user_id)

        # Total earnings from paid courses
        total_earnings = Payment.objects.filter(
            course__instructor=instructor, payment_status="Completed"
        ).aggregate(Sum('amount'))['amount__sum'] or 0.0

        # Earnings and enrollments per course (Including Free Courses)
        course_earnings = Course.objects.filter(instructor=instructor).annotate(
            total_revenue=Sum('payments__amount', filter=Q(payments__payment_status="Completed")),
            total_students=Count('enrolled_students')  # Count enrollments (for free & paid courses)
        )

        # Recent payments (transactions)
        recent_payments = Payment.objects.filter(
            course__instructor=instructor, payment_status="Completed"
        ).order_by('-payment_date')[:5]

        return render(request, "instructor/instructor_earning.html", {
            "total_earnings": total_earnings,
            "course_earnings": course_earnings,
            "recent_payments": recent_payments,
        })   
        
    def post(self,request):
        pass

class Settings(View):
    def get(self, request):
        user_id = request.session.get('user_id')  # Get logged-in instructor
        if not user_id:
            return redirect('login')  # Redirect if not logged in

        instructor = User.objects.get(id=user_id)  # Fetch instructor details
        return render(request, "Instructor/instructor_settings.html", {"instructor": instructor})

    def post(self, request):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('login')

        instructor = User.objects.get(id=user_id)

        # Handling Profile Update
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")

        if full_name and email:
            instructor.full_name = full_name
            instructor.email = email
            instructor.save()
            messages.success(request, "Profile updated successfully!")

        # Handling Password Change
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if current_password and new_password and confirm_password:
            if check_password(current_password, instructor.password):
                if new_password == confirm_password:
                    instructor.password = make_password(new_password)
                    instructor.save()
                    messages.success(request, "Password updated successfully!")
                else:
                    messages.error(request, "New passwords do not match!")
            else:
                messages.error(request, "Incorrect current password!")

        # Handling Payment Details Update
        bank_account = request.POST.get("bank_account")
        paypal_email = request.POST.get("paypal_email")

        if bank_account:
            instructor.bank_account = bank_account
        if paypal_email:
            instructor.paypal_email = paypal_email
        instructor.save()
        messages.success(request, "Payment details updated!")

        return redirect("settings") 

