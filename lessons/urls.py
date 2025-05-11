from django.urls import path
from . import views

urlpatterns = [
    
    path('course/<int:id>/lessons/',views.CourseLession.as_view(), name='course_lessons'),
    path('course/<int:id>/lessons/<int:lesson_id>/',views.CourseLession.as_view(), name='course_lessons'),
    path('add_lesson/<int:id>/',views.AddLesson.as_view(),name="add_lesson"),
    path('manage_lessons/<int:id>/',views.ManageLesson.as_view(),name='manage_lessons'),
    path('edit_lesson/<int:id>/',views.EditLesson.as_view(),name="edit_lesson"),
    path('view_lesson/<int:id>/',views.ViewLesson.as_view(),name='view_lesson'),  
    path('delete_lesson/<int:lesson_id>/',views.DeleteLesson.as_view(),name='delete_lesson'),
    path('course/<int:course_id>/lesson/<int:lesson_id>/complete/',views.MarkLessonCompleted.as_view(), name='mark_lesson_completed'),  


]
