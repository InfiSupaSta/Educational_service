from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from educational_service.forms import UserRegistrationForm
from educational_service.models import *
from educational_service.utils import Mixin
from educational_service.utils import menu
from django.contrib import messages


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
        # context['']
        return context | datamixin_context

    def get_queryset(self):
        return Theme.objects.all().order_by('id')


def theme_description(request, slug):
    description = get_object_or_404(Theme, slug=slug)
    context = get_context()
    context['theme'] = Theme.objects.get(slug=slug)
    return render(request, 'educational_service/theme_description.html', context=context)


def get_staticstics(user_id, theme_id):
    amount_of_all_questions = len(QuizComplitionInfo.objects.filter(bound_user=user_id, theme_id=theme_id))
    amount_of_correct_questions = len(
        QuizComplitionInfo.objects.filter(bound_user=user_id, theme_id=theme_id, is_correct=True))
    theme_name = Theme.objects.get(id=theme_id)

    success = round(
        (amount_of_correct_questions / amount_of_all_questions) * 100) if amount_of_all_questions != 0 else 0

    info_to_show = f'''

    Всего в теме под названием "{theme_name}" было {amount_of_all_questions} вопрос(а, ов), вы успешно ответили на
    {amount_of_correct_questions}.
    Успешность выполнения: {success}%!
    '''

    return info_to_show, success


def send_mail_after_test_ending(theme, email, success_percent):
    subject = f'\nInfo about test "{theme}" complition!'
    recipient_list = [email]
    message = f'''
Thanks for the test complition!
Your success percent looks like: 
{success_percent} %
'''
    from_email = "email_to_send_from@gmail.com"
    # send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    return f'{subject}{message}Sended from: {from_email}\n'


def theme_questions(request, pk):
    current_theme = Theme.objects.get(pk=pk)

    if MailThemeSuccess.objects.filter(email=request.user.email, theme=Theme.objects.get(pk=pk)):
        print('Called from views.theme_questions(). Email about test complition info already sent!')
        local_context_after_quiz_done = {
            'title': 'Текущие вопросы',
            'menu': menu,
            'queryset_len': 0,
            'question': get_staticstics(request.user.id, pk)[0],
            'all_questions': Question.objects.filter(theme=pk),
            'result_info': QuizComplitionInfo.objects.filter(bound_user=request.user.id, theme_id=pk),
            'answers': Answer.objects.all(),
            'right_answers': RightAsnwer.objects.all(),
            'current_theme': current_theme,
        }
        return render(request, 'educational_service/test.html', context=local_context_after_quiz_done)

    if len(QuizComplitionInfo.objects.filter(bound_user__exact=request.user.id,
                                             theme__exact=Theme.objects.get(pk=pk))):
        quiz_len = len(QuizComplitionInfo.objects.filter(bound_user__exact=request.user.id,
                                                         theme__exact=Theme.objects.get(pk=pk)))
    else:
        quiz_len = 0

    queryset_len = len(Question.objects.filter(theme__exact=pk)) - quiz_len

    context = {
        'title': 'Текущие вопросы',
        'menu': menu,
        'queryset_len': queryset_len,
        'question': Question.objects.filter(theme=pk)[queryset_len - 1] if queryset_len > 0 else get_staticstics(
            request.user.id, pk)[0],
        'all_questions': Question.objects.filter(theme=pk),
        'result_info': QuizComplitionInfo.objects.filter(bound_user=request.user.id, theme_id=pk),
        'answers': Answer.objects.all(),
        'right_answers': RightAsnwer.objects.all(),
        'current_theme': current_theme,

        # 'messages': messages,
    }

    if queryset_len == 0:
        print('no more questions')

        # if not data about test complition
        if not MailThemeSuccess.objects.filter(email=request.user.email, theme=current_theme,
                                               success_percent=get_staticstics(request.user.id, pk)[1]):
            new_entry = MailThemeSuccess()
            new_entry.email = request.user.email
            new_entry.theme = current_theme
            new_entry.success_percent = get_staticstics(request.user.id, pk)[1]

            try:
                new_entry.is_mail_sended = True

                # replace it for real mail sending function
                print(send_mail_after_test_ending(current_theme, request.user.email, get_staticstics(
                    request.user.id, pk)[1]))
            except Exception as exc:
                print(f'Something going wrong, reason: {exc}')

            new_entry.save()
            # print('new entry added')

        if not MailThemeSuccess.objects.filter(email=request.user.email, theme=current_theme,
                                               success_percent=get_staticstics(request.user.id, pk)[1])[
            0].is_mail_sended:
            print(
                '''\nEntry about test complition exists, but mail does not sended, 
                fix it! ( add another try to send mail here and change bounded_entry.is_mail_sended to True\n''')

    if request.method == "POST":

        if len(request.POST.getlist('check')) == 0:
            return redirect('test', pk)

        complition_info = QuizComplitionInfo()
        complition_info.bound_user = request.user.id
        complition_info.theme = Theme.objects.get(pk=pk)
        complition_info.question = Question.objects.filter(theme=pk)[queryset_len - 1]

        current_answer = RightAsnwer.objects.filter(theme_id=complition_info.theme.id,
                                                    question_id=complition_info.question.id)

        list_of_int_checks = [int(item) for item in request.POST.getlist('check')]

        if list_of_int_checks == RightAsnwer.objects.get(theme_id=complition_info.theme.id,
                                                         question_id=complition_info.question.id).list_od_answers:
            messages.add_message(request, messages.INFO, 'Правильно!')

        else:
            messages.add_message(request, messages.INFO, 'Неправильно!')

        if [item for item in current_answer.values_list()[0] if isinstance(item, list)][0] == [int(item) for item in
                                                                                               request.POST.getlist(
                                                                                                   'check')]:
            complition_info.is_correct = True

            complition_info.chosen_answers = list_of_int_checks
        else:
            complition_info.chosen_answers = list_of_int_checks

        if len(QuizComplitionInfo.objects.all()) == 0:
            complition_info.save()
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

    return render(request, 'educational_service/test.html', context=context)


class UserRegistration(Mixin, CreateView):
    form_class = UserRegistrationForm
    template_name = 'educational_service/registration.html'
    success_url = reverse_lazy('login')

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
