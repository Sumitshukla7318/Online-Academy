import numpy as np
import pandas as pd
from django.shortcuts import render,redirect
from django.views import View
from .models import UserProgress,UserGoal,UserStreak
from quizzes.models import QuizAttempt 
from django.contrib import messages
from users.models import User

# Create your views here.
class LeaderBoard(View):
    def get(self,request,course_id):
        top_users=UserProgress.objects.filter(course_id=course_id).order_by('-lessons_completed')[:10]
        context={
            'top_users':top_users
        }
        return render(request,"users/leader_board.html",context)
    

    def post(self,request,course_id):
        pass

class UserProgressView(View):
    def get(self,request):
        user_id = request.session['user_id']
        if not user_id:
            messages.error(request,"You need to Login First")
        user=User.objects.get(id=user_id)
            
        progress = UserProgress.objects.filter(user=user).select_related("course")

    # Get All Quiz Attempts
        quiz_attempts = QuizAttempt.objects.filter(user=user)

    # Pandas DataFrame for Quiz Performance Analysis
        if quiz_attempts.exists():
            quiz_data = pd.DataFrame(list(quiz_attempts.values("quiz__title", "score", "correct_answers", "incorrect_answers")))
        
            quiz_data["accuracy"] = (quiz_data["correct_answers"] / (quiz_data["correct_answers"] + quiz_data["incorrect_answers"])) * 100
            avg_score = np.mean(quiz_data["score"])
            avg_accuracy = np.mean(quiz_data["accuracy"])
        else:
            quiz_data = None
            avg_score = 0
            avg_accuracy = 0

    # Calculate Lesson Progress
        total_lessons = sum([p.total_lessons for p in progress])
        completed_lessons = sum([p.lessons_completed for p in progress])
        lesson_completion_percentage = (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0

    # Get Leaderboard Data
        all_users = UserProgress.objects.all().values("user__username", "lessons_completed")
        leaderboard_df = pd.DataFrame(list(all_users)).sort_values(by="lessons_completed", ascending=False)
        user_rank = (leaderboard_df.index[leaderboard_df["user__username"] == user.username].tolist()[0] + 1) if user.username in leaderboard_df["user__username"].values else "N/A"

        context = {
           "progress": progress,
           "total_lessons": total_lessons,
           "completed_lessons": completed_lessons,
           "lesson_completion_percentage": round(lesson_completion_percentage, 2),
           "quiz_data": quiz_data.to_dict(orient="records") if quiz_data is not None else [],
           "avg_score": round(avg_score, 2),
           "avg_accuracy": round(avg_accuracy, 2),
           "user_rank": user_rank,
        }

        return render(request, "users/user_progress.html", context)

    
    def post(self,request):
        pass


class SetGoals(View):
    def get(self, request):
        return render(request, "users/set-goals.html")

    def post(self, request):
        goal_type = request.POST.get("goal_type")
        target_value = request.POST.get("target_value")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")

        if not all([goal_type, target_value, start_date, end_date]):
            messages.error(request, "All fields are required!")
            return redirect("set-goals")

        try:
            # Convert target_value to integer and validate
            target_value = int(target_value)
            if target_value <= 0:
                raise ValueError("Target value must be positive")
                
            # Create the goal
            UserGoal.objects.create(
                user=User.objects.get(id=request.session["user_id"]),
                goal_type=goal_type,
                target_value=target_value,
                start_date=start_date,
                end_date=end_date,
            )
            messages.success(request, "Your goal has been set successfully!")
            return redirect("/")
            
        except ValueError as e:
            messages.error(request, f"Invalid target value: {e}")
            return redirect("set-goals")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect("set-goals")
