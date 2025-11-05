from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Главная и список
    path('', views.index, name='index'),
    path('posts/', views.posts_list, name='posts_list'),
    
    # Детали поста
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    
    # CRUD операции с постами
    path('post/create/', views.create_post, name='create_post'),
    path('post/<int:pk>/update/', views.update_post, name='update_post'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),
    
    # Лайки и подписки (AJAX)
    path('post/<int:pk>/like/', views.toggle_like, name='toggle_like'),
    path('user/<str:username>/subscribe/', views.toggle_subscribe, name='toggle_subscribe'),
    
    # Теги
    path('tag/<slug:slug>/', views.tag_posts, name='tag_posts'),
    
    # Поиск
    path('search/', views.search, name='search'),
]