from django.urls import path

from rest_api.views import *

urlpatterns = [
    path('theme', ThemeListAPIView.as_view(), name='list_of_themes'),
    path('theme/<int:pk>', ThemeRetrieveUpdateAPIView.as_view(), name='theme'),

    path('questions', QuestionListAPIView.as_view()),
    path('questions/<int:pk>', QuestionRetrieveUpdateDestroyAPIView.as_view()),

    path('right-answers', RightAnswerListAPIView.as_view()),
    # path('right-answers/add', RightAnswerCreateListAPIView.as_view()),
    path('right-answers/<int:pk>', RightAnswerRetrieveUpdateAPIView.as_view()),

    path('answers', AnswerListAPIView.as_view()),
    # path('answers/add', AnswerCreateAPIView.as_view()),
    path('answers/<int:pk>', AnswerRetrieveUpdateView.as_view()),

    path('user', UserProfileListAPIView.as_view(), name='user_create'),

    path('results', MailThemeSuccessListAPIView.as_view()),
]

