// ===== Лайки постов =====

document.addEventListener('DOMContentLoaded', function() {
    initLikes();
});

function initLikes() {
    const likeButtons = document.querySelectorAll('.like-btn');
    
    likeButtons.forEach(button => {
        button.addEventListener('click', async function(e) {
            e.preventDefault();
            
            const postId = this.dataset.postId;
            if (!postId) return;
            
            try {
                const response = await fetch(`/post/${postId}/like/`, {
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
                const likeCount = this.querySelector('.like-count');
                if (likeCount) {
                    likeCount.textContent = data.total_likes;
                }
                
                // Переключаем класс liked
                if (data.liked) {
                    this.classList.add('liked');
                    if (window.soundManager?.isEnabled()) {
                        window.soundManager.playSuccessSound();
                    }
                } else {
                    this.classList.remove('liked');
                }
                
            } catch (error) {
                console.error('Error:', error);
                window.showNotification('Ошибка при обработке лайка', 'error');
                if (window.soundManager?.isEnabled()) {
                    window.soundManager.playErrorSound();
                }
            }
        });
    });
}

// Утилита для получения CSRF токена
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

