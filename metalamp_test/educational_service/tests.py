from django.test import TestCase, Client
from educational_service.models import *


class AuthenticationTest(TestCase):

    @staticmethod
    def auth():
        user = UserProfile.objects.create(email='email')
        user.set_password('password')
        user.save()

        return {'email': 'email', 'password': 'password'}

    def test__user_login(self):
        user = self.auth()
        test_client = Client()
        logged_in = test_client.login(**user)
        self.assertEqual(logged_in, True)

        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'educational_service/login.html')

    def test__user_registration(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'educational_service/registration.html')

    def test__valid_registration_form(self):
        valid_initial = {
            'email': 'mail@mail.lmao',
            'password1': 'ghb123dtn',
            'password2': 'ghb123dtn'
        }

        response = self.client.post(reverse('register'), valid_initial)
        self.assertEqual(response.status_code, 302)

    def test__invalid_registration_form(self):
        invalid_initial = {
            'email': '',
            'password1': 'ghb123dtn',
            'password2': 'ghb123dtn'
        }

        response = self.client.post(reverse('register'), invalid_initial)

        self.assertFormError(response, 'form', 'email', 'This field is required.')

    def test__different_passwords_in_registration_form(self):
        invalid_initial = {
            'email': 'mail@mail.lmao',
            'password1': 'ghb123dtn',
            'password2': 'different'
        }

        response = self.client.post(reverse('register'), invalid_initial)

        self.assertFormError(response, 'form', 'password2', 'The two password fields didn’t match.')
