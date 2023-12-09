from django.http import JsonResponse
from rest_framework.decorators import api_view
from .serilizers import *


@api_view(['POST'])
def register(request):
    first_name = request.POST.get('first_name', '')
    last_name = request.POST.get('last_name', '')
    email = request.POST.get('email', '')
    password = request.POST.get('password', '')
    conform_password = request.POST.get('conform_password', '')
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


@api_view(['POST'])
def add_quiz(request):
    name = request.POST['name']
    description = request.POST['description']
    try:
        Quiz.objects.create(
            name=name,
            description=description
        )
        return JsonResponse({'Message': 'Add Quiz success'})
    except Exception as e:
        return JsonResponse({'Message': e.__str__()})


@api_view(['PUT'])
def update_quiz(request):
    primary_key = request.POST.get('id', '')
    name = request.POST.get('name', '')
    description = request.POST.get('description', '')
    try:
        update = Quiz.objects.get(id=primary_key)
        if not name == '':
            update.name = name
        if not description == '':
            update.description = description
        update.save()
        return JsonResponse({'Message': 'Quiz Update successfully'})
    except Exception as e:
        return JsonResponse({'Message': e.__str__()})


@api_view(['POST'])
def delete_quiz(request):
    primary_key = request.POST['id']
    try:
        delete = Quiz.objects.get(id=primary_key)
        delete.delete()
        return JsonResponse({'Message': 'Quiz Delete Successfully'})
    except Exception as e:
        return JsonResponse({'Message': e.__str__()})


@api_view(['POST'])
def add_question(request):
    quiz = request.POST['quiz']
    question = request.POST['question']
    option_one = request.POST['option_one']
    option_two = request.POST['option_two']
    option_three = request.POST['option_three']
    option_four = request.POST['option_four']
    answer = request.POST['answer']
    try:
        quiz = Quiz.objects.get(id=quiz)
        Question.objects.create(
            quiz=quiz,
            question=question,
            option_one=option_one,
            option_two=option_two,
            option_three=option_three,
            option_four=option_four,
            answer=answer
        )
        return JsonResponse({'Message': 'Add Question Successfully'})
    except Exception as e:
        return JsonResponse({'Message': e.__str__()})


@api_view(['PUT'])
def update_question(request):
    primary_key = request.POST.get('id', '')
    question = request.POST.get('question', '')
    option_one = request.POST.get('option_one', '')
    option_two = request.POST.get('option_two', '')
    option_three = request.POST.get('option_three', '')
    option_four = request.POST.get('option_four', '')
    answer = request.POST.get('answer', '')
    try:
        update = Question.objects.get(id=primary_key)
        if not question == '':
            update.question = question
        if not option_one == '':
            update.option_one = option_one
        if not option_two == '':
            update.option_two = option_two
        if not option_three == '':
            update.option_three = option_three
        if not option_four == '':
            update.option_four = option_four
        if not answer == '':
            update.answer = answer
        update.save()
        return JsonResponse({'Message': 'Update Successfully'})

    except Exception as e:
        return JsonResponse({'Message': e.__str__()})


@api_view(['POST'])
def delete_question(request):
    primary_key = request.POST['id']
    try:
        delete = Question.objects.get(id=primary_key)
        delete.delete()
        return JsonResponse({'Message': 'Delete Question successfully'})
    except Exception as e:
        return JsonResponse({'Message': e.__str__()})


@api_view(['GET'])
def quiz_name(request):
    try:
        user = Register.objects.get(email=request.session['email'])
        all_quiz = Quiz.objects.all()
        print(all_quiz)
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
    primary_key = request.POST['id']
    try:
        user = Register.objects.get(email=request.session['email'])
        list_of_question = []
        count = 0
        primary_key = int(primary_key)
        one_quiz = Quiz.objects.get(id=primary_key)
        all_question = Question.objects.filter(quiz=one_quiz)
        for question in all_question:
            question_data = {
                'Question': question.question,
                'Option No 1': question.option_one,
                'Option No 2': question.option_two,
                'Option No 3': question.option_three,
                'Option No 4': question.option_four,
            }
            list_of_question.append(question_data)
            count += 1
        return JsonResponse(
            {'User Name': f'{user.first_name} {user.last_name}', 'Quiz Name': f'Enter {one_quiz} Quiz',
             'Total Question': f'{count}',
             'Message': 'The answer is full not a A, B, C, D.., Example: (A) answer',
             'Questions': list_of_question})
    except Exception as e:
        return JsonResponse({'Message': e.__str__()})


@api_view(['POST'])
def answer(request):
    question = request.POST['question']
    answer = request.POST['answer']
    try:
        question_get = Question.objects.get(id=question)
        user = Register.objects.get(email=request.session['email'])
        previous_answers = User_Answer.objects.filter(user=user, questions_id=question_get)
        if not previous_answers:
            user_answer = User_Answer()
            user_answer.attempted = True
            user_answer.questions_id = question_get
            user_answer.quiz = question_get.quiz
            user_answer.answer = answer
            user_answer.user = user
            user_answer.save()
        else:
            user_answer = previous_answers[0]
            user_answer.answer = answer
            user_answer.save()

        if answer == question_get.answer:
            user_answer.complete = True
            user_answer.save()
            return JsonResponse({'User Name': f'{user.first_name} {user.last_name}', 'Question': question_get.question,
                                 'Answer': answer, 'Message': 'Your Answer is Correct'})
        else:
            user_answer.complete = False
            user_answer.save()
            return JsonResponse({'User Name': f'{user.first_name} {user.last_name}', 'Question': question_get.question,
                                 'Answer': answer, 'Message': 'Your Answer is Wrong'})
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
            user_data = User_Answer.objects.filter(quiz=quiz_id, user=user)
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
                 'Total Score': total_score})
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
                 'Total Question': total_question, 'Correct': correct, 'Wrong': wrong,
                 'Attempted': f'{attempted} Question', 'Unattempted': f'{unattempted_question} Question',
                 'Total Score': total_score})
    except Exception as e:
        return JsonResponse({'Message': e.__str__()})
