from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import *
from rest_framework.permissions import IsAdminUser

from educational_service.models import *
from rest_api.serizlizers import *


# show all Theme model entries api/v1/theme
class ThemeListAPIView(ListCreateAPIView):
    serializer_class = ThemeSerializer
    queryset = Theme.objects.all().order_by('id')

    @swagger_auto_schema(
        operation_summary="Get list of all themes",
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create new theme",
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# show single Model entry api/v1/theme/1
class ThemeRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = ThemeSerializer
    queryset = Theme.objects.all()

    @swagger_auto_schema(
        operation_summary="Get info about single theme",
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Fully change existing single theme",
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partially change existing single theme",
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


# show single Model entry api/v1/questions
class QuestionListAPIView(ListCreateAPIView):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all().order_by('id')

    @swagger_auto_schema(
        operation_summary="Get list of all questions",
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create new question",
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# show single Model entry api/v1/questions/1
class QuestionRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all().order_by('id')

    @swagger_auto_schema(
        operation_summary="Get info about single question",
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create new single question",
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partially change single question info",
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete a single question",
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# show single Model entry api/v1/user/1
class UserProfileListAPIView(ListAPIView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="Get list of all users, admin access only",
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class MailThemeSuccessListAPIView(ListAPIView):
    serializer_class = ResultSerializer
    queryset = MailThemeSuccess.objects.all().order_by('email')

    @swagger_auto_schema(
        operation_description="GET request to receive all results about passing the tests",
        operation_summary="Receive all results about passing the tests",
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


# show single Model entry api/v1/right-answers
class RightAnswerListAPIView(ListCreateAPIView):
    serializer_class = RightAnswerSerializer
    queryset = RightAsnwer.objects.all().order_by('id')

    @swagger_auto_schema(
        operation_summary="""Create new right answer(question must be created before). tuple of 
        (question_id, theme_id) should be unique""",
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Get list of all right answers",
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


# show single Model entry api/v1/right-answers/1
class RightAnswerRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = RightAnswerSerializer
    queryset = RightAsnwer.objects.all().order_by('id')

    @swagger_auto_schema(
        operation_summary="Get info about single right answer",
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Fully change existing right answer",
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partially change existing right answer",
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


# show single Model entry api/v1/answers
class AnswerListAPIView(ListCreateAPIView):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all().order_by('id')

    @swagger_auto_schema(
        operation_summary="Get list of all answers",
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="POST request to create new answer",
        operation_summary="Creating new answer",

        # request_body=openapi.Schema(
        #     type=openapi.TYPE_OBJECT,
        #     # required=['name'],
        #     properties={
        #         'answer': openapi.Schema(type=openapi.TYPE_STRING),
        #     },
        # ),
        tags=['answers']
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# show single Model entry api/v1/answers/1
class AnswerRetrieveUpdateView(RetrieveUpdateAPIView):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all().order_by('id')

    @swagger_auto_schema(
        operation_summary="Get info about single answer",
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Fully change existing answer",
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partially change existing answer",
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
