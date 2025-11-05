// ===== Подписки на авторов =====

document.addEventListener('DOMContentLoaded', function() {
    initSubscribe();
});

function initSubscribe() {
    const subscribeButtons = document.querySelectorAll('.subscribe-btn');
    
    subscribeButtons.forEach(button => {
        button.addEventListener('click', async function(e) {
            e.preventDefault();
            
            const username = this.dataset.username;
            if (!username) return;
            
            // Отключаем кнопку на время запроса
            this.disabled = true;
            
            try {
                const response = await fetch(`/user/${username}/subscribe/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                        'Content-Type': 'application/json',
                    },
                });
                
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                
                const data = await response.json();
                
                // Обновляем UI
                const subscribeText = this.querySelector('.subscribe-text');
                
                if (data.subscribed) {
                    this.classList.add('subscribed');
                    if (subscribeText) {
                        subscribeText.textContent = 'Отписаться';
                    }
                    window.showNotification('Вы подписались на автора', 'success');
                    if (window.soundManager?.isEnabled()) {
                        window.soundManager.playSuccessSound();
                    }
                } else {
                    this.classList.remove('subscribed');
                    if (subscribeText) {
                        subscribeText.textContent = 'Подписаться';
                    }
                    window.showNotification('Вы отписались от автора', 'info');
                }
                
                // Обновляем счетчик подписчиков если есть
                updateFollowersCount(data.followers_count);
                
            } catch (error) {
                console.error('Error:', error);
                window.showNotification('Ошибка при обработке подписки', 'error');
                if (window.soundManager?.isEnabled()) {
                    window.soundManager.playErrorSound();
                }
            } finally {
                this.disabled = false;
            }
        });
    });
}

function updateFollowersCount(count) {
    // Ищем элемент со счетчиком подписчиков
    const statsItems = document.querySelectorAll('.stat-item');
    statsItems.forEach(item => {
        const label = item.querySelector('.stat-label');
        if (label && label.textContent.includes('Подписчиков')) {
            const value = item.querySelector('.stat-value');
            if (value) {
                value.textContent = count;
                // Добавляем небольшую анимацию
                value.style.transform = 'scale(1.2)';
                setTimeout(() => {
                    value.style.transform = 'scale(1)';
                }, 200);
            }
        }
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

