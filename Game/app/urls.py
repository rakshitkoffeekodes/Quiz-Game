from django.urls import path
from . import views

urlpatterns = [
    path('', views.register),
    path('login/', views.login),
    path('logout/', views.logout),
    path('quiz_name/', views.quiz_name),
    path('enter_game/', views.enter_game),
    path('answer/', views.answer),
    path('score/', views.score),
]
