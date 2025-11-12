// ===== Управление темами =====

class ThemeManager {
    constructor() {
        this.currentTheme = this.getTheme();
        this.applyTheme(this.currentTheme);
        this.initThemeSelector();
    }
    
    getTheme() {
        // Получаем тему из data-theme атрибута
        const htmlElement = document.documentElement;
        const dataTheme = htmlElement.getAttribute('data-theme');
        
        if (dataTheme) {
            return dataTheme;
        }
        
        // Если нет, проверяем localStorage
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) {
            return savedTheme;
        }
        
        // По умолчанию - светлая тема
        return 'light';
    }
    
    applyTheme(theme) {
        const htmlElement = document.documentElement;
        htmlElement.setAttribute('data-theme', theme);
        this.currentTheme = theme;
        
        // Сохраняем в localStorage
        localStorage.setItem('theme', theme);
        
        // Применяем специальные эффекты для кибертемы
        if (theme === 'cyber') {
            this.enableCyberEffects();
        } else {
            this.disableCyberEffects();
        }
    }
    
    initThemeSelector() {
        // Находим селектор темы в настройках
        const themeSelect = document.querySelector('select[name="theme"]');
        
        if (themeSelect) {
            themeSelect.addEventListener('change', (e) => {
                this.applyTheme(e.target.value);
                
                // Проигрываем звук при смене темы
                if (window.soundManager?.isEnabled()) {
                    window.soundManager.playSuccessSound();
                }
                
                // Показываем уведомление
                window.showNotification('Тема изменена!', 'success');
            });
            
            // Устанавливаем текущее значение
            themeSelect.value = this.currentTheme;
        }
    }
    
    enableCyberEffects() {
        // Добавляем дополнительные эффекты для кибертемы
        this.addScanlines();
        this.addGlitchEffect();
    }
    
    disableCyberEffects() {
        // Удаляем эффекты кибертемы
        const scanlines = document.getElementById('cyber-scanlines');
        if (scanlines) {
            scanlines.remove();
        }
        
        const glitchStyle = document.getElementById('cyber-glitch-style');
        if (glitchStyle) {
            glitchStyle.remove();
        }
    }
    
    addScanlines() {
        // Добавляем эффект сканирующих линий
        if (document.getElementById('cyber-scanlines')) return;
        
        const scanlines = document.createElement('div');
        scanlines.id = 'cyber-scanlines';
        scanlines.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 9999;
            background: repeating-linear-gradient(
                0deg,
                rgba(0, 255, 255, 0.03),
                rgba(0, 255, 255, 0.03) 1px,
                transparent 1px,
                transparent 2px
            );
            opacity: 0.5;
        `;
        document.body.appendChild(scanlines);
    }
    
    addGlitchEffect() {
        // Добавляем случайный глитч эффект
        if (document.getElementById('cyber-glitch-style')) return;
        
        const style = document.createElement('style');
        style.id = 'cyber-glitch-style';
        style.textContent = `
            @keyframes textGlitch {
                0% {
                    text-shadow: 0.05em 0 0 rgba(255, 0, 0, 0.75),
                                -0.05em -0.025em 0 rgba(0, 255, 0, 0.75),
                                -0.025em 0.05em 0 rgba(0, 0, 255, 0.75);
                }
                14% {
                    text-shadow: 0.05em 0 0 rgba(255, 0, 0, 0.75),
                                -0.05em -0.025em 0 rgba(0, 255, 0, 0.75),
                                -0.025em 0.05em 0 rgba(0, 0, 255, 0.75);
                }
                15% {
                    text-shadow: -0.05em -0.025em 0 rgba(255, 0, 0, 0.75),
                                0.025em 0.025em 0 rgba(0, 255, 0, 0.75),
                                -0.05em -0.05em 0 rgba(0, 0, 255, 0.75);
                }
                49% {
                    text-shadow: -0.05em -0.025em 0 rgba(255, 0, 0, 0.75),
                                0.025em 0.025em 0 rgba(0, 255, 0, 0.75),
                                -0.05em -0.05em 0 rgba(0, 0, 255, 0.75);
                }
                50% {
                    text-shadow: 0.025em 0.05em 0 rgba(255, 0, 0, 0.75),
                                0.05em 0 0 rgba(0, 255, 0, 0.75),
                                0 -0.05em 0 rgba(0, 0, 255, 0.75);
                }
                99% {
                    text-shadow: 0.025em 0.05em 0 rgba(255, 0, 0, 0.75),
                                0.05em 0 0 rgba(0, 255, 0, 0.75),
                                0 -0.05em 0 rgba(0, 0, 255, 0.75);
                }
                100% {
                    text-shadow: -0.025em 0 0 rgba(255, 0, 0, 0.75),
                                -0.025em -0.025em 0 rgba(0, 255, 0, 0.75),
                                -0.025em -0.05em 0 rgba(0, 0, 255, 0.75);
                }
            }
            
            [data-theme="cyber"] h1,
            [data-theme="cyber"] h2 {
                animation: textGlitch 2s infinite;
            }
        `;
        document.head.appendChild(style);
        
        // Случайные глитчи экрана
        setInterval(() => {
            if (this.currentTheme === 'cyber' && Math.random() < 0.1) {
                document.body.style.animation = 'glitch 0.1s';
                setTimeout(() => {
                    document.body.style.animation = '';
                }, 100);
            }
        }, 3000);
    }
    
    toggle() {
        const themes = ['light', 'dark', 'cyber'];
        const currentIndex = themes.indexOf(this.currentTheme);
        const nextIndex = (currentIndex + 1) % themes.length;
        this.applyTheme(themes[nextIndex]);
    }
}

// Инициализация менеджера тем
const themeManager = new ThemeManager();

// Экспорт для глобального использования
window.themeManager = themeManager;

// Горячая клавиша для переключения темы (Ctrl+Shift+T)
document.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.shiftKey && e.key === 'T') {
        e.preventDefault();
        themeManager.toggle();
        window.showNotification('Тема изменена!', 'success');
    }
});

