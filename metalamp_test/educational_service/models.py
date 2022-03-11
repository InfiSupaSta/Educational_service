from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.urls import reverse


class UserProfileManager(BaseUserManager):

    def create_user(self, email, password=None):
        if not email:
            raise ValueError('User must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(email, name, password)
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    objects = UserProfileManager()

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'Информация о пользователе'
        verbose_name_plural = 'Информация о пользователях'


class Theme(models.Model):
    objects = models.Manager()
    title = models.CharField('Тема', max_length=200)
    description = models.TextField('Описание')
    slug = models.SlugField(max_length=100, unique=True, db_index=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('test', kwargs={'pk': self.pk})

    def get_absolute_url_for_description(self):
        return reverse('theme_desc', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Просмотр тем и создание'


class Question(models.Model):
    objects = models.Manager()
    theme = models.ForeignKey(Theme, verbose_name='Тема', on_delete=models.CASCADE)
    question = models.CharField('Вопрос', max_length=100)

    def __str__(self):
        return f'{self.question}'

    class Meta:
        verbose_name = 'Вопрос и ответы для имеющейся темы'
        verbose_name_plural = 'Вопрос и ответы для имеющейся темы'


class Answer(models.Model):
    objects = models.Manager()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField('Ответ', max_length=200)

    def __repr__(self):
        return f'{self.question}'

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Предлагаемые ответы'


class QuizComplitionInfo(models.Model):
    objects = models.Manager()
    bound_user = models.IntegerField()
    chosen_answers = ArrayField(models.IntegerField())

    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)  # new field

    def __str__(self):
        return f'{self.question}'


class RightAsnwer(models.Model):  # new model
    objects = models.Manager()
    theme = models.ForeignKey(Theme, verbose_name='Тема', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, verbose_name='Вопрос', on_delete=models.CASCADE)
    list_od_answers = ArrayField(models.IntegerField(), verbose_name='Список ответов')
    comment = models.CharField(max_length=100, default='')

    def __str__(self):
        return f'{self.question}'

    class Meta:
        verbose_name = 'Правильный ответ для вопроса'
        verbose_name_plural = 'Вопросы с правильными ответами'


class MailThemeSuccess(models.Model):
    objects = models.Manager()
    email = models.CharField(max_length=100)
    theme = models.CharField(max_length=150)
    success_percent = models.IntegerField()
    is_mail_sended = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'Информация о прохождении тестов'
        verbose_name_plural = 'Информация о прохождении тестов'
