#!/usr/bin/env python
"""
Скрипт для создания суперюзера root/root
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User

# Проверяем, существует ли уже пользователь root
if not User.objects.filter(username='root').exists():
    User.objects.create_superuser(
        username='root',
        email='',
        password='root'
    )
    print('Суперюзер root создан успешно!')
else:
    print('Пользователь root уже существует')

