from django_filters import rest_framework as filters

from .models import TelegramUser


class FilterUsers(filters.FilterSet):
    """
    Filter for TelegramUser model.
    """
    class Meta:
        model = TelegramUser
        fields = ('is_admin', )
