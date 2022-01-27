from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView
from rest_framework import permissions

from telegram.models import TelegramUser
from telegram import serializers
from telegram.paginations import UsersPagination


class TelegramUserCreateAPIView(CreateAPIView):
    """View for creating a Telegram user."""
    serializer_class = serializers.TelegramUserSerializer
    queryset = TelegramUser.objects.all()
    permission_classes = (permissions.IsAuthenticated,)


class TelegramUsersListAPIView(ListAPIView):
    """View that return bot users."""
    serializer_class = serializers.TelegramUsersList
    queryset = TelegramUser.objects.all()
    permission_classes = (permissions.AllowAny,)
    pagination_class = UsersPagination


class TelegramUserGetAPIView(RetrieveUpdateAPIView):
    """TelegramUser GET, PATCH, PUT view."""
    serializer_class = serializers.TelegramUserDetailSerializer
    queryset = TelegramUser.objects.all()
    permission_classes = (permissions.AllowAny,)
