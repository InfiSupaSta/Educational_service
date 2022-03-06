from django.urls import path

from rest_api.views import *

urlpatterns = [
    path('theme', ThemeListAPIView.as_view()),
    path('theme/<int:pk>', ThemeRetrieveUpdateAPIView.as_view()),

    path('questions', QuestionListAPIView.as_view()),
    path('questions/<int:pk>', QuestionRetrieveUpdateDestroyAPIView.as_view()),

    path('right-answers', RightAnswerListAPIView.as_view()),
    path('right-answers/add', RightAnswerCreateListAPIView.as_view()),
    path('right-answers/<int:pk>', RightAnswerRetrieveUpdateAPIView.as_view()),

    path('answers', AnswerListAPIView.as_view()),
    path('answers/add', AnswerCreateAPIView.as_view()),
    path('answers/<int:pk>', AnswerRetrieveUpdateView.as_view()),

    path('user/<int:pk>', UserProfileRetrieveAPIView.as_view()),

    path('results', MailThemeSuccessListAPIView.as_view()),
]
