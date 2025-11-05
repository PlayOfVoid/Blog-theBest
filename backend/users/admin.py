from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile, UserSettings


# Register your models here.


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Профиль'


class UserSettingsInline(admin.StackedInline):
    model = UserSettings
    can_delete = False
    verbose_name_plural = 'Настройки'


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, UserSettingsInline)
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined']


# Перерегистрируем User с новым админом
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'get_followers_count', 'get_total_likes']
    search_fields = ['user__username', 'bio', 'location']


@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ['user', 'theme', 'sound_enabled', 'email_notifications']
    list_filter = ['theme', 'sound_enabled', 'email_notifications']
