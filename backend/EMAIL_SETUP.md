# Настройка Email уведомлений

## Режим разработки (по умолчанию)

В режиме разработки все письма выводятся в консоль сервера. Это позволяет тестировать функциональность без реальной отправки писем.

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

## Production настройка

### Использование Gmail

1. Создайте "App Password" в Google Account:
   - Перейдите в https://myaccount.google.com/security
   - Включите 2FA (двухфакторную аутентификацию)
   - Создайте App Password для приложения

2. Обновите `backend/settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'  # App Password, не обычный пароль!
DEFAULT_FROM_EMAIL = 'TechBlog <your-email@gmail.com>'
```

### Использование других SMTP провайдеров

#### SendGrid
```python
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = 'your-sendgrid-api-key'
```

#### Mailgun
```python
EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'postmaster@yourdomain.mailgun.org'
EMAIL_HOST_PASSWORD = 'your-mailgun-password'
```

#### Amazon SES
```python
EMAIL_BACKEND = 'django_ses.SESBackend'
AWS_ACCESS_KEY_ID = 'your-access-key'
AWS_SECRET_ACCESS_KEY = 'your-secret-key'
AWS_SES_REGION_NAME = 'us-east-1'
AWS_SES_REGION_ENDPOINT = 'email.us-east-1.amazonaws.com'
```

## Типы уведомлений

Система автоматически отправляет уведомления при:

1. **Новый комментарий** - автору поста
2. **Новый лайк** - автору поста
3. **Новый подписчик** - автору
4. **Новый пост** - всем подписчикам автора

## Управление уведомлениями

Пользователи могут включать/выключать уведомления в настройках профиля:
- `/users/settings/` → Email уведомления

## Безопасность

⚠️ **ВАЖНО для Production:**

1. Никогда не коммитьте пароли в Git
2. Используйте переменные окружения:

```python
import os

EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
```

3. Создайте `.env` файл (добавьте в .gitignore):

```bash
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

4. Установите python-decouple:

```bash
pip install python-decouple
```

5. Используйте в settings.py:

```python
from decouple import config

EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
```

## Тестирование

Для тестирования отправки писем:

```python
# В Django shell
python manage.py shell

from django.core.mail import send_mail

send_mail(
    'Тест',
    'Это тестовое письмо',
    'noreply@techblog.com',
    ['recipient@example.com'],
    fail_silently=False,
)
```

## Отключение уведомлений

Чтобы полностью отключить отправку писем, закомментируйте импорт сигналов в `blog/apps.py`:

```python
def ready(self):
    # import blog.signals  # Закомментируйте эту строку
    pass
```

