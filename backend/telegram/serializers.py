from rest_framework import serializers

from telegram.models import TelegramUser


class TelegramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = ('user_id', 'username', 'first_name', 'last_name', 'language_code')
