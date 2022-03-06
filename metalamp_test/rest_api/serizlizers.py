from rest_framework import serializers

from educational_service.models import *


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = 'id', 'email'


class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        # fields = ('title', 'description')
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = 'id', 'answer'


class NewAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'


class RightAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = RightAsnwer
        fields = '__all__'


class NewRightAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = RightAsnwer
        fields = '__all__'


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailThemeSuccess
        fields = '__all__'
