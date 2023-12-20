from django.urls import path
from . import views
urlpatterns = [
    path('', views.register),
    path('login/', views.login),
    path('logout/', views.logout),
    path('function_based_view/', views.function_based_view),
    path('add_quiz/', views.add_quiz),
    path('update_quiz/', views.update_quiz),
    path('delete_quiz/', views.delete_quiz),
    path('view_quiz/', views.view_quiz),
    path('add_question/', views.add_question),
    path('update_question/', views.update_question),
    path('delete_question/', views.delete_question),
    path('view_question/', views.view_question),
    path('quiz_name/', views.quiz_name),
    path('quiz_level/', views.quiz_level),
    path('enter_game/', views.enter_game),
    path('answer/', views.answer),
    path('score/', views.score),
]
