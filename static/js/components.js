// Gestion des modales de confirmation
document.addEventListener('DOMContentLoaded', function() {
    const confirmationModal = document.getElementById('confirmationModal');
    if (confirmationModal) {
        const modal = new bootstrap.Modal(confirmationModal);
        
        document.querySelectorAll('[data-confirm]').forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                const message = this.getAttribute('data-confirm-message');
                const title = this.getAttribute('data-confirm-title');
                const action = this.getAttribute('href') || this.getAttribute('data-action');
                
                const modalTitle = confirmationModal.querySelector('.modal-title');
                const modalBody = confirmationModal.querySelector('.modal-body');
                const modalForm = confirmationModal.querySelector('form');
                
                if (title) modalTitle.textContent = title;
                if (message) modalBody.textContent = message;
                if (action) modalForm.action = action;
                
                modal.show();
            });
        });
    }
});

// Gestion des favoris
document.querySelectorAll('.toggle-favorite').forEach(button => {
    button.addEventListener('click', async function(e) {
        e.preventDefault();
        const listingId = this.getAttribute('data-listing-id');
        const icon = this.querySelector('i');
        
        try {
            const response = await fetch('/api/favorites/toggle/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ listing_id: listingId })
            });
            
            const data = await response.json();
            
            if (data.is_favorite) {
                icon.classList.replace('far', 'fas');
            } else {
                icon.classList.replace('fas', 'far');
            }
        } catch (error) {
            console.error('Erreur lors de la mise à jour des favoris:', error);
        }
    });
});

// Gestion des notifications
document.querySelectorAll('.mark-read-btn').forEach(button => {
    button.addEventListener('click', async function(e) {
        e.preventDefault();
        const notificationId = this.closest('form').action.split('/').pop();
        
        try {
            const response = await fetch(`/api/notifications/${notificationId}/mark-read/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            });
            
            if (response.ok) {
                const notificationItem = this.closest('.notification-item');
                notificationItem.classList.remove('unread');
                this.remove();
                
                // Mise à jour du compteur de notifications
                const badge = document.querySelector('.notification-badge');
                if (badge) {
                    const count = parseInt(badge.textContent) - 1;
                    if (count <= 0) {
                        badge.remove();
                    } else {
                        badge.textContent = count;
                    }
                }
            }
        } catch (error) {
            console.error('Erreur lors du marquage de la notification:', error);
        }
    });
});

// Fonction utilitaire pour récupérer les cookies
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