from django.urls import path
from .views import LeaderBoard,UserProgressView,SetGoals

urlpatterns = [    
path('leaderboard/<int:course_id>/',LeaderBoard.as_view(), name='leaderboard'),
path('my-progress/', UserProgressView.as_view(), name='user_progress'),
path('set-goals',SetGoals.as_view(),name='set-goals'),
]

