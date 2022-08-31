from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase, APIClient

from telegram.models import TelegramUser

User = get_user_model()


class BaseTestCase(APITestCase, APIClient):
    """
    Base test case.
    """
    def setUp(self):
        self.User = get_user_model()
        self.data = {
            'username': 'first_user',
            'password': 'foo',
        }
        self.user = self.User.objects.create_user(**self.data)
        self.tg_user = TelegramUser.objects.create(user_id=1, first_name='Adam')

    def get_jwt(self):
        """Method generate and return JWT token for user."""
        url = reverse('token_obtain_pair')
        response = self.client.post(url, data=self.data)
        return response.data['access']
