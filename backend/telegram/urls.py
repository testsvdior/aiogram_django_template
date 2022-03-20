from django.urls import path

from telegram import views

urlpatterns = [
    path('users/', views.TelegramUserListCreateAPIView.as_view(), name='list-create-user'),
    path('users/<int:pk>', views.TelegramUserGetAPIView.as_view(), name='user-detail'),
]
