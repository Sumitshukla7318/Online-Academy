from django.urls import path
from . import views

urlpatterns = [
    path('signup/',views.SignupView.as_view(),name="signup"),
    path('login/',views.LoginView.as_view(),name="login"),
    path('logout/',views.LogoutView.as_view(),name="logout"),
    path('profile/',views.ProfileView.as_view(),name="profile"),
    path('Instructor_dashboard/',views.InstructorDashboard.as_view(),name="Instructor_dashboard"),
    path('student_detail/<int:id>/',views.StudentDetail.as_view(),name='student_detail'),
    path('request_instructorship/',views.RequestInstructorship.as_view(),name='request_instructorship'),
    path('request_adminship/',views.RequestAdminship.as_view(),name='request_adminship'),
    
]
