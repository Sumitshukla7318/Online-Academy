from django.contrib import admin
from .models import Question,Answer,QuestionAttempt,Quiz,QuizAttempt

class QuestionAdmin(admin.ModelAdmin):
    list_display=('id','quiz','text','difficulty')
admin.site.register(Question,QuestionAdmin)

class QuizAdmin(admin.ModelAdmin):
    list_display=('id','course','title','description','time_limit')

class QuizAttemptAdmin(admin.ModelAdmin):
    list_display=('user','quiz','score','correct_answers')

admin.site.register(Quiz,QuizAdmin)
admin.site.register(QuizAttempt,QuizAttemptAdmin)

# Register your models here.
