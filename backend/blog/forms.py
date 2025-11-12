from django import forms
from .models import Post, Comment, Tag
from django.utils.text import slugify


class PostForm(forms.ModelForm):
    """Форма создания/редактирования поста"""
    new_tags = forms.CharField(
        required=False,
        help_text='Введите новые теги через запятую',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'python, django, web'
        })
    )
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Заголовок поста'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control markdown-editor',
                'placeholder': 'Содержание поста (поддерживается Markdown)',
                'rows': 15
            }),
            'tags': forms.CheckboxSelectMultiple(),
        }
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        if commit:
            instance.save()
            self.save_m2m()
            
            # Обрабатываем новые теги после сохранения
            new_tags_str = self.cleaned_data.get('new_tags', '')
            if new_tags_str:
                new_tag_names = [tag.strip() for tag in new_tags_str.split(',') if tag.strip()]
                for tag_name in new_tag_names:
                    tag, created = Tag.objects.get_or_create(
                        name=tag_name,
                        defaults={'slug': slugify(tag_name)}
                    )
                    instance.tags.add(tag)
        
        return instance


class CommentForm(forms.ModelForm):
    """Форма комментария (без Markdown)"""
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ваш комментарий...',
                'rows': 3
            })
        }


class SearchForm(forms.Form):
    """Форма поиска"""
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control search-input',
            'placeholder': 'Поиск по постам, тегам...',
            'autocomplete': 'off'
        })
    )



