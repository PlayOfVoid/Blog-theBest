"""
Template tags для обработки Markdown
"""
from django import template
from blog.utils import sanitize_markdown

register = template.Library()


@register.filter(name='markdown')
def markdown_filter(value):
    """
    Фильтр для конвертации Markdown в HTML
    Использование: {{ post.content|markdown }}
    """
    return sanitize_markdown(value)

