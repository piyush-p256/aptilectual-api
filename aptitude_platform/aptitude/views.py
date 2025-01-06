from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.db.models import Count, Q, Min
from .models import CustomUser, Problem, UserAnswer, LeaderDaily
from .serializers import CustomUserSerializer, ProblemSerializer, UserAnswerSerializer, LeaderboardUserSerializer
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)

class ProfileView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_object(self):
        return self.request.user

class DailyProblemsView(generics.ListAPIView):
    serializer_class = ProblemSerializer

    def get_queryset(self):
        now = timezone.localtime(timezone.now())
        start_time = now.replace(hour=1, minute=0, second=0, microsecond=0)
        end_time = now.replace(hour=18, minute=0, second=0, microsecond=0)

        print(f"Current time: {now}")
        print(f"Start time: {start_time}")
        print(f"End time: {end_time}")

        if start_time <= now <= end_time:
            print("Within time window")
            queryset = Problem.objects.filter(is_active=True, done=False)
            print(f"Queryset: {queryset}")
            return queryset
        else:
            print("Outside time window")
            return Problem.objects.none()


class SubmitAnswerView(generics.CreateAPIView):
    serializer_class = UserAnswerSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        problem = serializer.validated_data['problem']
        selected_option = serializer.validated_data['selected_option']
        solution_image_url = serializer.validated_data.get('solution_image_url', '')

        # Convert current time to the local timezone
        now = timezone.localtime(timezone.now())
        start_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_time = now.replace(hour=18, minute=0, second=0, microsecond=0)

        # Check if the current time is within the allowed time window
        if not (start_time <= now <= end_time):
            raise ValueError("Submission is not allowed at this time.")

        # Check if the user has already submitted an answer for this problem
        if UserAnswer.objects.filter(user=user, problem=problem).exists():
            raise ValueError("You have already submitted an answer for this problem.")

        # Determine if the answer is correct
        is_correct = problem.correct_option == selected_option

        # Update user stats
        user.total_attempted += 1
        if is_correct:
            user.total_correct += 1

        # Update streak
        last_submission = UserAnswer.objects.filter(user=user).order_by('-time_solved').first()
        if last_submission and last_submission.time_solved.date() == (timezone.localtime(timezone.now()).date() - timezone.timedelta(days=1)):
            user.current_streak += 1
        else:
            user.current_streak = 1

        if user.current_streak > user.highest_streak:
            user.highest_streak = user.current_streak

        user.save()

        # Save the UserAnswer instance
        serializer.save(user=user, is_correct=is_correct, solution_image_url=solution_image_url)

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            if response.status_code == status.HTTP_201_CREATED:
                return response
            return Response(response.data, status=response.status_code)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        


class DailyLeaderboardView(generics.ListAPIView):
    serializer_class = LeaderboardUserSerializer

    def get_queryset(self):
        leader_daily = LeaderDaily.objects.first()
        if leader_daily and leader_daily.show_leaderboard:
            # Get users who have submitted answers today
            now = timezone.now()
            start_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end_time = now.replace(hour=23, minute=59, second=59, microsecond=999999)

            # Annotate users with the number of correct answers and the minimum time taken to solve them
            users_with_answers = UserAnswer.objects.filter(time_solved__range=(start_time, end_time))
            users = CustomUser.objects.filter(id__in=users_with_answers.values_list('user', flat=True)).annotate(
                correct_answers_today=Count('useranswer', filter=Q(useranswer__is_correct=True, useranswer__time_solved__range=(start_time, end_time))),
                min_time_solved=Min('useranswer__time_solved', filter=Q(useranswer__is_correct=True, useranswer__time_solved__range=(start_time, end_time)))
            ).order_by('-correct_answers_today', 'min_time_solved')[:3]  # Limit to top 3 users

            # Prepare the response data
            leaderboard_data = []
            for rank, user in enumerate(users, start=1):
                user_answers = UserAnswer.objects.filter(user=user, time_solved__range=(start_time, end_time))
                solution_image_url = user_answers.first().solution_image_url if user_answers.exists() else None
                leaderboard_data.append({
                    'rank': rank,
                    'username': user.username,
                    'solution_image_url': solution_image_url,
                })

            return leaderboard_data
        else:
            return Response({"error": "Leaderboard is not available at this time."}, status=status.HTTP_403_FORBIDDEN)



class MonthlyLeaderboardView(generics.ListAPIView):
    serializer_class = LeaderboardUserSerializer

    def get_queryset(self):
        now = timezone.now()
        users = CustomUser.objects.filter(useranswer__time_solved__month=now.month).distinct().annotate(
            correct_answers=Count('useranswer', filter=Q(useranswer__is_correct=True)),
            total_answers=Count('useranswer')
        ).order_by('-correct_answers', '-first_position_count', '-second_position_count', '-third_position_count')
        return users

class PastProblemsView(generics.ListAPIView):
    serializer_class = ProblemSerializer

    def get_queryset(self):
        return Problem.objects.filter(done=True)
