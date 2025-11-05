"""
Утилиты для безопасной обработки Markdown
"""
import markdown
import bleach
from django.utils.safestring import mark_safe


def sanitize_markdown(md_text):
    """
    Конвертирует Markdown в безопасный HTML
    
    Args:
        md_text: Текст в формате Markdown
        
    Returns:
        Безопасный HTML
    """
    if not md_text:
        return ''
    
    # Расширения для Markdown
    extensions = [
        'fenced_code',      # Блоки кода с ```
        'tables',           # Таблицы
        'nl2br',            # Автоматические переносы строк
        'sane_lists',       # Улучшенные списки
        'codehilite',       # Подсветка синтаксиса
    ]
    
    # Конфигурация для подсветки кода
    extension_configs = {
        'codehilite': {
            'css_class': 'highlight',
            'linenums': False,
        }
    }
    
    # Конвертируем Markdown в HTML
    html = markdown.markdown(
        md_text,
        extensions=extensions,
        extension_configs=extension_configs,
        output_format='html5'
    )
    
    # Разрешенные HTML теги (безопасные)
    allowed_tags = [
        'a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'p', 'br', 'span', 'div',
        'table', 'thead', 'tbody', 'tr', 'th', 'td',
        'img', 'hr', 'del', 'ins', 'sup', 'sub',
    ]
    
    # Разрешенные атрибуты для тегов
    allowed_attributes = {
        'a': ['href', 'title', 'rel'],
        'abbr': ['title'],
        'acronym': ['title'],
        'img': ['src', 'alt', 'title'],
        'code': ['class'],  # Для подсветки синтаксиса
        'pre': ['class'],
        'div': ['class'],
        'span': ['class'],
        'td': ['align'],
        'th': ['align'],
    }
    
    # Разрешенные протоколы для ссылок (защита от javascript:)
    allowed_protocols = ['http', 'https', 'mailto']
    
    # Санитизируем HTML с помощью bleach
    clean_html = bleach.clean(
        html,
        tags=allowed_tags,
        attributes=allowed_attributes,
        protocols=allowed_protocols,
        strip=True  # Удаляем запрещенные теги, а не экранируем
    )
    
    return mark_safe(clean_html)

