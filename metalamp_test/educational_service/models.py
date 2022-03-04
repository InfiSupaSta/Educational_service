from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Theme(models.Model):
    objects = models.Manager()
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('test', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'


class Question(models.Model):
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    question = models.CharField(max_length=100)

    # answer = models.BooleanField(default=False)

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    # bound_user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=200)
    vote_tally = models.IntegerField(default=0)

    def __repr__(self):
        return self.question


class RightAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    right_answer = models.CharField(max_length=150)
    comment = models.TextField()

    def __repr__(self):
        return self.right_answer


class WrongAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    wrong_answer = models.CharField(max_length=150)
    comment = models.TextField()

    def __repr__(self):
        return self.wrong_answer
