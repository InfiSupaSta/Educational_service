from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import Form

from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    # username = forms.CharField(label='Ваш псевдоним')
    email = forms.EmailField(label='Адрес электронной почты')
    password1 = forms.CharField(widget=forms.PasswordInput(), label='Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Повторите пароль')

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserLogInForm(AuthenticationForm):
    email = forms.CharField(label='Ваш email:')
    password1 = forms.CharField(label='Введите пароль:')
