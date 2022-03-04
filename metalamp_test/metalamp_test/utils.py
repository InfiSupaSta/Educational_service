menu = [

    {'title': 'О проекте', 'url_name': 'home'},
    {'title': 'Тесты', 'url_name': 'tests'},
    {'title': 'API', 'url_name': 'api'},

]


class Mixin:

    def get_user_context(self, **kwargs):
        kwargs['menu'] = menu

        return kwargs
