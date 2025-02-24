from django.db import models
from users.models import User
from quizzes.models import Quiz

class QuizResult(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="quiz_results")
    quiz=models.ForeignKey(Quiz,on_delete=models.CASCADE,related_name="results")
    score=models.FloatField()
    time_taken=models.PositiveIntegerField()
    completed_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} - Score :{self.score}"

