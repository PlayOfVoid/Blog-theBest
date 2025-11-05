from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.


class Profile(models.Model):
    """Расширенный профиль пользователя"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True, verbose_name='О себе')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Аватар')
    location = models.CharField(max_length=100, blank=True, verbose_name='Местоположение')
    website = models.URLField(blank=True, verbose_name='Веб-сайт')
    
    def __str__(self):
        return f'Профиль {self.user.username}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def get_total_likes(self):
        """Получить общее количество лайков на всех постах пользователя"""
        from blog.models import Like
        return Like.objects.filter(post__author=self.user).count()

    def get_followers_count(self):
        """Количество подписчиков"""
        return self.user.subscribers.count()

    def get_following_count(self):
        """Количество подписок"""
        return self.user.subscribes.count()


class UserSettings(models.Model):
    """Настройки пользователя"""
    THEME_CHOICES = [
        ('light', 'Светлая'),
        ('dark', 'Темная'),
        ('cyber', 'Кибердизайн'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='settings')
    theme = models.CharField(max_length=10, choices=THEME_CHOICES, default='light', verbose_name='Тема')
    sound_enabled = models.BooleanField(default=True, verbose_name='Звуки включены')
    email_notifications = models.BooleanField(default=True, verbose_name='Email уведомления')
    
    def __str__(self):
        return f'Настройки {self.user.username}'

    class Meta:
        verbose_name = 'Настройки пользователя'
        verbose_name_plural = 'Настройки пользователей'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Автоматически создаем профиль и настройки при создании пользователя"""
    if created:
        Profile.objects.create(user=instance)
        UserSettings.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Сохраняем профиль и настройки при сохранении пользователя"""
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        Profile.objects.create(user=instance)
    
    if hasattr(instance, 'settings'):
        instance.settings.save()
    else:
        UserSettings.objects.create(user=instance)
