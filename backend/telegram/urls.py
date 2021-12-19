from django.urls import path

from telegram.views import TelegramUserCreateAPIView, TelegramUsersListAPIView

urlpatterns = [
    path('user/', TelegramUserCreateAPIView.as_view(), name='create-user'),
    path('users/', TelegramUsersListAPIView.as_view(), name='users-list'),
]
