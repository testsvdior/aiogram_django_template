from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework import permissions

from telegram.models import TelegramUser
from telegram.serializers import TelegramUserSerializer, TelegramUsersList


class TelegramUserCreateAPIView(CreateAPIView):
    """View for creating a Telegram user."""
    serializer_class = TelegramUserSerializer
    queryset = TelegramUser.objects.all()
    permission_classes = (permissions.IsAuthenticated,)


class TelegramUsersListAPIView(ListAPIView):
    """View that return bot users."""
    # todo - создать endpoint который возвращает список пользователей + пагинация
    serializer_class = TelegramUsersList

    def get_queryset(self):
        queryset = TelegramUser.objects.all().values('user_id', 'username', 'first_name')
        return queryset
