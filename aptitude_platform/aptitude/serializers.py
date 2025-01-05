from rest_framework import serializers
from .models import CustomUser, Problem, UserAnswer

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'total_attempted', 'total_correct', 'current_streak', 'highest_streak']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

class LeaderboardUserSerializer(serializers.Serializer):
    rank = serializers.IntegerField()
    username = serializers.CharField()
    solution_image_url = serializers.URLField()

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = '__all__'

class UserAnswerSerializer(serializers.ModelSerializer):
    problem = serializers.PrimaryKeyRelatedField(queryset=Problem.objects.all())

    class Meta:
        model = UserAnswer
        fields = ['problem', 'selected_option', 'solution_image_url', 'time_solved']
        read_only_fields = ['user', 'time_solved']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data.pop('user', None)  # Ensure 'user' is not in validated_data
        return UserAnswer.objects.create(user=user, **validated_data)
