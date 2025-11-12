from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Аутентификация
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Профиль
    path('profile/<str:username>/', views.profile, name='profile'),
    
    # Настройки
    path('settings/', views.settings, name='settings'),
    
    # Подписки
    path('subscriptions/', views.my_subscriptions, name='my_subscriptions'),
    path('subscribers/', views.my_subscribers, name='my_subscribers'),
]

