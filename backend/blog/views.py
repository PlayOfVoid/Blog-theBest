from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import Post, Comment, Subscribe, Like, Tag
from .forms import CommentForm, PostForm, SearchForm


# Create your views here.


def index(request):
    """Главная страница"""
    recent_posts = Post.objects.select_related('author').prefetch_related('tags').all()[:10]
    popular_tags = Tag.objects.annotate(post_count=Count('posts')).order_by('-post_count')[:10]
    
    context = {
        'recent_posts': recent_posts,
        'popular_tags': popular_tags,
    }
    return render(request, 'blog/index.html', context)


def posts_list(request):
    """Список всех постов с пагинацией"""
    posts = Post.objects.select_related('author').prefetch_related('tags').all()
    
    # Пагинация
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'blog/posts_list.html', context)


def post_detail(request, pk):
    """Детальная страница поста с комментариями"""
    post = get_object_or_404(
        Post.objects.select_related('author').prefetch_related('tags', 'comments__author'),
        pk=pk
    )
    
    # Увеличиваем счетчик просмотров
    post.increment_views()
    
    # Проверяем, лайкнул ли пользователь пост
    user_liked = False
    if request.user.is_authenticated:
        user_liked = Like.objects.filter(post=post, user=request.user).exists()
    
    # Форма комментария
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid() and request.user.is_authenticated:
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Комментарий добавлен!')
            return redirect('blog:post_detail', pk=pk)
    else:
        comment_form = CommentForm()
    
    context = {
        'post': post,
        'comment_form': comment_form,
        'user_liked': user_liked,
    }
    return render(request, 'blog/post_detail.html', context)


@login_required
def create_post(request):
    """Создание нового поста"""
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            messages.success(request, 'Пост успешно создан!')
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm()
    
    context = {
        'form': form,
    }
    return render(request, 'blog/create_post.html', context)


@login_required
def update_post(request, pk):
    """Редактирование поста"""
    post = get_object_or_404(Post, pk=pk, author=request.user)
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пост успешно обновлен!')
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    
    context = {
        'form': form,
        'post': post,
    }
    return render(request, 'blog/update_post.html', context)


@login_required
def delete_post(request, pk):
    """Удаление поста"""
    post = get_object_or_404(Post, pk=pk, author=request.user)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Пост успешно удален!')
        return redirect('blog:posts_list')
    
    context = {
        'post': post,
    }
    return render(request, 'blog/delete_post.html', context)


@login_required
@require_POST
def toggle_like(request, pk):
    """AJAX: Лайк/анлайк поста"""
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    
    return JsonResponse({
        'liked': liked,
        'total_likes': post.total_likes()
    })


@login_required
@require_POST
def toggle_subscribe(request, username):
    """AJAX: Подписка/отписка от автора"""
    from django.contrib.auth.models import User
    author = get_object_or_404(User, username=username)
    
    if author == request.user:
        return JsonResponse({'error': 'Нельзя подписаться на самого себя'}, status=400)
    
    subscription, created = Subscribe.objects.get_or_create(
        user=request.user,
        author=author
    )
    
    if not created:
        subscription.delete()
        subscribed = False
    else:
        subscribed = True
    
    return JsonResponse({
        'subscribed': subscribed,
        'followers_count': author.subscribers.count()
    })


def tag_posts(request, slug):
    """Посты по тегу"""
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=tag).select_related('author').prefetch_related('tags')
    
    # Пагинация
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'tag': tag,
        'page_obj': page_obj,
    }
    return render(request, 'blog/tag_posts.html', context)


def search(request):
    """Поиск по постам"""
    form = SearchForm(request.GET)
    posts = Post.objects.none()
    query = None
    
    if form.is_valid():
        query = form.cleaned_data.get('q')
        if query:
            # Поиск по заголовку, содержанию и тегам
            posts = Post.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(tags__name__icontains=query)
            ).select_related('author').prefetch_related('tags').distinct()
    
    # Пагинация
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'form': form,
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'blog/search.html', context)




