// ===== Markdown редактор =====

document.addEventListener('DOMContentLoaded', function() {
    initMarkdownEditor();
});

function initMarkdownEditor() {
    const markdownTextareas = document.querySelectorAll('.markdown-editor');
    
    markdownTextareas.forEach(textarea => {
        // Добавляем toolbar для markdown
        addMarkdownToolbar(textarea);
        
        // Горячие клавиши
        addMarkdownShortcuts(textarea);
        
        // Предпросмотр (опционально)
        addMarkdownPreview(textarea);
    });
}

function addMarkdownToolbar(textarea) {
    const toolbar = document.createElement('div');
    toolbar.className = 'markdown-toolbar';
    toolbar.innerHTML = `
        <button type="button" class="md-btn" data-action="bold" title="Жирный (Ctrl+B)"><strong>B</strong></button>
        <button type="button" class="md-btn" data-action="italic" title="Курсив (Ctrl+I)"><em>I</em></button>
        <button type="button" class="md-btn" data-action="heading" title="Заголовок">H</button>
        <button type="button" class="md-btn" data-action="link" title="Ссылка (Ctrl+K)">🔗</button>
        <button type="button" class="md-btn" data-action="code" title="Код">&lt;/&gt;</button>
        <button type="button" class="md-btn" data-action="list" title="Список">☰</button>
        <button type="button" class="md-btn" data-action="quote" title="Цитата">"</button>
    `;
    
    // Вставляем toolbar перед textarea
    textarea.parentNode.insertBefore(toolbar, textarea);
    
    // Обработчики для кнопок
    toolbar.querySelectorAll('.md-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const action = this.dataset.action;
            applyMarkdownAction(textarea, action);
            
            if (window.soundManager?.isEnabled()) {
                window.soundManager.playClickSound();
            }
        });
    });
}

function applyMarkdownAction(textarea, action) {
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const text = textarea.value;
    const selectedText = text.substring(start, end);
    
    let replacement = '';
    let cursorOffset = 0;
    
    switch (action) {
        case 'bold':
            replacement = `**${selectedText || 'текст'}**`;
            cursorOffset = selectedText ? 0 : -2;
            break;
        case 'italic':
            replacement = `*${selectedText || 'текст'}*`;
            cursorOffset = selectedText ? 0 : -1;
            break;
        case 'heading':
            replacement = `## ${selectedText || 'Заголовок'}`;
            cursorOffset = selectedText ? 0 : -9;
            break;
        case 'link':
            replacement = `[${selectedText || 'текст ссылки'}](url)`;
            cursorOffset = selectedText ? -5 : -15;
            break;
        case 'code':
            if (selectedText.includes('\n')) {
                replacement = `\`\`\`\n${selectedText || 'код'}\n\`\`\``;
                cursorOffset = selectedText ? 0 : -4;
            } else {
                replacement = `\`${selectedText || 'код'}\``;
                cursorOffset = selectedText ? 0 : -1;
            }
            break;
        case 'list':
            replacement = selectedText
                ? selectedText.split('\n').map(line => `- ${line}`).join('\n')
                : '- Элемент списка';
            cursorOffset = 0;
            break;
        case 'quote':
            replacement = selectedText
                ? selectedText.split('\n').map(line => `> ${line}`).join('\n')
                : '> Цитата';
            cursorOffset = 0;
            break;
    }
    
    // Заменяем текст
    textarea.value = text.substring(0, start) + replacement + text.substring(end);
    
    // Устанавливаем курсор
    const newCursorPos = start + replacement.length + cursorOffset;
    textarea.selectionStart = textarea.selectionEnd = newCursorPos;
    textarea.focus();
}

function addMarkdownShortcuts(textarea) {
    textarea.addEventListener('keydown', function(e) {
        // Ctrl+B - жирный
        if (e.ctrlKey && e.key === 'b') {
            e.preventDefault();
            applyMarkdownAction(textarea, 'bold');
        }
        // Ctrl+I - курсив
        else if (e.ctrlKey && e.key === 'i') {
            e.preventDefault();
            applyMarkdownAction(textarea, 'italic');
        }
        // Ctrl+K - ссылка
        else if (e.ctrlKey && e.key === 'k') {
            e.preventDefault();
            applyMarkdownAction(textarea, 'link');
        }
        // Tab - вставить 4 пробела
        else if (e.key === 'Tab') {
            e.preventDefault();
            const start = this.selectionStart;
            const end = this.selectionEnd;
            this.value = this.value.substring(0, start) + '    ' + this.value.substring(end);
            this.selectionStart = this.selectionEnd = start + 4;
        }
    });
}

function addMarkdownPreview(textarea) {
    // Добавляем кнопку предпросмотра
    const previewBtn = document.createElement('button');
    previewBtn.type = 'button';
    previewBtn.className = 'btn btn-outline btn-sm markdown-preview-btn';
    previewBtn.textContent = '👁 Предпросмотр';
    previewBtn.style.marginTop = '0.5rem';
    
    textarea.parentNode.insertBefore(previewBtn, textarea.nextSibling);
    
    // Создаем контейнер для предпросмотра
    const previewContainer = document.createElement('div');
    previewContainer.className = 'markdown-preview';
    previewContainer.style.display = 'none';
    previewContainer.style.marginTop = '1rem';
    previewContainer.style.padding = '1rem';
    previewContainer.style.border = '1px solid var(--border-color)';
    previewContainer.style.borderRadius = 'var(--border-radius)';
    previewContainer.style.backgroundColor = 'var(--bg-secondary)';
    
    textarea.parentNode.insertBefore(previewContainer, previewBtn.nextSibling);
    
    let previewMode = false;
    
    previewBtn.addEventListener('click', function() {
        previewMode = !previewMode;
        
        if (previewMode) {
            textarea.style.display = 'none';
            previewContainer.style.display = 'block';
            previewContainer.innerHTML = '<em>Предпросмотр недоступен. Содержимое будет отображено после публикации.</em>';
            this.textContent = '✏️ Редактировать';
        } else {
            textarea.style.display = 'block';
            previewContainer.style.display = 'none';
            this.textContent = '👁 Предпросмотр';
        }
        
        if (window.soundManager?.isEnabled()) {
            window.soundManager.playClickSound();
        }
    });
}

// Добавляем стили для toolbar
const toolbarStyle = document.createElement('style');
toolbarStyle.textContent = `
    .markdown-toolbar {
        display: flex;
        gap: 0.5rem;
        margin-bottom: 0.5rem;
        flex-wrap: wrap;
    }
    
    .md-btn {
        padding: 0.5rem 0.75rem;
        background-color: var(--bg-secondary);
        color: var(--text-primary);
        border: 1px solid var(--border-color);
        border-radius: var(--border-radius);
        cursor: pointer;
        transition: all var(--transition-fast);
        font-size: 0.875rem;
    }
    
    .md-btn:hover {
        background-color: var(--primary-color);
        color: white;
        border-color: var(--primary-color);
    }
    
    .md-btn strong,
    .md-btn em {
        pointer-events: none;
    }
`;
document.head.appendChild(toolbarStyle);

