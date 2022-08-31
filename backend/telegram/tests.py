from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status

from tests.base import BaseTestCase
from telegram.models import TelegramUser
from telegram import serializers

User = get_user_model()


class TestAPI(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.tg_user2 = TelegramUser.objects.create(user_id=300, first_name='Nooh')

    def test_get_telegram_user_list(self):
        url = reverse('list_create_user')
        token = self.get_jwt()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializers.TelegramUserSerializer(TelegramUser.objects.all(), many=True).data)

    def test_get_telegram_user_list_negative(self):
        url = reverse('list_create_user')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_telegram_user(self):
        url = reverse('list_create_user')
        token = self.get_jwt()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        data = {
            'user_id': 2,
            'first_name': 'Nooh',
        }

        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user_id'], data['user_id'])
        self.assertEqual(response.data['first_name'], data['first_name'])

    def test_post_telegram_user_negative(self):
        url = reverse('list_create_user')
        data = {
            'user_id': 2,
            'first_name': 'Nooh',
        }

        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_telegram_user_detail(self):
        url = reverse('user_detail', kwargs={'pk': self.tg_user.user_id})
        token = self.get_jwt()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializers.TelegramUserDetailSerializer(self.tg_user).data)

    def test_get_telegram_user_detail_negative(self):
        url = reverse('user_detail', kwargs={'pk': self.tg_user.user_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
