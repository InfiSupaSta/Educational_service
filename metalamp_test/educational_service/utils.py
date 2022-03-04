menu = [

    {'title': 'О проекте', 'url_name': 'home'},
    {'title': 'Тесты', 'url_name': 'tests'},
    {'title': 'API', 'url_name': 'api'},
    {'title': 'Выход с аккаунта', 'url_name': 'logout'},
    {'title': 'Логин', 'url_name': 'login'},
    {'title': 'Регистрация', 'url_name': 'register'},
    # {'title': 'Админка', 'url_name': 'admin:index'},

]


class Mixin:

    def get_user_context(self, **kwargs):
        context = kwargs
        context['menu'] = menu

        return context
