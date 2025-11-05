from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse


# Create your models here.


class Tag(models.Model):
    """Теги для постов"""
    name = models.CharField(max_length=50, unique=True, verbose_name='Название тега')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='URL')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def get_absolute_url(self):
        return reverse('blog:tag_posts', kwargs={'slug': self.slug})


class Post(models.Model):
    """Посты блога с поддержкой Markdown"""
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание (Markdown)')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name='Автор')
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True, verbose_name='Теги')
    views = models.PositiveIntegerField(default=0, verbose_name='Просмотры')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.pk})

    def total_likes(self):
        """Общее количество лайков"""
        return self.likes.count()
    
    def increment_views(self):
        """Увеличить счетчик просмотров"""
        self.views += 1
        self.save(update_fields=['views'])


class Comment(models.Model):
    """Комментарии к постам (без Markdown)"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='Пост')
    content = models.TextField(verbose_name='Содержание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='Автор')

    def __str__(self):
        return f'Комментарий к "{self.post.title}" от {self.author.username}'

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Like(models.Model):
    """Лайки к постам"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes', verbose_name='Пост')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes', verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'{self.user.username} лайкнул "{self.post.title}"'

    class Meta:
        unique_together = ['post', 'user']
        ordering = ['-created_at']
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'


class Subscribe(models.Model):
    """Подписки на авторов"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscribes', verbose_name='Подписчик')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscribers', verbose_name='Автор')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата подписки')

    def __str__(self):
        return f'{self.user.username} подписан на {self.author.username}'

    class Meta:
        unique_together = ['user', 'author']
        ordering = ['-created_at']
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

