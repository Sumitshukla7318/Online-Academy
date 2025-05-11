from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from courses.views import Course
from lessons.models import Lesson
from django.contrib import messages
import json
from django.core.files.storage import default_storage
from courses.models import Enrollment
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from analytics.models import UserProgress
from users.models import User

# Create your views here.
class CourseLession(View):
    def get(self, request, id, lesson_id=None):
        user_id=request.session.get('user_id')
        if not user_id:
            messages.error(request,"you need to login first!")
            return redirect("login")
        course = get_object_or_404(Course, id=id)

        user=request.session['user_id']

        if not Enrollment.objects.filter(user=user, course=course).exists():
            return redirect('course_detail', id=id)

        # Get all lessons for the course
        lessons = Lesson.objects.filter(course=course).order_by('order')

        # Select the first lesson if none is chosen
        selected_lesson = get_object_or_404(Lesson, id=lesson_id) if lesson_id else lessons.first()

        # Get next and previous lesson
        lesson_list = list(lessons)
        current_index = lesson_list.index(selected_lesson) if selected_lesson in lesson_list else 0
        previous_lesson = lesson_list[current_index - 1] if current_index > 0 else None
        next_lesson = lesson_list[current_index + 1] if current_index < len(lesson_list) - 1 else None

        context = {
            'course': course,
            'lessons': lessons,
            'selected_lesson': selected_lesson,
            'previous_lesson': previous_lesson,
            'next_lesson': next_lesson
        }
        return render(request, 'lesson/course_lessons.html', context)

    def post(self,request,id):
        pass





@method_decorator(csrf_exempt, name='dispatch')
class MarkLessonCompleted(View):
    def post(self, request, course_id, lesson_id):
        user_id=request.session.get('user_id')
        if not user_id:
            messages.error(request,"you need to login first!")
            return redirect("login")
        try:
            # Fetch user instance from session ID
            user_id = request.session.get('user_id')
            user = get_object_or_404(User, id=user_id)  

            # Get course and lesson instances
            course = get_object_or_404(Course, id=course_id)
            lesson = get_object_or_404(Lesson, id=lesson_id)

            # Get or create UserProgress entry
            progress, created = UserProgress.objects.get_or_create(user=user, course=course)

            # Parse JSON request data
            data = json.loads(request.body)

            # Update completed lessons
            if data.get("completed", False):
                progress.completed_lessons.add(lesson)  # Add lesson to completed lessons
            else:
                progress.completed_lessons.remove(lesson)  # Remove lesson from completed lessons

            # Update lessons completed count
            progress.lessons_completed = progress.completed_lessons.count()
            progress.save()
            print("sucessfully completed")
            return JsonResponse({"message": "Lesson completion status updated", "completed_count": progress.lessons_completed})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


class AddLesson(View):
    def get(self, request, id):
        user_id=request.session.get('user_id')
        if not user_id:
            messages.error(request,"you need to login first!")
            return redirect("login")
        user=User.objects.get(id=user_id)
        if not user.role.lower()=='instructor':
            messages.error(request,"You have no permission to add lesson")
        return render(request, 'lesson/add_lesson.html', {"id": id})

    def post(self, request, id):
        title = request.POST.get('title')
        order = request.POST.get('order')
        
        # Handle dynamic section content
        extra_sections = json.loads(request.POST.get('sections_data', '[]'))
        content = extra_sections[0]['content'] if extra_sections else ""  # Use first section as main content
        
        # Handle dynamic PDF & Image uploads
        pdf_files = []
        images = []
        for key in request.FILES:
            if key.startswith("pdf_files_"):  
                pdf_files.extend(request.FILES.getlist(key))
            elif key.startswith("image_files_"):
                images.extend(request.FILES.getlist(key))
        
        # Save files using Django's default storage
        pdf_files_data = [default_storage.save(f"course_pdfs/{pdf.name}", pdf) for pdf in pdf_files]
        images_data = [default_storage.save(f"course_images/{img.name}", img) for img in images]

        # Get course & create lesson
        course = Course.objects.get(id=id)
        lesson = Lesson.objects.create(
            course=course,
            title=title,
            content=content,
            pdf_files=pdf_files_data,
            images=images_data,
            extra_sections=extra_sections,
            order=order
        )

        messages.success(request, "Lesson added successfully!")
        return redirect('instructor_courses')  # Change to correct URL name


class ManageLesson(View):
    def get(self, request,id):
        course_id = request.GET.get('course_id', None)
        lessons = Lesson.objects.all().order_by('order')

        if course_id:
            lessons = lessons.filter(course_id=course_id)

        search_query = request.GET.get('search', '')
        if search_query:
            lessons = lessons.filter(title__icontains=search_query)

        courses = Course.objects.all()
        
        context = {
            'lessons': lessons,
            'courses': courses,
            'selected_course': int(course_id) if course_id else None,
            'search_query': search_query,
        }
        return render(request, 'instructor/manage_lessons.html', context)

    def post(self, request,id):
        lesson_id = request.POST.get('lesson_id')
        action = request.POST.get('action')

        if action == "delete":
            lesson = get_object_or_404(Lesson, id=lesson_id)
            lesson.delete()
            messages.success(request, "Lesson deleted successfully!")
        
        return redirect('view_lessons')
    

class ViewLesson(View):
    def get(self,request):
        pass
    def post(self,request):
        pass


class EditLesson(View):
    def get(self, request, id):
        user_id=request.session.get('user_id')
        if not user_id:
            messages.error(request,"you need to login first!")
            return redirect("login")
        user=User.objects.get(id=user_id)
        if not user.role.lower()=="instructor":
            messages.error(request,"You have no permission to Edit Lesson")
        lesson = get_object_or_404(Lesson, id=id)
        return render(request, 'lesson/edit_lesson.html', {'lesson': lesson})

    def post(self, request, id):
        lesson = get_object_or_404(Lesson, id=id)
        lesson.title = request.POST.get('title')
        lesson.content = request.POST.get('content')  # Quill.js se HTML format me milega
        lesson.video_url = request.POST.get('video_url')
        lesson.save()
        return redirect('manage_lessons', id=lesson.course.id)

class DeleteLesson(View):
    def get(self,request):
        pass
    def post(self,request):
        pass
    