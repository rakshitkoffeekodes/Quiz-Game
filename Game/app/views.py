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
            {'Message': 'All Quiz',
             'Quiz': all_quiz_list})
    except Exception as e:
        return JsonResponse({'Message': f'{e.__str__()}'})


@api_view(['POST'])
def quiz_level(request):
    levels = []
    quiz_id = request.POST['quiz id']
    quiz = Quiz.objects.get(id=quiz_id)
    quiz_levels = Question.objects.filter(quiz=quiz_id)
    for lev in quiz_levels:
        if lev.level not in levels:
            levels.append(lev.level)
    return JsonResponse({'Quiz Name': f'{quiz}', 'Quiz Level': levels})


@api_view(['POST'])
def enter_game(request):
    primary_key = request.POST['id']
    level = request.POST['level']
    try:
        user = Register.objects.get(email=request.session['email'])
        list_of_question = []
        count = 0
        primary_key = int(primary_key)
        one_quiz = Quiz.objects.get(id=primary_key)
        all_question = Question.objects.filter(quiz=one_quiz, level=level)
        levels = UserAnswer.objects.filter(user=user, level=level, quiz=one_quiz)
        lev = []
        for i in levels:
            one_level = UserAnswer.objects.filter(user=user, level=int(i.level) - 1, quiz=one_quiz)
            lev.append(all(one.completed for one in one_level))
        if levels is None:
            if all(lev) or int(level) == 1:
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
            else:
                return JsonResponse({'Message': 'Complete the next level first'})
        else:
            if int(level) == 1:
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
            else:
                return JsonResponse({'Message': 'Complete the next level first'})
        return JsonResponse(
            {'User Name': f'{user.first_name} {user.last_name}', 'Quiz Name': f'Enter {one_quiz} Quiz',
             'Total Question': f'{count}',
             'Message': 'The answer is full not a A, B, C, D.., Example: (A) answer',
             'Questions': list_of_question})
    except Exception as e:
        return JsonResponse({'Message': e.__str__()})


def no_empty_answer(previous, previous_answers, question_get, user, dict1, level):
    result = {}
    if not previous_answers:
        user_answer = UserAnswer()
        user_answer.attempted = True
        user_answer.questions_id = question_get
        user_answer.quiz = question_get.quiz
        user_answer.level = level
        user_answer.answer = dict1
        user_answer.user = user
        user_answer.save()

    elif previous_answers and previous == [True]:
        user_answer = previous_answers[0]
        user_answer.answer = dict1
        result = {
            'Quiz Name': question_get.quiz.name,
            'Question': question_get.question,
            'Message': 'Correct answer is already exist.'
        }
    elif dict1 == question_get.answer:
        user_answer = previous_answers[0]
        user_answer.completed = True
        user_answer.save()
        result = {
            'Quiz Name': question_get.quiz.name,
            'Question': question_get.question,
            'Answer': dict1,
            'Message': 'Your Answer is Correct'
        }
    else:
        user_answer = previous_answers[0]
        user_answer.completed = False
        user_answer.save()
        result = {
            'Quiz Name': question_get.quiz.name,
            'Question': question_get.question,
            'Your Answer': dict1,
            'Message': 'Your Answer is Wrong'
        }
    return result


def empty_answer(previous_answers, question_get, dict1, user, level):
    if not previous_answers:
        user_answer = UserAnswer()
        user_answer.attempted = True
        user_answer.questions_id = question_get
        user_answer.quiz = question_get.quiz
        user_answer.level = level
        user_answer.answer = dict1
        user_answer.user = user
        user_answer.save()
        result = {
            'Quiz Name': question_get.quiz.name,
            'Question': question_get.question,
        }
    else:
        user_answer = previous_answers[0]
        user_answer.completed = False
        user_answer.save()
        result = {
            'Quiz Name': question_get.quiz.name,
            'Question': question_get.question,
        }
    return result


# @api_view(['POST'])
# def answer(request):
#     user = Register.objects.get(email=request.session['email'])
#     all_answer = []
#     quiz_id = request.POST['quiz']
#     question = request.POST['question'].split(',')
#     answers = request.POST.get('answer', '').split('.,')
#     dict1 = {key: value.strip() for key, value in zip(question, answers)}
#     try:
#         for key in dict1:
#             question_get = Question.objects.get(id=key, quiz=quiz_id)
#             print(question_get)
#             previous_answers = UserAnswer.objects.filter(user=user, questions_id=question_get)
#             previous = [previous.completed is True for previous in previous_answers]
#             if not dict1[key] == '':
#                 result = {f'Answer': no_empty_answer(previous, previous_answers, question_get, user, dict1[key])}
#
#             else:
#                 result = {'Answer': empty_answer(previous_answers, question_get, dict1[key], user)}
#
#             all_answer.append(result)
#
#         quiz_question = Question.objects.filter(quiz=quiz_id)
#         user_answer = UserAnswer.objects.filter(quiz=quiz_id, user=user)
#
#         result = {
#             'User Name': f'{user.first_name} {user.last_name}',
#             'Total_question': quiz_question.count(),
#             'Correct': user_answer.filter(completed=True).count(),
#             'Wrong': user_answer.filter(completed=False).count(),
#             'Attempted': user_answer.filter(attempted=True).count(),
#             'UnAttempted': quiz_question.count() - user_answer.filter(attempted=True).count(),
#             'Total Score': int(user_answer.filter(completed=True).count() * 100 / quiz_question.count())}
#
#         return JsonResponse({'Data': result, 'All Answer': all_answer})
#
#     except Exception as e:
#         return JsonResponse({'Message': e.__str__()})


@api_view(['POST'])
def answer(request):
    user = Register.objects.get(email=request.session['email'])
    all_answer = []
    quiz_id = request.POST['quiz']
    level = request.POST['level']
    question = request.POST['question'].split(',')
    answers = request.POST.get('answer', '').split('.,')
    dict1 = {key: value.strip() for key, value in zip(question, answers)}

    try:
        for key in dict1:
            question_get = Question.objects.get(id=key, quiz=quiz_id, level=level)
            previous_answers = UserAnswer.objects.filter(user=user, questions_id=question_get, level=level)
            previous = [previous.completed is True for previous in previous_answers]

            if not dict1[key] == '':
                result = {f'Answer': no_empty_answer(previous, previous_answers, question_get, user, dict1[key], level)}

            else:
                result = {'Answer': empty_answer(previous_answers, question_get, dict1[key], user, level)}

            all_answer.append(result)

        quiz_question = Question.objects.filter(quiz=quiz_id, level=level)
        user_answer = UserAnswer.objects.filter(quiz=quiz_id, user=user, level=level)

        result = {
            'User Name': f'{user.first_name} {user.last_name}',
            'Level': f'Level Is {level}',
            'Total_question': quiz_question.count(),
            'Correct': user_answer.filter(completed=True).count(),
            'Wrong': user_answer.filter(completed=False).count(),
            'Attempted': user_answer.filter(attempted=True).count(),
            'UnAttempted': quiz_question.count() - user_answer.filter(attempted=True).count(),
            'Total Score': int(user_answer.filter(completed=True).count() * 100 / quiz_question.count())}

        return JsonResponse({'Data': result, 'All Answer': all_answer})

    except Exception as e:
        return JsonResponse({'Message': e.__str__()})


@api_view(['POST'])
def score(request):
    quiz_id = request.POST.get('quiz_id', '')
    user = Register.objects.get(email=request.session['email'])
    try:
        if quiz_id != '':
            quiz_question = Question.objects.filter(quiz=quiz_id)
            user_data = UserAnswer.objects.filter(quiz=quiz_id, user=user)
            quiz_title = ''
            for quiz in quiz_question:
                quiz_title = quiz.quiz.name

            data = {
                'Total_question': quiz_question.count(),
                'Correct': user_data.filter(completed=True).count(),
                'Wrong': user_data.filter(completed=False).count(),
                'Attempted': user_data.filter(attempted=True).count(),
                'UnAttempted': quiz_question.count() - user_data.filter(attempted=True).count(),
                'Total Score': int(user_data.filter(completed=True).count() * 100 / quiz_question.count())}

            return JsonResponse(
                {'User': f'{user.first_name} {user.last_name}', 'Quiz Name': f'{quiz_title}',
                 'Score': data})
        else:
            user_data = UserAnswer.objects.filter(user=user)
            quiz_title = 'All Quiz'
            list_of_score = []
            other_list = []
            for i in user_data:
                quiz_question = Question.objects.filter(quiz=i.quiz)
                user_answer = UserAnswer.objects.filter(quiz=i.quiz, user=user)
                data = {
                    'Quiz Name': i.quiz.name,
                    'Total_question': quiz_question.count(),
                    'Correct': user_answer.filter(completed=True).count(),
                    'Wrong': user_answer.filter(completed=False).count(),
                    'Attempted': user_answer.filter(attempted=True).count(),
                    'UnAttempted': quiz_question.count() - user_answer.filter(attempted=True).count(),
                    'Total Score': int(user_answer.filter(completed=True).count() * 100 / quiz_question.count())}
                list_of_score.append(data)
            for name in list_of_score:
                for other_name in list_of_score:
                    if name == other_name and other_list.count(other_name) == 0:
                        other_list.append(other_name)

        return JsonResponse({'User': f'{user.first_name} {user.last_name}', 'Quiz Name': f'{quiz_title}',
                             'All Score': other_list})

    except Exception as e:
        return JsonResponse({'Message': e.__str__()})
