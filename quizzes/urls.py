from django.urls import path
from . import views


urlpatterns = [

    path('add_quiz/<int:course_id>/',views.AddQuiz.as_view(),name='add_quiz'),
    path('edit_quiz/<int:quiz_id>/',views.EditQuiz.as_view(),name='edit_quiz'),
    path('delete_quiz/<int:quiz_id>/',views.DeleteQuiz.as_view(),name='delete_quiz'),
    path('start_quiz/<int:course_id>/<int:quiz_id>/',views.StartQuizView.as_view(),name='start_quiz'),
    path('quiz_result/<int:quiz_id>/',views.QuizResult.as_view(),name='quiz_result'),
]
