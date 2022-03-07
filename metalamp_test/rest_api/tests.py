from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from educational_service.models import *


# class AccountTests(APITestCase):
#     def test_create_account(self):
#         """
#         Ensure we can create a new account object.
#         """
#
#         url = reverse('register')
#
#         data = {'email': 'qwe@qwe.tu', 'password1': 'ghbdtn123', 'password2': 'ghbdtn123'}
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(UserProfile.objects.count(), 1)
#         self.assertEqual(UserProfile.objects.get().email, 'qwe@qwe.tu')

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
        # print([item for item in response.data.get('slug')][0])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('slug')[0],
                         'Enter a valid "slug" consisting of letters, numbers, underscores or hyphens.')
        self.assertEqual(Theme.objects.count(), 0)

    def test_get__get_non_existing_theme(self, pk=1):
        url = reverse('theme', kwargs={'pk': pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post__get_theme_with_wrong_method(self, pk=1):
        url = reverse('theme', kwargs={'pk': pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_put__change_existing_theme(self):
        url_for_create = reverse('list_of_themes')
        data = {'title': 'new theme 2', 'description': 'new description 2', 'slug': 'new_theme_2'}
        response = self.client.post(url_for_create, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # print(response.data)
        # print(Theme.objects.all())

        url_for_change = reverse('theme', kwargs={'pk': response.data.get('id')})
        changed_data = {'title': 'new theme 2 changed',
                        'description': 'new description 2 changed',
                        'slug': 'new_theme_2_changed'}
        response = self.client.put(url_for_change, changed_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put__change_not_existing_theme(self):
        url_for_create = reverse('list_of_themes')
        data = {'title': 'new theme 2', 'description': 'new description 2', 'slug': 'new_theme_2'}
        response = self.client.post(url_for_create, data)

        url_for_change = reverse('theme', kwargs={'pk': response.data.get('id') + 1})
        changed_data = {'title': 'new theme 9999', 'description': 'new description 9999', 'slug': 'new_theme_9999'}
        response = self.client.put(url_for_change, changed_data)
        # print(Theme.objects.all())
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put__change_existing_theme_but_title_does_not_filled(self):
        url_for_create = reverse('list_of_themes')
        data = {'title': 'new theme 2', 'description': 'new description 2', 'slug': 'new_theme_2'}
        response = self.client.post(url_for_create, data)

        url_for_change = reverse('theme', kwargs={'pk': response.data.get('id')})
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
        print(response.data)
        self.assertEqual('with this slug already exists' in response.data.get('slug')[0], True)
