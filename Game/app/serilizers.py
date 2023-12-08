from rest_framework import serializers
from .models import *


class Quizserilizer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ('id', 'name', 'description')


class Questionserilizer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('user', 'quiz', 'question', 'option_one', 'option_two', 'option_three', 'option_four')
