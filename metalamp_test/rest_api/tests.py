from django.test import RequestFactory
from rest_framework import status
from rest_framework.test import APITestCase
from educational_service.models import *
from rest_api.serizlizers import *
from rest_framework.permissions import IsAdminUser


# to run tests
# python manage.py test rest_api.tests

class ThemeTests(APITestCase):

    def test_get__get_list_of_themes(self):
        url = reverse('list_of_themes')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post__create_theme(self):
        url = reverse('list_of_themes')
        data = {'title': 'new theme', 'description': 'new description', 'slug': 'new_theme'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Theme.objects.count(), 1)

    def test_post__create_with_wrong_slug(self):
        url = reverse('list_of_themes')
        data = {'title': 'new theme', 'description': 'new description', 'slug': 'new theme'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('slug')[0],
                         'Enter a valid "slug" consisting of letters, numbers, underscores or hyphens.')
        self.assertEqual(Theme.objects.count(), 0)

    def test_get__get_non_existing_theme(self, pk=1):
        url = reverse('themes', kwargs={'pk': pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post__get_theme_with_wrong_method(self, pk=1):
        url = reverse('themes', kwargs={'pk': pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_put__change_existing_theme(self):
        url_for_create = reverse('list_of_themes')
        data = {'title': 'new theme 2', 'description': 'new description 2', 'slug': 'new_theme_2'}
        response = self.client.post(url_for_create, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url_for_change = reverse('themes', kwargs={'pk': response.data.get('id')})
        changed_data = {'title': 'new theme 2 changed',
                        'description': 'new description 2 changed',
                        'slug': 'new_theme_2_changed'}
        response = self.client.put(url_for_change, changed_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put__change_not_existing_theme(self):
        url_for_create = reverse('list_of_themes')
        data = {'title': 'new theme 2', 'description': 'new description 2', 'slug': 'new_theme_2'}
        response = self.client.post(url_for_create, data)

        url_for_change = reverse('themes', kwargs={'pk': response.data.get('id') + 1})
        changed_data = {'title': 'new theme 9999', 'description': 'new description 9999', 'slug': 'new_theme_9999'}
        response = self.client.put(url_for_change, changed_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put__change_existing_theme_but_title_does_not_filled(self):
        url_for_create = reverse('list_of_themes')
        data = {'title': 'new theme 2', 'description': 'new description 2', 'slug': 'new_theme_2'}
        response = self.client.post(url_for_create, data)

        url_for_change = reverse('themes', kwargs={'pk': response.data.get('id')})
        changed_data = {'description': 'new description 9999', 'slug': 'new_theme_9999'}
        new_response = self.client.put(url_for_change, changed_data)
        self.assertEqual(new_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post__theme_creating_but_slug_exists(self):
        url_for_create = reverse('list_of_themes')
        data = {'title': 'new theme 2', 'description': 'new description 2', 'slug': 'new_theme_2'}
        response = self.client.post(url_for_create, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        another_data = {'title': 'new theme 3', 'description': 'new description 3', 'slug': 'new_theme_2'}
        response = self.client.post(url_for_create, another_data)
        self.assertEqual('with this slug already exists' in response.data.get('slug')[0], True)

    def test__is_theme_endpoints_use_correct_url(self, pk=1):
        self.assertTrue(reverse('list_of_themes') == '/api/v1/themes')
        self.assertTrue(reverse('themes', kwargs={'pk': pk}) == f'/api/v1/themes/{pk}')


class AccountTests(APITestCase):

    def test__create_new_account(self):
        url = reverse('register')

        data = {'email': 'qwe@qwe.tu', 'password': 'ghbdtn123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        UserProfile.objects.create_user(**data)
        self.assertEqual(UserProfile.objects.count(), 1)
        self.assertEqual(UserProfile.objects.get().email, 'qwe@qwe.tu')

    def test__create_new_account_with_blank_email(self):
        url = reverse('register')
        data = {'email': '', 'password': 'ghbdtn123'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        try:
            UserProfile.objects.create_user(**data)
        except ValueError as exc:
            self.assertEqual(ValueError, type(exc))

    def test__create_new_account_with_not_str_email(self):
        url = reverse('register')
        data = {'email': 234, 'password': 'ghbdtn123'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        try:
            UserProfile.objects.create_user(**data)
        except AttributeError as exc:
            self.assertEqual(AttributeError, type(exc))


class QuestionTests(APITestCase):

    def test_get__get_list_of_questions(self):
        url = reverse('list_of_questions')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post__create_and_change_question(self):
        # new theme entry for current test
        url_theme = reverse('list_of_themes')
        data_theme = {'title': 'new theme', 'description': 'new description', 'slug': 'new_theme'}
        response = self.client.post(url_theme, data_theme)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # new question entry bound with the new theme entry
        url_question = reverse('list_of_questions')
        data_question = {'question': 'new question', 'theme': response.data.get('id')}
        response = self.client.post(url_question, data_question)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), 1)

        # change recently created question
        changed_url_question = reverse('questions', kwargs={'pk': response.data.get('id')})
        changed_data_question = {'question': 'new question changed', 'theme': response.data.get('id')}
        response = self.client.put(changed_url_question, changed_data_question)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Question.objects.count(), 1)

    def test_post__create_question_with_non_existing_theme(self):
        url_theme = reverse('list_of_themes')
        data_theme = {'title': 'new theme', 'description': 'new description', 'slug': 'new_theme'}
        response = self.client.post(url_theme, data_theme)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url_question = reverse('list_of_questions')
        data_question = {'question': 'new question', 'theme': response.data.get('id') + 1}
        response = self.client.post(url_question, data_question)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test__is_question_endpoints_use_correct_url(self, pk=1):
        self.assertTrue(reverse('list_of_questions') == '/api/v1/questions')
        self.assertTrue(reverse('questions', kwargs={'pk': pk}) == f'/api/v1/questions/{pk}')

    def test_post__get_question_with_wrong_method(self, pk=1):
        url = reverse('questions', kwargs={'pk': pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_post__question_creating_but_theme_does_not_exists(self):
        url_question = reverse('list_of_questions')
        data_question = {'question': 'new question', 'theme': 980}
        response = self.client.post(url_question, data_question)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Question.objects.count(), 0)


class ResultsTest(APITestCase):

    def test_get__get_list_of_results(self):
        url = reverse('results')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test__is_results_endpoint_use_correct_url(self):
        self.assertTrue(reverse('results') == '/api/v1/results')


class AnswerTests(APITestCase):
    def test_get__get_list_of_answers(self):
        url = reverse('list_of_answers')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_and_put__create_and_change_answer(self):
        # new theme entry for current test
        url_theme = reverse('list_of_themes')
        data_theme = {'title': 'new theme', 'description': 'new description', 'slug': 'new_theme'}
        response = self.client.post(url_theme, data_theme)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # new question entry bound with the new theme entry
        url_question = reverse('list_of_questions')
        data_question = {'question': 'new question', 'theme': response.data.get('id')}
        response = self.client.post(url_question, data_question)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), 1)

        # new answer entry bound with the new question entry
        url_answer = reverse('list_of_answers')
        data_answer = {'question': response.data.get('id'), 'answer': 'answer'}
        response = self.client.post(url_answer, data_answer)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), 1)

        # change answer
        changed_url_answer = reverse('answers', kwargs={'pk': response.data.get('id')})
        changed_data_answer = {'question': response.data.get('id'), 'answer': 'answer changed'}
        response = self.client.put(changed_url_answer, changed_data_answer)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Question.objects.count(), 1)

    def test__is_question_endpoints_use_correct_url(self, pk=1):
        self.assertTrue(reverse('list_of_answers') == '/api/v1/answers')
        self.assertTrue(reverse('answers', kwargs={'pk': pk}) == f'/api/v1/answers/{pk}')


class RightAnswerTests(APITestCase):
    def test_get__get_list_of_right_answers(self):
        url = reverse('list_of_right_answers')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_and_put__create_and_change_answer(self):
        # new theme entry for current test
        url_theme = reverse('list_of_themes')
        data_theme = {'title': 'new theme', 'description': 'new description', 'slug': 'new_theme'}
        response = self.client.post(url_theme, data_theme)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # new question entry bound with the new theme entry
        url_question = reverse('list_of_questions')
        data_question = {'question': 'new question', 'theme': response.data.get('id')}
        response = self.client.post(url_question, data_question)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), 1)

        # new answer entry bound with the new question entry
        url_answer = reverse('list_of_answers')
        data_answer = {'question': response.data.get('id'), 'answer': 'answer'}
        response = self.client.post(url_answer, data_answer)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), 1)

        # create right answer
        changed_url_right_answer = reverse('list_of_right_answers')
        changed_data_right_answer = {'question': data_answer['question'],
                                     'theme': data_question['theme'],
                                     'comment': 'comment',
                                     'list_od_answers': [response.data.get('id')]}

        response = self.client.post(changed_url_right_answer, changed_data_right_answer)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RightAsnwer.objects.count(), 1)

    def test__is_right_answer_endpoints_use_correct_url(self, pk=1):
        self.assertTrue(reverse('list_of_right_answers') == '/api/v1/right-answers')
        self.assertTrue(reverse('right_answers', kwargs={'pk': pk}) == f'/api/v1/right-answers/{pk}')


class PermissionsTests(APITestCase):

    def setUp(self):
        self.admin_user = UserProfile.objects.create(email='suemail', is_staff=True)
        self.non_admin_user = UserProfile.objects.create(email='uemail')
        self.factory = RequestFactory()

    def test__admin_user_returns_true(self):
        request = self.factory.delete('/')
        request.user = self.admin_user
        permission_check = IsAdminUser()
        permission = permission_check.has_permission(request, None)
        self.assertTrue(permission)

    def test__access_to_users_list_by_non_admin_user(self):
        url = reverse('user_create')
        login = self.client.login()
        response = self.client.get(url, format='json')
        self.assertFalse(login)
        self.assertEqual(response.status_code, 403)

    def test__access_to_themes_page_for_any(self):
        url = reverse('list_of_themes')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)


class SerializersTests(APITestCase):

    def test__theme_serializer_is_not_valid_if_any_required_field_is_missing(self):
        data = {'title': 'theme', 'description': 'description', 'slug': '', 'is_published': True}
        serializer = ThemeSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test__theme_serializer_is_valid(self):
        data = {'title': 'theme', 'description': 'description', 'slug': 'slug', 'is_published': True}
        serializer = ThemeSerializer(data=data)
        self.assertTrue(serializer.is_valid())
