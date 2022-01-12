from django.urls import path

from telegram import views

urlpatterns = [
    path('user/', views.TelegramUserCreateAPIView.as_view(), name='create-user'),
    path('user/<int:pk>', views.TelegramUserGetAPIView.as_view(), name='user-detail'),
    path('users/', views.TelegramUsersListAPIView.as_view(), name='users-list'),
]
