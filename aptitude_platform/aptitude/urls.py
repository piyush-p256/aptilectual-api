from django.urls import path
from .views import RegisterView, LoginView, ProfileView, DailyProblemsView, SubmitAnswerView, DailyLeaderboardView, MonthlyLeaderboardView, PastProblemsView, LogoutView

urlpatterns = [
   path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('problems/daily/', DailyProblemsView.as_view(), name='daily_problems'),
    path('submit_answer/', SubmitAnswerView.as_view(), name='submit_answer'),
    path('leaderboard/daily/', DailyLeaderboardView.as_view(), name='daily_leaderboard'),
    path('leaderboard/monthly/', MonthlyLeaderboardView.as_view(), name='monthly_leaderboard'),
    path('past_problems/', PastProblemsView.as_view(), name='past_problems'),
]
