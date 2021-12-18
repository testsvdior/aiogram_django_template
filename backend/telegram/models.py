from django.db import models


class TelegramUser(models.Model):
    # fields copied from https://github.com/itisnotyourenv/django-telegram-bot/blob/main/utils/models.py
    user_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=32, null=True, blank=True)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256, null=True, blank=True)
    language_code = models.CharField(max_length=8, help_text="Telegram client's lang", null=True, blank=True)
    deep_link = models.CharField(max_length=64, null=True, blank=True)

    is_blocked_bot = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)

    is_admin = models.BooleanField(default=False)
    is_moderator = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'telegram_users'
        ordering = ('-created_at',)
        verbose_name = 'TG user'
        verbose_name_plural = 'TG users'

    def __str__(self):
        return self.username if self.username else self.user_id

    def save(self, *args, **kwargs):
        self.deep_link = f't.me/{self.username}' if self.username else None
        super().save(*args, **kwargs)
