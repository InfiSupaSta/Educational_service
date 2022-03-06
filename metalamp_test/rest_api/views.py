from django.shortcuts import render
from rest_framework.generics import *

from educational_service.models import *
from rest_api.serizlizers import *


# show all Theme model entries api/v1/theme
class ThemeListAPIView(ListCreateAPIView):
    serializer_class = ThemeSerializer
    queryset = Theme.objects.all().order_by('id')


# show single Model entry api/v1/theme/1
class ThemeRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = ThemeSerializer
    queryset = Theme.objects.all()


# show single Model entry api/v1/user/1
class UserProfileRetrieveAPIView(RetrieveAPIView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()


# show single Model entry api/v1/questions
class QuestionListAPIView(ListAPIView, CreateAPIView):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all().order_by('id')


# show single Model entry api/v1/questions/1
class QuestionRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all().order_by('id')


# show single Model entry api/v1/right-answers
class RightAnswerListAPIView(ListAPIView):
    serializer_class = RightAnswerSerializer
    queryset = RightAsnwer.objects.all().order_by('id')


# show single Model entry api/v1/right-answers/1
class RightAnswerRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = RightAnswerSerializer
    queryset = RightAsnwer.objects.all().order_by('id')


class RightAnswerCreateListAPIView(CreateAPIView):
    serializer_class = NewRightAnswerSerializer
    queryset = RightAsnwer.objects.all().order_by('id')


# show single Model entry api/v1/answers
class AnswerListAPIView(ListAPIView, CreateAPIView):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all().order_by('id')


class AnswerCreateAPIView(CreateAPIView):
    serializer_class = NewAnswerSerializer
    queryset = Answer.objects.all().order_by('id')


# show single Model entry api/v1/answers/1
class AnswerRetrieveUpdateView(RetrieveUpdateAPIView):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all().order_by('id')


class MailThemeSuccessListAPIView(ListAPIView):
    serializer_class = ResultSerializer
    queryset = MailThemeSuccess.objects.all().order_by('email')
