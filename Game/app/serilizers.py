from rest_framework import serializers
from .models import *


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ('id', 'name', 'description')


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('user', 'quiz', 'question', 'option_one', 'option_two', 'option_three', 'option_four')


class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = '__all__'
