from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from educational_service.forms import UserRegistrationForm
from educational_service.models import *
from educational_service.utils import Mixin
from educational_service.utils import menu
from django.contrib import messages



class Tests(Mixin, ListView):
    model = Theme
    template_name = 'educational_service/tests.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        datamixin_context = self.get_user_context()
        context['title'] = 'Тематические выкладки и тесты'
        return context | datamixin_context

    def get_queryset(self):
        return Theme.objects.all().order_by('id')


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


def get_context():
    context = {
        'menu': menu
    }
    return context


def main_page(request):
    context = get_context()
    context['title'] = 'Главная страница'
    return render(request, 'educational_service/main_page.html', context=context)


def theme_description(request, slug):

    context = get_context()
    context['theme'] = get_object_or_404(Theme, slug=slug)
    return render(request, 'educational_service/theme_description.html', context=context)


def get_statistics(user_id, theme_id):
    amount_of_all_questions = len(QuizComplitionInfo.objects.filter(bound_user=user_id,
                                                                    theme_id=theme_id))

    amount_of_correct_questions = len(QuizComplitionInfo.objects.filter(bound_user=user_id,
                                                                        theme_id=theme_id,
                                                                        is_correct=True))
    theme_name = Theme.objects.get(id=theme_id)

    success = round((amount_of_correct_questions / amount_of_all_questions) * 100) \
        if amount_of_all_questions != 0 else 0

    info_to_show = f'''
    Всего в теме под названием "{theme_name}" было {amount_of_all_questions} вопрос(а, ов), вы успешно ответили на
    {amount_of_correct_questions}.
    Тест выполнен на {success}%!
    '''

    return info_to_show, success


# def fake__send_mail_after_test_ending(theme, email, success_percent):
#     subject = f'\nInfo about test "{theme}" completion!'
#     recipient_list = [email]
#     message = f'''
# Thanks for the test completion!
# Your success percent looks like:
# {success_percent} %
# '''
#     from_email = "email_to_send_from@gmail.com"
#     # send_mail(subject, message, from_email, recipient_list, fail_silently=False)
#     return f'{subject}{message}Sended from: {from_email}\n'


def real__send_mail_after_test_ending(theme, email, success_percent):
    subject = f'Info about test "{theme}" completion!'
    recipient_list = [email]
    message = f'''
        Thanks for the test completion!
        Your success percent looks like: 
        {success_percent} %
    '''
    from_email = "some_cool_email_here@gmail.com"

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)


def theme_questions(request, pk):
    current_theme = Theme.objects.get(pk=pk)

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
        'question': Question.objects.filter(theme=pk)[queryset_len - 1] if queryset_len > 0 else get_statistics(
            request.user.id, pk)[0],
        'all_questions': Question.objects.filter(theme=pk),
        'result_info': QuizComplitionInfo.objects.filter(bound_user=request.user.id,
                                                         theme_id=pk),
        'answers': Answer.objects.all(),
        'right_answers': RightAsnwer.objects.all(),
        'current_theme': current_theme,
    }

    # if no more questions in QUIZ list
    if queryset_len == 0:

        # if not saved data about test completion
        if not MailThemeSuccess.objects.filter(email=request.user.email,
                                               theme=current_theme,
                                               success_percent=get_statistics(request.user.id, pk)[1]):

            info_about_test_completion = MailThemeSuccess()
            info_about_test_completion.email = request.user.email
            info_about_test_completion.theme = current_theme
            info_about_test_completion.success_percent = get_statistics(request.user.id, pk)[1]

            try:
                info_about_test_completion.is_mail_sended = True

                # replace it for real mail sending function
                # print(fake__send_mail_after_test_ending(current_theme,
                #                                         request.user.email,
                #                                         get_statistics(request.user.id, pk)[1]))

                real__send_mail_after_test_ending(current_theme,
                                                  request.user.email,
                                                  get_statistics(request.user.id, pk)[1])
            except Exception as exc:
                print(f'Something going wrong, reason: {exc}')

            info_about_test_completion.save()

        # check if email not sent for any reason after QUIZ complition
        if MailThemeSuccess.objects.filter(email=request.user.email,
                                           theme=current_theme,
                                           success_percent=get_statistics(request.user.id,
                                                                          pk)[1])[0].is_mail_sended is False:
            print(
                f'''\nEntry about test completion exists, but mail does not sent for any reason, 
                fix it! ( add another try to send mail here and change bounded_entry.is_mail_sended to True\n''')

    #  block of code to serve the answers
    if request.method == "POST":

        #  if user does not choose at least one answer just redirect him to the same page with the same question
        if len(request.POST.getlist('check')) == 0:
            return redirect('test', pk)

        completion_info = QuizComplitionInfo()
        completion_info.bound_user = request.user.id
        completion_info.theme = Theme.objects.get(pk=pk)
        completion_info.question = Question.objects.filter(theme=pk)[queryset_len - 1]

        list_of_int_checks = [int(item) for item in request.POST.getlist('check')]

        # block of code to indicate about correct or not was the answer
        if list_of_int_checks == RightAsnwer.objects.get(theme_id=completion_info.theme.id,
                                                         question_id=completion_info.question.id).list_od_answers:
            messages.add_message(request, messages.INFO, 'Правильно!')
        else:
            messages.add_message(request, messages.INFO, 'Неправильно!')

        # searching for list of right answers according to current answer
        # (and yes, storing any type of lists or arrays in the field goes against first normal form)
        current_answer = RightAsnwer.objects.filter(theme_id=completion_info.theme.id,
                                                    question_id=completion_info.question.id)
        if [item for item in current_answer.values_list()[0] if isinstance(item, list)][0] == [int(item) for item in
                                                                                               request.POST.getlist(
                                                                                                   'check')]:
            # mark answer as correct
            completion_info.is_correct = True
            completion_info.chosen_answers = list_of_int_checks
        else:
            completion_info.chosen_answers = list_of_int_checks

        # just another level of checks before saving
        if not QuizComplitionInfo.objects.filter(bound_user__exact=completion_info.bound_user,
                                                 theme__exact=completion_info.theme.id,
                                                 question__exact=completion_info.question.id):
            completion_info.save()
            return redirect('test', pk)

        # if for some reason that entry exists(which must not)
        else:
            print('Somehow entry about question exists')
            return redirect('test', pk)

    return render(request, 'educational_service/test.html', context=context)


def user_logout(request):
    logout(request)
    return redirect('login')
