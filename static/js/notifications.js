class NotificationCenter {
    constructor(container) {
        this.container = container;
        this.dropdown = container.querySelector('[data-notification-dropdown]');
        this.notificationList = container.querySelector('[data-notification-list]');
        this.countBadge = container.querySelector('[data-notification-count]');
        this.page = 1;
        this.loading = false;
        
        this.setupWebSocket();
        this.setupEventListeners();
    }

    setupWebSocket() {
        this.ws = new WebSocket(
            `${window.location.protocol === 'https:' ? 'wss:' : 'ws:'}//${window.location.host}/ws/notifications/`
        );

        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleNewNotification(data);
        };

        this.ws.onclose = () => {
            console.log('WebSocket connection closed');
            setTimeout(() => this.setupWebSocket(), 5000);
        };
    }

    setupEventListeners() {
        // Toggle du dropdown
        const toggleButton = this.container.querySelector('[data-notification-toggle]');
        if (toggleButton) {
            toggleButton.addEventListener('click', () => this.toggleDropdown());
        }

        // Marquer tout comme lu
        const markAllReadButton = this.container.querySelector('[data-mark-all-read]');
        if (markAllReadButton) {
            markAllReadButton.addEventListener('click', () => this.markAllAsRead());
        }

        // Charger plus de notifications
        const loadMoreButton = this.container.querySelector('[data-load-more]');
        if (loadMoreButton) {
            loadMoreButton.addEventListener('click', () => this.loadMore());
        }

        // Marquer une notification comme lue
        this.notificationList.addEventListener('click', (e) => {
            const markReadButton = e.target.closest('[data-mark-read]');
            if (markReadButton) {
                const notificationItem = markReadButton.closest('.notification-item');
                this.markAsRead(notificationItem.dataset.notificationId);
            }
        });

        // Fermer le dropdown en cliquant à l'extérieur
        document.addEventListener('click', (e) => {
            if (!this.container.contains(e.target)) {
                this.dropdown.classList.remove('show');
            }
        });

        // Défilement infini
        this.notificationList.addEventListener('scroll', () => {
            if (this.shouldLoadMore()) {
                this.loadMore();
            }
        });
    }

    toggleDropdown() {
        this.dropdown.classList.toggle('show');
    }

    async markAsRead(notificationId) {
        try {
            const response = await fetch(`/api/notifications/${notificationId}/read/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': this.getCsrfToken()
                }
            });

            if (response.ok) {
                const notificationItem = this.notificationList.querySelector(
                    `[data-notification-id="${notificationId}"]`
                );
                notificationItem.classList.remove('unread');
                notificationItem.querySelector('[data-mark-read]')?.remove();
                
                this.updateUnreadCount(-1);
            }
        } catch (error) {
            console.error('Erreur lors du marquage comme lu:', error);
        }
    }

    async markAllAsRead() {
        try {
            const response = await fetch('/api/notifications/mark-all-read/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': this.getCsrfToken()
                }
            });

            if (response.ok) {
                this.notificationList.querySelectorAll('.notification-item.unread').forEach(item => {
                    item.classList.remove('unread');
                    item.querySelector('[data-mark-read]')?.remove();
                });
                
                this.updateUnreadCount(0);
            }
        } catch (error) {
            console.error('Erreur lors du marquage comme lu:', error);
        }
    }

    async loadMore() {
        if (this.loading) return;
        
        this.loading = true;
        this.page += 1;

        try {
            const response = await fetch(`/api/notifications/?page=${this.page}`);
            const data = await response.json();
            
            this.appendNotifications(data.notifications);
            
            if (!data.has_more) {
                this.container.querySelector('[data-load-more]')?.remove();
            }
        } catch (error) {
            console.error('Erreur lors du chargement des notifications:', error);
        } finally {
            this.loading = false;
        }
    }

    handleNewNotification(data) {
        const notificationHtml = this.createNotificationHtml(data.notification);
        this.notificationList.insertAdjacentHTML('afterbegin', notificationHtml);
        
        this.updateUnreadCount(1);
        AlertSystem.show(data.notification.message, 'info');
    }

    createNotificationHtml(notification) {
        // Création du HTML pour une nouvelle notification
        return `
            <div class="notification-item unread" data-notification-id="${notification.id}">
                <!-- Structure de la notification similaire au template -->
            </div>
        `;
    }

    updateUnreadCount(change) {
        const currentCount = parseInt(this.countBadge.textContent);
        const newCount = change === 0 ? 0 : currentCount + change;
        this.countBadge.textContent = newCount;
        this.countBadge.style.display = newCount > 0 ? 'block' : 'none';
    }

    shouldLoadMore() {
        const { scrollTop, scrollHeight, clientHeight } = this.notificationList;
        return scrollHeight - scrollTop - clientHeight < 50;
    }

    getCsrfToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }
}

class AlertSystem {
    static container = null;
    static template = null;

    static init() {
        this.container = document.querySelector('[data-alert-container]');
        this.template = document.getElementById('alertTemplate');
    }

    static show(message, type = 'info', duration = 5000) {
        if (!this.container || !this.template) return;

        const alert = this.template.content.cloneNode(true).querySelector('.alert');
        alert.classList.add(`alert-${type}`);
        
        const icon = alert.querySelector('.alert-icon i');
        icon.classList.add(this.getIconClass(type));
        
        alert.querySelector('.alert-message').textContent = message;

        this.container.appendChild(alert);

        setTimeout(() => {
            alert.classList.add('fade-out');
            setTimeout(() => alert.remove(), 300);
        }, duration);
    }

    static getIconClass(type) {
        const icons = {
            success: 'fa-check-circle',
            danger: 'fa-exclamation-circle',
            warning: 'fa-exclamation-triangle',
            info: 'fa-info-circle'
        };
        return `fas ${icons[type] || icons.info}`;
    }
}

// Initialisation
document.addEventListener('DOMContentLoaded', function() {
    // Initialiser le centre de notifications
    document.querySelectorAll('[data-notification-center]').forEach(container => {
        new NotificationCenter(container);
    });

    // Initialiser le système d'alertes
    AlertSystem.init();
}); 