from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView, ListCreateAPIView
from rest_framework.response import Response

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

    def create(self, request, *args, **kwargs):
        instance, created = TelegramUser.objects.update_or_create(
            user_id=request.data['user_id'],
            first_name=request.data['first_name'],
        )
        serializer = serializers.TelegramUserSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
        if created:
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status.HTTP_200_OK)


class TelegramUserGetAPIView(RetrieveUpdateAPIView):
    """TelegramUser GET, PATCH, PUT view."""
    serializer_class = serializers.TelegramUserDetailSerializer
    queryset = TelegramUser.objects.all()
