menu = [

    {'title': 'Регистрация', 'url_name': 'register'},
    {'title': 'Логин', 'url_name': 'login'},
    {'title': 'О проекте', 'url_name': 'home'},
    {'title': 'Тесты', 'url_name': 'tests'},
    {'title': 'Выход с аккаунта', 'url_name': 'logout'},
    # {'title': 'API', 'url_name': 'api'},
    # {'title': 'Админка', 'url_name': 'admin:index'},

]


# зареган: о проекте, тесты, выход с аккаунта
# не зареган: о проекте, логин, регистрация

class Mixin:

    def get_user_context(self, **kwargs):
        context = kwargs
        context['menu'] = menu

        return context
