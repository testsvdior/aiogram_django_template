from django.urls import path

from telegram.views import TelegramUserCreateAPIView

urlpatterns = [
    path('user', TelegramUserCreateAPIView.as_view(), name='create-user'),
]
