import requests
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .serilizers import *


@api_view(['POST'])
def register(request):
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    password = request.POST['password']
    conform_password = request.POST['conform_password']
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
    email = request.POST['email']
    password = request.POST['password']
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
    description = request.POST.get('description', '')

    name_list = name.split(',')
    description_list = description.split('.,')
    try:
        for i in range(len(name_list)):
            quiz_add = Quiz()
            quiz_add.name = name_list[i]
            quiz_add.description = description_list[i]
            quiz_add.save()
        return JsonResponse({'Message': 'Add Quiz success'})
    except Exception as e:
        return JsonResponse({'Message': e.__str__()})


@api_view(['PUT'])
def update_quiz(request):
    primary_key = request.POST['id']
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


@api_view(['DELETE'])
def delete_quiz(request):
    primary_key = request.POST['id']
    try:
        delete = Quiz.objects.get(id=primary_key)
        delete.delete()
        return JsonResponse({'Message': 'Quiz Delete Successfully'})
    except Exception as e:
        return JsonResponse({'Message': e.__str__()})


@api_view(['GET'])
def view_quiz(request):
    all_quiz = Quiz.objects.all()
    serial = QuizSerializer(all_quiz, many=True)
    return JsonResponse({'Message': 'All Quiz', 'Quiz': serial.data})


@api_view(['POST'])
def add_question(request):
    quiz = request.POST['quiz']
    question = request.POST['question']
    option_one = request.POST['option_one']
    option_two = request.POST['option_two']
    option_three = request.POST['option_three']
    option_four = request.POST['option_four']
    answers = request.POST['answer']

    question_list = question.split('.,')
    option_one_list = option_one.split(',')
    option_two_list = option_two.split(',')
    option_three_list = option_three.split(',')
    option_four_list = option_four.split(',')
    answer_list = answers.split(',')

    try:
        quiz_id = Quiz.objects.get(id=quiz)
        for i in range(len(question_list)):
            question_add = Question()
            question_add.quiz = quiz_id
            question_add.question = question_list[i]
            question_add.option_one = option_one_list[i]
            question_add.option_two = option_two_list[i]
            question_add.option_three = option_three_list[i]
            question_add.option_four = option_four_list[i]
            question_add.answer = answer_list[i]
            question_add.save()
        return JsonResponse({'Message': 'Add Question Success'})

    except Exception as e:
        return JsonResponse({'Message': e.__str__()})


@api_view(['PUT'])
def update_question(request):
    primary_key = request.POST['id']
    question = request.POST.get('question', '')
    option_one = request.POST.get('option_one', '')
    option_two = request.POST.get('option_two', '')
    option_three = request.POST.get('option_three', '')
    option_four = request.POST.get('option_four', '')
    answers = request.POST.get('answer', '')
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
            update.answer = answers
        update.save()
        return JsonResponse({'Message': 'Update Question Successfully'})

    except Exception as e:
        return JsonResponse({'Message': e.__str__()})


@api_view(['DELETE'])
def delete_question(request):
    primary_key = request.POST['id']
    try:
        delete = Question.objects.get(id=primary_key)
        delete.delete()
        return JsonResponse({'Message': 'Delete Question successfully'})
    except Exception as e:
        return JsonResponse({'Message': e.__str__()})


@api_view(['GET'])
def view_question(request):
    list_of_question = []
    all_question = Question.objects.all()
    for question in all_question:
        question_data = {
            'Quiz': question.quiz.name,
            'Question': question.question,
            'Option No 1': question.option_one,
            'Option No 2': question.option_two,
            'Option No 3': question.option_three,
            'Option No 4': question.option_four,
            'Answer': question.answer
        }
        list_of_question.append(question_data)
    return JsonResponse({'Message': 'All Question', 'Question': list_of_question})


@api_view(['GET'])
def quiz_name(request):
    try:
        user = Register.objects.get(email=request.session['email'])
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
            {'User Name': f'{user.first_name} {user.last_name}', 'Message': 'All Quiz',
             'Quiz': all_quiz_list})
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
    user = Register.objects.get(email=request.session['email'])
    dict1 = {}
    all_answer = []
    correct = 0
    wrong = 0
    attempted = 0
    unattempted = 0
    quiz_id = request.POST['quiz']
    question = request.POST['question']
    answers = request.POST.get('answer', '')
    question_list = question.split(',')
    answer_list = answers.split(',')

    for key, value in zip(question_list, answer_list):
        dict1[key] = value.strip()

    try:

        for key in dict1:
            question_get = Question.objects.get(id=key, quiz=quiz_id)
            previous_answers = UserAnswer.objects.filter(user=user, questions_id=question_get)
            if not dict1[key] == '':
                if not previous_answers:
                    user_answer = UserAnswer()
                    user_answer.attempted = True
                    user_answer.questions_id = question_get
                    user_answer.quiz = question_get.quiz
                    user_answer.answer = dict1[key]
                    user_answer.user = user
                    user_answer.save()
                else:
                    user_answer = previous_answers[0]
                    user_answer.answer = dict1[key]
                    user_answer.save()

                if dict1[key] == question_get.answer:
                    user_answer.completed = True
                    user_answer.save()
                    result = {
                        'Quiz Name': question_get.quiz.name,
                        'Question': question_get.question,
                        'Answer': dict1[key],
                        'Message': 'Your Answer is Correct'
                    }
                else:
                    user_answer.completed = False
                    user_answer.save()
                    result = {
                        'Quiz Name': question_get.quiz.name,
                        'Question': question_get.question,
                        'Your Answer': dict1[key],
                        'Correct Answer': question_get.answer,
                        'Message': 'Your Answer is Wrong'
                    }
            else:
                if not previous_answers:
                    user_answer = UserAnswer()
                    user_answer.attempted = True
                    user_answer.questions_id = question_get
                    user_answer.quiz = question_get.quiz
                    user_answer.answer = dict1[key]
                    user_answer.user = user
                    user_answer.save()
                    result = {
                        'Quiz Name': question_get.quiz.name,
                        'Question': question_get.question,
                    }
                else:
                    user_answer.completed = False
                    user_answer.save()
                    result = {
                        'Quiz Name': question_get.quiz.name,
                        'Question': question_get.question,
                    }
            all_answer.append(result)
        quiz_question = Question.objects.filter(quiz=quiz_id)
        user_answer = UserAnswer.objects.filter(quiz=quiz_id, user=user)
        for i in user_answer:
            if i.attempted:
                attempted += 1
                if i.completed:
                    correct += 1
                else:
                    wrong += 1
            else:
                unattempted += 1

        total_question = quiz_question.count()
        unattempted_question = total_question - attempted
        total_score = int(correct * 100 / total_question)
        return JsonResponse(
            {'User Name': f'{user.first_name} {user.last_name}', 'Total_question': total_question, 'Correct': correct,
             'Wrong': wrong, 'Attempted': attempted, 'UnAttempted': unattempted_question, 'Total Score': total_score,
             'Answers': all_answer})
    except Exception as e:
        return JsonResponse({'Message': e.__str__()})


@api_view(['POST'])
def score(request):
    quiz_id = request.POST.get('quiz_id', '')
    quiz_title = ''
    user = Register.objects.get(email=request.session['email'])
    try:
        if quiz_id != '':
            correct = 0
            wrong = 0
            attempted = 0
            quiz_question = Question.objects.filter(quiz=quiz_id)
            user_data = UserAnswer.objects.filter(quiz=quiz_id, user=user)
            for quiz in quiz_question:
                quiz_title = quiz.quiz.name
            for i in user_data:
                if i.attempted:
                    attempted += 1
                    if i.completed:
                        correct += 1
                    else:
                        wrong += 1
            total_question = quiz_question.count()
            unattempted_question = total_question - attempted
            total_score = int(correct * 100 / total_question)

            return JsonResponse(
                {'User': f'{user.first_name} {user.last_name}', 'Quiz Name': f'{quiz_title}',
                 'Total Question': total_question, 'Correct': correct,
                 'Wrong': wrong,
                 'Attempted': f'{attempted} Question', 'Unattempted': f'{unattempted_question} Question',
                 'Total Score': total_score})
        else:
            user = Register.objects.get(email=request.session['email'])
            user_data = UserAnswer.objects.filter(user=user)
            quiz_title = 'All Quiz'
            list_of_score = []
            other_list = []
            data = {}
            for i in user_data:
                quiz_question = Question.objects.filter(quiz=i.quiz)
                user_answer = UserAnswer.objects.filter(quiz=i.quiz, user=user)
                correct = 0
                wrong = 0
                attempt = 0
                unattempted = 0
                for quiz in user_answer:
                    if quiz.attempted:
                        attempt += 1
                        if quiz.completed:
                            correct += 1
                        else:
                            wrong += 1
                    else:
                        unattempted += 1
                    total_question = quiz_question.count()
                    total_score = correct * 100 / total_question
                    unattempted_question = total_question - attempt
                    data = {'Quiz': i.quiz.name,
                            'Total Question': total_question,
                            'Correct': correct,
                            'Wrong': wrong,
                            'Attempted': attempt,
                            'Unattempted': unattempted_question,
                            'Total Score': int(total_score)}

                list_of_score.append(data)
            for name in list_of_score:
                for other_name in list_of_score:
                    if name == other_name and other_list.count(other_name) == 0:
                        other_list.append(other_name)

        return JsonResponse({'User': f'{user.first_name} {user.last_name}', 'Quiz Name': f'{quiz_title}',
                             'All Score': other_list})

    except Exception as e:
        return JsonResponse({'Message': e.__str__()})
