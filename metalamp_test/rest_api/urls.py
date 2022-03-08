from django.urls import path

from rest_api.views import *

urlpatterns = [
    path('themes', ThemeListAPIView.as_view(), name='list_of_themes'),
    path('themes/<int:pk>', ThemeRetrieveUpdateAPIView.as_view(), name='themes'),

    path('questions', QuestionListAPIView.as_view(), name='list_of_questions'),
    path('questions/<int:pk>', QuestionRetrieveUpdateDestroyAPIView.as_view(), name='questions'),

    path('right-answers', RightAnswerListAPIView.as_view(), name='list_of_right_answers'),
    path('right-answers/<int:pk>', RightAnswerRetrieveUpdateAPIView.as_view(), name='right_answers'),

    path('answers', AnswerListAPIView.as_view(), name='list_of_answers'),
    path('answers/<int:pk>', AnswerRetrieveUpdateView.as_view(), name='answers'),

    path('user', UserProfileListAPIView.as_view(), name='user_create'),

    path('results', MailThemeSuccessListAPIView.as_view(), name='results'),
]
