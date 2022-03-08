menu = [
    {'title': 'Регистрация', 'url_name': 'register'},
    {'title': 'Логин', 'url_name': 'login'},
    {'title': 'О проекте', 'url_name': 'home'},
    {'title': 'Темы + тесты', 'url_name': 'tests'},
    {'title': 'Выход с аккаунта', 'url_name': 'logout'},
]

class Mixin:

    def get_user_context(self, **kwargs):
        context = kwargs
        context['menu'] = menu

        return context
