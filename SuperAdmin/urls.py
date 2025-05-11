from django.urls import path
from . import views

urlpatterns = [
    path('',views.SuperAdminDashboard.as_view(),name='superadmin_dashboard'),
    path('user_management/<int:user_id>/',views.UserManagementView.as_view(),name='user_management'),
    path('user_management/',views.UserManagementView.as_view(),name='user_management'),
    path('Sinstructor_management/',views.InstructorManagementView.as_view(),name='Sinstructor_management'),
    path('admin_management/',views.AdminManagementView.as_view(),name='admin_management'),
    path('activity_reports/',views.ActivityReports.as_view(),name='activity_reports'),
    path('course_control/',views.CourseConrol.as_view(),name='course_control'),

    path('admin_dashboard',views.AdminDashboard.as_view(),name='admin_dashboard'),
    path('instructor-approval/', views.InstructorApprovalView.as_view(), name='instructor_approval'),
    path('approve_instructor/<int:user_id>/', views.ApproveInstructorView.as_view(), name='approve_instructor'),
    path('reject_instructor/<int:user_id>/', views.RejectInstructorView.as_view(), name='reject_instructor'),
    path('instructor_management',views.Instructor_management.as_view(),name='instructor_management'),
    path('edit-user/<int:user_id>/', views.EditUserView.as_view(), name='edit_user'),
    path('delete-user/', views.DeleteUserView.as_view(), name='delete_user'),
    path('restore-user/',views.RestoreUser.as_view(),name='restore_user'),
    path('manage_users/',views.UserManagement.as_view(),name='manage_users'),
]
