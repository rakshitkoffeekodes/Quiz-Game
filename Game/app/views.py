from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import *
from .serilizers import *
from rest_framework.authentication import SessionAuthentication


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
            user = request.session[email] = email
            print(user)
            return JsonResponse({'Message': 'Login Success..'})
        else:
            return JsonResponse({'Message': 'Password is not match'})
    except Exception as e:
        return JsonResponse({'Message': e.__str__()})


@api_view(['GET'])
def quiz_name(request):
    # user = Register.objects.get(email=request.session['email'])
    print(request.session.items())
    return JsonResponse({'Message': 'success'})


@api_view(['POST'])
def enter_game(request):
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
                {'Quiz Name': f'Enter {one_quiz} Quiz', 'Total Question': f'{count}',
                 'Message': 'The answer is full not a A, B, C, D.., Example: (A) answer',
                 'Questions': list_of_question})
        except Exception as e:
            return JsonResponse({'message': f'{e.__str__()}'})
    else:
        return JsonResponse({'Message': 'Enter Number'})


# @api_view(['POST'])
# def answer(request):
#     question = request.POST['question']
#     answer = request.POST['answer']
#     question_get = Question.objects.get(id=question)
#     try:
#         question_get.attempted = True
#         question_get.save()
#         print(question_get.attempted)
#         print(question_get.complet)
#         if answer == question_get.answer:
#             question_get.complet = True
#             question_get.save()
#             print(question_get.complet)
#             return JsonResponse(
#                 {'Question': question_get.question, 'Your Answer': answer, 'Message': 'Your Answer is Correct'})
#         else:
#             print('===================')
#             return JsonResponse(
#                 {'Question': question_get.question, 'Your Answer': answer, 'Message': 'Your Answer is Wrong'})
#     except Exception as e:
#         return JsonResponse({'Message': e.__str__()})

@api_view(['POST'])
def answer(request):
    question = request.POST['question']
    answer = request.POST['answer']
    print(request.session["email"])
    print('===============')
    user = Register.objects.get(email=request.session['email'])
    print(user)
    return JsonResponse({'adf': 'dgadf'})


@api_view(['POST'])
def score(request):
    quiz_id = request.POST.get('quiz_id', '')
    correct = 0
    wrong = 0
    attempted = 0
    unattempted = 0
    quiz = ''
    if quiz_id:
        score_quiz = Question.objects.filter(quiz=quiz_id)
        for question in score_quiz:
            quiz = question.quiz.name
    else:
        score_quiz = Question.objects.all()
        quiz = 'All Quiz'
    for question in score_quiz:
        if question.attempted:
            attempted += 1
            if question.complet:
                correct += 1
            else:
                wrong += 1
        else:
            unattempted += 1
    total_socre = correct * 100 / score_quiz.count()
    return JsonResponse(
        {'Message': quiz, 'Total Question': score_quiz.count(), 'Correct': correct, 'Wrong': wrong,
         'Attempted': f'{attempted} Question', 'Unattempted': f'{unattempted} Question', 'Total Socre': total_socre})
