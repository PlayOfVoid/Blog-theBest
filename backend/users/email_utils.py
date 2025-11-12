"""
Утилиты для отправки email уведомлений
"""
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string


def send_notification_email(user, subject, template_name, context):
    """
    Отправка email уведомления пользователю
    
    Args:
        user: Пользователь-получатель
        subject: Тема письма
        template_name: Имя шаблона для письма
        context: Контекст для шаблона
    """
    # Проверяем настройки пользователя
    if not hasattr(user, 'settings') or not user.settings.email_notifications:
        return False
    
    if not user.email:
        return False
    
    try:
        # Рендерим HTML письмо
        html_message = render_to_string(template_name, context)
        
        # Создаем текстовую версию (простую)
        text_message = f"""
        {subject}
        
        Это уведомление с сайта TechBlog.
        
        Вы можете отключить email уведомления в настройках профиля:
        {settings.SITE_URL}/users/settings/
        """
        
        send_mail(
            subject=subject,
            message=text_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=True,
        )
        return True
    except Exception as e:
        print(f"Error sending email to {user.email}: {e}")
        return False


def notify_new_comment(comment):
    """Уведомление автору поста о новом комментарии"""
    post_author = comment.post.author
    
    # Не уведомляем если автор сам комментирует
    if comment.author == post_author:
        return
    
    subject = f'Новый комментарий к вашему посту "{comment.post.title}"'
    context = {
        'post': comment.post,
        'comment': comment,
        'author': post_author,
    }
    
    send_notification_email(
        user=post_author,
        subject=subject,
        template_name='emails/new_comment.html',
        context=context
    )


def notify_new_like(like):
    """Уведомление автору поста о новом лайке"""
    post_author = like.post.author
    
    # Не уведомляем если автор сам лайкает
    if like.user == post_author:
        return
    
    subject = f'{like.user.username} лайкнул ваш пост "{like.post.title}"'
    context = {
        'post': like.post,
        'liker': like.user,
        'author': post_author,
    }
    
    send_notification_email(
        user=post_author,
        subject=subject,
        template_name='emails/new_like.html',
        context=context
    )


def notify_new_follower(subscription):
    """Уведомление пользователю о новом подписчике"""
    subject = f'{subscription.user.username} подписался на вас!'
    context = {
        'follower': subscription.user,
        'author': subscription.author,
    }
    
    send_notification_email(
        user=subscription.author,
        subject=subject,
        template_name='emails/new_follower.html',
        context=context
    )


def notify_new_post_to_followers(post):
    """Уведомление подписчикам о новом посте автора"""
    from blog.models import Subscribe
    
    # Получаем всех подписчиков автора
    subscribers = Subscribe.objects.filter(author=post.author).select_related('user')
    
    subject = f'{post.author.username} опубликовал новый пост: "{post.title}"'
    
    for subscription in subscribers:
        context = {
            'post': post,
            'author': post.author,
            'subscriber': subscription.user,
        }
        
        send_notification_email(
            user=subscription.user,
            subject=subject,
            template_name='emails/new_post.html',
            context=context
        )

