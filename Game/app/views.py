from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .serilizers import *


# Create your views here.


@api_view(['POST'])
def register(reuqest):
    first_name = reuqest.POST.get('first_name', '')
    last_name = reuqest.POST.get('last_name', '')
    email = reuqest.POST.get('email', '')
    password = reuqest.POST.get('password', '')
    conform_password = reuqest.POST.get('conform_password', '')
    try:
        if password == conform_password:
            user = Register()
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.password = password
            user.save()
            return JsonResponse({'Message': 'Register Success.. '})
        else:
            return JsonResponse({'Message': 'Password and Conform Password is not match..'})
    except Exception as e:
        return JsonResponse({'Message': e.__str__()})


@api_view(['POST'])
def login(request):
    email = request.POST.get('email', '')
    password = request.POST.get('password', '')
    try:
        user_login = Register.objects.get(email=email)
        if user_login.password == password:
            user = request.session['email'] = email
            print(user)
            return JsonResponse({'Message': 'Login Success..'})
        else:
            return JsonResponse({'Message': 'Password is not match'})
    except Exception as e:
        return JsonResponse({'Message': e.__str__()})


@api_view(['GET'])
def logout(request):
    del request.session['email']
    return JsonResponse({'Message': 'Logout Success'})


@api_view(['GET'])
def quiz_name(request):
    try:
        user = Register.objects.get(email=request.session['email'])
        print(user)
        all_quiz = Quiz.objects.all()
        all_quiz_list = []
        for quiz in all_quiz:
            data = {
                'ID': quiz.id,
                'Name': quiz.name,
                'Description': quiz.description
            }
            all_quiz_list.append(data)
        return JsonResponse(
            {'User Name': f'{user.first_name} {user.last_name}', 'Message': 'All Quiz', 'Quiz': all_quiz_list})
    except Exception as e:
        return JsonResponse({'Message': f'{e.__str__()}'})


@api_view(['POST'])
def enter_game(request):
    try:
        user = Register.objects.get(email=request.session['email'])
        Number = request.POST.get('Number', '')
        list_of_question = []
        count = 0

        if Number is not '':
            try:
                Number = int(Number)
                one_quiz = Quiz.objects.get(id=Number)
                all_question = Question.objects.filter(quiz=one_quiz)
                for question in all_question:
                    question_data = {
                        'Question': question.question,
                        'Option No 1': question.option_one,
                        'Option No 2': question.option_two,
                        'Option No 3': question.option_three,
                        'Option No 4': question.option_four,
                    }
                    count += 1
                    list_of_question.append(question_data)
                return JsonResponse(
                    {'User Name': f'{user.first_name} {user.last_name}', 'Quiz Name': f'Enter {one_quiz} Quiz',
                     'Total Question': f'{count}',
                     'Message': 'The answer is full not a A, B, C, D.., Example: (A) answer',
                     'Questions': list_of_question})
            except Exception as e:
                return JsonResponse({'message': f'{e.__str__()}'})
        else:
            return JsonResponse({'Message': 'Enter Number'})
    except Exception as e:
        return JsonResponse({'Message': e.__str__()})


@api_view(['POST'])
def answer(request):
    question = request.POST['question']
    answer = request.POST['answer']
    question_get = Question.objects.get(id=question)
    print(question_get)
    user_answer = User_Answer()
    user = Register.objects.get(email=request.session['email'])
    try:
        user_answer.attempted = True
        user_answer.questions_id = question_get
        user_answer.quiz = question_get.quiz
        user_answer.answer = answer
        user_answer.user = user
        user_answer.save()
        print(user_answer.answer)
        if answer == question_get.answer:
            user_answer.complet = True
            user_answer.save()
            print(user_answer.user, user_answer.complet)
            return JsonResponse(
                {'User Name': f'{user.first_name} {user.last_name}', 'Question': question_get.question, 'Answer': answer,
                 'Message': 'Your Answer is Coreact'})
        else:
            print(user_answer.user, user_answer.answer)
            return JsonResponse(
                {'User Name': f'{user}', 'Question': question_get.question, 'Answer': answer,
                 'Message': 'Your Answer is Wrong'})
    except Exception as e:
        return JsonResponse({'Message': e.__str__()})


@api_view(['POST'])
def score(request):
    quiz_id = request.POST.get('quiz_id', '')
    correct = 0
    wrong = 0
    attempted = 0
    unattempted = 0
    quiz_title = ''
    try:
        user = Register.objects.get(email=request.session['email'])
        if quiz_id is not '':
            quiz_question = Question.objects.filter(quiz=quiz_id)
            user_data = User_Answer.objects.filter(quiz=quiz_id)
            print(user_data)
            for quiz in quiz_question:
                quiz_title = quiz.quiz.name
            for i in user_data:
                if i.attempted:
                    attempted += 1
                    if i.complet:
                        correct += 1
                    else:
                        wrong += 1
            total_question = quiz_question.count()
            unattempted_question = total_question - attempted
            total_score = correct * 100 / total_question
            return JsonResponse(
                {'User': f'{user.first_name} {user.last_name}', 'Quiz Name': f'{quiz_title}',
                 'Total Question': total_question, 'Correct': correct,
                 'Wrong': wrong,
                 'Attempted': f'{attempted} Question', 'Unattempted': f'{unattempted_question} Question',
                 'Total Socre': total_score})
        else:
            all_question = Question.objects.all()
            user_data = User_Answer.objects.filter(user=user)
            quiz_title = 'All Quiz'
            for i in user_data:
                if i.attempted:
                    attempted += 1
                    if i.complet:
                        correct += 1
                    else:
                        wrong += 1
                else:
                    unattempted += 1
            total_question = all_question.count()
            unattempted_question = total_question - attempted
            total_score = correct * 100 / total_question
            return JsonResponse(
                {'User': f'{user.first_name} {user.last_name}', 'Quiz Name': f'{quiz_title}',
                 'Total Question': total_question, 'Correct': correct,
                 'Wrong': wrong,
                 'Attempted': f'{attempted} Question', 'Unattempted': f'{unattempted_question} Question',
                 'Total Socre': total_score})
    except Exception as e:
        return JsonResponse({'Message': e.__str__()})
