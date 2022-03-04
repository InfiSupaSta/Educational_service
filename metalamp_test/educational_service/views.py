from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy

from django.views.generic import ListView, CreateView

from educational_service.forms import UserRegistrationForm, UserLogInForm
from educational_service.utils import Mixin
from educational_service.utils import menu
from educational_service.models import *


def get_context():
    context = {
        'menu': menu
    }
    return context


def main_page(request):
    context = get_context()
    context['title'] = 'Главная страница'
    return render(request, 'educational_service/main_page.html', context=context)


class Tests(Mixin, ListView):
    model = Theme
    template_name = 'educational_service/tests.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        datamixin_context = self.get_user_context()
        context['title'] = 'Тесты'
        return context | datamixin_context

    def get_queryset(self):
        return Theme.objects.all()


# class ThemeQuestions(Mixin, ListView):
#     template_name = 'educational_service/test.html'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         datamixin_context = self.get_user_context()
#         return context | datamixin_context
#
#     def post(self):
#         pass


def theme_questions(request, pk):
    current_theme = Theme.objects.get(pk=pk)

    context = {
        'title': 'Текущие вопросы',
        'menu': menu,
        'questions': Question.objects.filter(theme=pk),
        'answers': Answer.objects.all(),
        'current_theme': current_theme,
    }

    return render(request, 'educational_service/test.html', context)


# def theme_test(request, theme_id):
def theme_test(request):
    # context = get_context()
    # context['item'] = Theme.objects.get(id=theme_id)
    # rev = reverse('test', kwargs={'theme_id': theme_id})
    # return reverse(f'tests/{theme_id}')
    return reverse(request.GET)
    # return render(request, 'educational_service/test.html', context=context)
    # return HttpResponse(f'{rev}')


# class MainPage(Mixin, TemplateView):
#
#     template_name = 'educational_service/main_page.html'
#
#     def get(self, request, *args, **kwargs):
#         context = self.get_context_data(**kwargs)
#         return self.render_to_response(context)
#
#     def get_user_context(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         datamixin_context = self.get_user_context(title='Главная страница')
#
#
#         print(context | datamixin_context)
#         return context | datamixin_context

class UserRegistration(Mixin, CreateView):
    form_class = UserRegistrationForm
    template_name = 'educational_service/registration.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        datamixin_context = self.get_user_context(title='Регистрация')
        return context | datamixin_context


class UserLogin(Mixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'educational_service/login.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        datamixin_context = self.get_user_context(title='Авторизация')

        return context | datamixin_context

    def get_success_url(self):
        return reverse_lazy('home')
