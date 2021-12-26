from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework import status

from telegram.models import TelegramUser

User = get_user_model()


class TestAPI(APITestCase, APIClient):
    def setUp(self):
        self.User = get_user_model()
        self.data = {
            'username': 'first_user',
            'password': 'foo',
        }
        self.user = self.User.objects.create_user(**self.data)
        print('created test user:' + str(self.user))

    def get_jwt(self):
        url = reverse('token_obtain_pair')
        response = self.client.post(url, data=self.data)
        return response.data['access']

    def test_GET_users(self):
        url = reverse('users-list')
        token = self.get_jwt()
        # устанавливаю headers
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
