from django.contrib import admin
from .models import *


# Register your models here.


class Registeradmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'password')


class Quizadmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')


class Questionadmin(admin.ModelAdmin):
    list_display = ('id', 'quiz', 'level', 'question', 'option_one', 'option_two', 'option_three', 'option_four', 'answer')


class Useransweradmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'level', 'questions_id', 'quiz', 'attempted', 'completed', 'answer')


admin.site.register(Register, Registeradmin)
admin.site.register(Quiz, Quizadmin)
admin.site.register(Question, Questionadmin)
admin.site.register(UserAnswer, Useransweradmin)
