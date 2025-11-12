// ===== Звуковые эффекты =====

class SoundManager {
    constructor() {
        this.enabled = window.userSettings?.soundEnabled !== false;
        this.audioContext = null;
        this.initAudioContext();
        this.bindEvents();
    }
    
    initAudioContext() {
        try {
            window.AudioContext = window.AudioContext || window.webkitAudioContext;
            this.audioContext = new AudioContext();
        } catch (e) {
            console.warn('Web Audio API not supported:', e);
        }
    }
    
    isEnabled() {
        return this.enabled;
    }
    
    setEnabled(enabled) {
        this.enabled = enabled;
    }
    
    bindEvents() {
        // Звук при наведении на кнопки
        document.addEventListener('mouseover', (e) => {
            if (!this.enabled) return;
            
            if (e.target.closest('.btn, .nav-link, .dropdown-item, .post-title a')) {
                this.playHoverSound();
            }
        });
        
        // Звук при клике на кнопки
        document.addEventListener('click', (e) => {
            if (!this.enabled) return;
            
            if (e.target.closest('.btn, .nav-link')) {
                this.playClickSound();
            }
        });
        
        // Звук при печати
        const inputs = document.querySelectorAll('input[type="text"], input[type="email"], textarea');
        inputs.forEach(input => {
            input.addEventListener('keypress', () => {
                if (this.enabled) {
                    this.playKeypressSound();
                }
            });
        });
    }
    
    // Генерация звуков с помощью Web Audio API
    playSound(frequency, duration, type = 'sine', volume = 0.1) {
        if (!this.audioContext || !this.enabled) return;
        
        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(this.audioContext.destination);
        
        oscillator.type = type;
        oscillator.frequency.value = frequency;
        gainNode.gain.value = volume;
        
        oscillator.start(this.audioContext.currentTime);
        oscillator.stop(this.audioContext.currentTime + duration);
    }
    
    playHoverSound() {
        this.playSound(600, 0.05, 'sine', 0.05);
    }
    
    playClickSound() {
        this.playSound(800, 0.1, 'sine', 0.1);
    }
    
    playKeypressSound() {
        const frequencies = [400, 450, 500, 550, 600];
        const randomFreq = frequencies[Math.floor(Math.random() * frequencies.length)];
        this.playSound(randomFreq, 0.05, 'sine', 0.03);
    }
    
    playSuccessSound() {
        this.playSound(800, 0.1, 'sine', 0.1);
        setTimeout(() => this.playSound(1000, 0.15, 'sine', 0.1), 100);
    }
    
    playErrorSound() {
        this.playSound(200, 0.2, 'sawtooth', 0.1);
    }
    
    playNotificationSound() {
        this.playSound(1000, 0.1, 'sine', 0.08);
        setTimeout(() => this.playSound(800, 0.1, 'sine', 0.08), 100);
    }
}

// Инициализация менеджера звуков
const soundManager = new SoundManager();

// Экспорт для глобального использования
window.soundManager = soundManager;

// Слушаем изменения настроек звука
document.addEventListener('DOMContentLoaded', function() {
    // Если есть checkbox настройки звуков
    const soundToggle = document.querySelector('input[name="sound_enabled"]');
    if (soundToggle) {
        soundToggle.addEventListener('change', function() {
            soundManager.setEnabled(this.checked);
            if (this.checked) {
                soundManager.playSuccessSound();
            }
        });
    }
});

// Дополнительные звуковые эффекты для кибертемы
document.addEventListener('DOMContentLoaded', function() {
    const theme = document.documentElement.getAttribute('data-theme');
    
    if (theme === 'cyber' && soundManager.isEnabled()) {
        // Добавляем "глитч" звуки для кибертемы
        setInterval(() => {
            if (Math.random() < 0.05 && soundManager.isEnabled()) {
                const glitchFreq = Math.random() * 1000 + 500;
                soundManager.playSound(glitchFreq, 0.02, 'square', 0.02);
            }
        }, 1000);
    }
});

