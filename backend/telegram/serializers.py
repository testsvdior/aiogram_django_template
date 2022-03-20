from rest_framework import serializers

from telegram.models import TelegramUser


class TelegramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = ('user_id', 'username', 'first_name', 'last_name', 'language_code')


class TelegramUsersList(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = ('user_id', 'username', 'first_name')


class TelegramUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = ('user_id', 'username', 'first_name', 'last_name', 'language_code', 'is_banned')
        read_only_fields = ['user_id']


class TelegramUserIDSerializer(serializers.ModelSerializer):
    """Using for handler cmd_message."""
    class Meta:
        model = TelegramUser
        fields = ('user_id',)
