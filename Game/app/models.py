from django.db import models


# Create your models here.

class Register(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)


class Quiz(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.CharField(max_length=250)
    option_one = models.CharField(max_length=50, null=True)
    option_two = models.CharField(max_length=50, null=True)
    option_three = models.CharField(max_length=50, null=True)
    option_four = models.CharField(max_length=50, null=True)
    answer = models.CharField(max_length=50)

    def __str__(self):
        return self.question


class User_Answer(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    questions_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True)
    attempted = models.BooleanField(default=False)
    complet = models.BooleanField(default=False)
    answer = models.CharField(max_length=50)


