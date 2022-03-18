from __future__ import annotations

from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest
from django.db.models.query import QuerySet

from telegram.models import TelegramUser


def block_selected_users(model_admin: UserAdmin, request: WSGIRequest, queryset: QuerySet[TelegramUser]):
    """
    Function set action in Admin-panel that block selected users.
    """
    queryset.all().update(is_banned=True)


def unlock_selected_users(model_admin: UserAdmin, request: WSGIRequest, queryset: QuerySet[TelegramUser]):
    """
    Function set action in Admin-panel that unlock selected users.
    """
    queryset.all().update(is_banned=False)


@admin.register(TelegramUser)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'user_id', 'username', 'first_name', 'language_code', 'created_at', "is_blocked_bot", 'is_banned', 'deep_link'
    ]
    list_filter = ["is_blocked_bot", "is_moderator"]
    search_fields = ('first_name', 'last_name', 'username', 'user_id')
    actions = [block_selected_users, unlock_selected_users]
