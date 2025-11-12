"""
Сигналы для автоматической отправки email уведомлений
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Comment, Like, Subscribe, Post
from users.email_utils import (
    notify_new_comment,
    notify_new_like,
    notify_new_follower,
    notify_new_post_to_followers
)


@receiver(post_save, sender=Comment)
def comment_created(sender, instance, created, **kwargs):
    """Отправка уведомления при создании комментария"""
    if created:
        notify_new_comment(instance)


@receiver(post_save, sender=Like)
def like_created(sender, instance, created, **kwargs):
    """Отправка уведомления при лайке"""
    if created:
        notify_new_like(instance)


@receiver(post_save, sender=Subscribe)
def subscription_created(sender, instance, created, **kwargs):
    """Отправка уведомления при новой подписке"""
    if created:
        notify_new_follower(instance)


@receiver(post_save, sender=Post)
def post_created(sender, instance, created, **kwargs):
    """Отправка уведомления подписчикам при создании поста"""
    if created:
        # Отправляем уведомления подписчикам
        notify_new_post_to_followers(instance)

