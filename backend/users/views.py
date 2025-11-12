from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator

from .forms import UserRegisterForm, UserLoginForm, UserUpdateForm, ProfileUpdateForm, UserSettingsForm
from .models import Profile
from blog.models import Post, Subscribe


def register(request):
    """Регистрация нового пользователя"""
    if request.user.is_authenticated:
        return redirect('blog:index')
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт {username} успешно создан!')
            login(request, user)
            return redirect('blog:index')
    else:
        form = UserRegisterForm()
    
    context = {
        'form': form,
    }
    return render(request, 'users/register.html', context)


def user_login(request):
    """Вход в систему"""
    if request.user.is_authenticated:
        return redirect('blog:index')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {username}!')
                next_url = request.GET.get('next', 'blog:index')
                return redirect(next_url)
    else:
        form = UserLoginForm()
    
    context = {
        'form': form,
    }
    return render(request, 'users/login.html', context)


@login_required
def user_logout(request):
    """Выход из системы"""
    logout(request)
    messages.info(request, 'Вы вышли из системы')
    return redirect('blog:index')


def profile(request, username):
    """Профиль пользователя"""
    user = get_object_or_404(User, username=username)
    profile = user.profile
    posts = Post.objects.filter(author=user).select_related('author').prefetch_related('tags')
    
    # Проверяем, подписан ли текущий пользователь
    is_subscribed = False
    if request.user.is_authenticated and request.user != user:
        is_subscribed = Subscribe.objects.filter(
            user=request.user,
            author=user
        ).exists()
    
    # Пагинация постов
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'profile_user': user,
        'profile': profile,
        'page_obj': page_obj,
        'is_subscribed': is_subscribed,
    }
    return render(request, 'users/profile.html', context)


@login_required
def settings(request):
    """Настройки аккаунта"""
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )
        settings_form = UserSettingsForm(
            request.POST,
            instance=request.user.settings
        )
        
        if user_form.is_valid() and profile_form.is_valid() and settings_form.is_valid():
            user_form.save()
            profile_form.save()
            settings_form.save()
            messages.success(request, 'Настройки успешно обновлены!')
            return redirect('users:settings')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        settings_form = UserSettingsForm(instance=request.user.settings)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'settings_form': settings_form,
    }
    return render(request, 'users/settings.html', context)


@login_required
def my_subscriptions(request):
    """Мои подписки"""
    subscriptions = Subscribe.objects.filter(user=request.user).select_related('author')
    
    context = {
        'subscriptions': subscriptions,
    }
    return render(request, 'users/subscriptions.html', context)


@login_required
def my_subscribers(request):
    """Мои подписчики"""
    subscribers = Subscribe.objects.filter(author=request.user).select_related('user')
    
    context = {
        'subscribers': subscribers,
    }
    return render(request, 'users/subscribers.html', context)
