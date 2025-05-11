from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from courses.models import Course
from . models import Quiz,QuizAttempt,Question,Answer,QuestionAttempt
from django.contrib import messages
from django.http import JsonResponse
from users.models import User
from django.utils.timezone import now

# Create your views here.
class AddQuiz(View):
    
    def get(self, request, course_id):
        user_id=request.session.get('user_id')
        if not user_id:
            messages.error(request,"you need to login first!")
            return redirect("login")
        user=User.objects.get(id=user_id)
        if not user.role.lower()=='instructor':
            messages.error(request,"you have no permission do this")
        course = get_object_or_404(Course, id=course_id)  # Fetch course
        return render(request, "Instructor/add_quiz.html", {"course": course})

    def post(self, request, course_id):
        title = request.POST.get("title")
        description = request.POST.get("description")
        time_limit = request.POST.get("duration")  # Ensure matching field name
        
        # Create the Quiz
        quiz = Quiz.objects.create(title=title, description=description, time_limit=time_limit, course_id=course_id)

        # Process Questions
        questions = request.POST.getlist("questions[]")
        for i, question_text in enumerate(questions):
            # print("ddd",question_text)
            question = Question.objects.create(quiz=quiz, text=question_text)
            
            # Process Answer Options
            for option_label in ["A", "B", "C", "D"]:
                option_text = request.POST.get(f"option_{i}_{option_label}", "")
                is_correct = request.POST.get(f"correct_answer_{i}") == option_label
                
                if option_text:  # Ensure option is not empty
                    Answer.objects.create(question=question, text=option_text, is_correct=is_correct)

        messages.success(request, "Quiz added successfully!")
        return redirect("Icourse_details", id=course_id)  # Use correct URL name





class StartQuizView(View):
    def get(self, request, course_id=None, quiz_id=None):
        user_id=request.session.get('user_id')
        if not user_id:
            messages.error(request,"you need to login first!")
            return redirect("login")
        course = get_object_or_404(Course, id=course_id)
        quizzes = Quiz.objects.filter(course=course)
        
        quiz = None
        if quiz_id:
            quiz = get_object_or_404(Quiz, id=quiz_id, course=course)

        return render(request, 'quiz/start_quiz.html', {'quizzes': quizzes, 'quiz': quiz})

    def post(self, request, course_id, quiz_id):
        user = get_object_or_404(User, id=request.session['user_id'])
        course = get_object_or_404(Course, id=course_id)
        quiz = get_object_or_404(Quiz, id=quiz_id, course=course)
        
        questions = quiz.questions.all()
        score = 0
        correct_answers = 0
        incorrect_answers = 0

        # Check if the user has an existing attempt for this quiz
        attempt, created = QuizAttempt.objects.get_or_create(
            user=user, quiz=quiz, defaults={'score': 0, 'correct_answers': 0, 'incorrect_answers': 0, 'completed': True, 'timestamp': now()}
        )

        # Delete previous question attempts if re-attempting
        if not created:
            attempt.question_attempts.all().delete()

        for question in questions:
            selected_option_id = request.POST.get(f"question_{question.id}")
            selected_option = Answer.objects.filter(id=selected_option_id).first() if selected_option_id else None
            is_correct = selected_option.is_correct if selected_option else False

            if is_correct:
                score += 1
                correct_answers += 1
            else:
                incorrect_answers += 1

            QuestionAttempt.objects.create(
                quiz_attempt=attempt,
                question=question,
                selected_answer=selected_option,
                is_correct=is_correct
            )

        # Update attempt instead of creating a new one
        attempt.score = score
        attempt.correct_answers = correct_answers
        attempt.incorrect_answers = incorrect_answers
        attempt.timestamp = now()
        attempt.save()

        messages.success(request, f"Quiz completed! Your score: {score}/{len(questions)}")
        return redirect('quiz_result', quiz_id=quiz.id)


class EditQuiz(View):
    def get(self, request, quiz_id):
        user_id=request.session.get('user_id')
        if not user_id:
            messages.error(request,"you need to login first!")
            return redirect("login")
        user=User.objects.get(id=user_id)
        if not user.role.lower()=='instructor':
            messages.error(request,"you have no permission do this")
        quiz = get_object_or_404(Quiz, id=quiz_id)
        return render(request, "quiz/edit_quiz.html", {"quiz": quiz})

    def post(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id)

        # Update quiz title
        quiz_title = request.POST.get("quiz_title")
        if quiz_title:
            quiz.title = quiz_title
            quiz.save()

        # Handle questions
        existing_questions = {q.id: q for q in quiz.questions.all()}
        new_questions = request.POST.getlist("questions[]")

        # Update or create questions
        for index, question_text in enumerate(new_questions):
            if question_text.strip():
                if index < len(existing_questions):  # Update existing question
                    question = list(existing_questions.values())[index]
                    question.text = question_text.strip()
                    question.save()
                else:  # Create new question
                    Question.objects.create(quiz=quiz, text=question_text.strip())

        # Delete extra existing questions that are not in the new list
        if len(existing_questions) > len(new_questions):
            for question in list(existing_questions.values())[len(new_questions):]:
                question.delete()

        messages.success(request, "Quiz updated successfully!")
        return redirect("edit_quiz", quiz_id=quiz.id)
    


class DeleteQuiz(View):
    def get(self,request,quiz_id):
        user_id=request.session.get('user_id')
        if not user_id:
            messages.error(request,"you need to login first!")
            return redirect("login")
        quiz=Quiz.objects.get(id=quiz_id)
        course_id=quiz.course.id
        quiz.delete()
        return redirect('Icourse_details',id=course_id)
    
class QuizResult(View):
    def get(self, request, quiz_id):
        user_id=request.session.get('user_id')
        if not user_id:
            messages.error(request,"you need to login first!")
            return redirect("login")
        # Get the latest attempt of the logged-in user
        quiz = get_object_or_404(Quiz, id=quiz_id)
        latest_attempt = QuizAttempt.objects.filter(user=User.objects.get(id=request.session['user_id']), quiz=quiz, completed=True).order_by('-timestamp').first()

        if not latest_attempt:
            return redirect('start_quiz', course_id=quiz.course.id)  # Redirect if no attempt found

        # Fetch question attempts related to this attempt
        question_attempts = QuestionAttempt.objects.filter(quiz_attempt=latest_attempt)

        # Calculate total questions and percentage
        total_questions = quiz.questions.count()
        percentage = (latest_attempt.score / total_questions) * 100 if total_questions > 0 else 0

        context = {
            'quiz': quiz,
            'score': latest_attempt.score,
            'total_questions': total_questions,
            'percentage': round(percentage, 2),
            'question_attempts': question_attempts,
        }

        return render(request, 'quiz/quiz_result.html', context)

        