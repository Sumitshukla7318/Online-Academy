from django.urls import path
from . import views

urlpatterns = [
    path("add_course/",views.AddCourse.as_view(),name="add_course"),
    path('course/<int:id>/', views.CourseDetail.as_view(), name='course_detail'),
    path('courses/',views.Courses.as_view(),name="courses"),
    path('my-courses/', views.MyCourses.as_view(), name='my_courses'),
     path('instructor_courses/',views.InstructorCourses.as_view(),name='instructor_courses'),
    path('Icourse_details/<int:id>/',views.InstructorCourseDetail.as_view(),name='Icourse_details'),
    path('Iedit_course/<int:id>/',views.EditCourse.as_view(),name='Iedit_course'),
    path('Idelete_course/<int:id>/',views.DeleteCourse.as_view(),name='Idelete_course'),
    path('students/',views.StudentsEnrolledInCourse.as_view(),name="students"),
    path('student_detail/<int:id>/',views.StudentDetail.as_view(),name='student_detail'),
    path('earnings',views.Earning.as_view(),name='earnings'),
    path('settings',views.Settings.as_view(),name='settings'),
    
    
]
