from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy

from django.views.generic import ListView, CreateView, DetailView

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


# class ThemeQuestions(Mixin, DetailView):
#     model = Question
#     template_name = 'educational_service/test.html'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         datamixin_context = self.get_user_context()
#         context['question'] = self.get_queryset()[0]
#         return context | datamixin_context

# def get_object(self, queryset=None):
#     slug = self.kwargs.get(self.slug_url_kwarg, None)
#     try:
#         return queryset.get(slug=slug)
#     except PostDoesNotExist:
#         raise Http404('Ох, нет объекта;)')
# def post(self):
#     pass

# def get_queryset(self):
#     Question.objects.all()

def theme_questions(request, pk):
    current_theme = Theme.objects.get(pk=pk)

    if len(QuizComplitionInfo.objects.filter(bound_user__exact=request.user.id,
                                             theme__exact=Theme.objects.get(pk=pk))):
        quiz_len = len(QuizComplitionInfo.objects.filter(bound_user__exact=request.user.id,
                                                         theme__exact=Theme.objects.get(pk=pk)))
    else:
        quiz_len = 0

    queryset_len = len(Question.objects.filter(theme__exact=pk)) - quiz_len

    # print(quiz_len, queryset_len, request.user.id)
    # print(Question.objects.filter(theme=pk)[queryset_len - 1])
    context = {
        'title': 'Текущие вопросы',
        'menu': menu,
        # 'question': Question.objects.filter(theme=pk).first(),
        'question': Question.objects.filter(theme=pk)[queryset_len - 1] if queryset_len > 0 else 'Вопросов больше нет!',
        'answers': Answer.objects.all(),
        'current_theme': current_theme,
    }

    if request.method == "POST":
        complition_info = QuizComplitionInfo()
        complition_info.bound_user = request.user.id
        complition_info.theme = Theme.objects.get(pk=pk)
        # complition_info.question = context.get('question')
        complition_info.question = Question.objects.filter(theme=pk)[queryset_len - 1]
        print(complition_info.bound_user)
        print(complition_info.theme.id)
        print(complition_info.question.id)

        if len(QuizComplitionInfo.objects.all()) == 0:
            complition_info.save()
            # return render(request, 'educational_service/test.html', context)
            return redirect('test', pk)
        elif not QuizComplitionInfo.objects.filter(bound_user__exact=complition_info.bound_user,
                                                   theme__exact=complition_info.theme.id,
                                                   question__exact=complition_info.question.id):

            complition_info.save()
            return redirect('test', pk)
        else:
            print('Entry exists')
            complition_info.save()
            return redirect('test', pk)
            # return render(request, 'educational_service/test.html')
            # return redirect('home')
            # print(request.POST.getlist('check'))
            # print(Question.objects.filter(theme=pk))

    return render(request, 'educational_service/test.html', context=context)


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


def user_logout(request):
    logout(request)
    return redirect('login')
