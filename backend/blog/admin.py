from django.contrib import admin
from .models import Post, Comment, Tag, Like, Subscribe


# Register your models here.


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'views', 'total_likes']
    list_filter = ['created_at', 'author', 'tags']
    search_fields = ['title', 'content']
    filter_horizontal = ['tags']
    date_hierarchy = 'created_at'
    readonly_fields = ['views', 'created_at', 'updated_at']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'created_at', 'short_content']
    list_filter = ['created_at', 'author']
    search_fields = ['content', 'post__title']
    date_hierarchy = 'created_at'
    
    def short_content(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    short_content.short_description = 'Содержание'


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'post__title']
    date_hierarchy = 'created_at'


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ['user', 'author', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'author__username']
    date_hierarchy = 'created_at'
