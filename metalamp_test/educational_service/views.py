from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse

from django.views.generic import ListView
from educational_service.utils import Mixin
from educational_service.utils import menu
from educational_service.models import Theme


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


def theme_questions(request, pk):
    current_theme = Theme.objects.get(pk=pk)

    context = {
        'title': 'Текущие вопросы',
        'menu': menu,
        'current_theme': current_theme,
    }

    return render(request, r'educational_service/test.html', context)


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
