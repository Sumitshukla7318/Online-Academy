from django.db import models
from courses.models import Course
from users.models import User

class Quiz(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="quizzes")
    title = models.CharField(max_length=255)
    description = models.TextField()
    time_limit = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class Question(models.Model):
    id = models.AutoField(primary_key=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()
    difficulty = models.CharField(max_length=50, choices=[("Easy", "Easy"), ("Medium", "Medium"), ("Hard", "Hard")])

    def __str__(self):
        return self.text

class Answer(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="attempts")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)
    correct_answers = models.PositiveIntegerField(default=0) 
    incorrect_answers = models.PositiveIntegerField(default=0)  
    completed = models.BooleanField(default=False) 
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} - {self.score}"

class QuestionAttempt(models.Model):
    quiz_attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name="question_attempts")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.ForeignKey(Answer, on_delete=models.SET_NULL, null=True, blank=True) 
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quiz_attempt.user.username} - {self.question.text} - {'Correct' if self.is_correct else 'Wrong'}"
