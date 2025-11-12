// ===== Основная функциональность =====

document.addEventListener('DOMContentLoaded', function() {
    // Мобильное меню
    initMobileMenu();
    
    // Dropdown меню
    initDropdowns();
    
    // Автоматическое закрытие сообщений
    initAlerts();
    
    // Markdown модальное окно
    initMarkdownGuide();
});

// Мобильное меню
function initMobileMenu() {
    const mobileMenuToggle = document.getElementById('mobileMenuToggle');
    const navbarMenu = document.getElementById('navbarMenu');
    
    if (mobileMenuToggle && navbarMenu) {
        mobileMenuToggle.addEventListener('click', function() {
            navbarMenu.classList.toggle('active');
            this.classList.toggle('active');
        });
    }
}

// Dropdown меню для аккаунта
function initDropdowns() {
    const accountBtn = document.getElementById('accountBtn');
    const accountDropdown = document.getElementById('accountDropdown');
    
    if (accountBtn && accountDropdown) {
        // Клик по кнопке
        accountBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            accountDropdown.classList.toggle('show');
        });
        
        // Закрытие при клике вне меню
        document.addEventListener('click', function(e) {
            if (!accountBtn.contains(e.target) && !accountDropdown.contains(e.target)) {
                accountDropdown.classList.remove('show');
            }
        });
    }
}

// Автозакрытие уведомлений
function initAlerts() {
    const alerts = document.querySelectorAll('.alert');
    
    alerts.forEach(alert => {
        // Кнопка закрытия
        const closeBtn = alert.querySelector('.alert-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', function() {
                alert.style.animation = 'slideOut 0.3s ease';
                setTimeout(() => alert.remove(), 300);
            });
        }
        
        // Автозакрытие через 5 секунд
        setTimeout(() => {
            if (alert.parentElement) {
                alert.style.animation = 'slideOut 0.3s ease';
                setTimeout(() => alert.remove(), 300);
            }
        }, 5000);
    });
}

// Анимация для закрытия сообщений
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Markdown guide модальное окно
function initMarkdownGuide() {
    const markdownGuideBtn = document.getElementById('markdownGuideBtn');
    const markdownGuideModal = document.getElementById('markdownGuideModal');
    
    if (markdownGuideBtn && markdownGuideModal) {
        markdownGuideBtn.addEventListener('click', function(e) {
            e.preventDefault();
            markdownGuideModal.classList.add('active');
        });
        
        // Закрытие модального окна
        const closeBtn = markdownGuideModal.querySelector('.modal-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', function() {
                markdownGuideModal.classList.remove('active');
            });
        }
        
        // Закрытие при клике на фон
        markdownGuideModal.addEventListener('click', function(e) {
            if (e.target === markdownGuideModal) {
                markdownGuideModal.classList.remove('active');
            }
        });
        
        // Закрытие по Escape
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && markdownGuideModal.classList.contains('active')) {
                markdownGuideModal.classList.remove('active');
            }
        });
    }
}

// Утилита для AJAX запросов
async function fetchAPI(url, options = {}) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
    
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken || '',
        },
    };
    
    const response = await fetch(url, { ...defaultOptions, ...options });
    
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
}

// Показать уведомление
function showNotification(message, type = 'info') {
    const messagesContainer = document.querySelector('.messages-container') || createMessagesContainer();
    
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.innerHTML = `
        ${message}
        <button class="alert-close">&times;</button>
    `;
    
    messagesContainer.appendChild(alert);
    
    // Инициализируем закрытие для нового уведомления
    const closeBtn = alert.querySelector('.alert-close');
    closeBtn.addEventListener('click', () => {
        alert.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => alert.remove(), 300);
    });
    
    // Автозакрытие
    setTimeout(() => {
        if (alert.parentElement) {
            alert.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => alert.remove(), 300);
        }
    }, 5000);
}

function createMessagesContainer() {
    const container = document.createElement('div');
    container.className = 'messages-container';
    document.body.appendChild(container);
    return container;
}

// Экспорт функций
window.fetchAPI = fetchAPI;
window.showNotification = showNotification;

