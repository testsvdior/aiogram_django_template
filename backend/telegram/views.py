from rest_framework.generics import CreateAPIView

from telegram.models import TelegramUser
from telegram.serializers import TelegramUserSerializer


class TelegramUserCreateAPIView(CreateAPIView):
    """View for creating a Telegram user."""
    serializer_class = TelegramUserSerializer
    queryset = TelegramUser.objects.all()
