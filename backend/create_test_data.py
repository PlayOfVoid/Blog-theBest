#!/usr/bin/env python
"""
Скрипт для создания тестовых данных
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import Post, Tag, Comment, Like
from django.utils.text import slugify

print("Creating test data...")

# Create users
users_data = [
    ('alice', 'alice@example.com', 'Alice'),
    ('bob', 'bob@example.com', 'Bob'),
    ('charlie', 'charlie@example.com', 'Charlie'),
]

users = {}
for username, email, first_name in users_data:
    user, created = User.objects.get_or_create(
        username=username,
        defaults={'email': email, 'first_name': first_name}
    )
    if created:
        user.set_password('password123')
        user.save()
        print(f"[+] Created user: {username}")
    users[username] = user

# Create tags
tags_data = ['Python', 'Django', 'JavaScript', 'Web', 'Tutorial', 'Backend', 'Frontend']
tags = {}
for tag_name in tags_data:
    tag, created = Tag.objects.get_or_create(
        name=tag_name,
        defaults={'slug': slugify(tag_name)}
    )
    if created:
        print(f"[+] Created tag: {tag_name}")
    tags[tag_name] = tag

# Создаем посты
posts_data = [
    {
        'title': 'Введение в Django',
        'content': '''# Добро пожаловать в Django!

Django - это мощный веб-фреймворк на Python, который позволяет быстро создавать веб-приложения.

## Основные преимущества

- **Быстрая разработка** - Django включает множество готовых компонентов
- **Безопасность** - защита от XSS, CSRF и SQL-инъекций из коробки
- **Масштабируемость** - используется крупными компаниями

## Пример кода

```python
from django.http import HttpResponse

def hello(request):
    return HttpResponse("Hello, World!")
```

Начните изучать Django сегодня!''',
        'author': 'alice',
        'tags': ['Python', 'Django', 'Backend', 'Tutorial']
    },
    {
        'title': 'Основы JavaScript для начинающих',
        'content': '''# JavaScript - язык веба

JavaScript является основным языком программирования для веб-разработки.

## Что можно делать с JavaScript?

1. Создавать интерактивные веб-страницы
2. Разрабатывать серверные приложения (Node.js)
3. Создавать мобильные приложения

## Простой пример

```javascript
function greet(name) {
    console.log(`Hello, ${name}!`);
}

greet("World");
```

> JavaScript постоянно развивается и остается актуальным!''',
        'author': 'bob',
        'tags': ['JavaScript', 'Frontend', 'Tutorial']
    },
    {
        'title': 'Создание REST API с Django Rest Framework',
        'content': '''# REST API с Django

Django Rest Framework (DRF) упрощает создание RESTful API.

## Установка

```bash
pip install djangorestframework
```

## Создание сериализатора

```python
from rest_framework import serializers

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
```

## ViewSet

```python
from rest_framework import viewsets

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
```

Теперь у вас есть полнофункциональное API!''',
        'author': 'alice',
        'tags': ['Python', 'Django', 'Backend', 'Web']
    },
    {
        'title': 'Адаптивный дизайн: лучшие практики',
        'content': '''# Адаптивный веб-дизайн

Создание сайтов, которые хорошо выглядят на всех устройствах.

## Media Queries

```css
/* Мобильные устройства */
@media (max-width: 768px) {
    .container {
        padding: 10px;
    }
}

/* Планшеты */
@media (min-width: 768px) and (max-width: 1024px) {
    .container {
        padding: 20px;
    }
}
```

## Flexbox и Grid

- **Flexbox** - для одномерных макетов
- **Grid** - для двумерных макетов

Используйте правильные инструменты для правильных задач!''',
        'author': 'charlie',
        'tags': ['Frontend', 'Web', 'Tutorial']
    },
    {
        'title': 'Markdown - простой способ форматирования',
        'content': '''# Markdown - это просто!

Markdown позволяет форматировать текст с помощью простого синтаксиса.

## Базовое форматирование

**Жирный текст** и *курсив*

## Списки

- Первый элемент
- Второй элемент
  - Вложенный элемент

## Таблицы

| Заголовок 1 | Заголовок 2 |
|-------------|-------------|
| Ячейка 1    | Ячейка 2    |

## Цитаты

> Markdown делает написание контента легким и приятным!

Попробуйте сами!''',
        'author': 'bob',
        'tags': ['Tutorial', 'Web']
    },
]

created_posts = []
for post_data in posts_data:
    post, created = Post.objects.get_or_create(
        title=post_data['title'],
        defaults={
            'content': post_data['content'],
            'author': users[post_data['author']]
        }
    )
    if created:
        # Add tags
        for tag_name in post_data['tags']:
            post.tags.add(tags[tag_name])
        print(f"[+] Created post: {post.title}")
        created_posts.append(post)

# Create comments
comments_data = [
    (0, 'bob', 'Great article! Thanks for explanation!'),
    (0, 'charlie', 'Very helpful for understanding Django.'),
    (1, 'alice', 'JavaScript is really powerful!'),
    (2, 'charlie', 'DRF is a must-have for Django developers.'),
]

if created_posts:
    for post_idx, author_name, content in comments_data:
        if post_idx < len(created_posts):
            Comment.objects.get_or_create(
                post=created_posts[post_idx],
                author=users[author_name],
                content=content
            )
            print(f"[+] Created comment for post '{created_posts[post_idx].title}'")

# Create likes
if created_posts:
    for post in created_posts[:3]:
        for user in users.values():
            if user != post.author:
                Like.objects.get_or_create(post=post, user=user)
    print(f"[+] Added likes to posts")

print("\n[SUCCESS] Test data created successfully!")
print("\nYou can now:")
print("1. Go to http://127.0.0.1:8000/ - main page")
print("2. Go to http://127.0.0.1:8000/posts/ - all posts")
print("3. Click on any post to view details")
print("4. Login as root/root to create your own posts")

