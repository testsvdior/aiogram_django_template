from django.urls import path

from telegram import views

urlpatterns = [
    path('users/', views.TelegramUserListCreateAPIView.as_view(), name='list_create_user'),
    path('users/<int:pk>', views.TelegramUserGetAPIView.as_view(), name='user_detail'),
]
