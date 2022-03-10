from rest_framework.generics import RetrieveUpdateAPIView, ListCreateAPIView

from telegram.models import TelegramUser
from telegram import serializers
from telegram.paginations import UsersPagination


class TelegramUserListCreateAPIView(ListCreateAPIView):
    """
    View create user if request method POST.
    Return users-list if request method GET.
    Return only user_id if request method GET and having param only_id.
    """
    queryset = TelegramUser.objects.all()
    pagination_class = UsersPagination

    def get_serializer_class(self):
        if self.request.GET:
            if self.request.GET.get('only_id'):
                return serializers.TelegramUserIDSerializer
            return serializers.TelegramUsersList
        return serializers.TelegramUserSerializer


class TelegramUserGetAPIView(RetrieveUpdateAPIView):
    """TelegramUser GET, PATCH, PUT view."""
    serializer_class = serializers.TelegramUserDetailSerializer
    queryset = TelegramUser.objects.all()
