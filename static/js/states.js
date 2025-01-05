class StateManager {
    constructor(container) {
        this.container = container;
        this.emptyState = container.querySelector('.empty-state');
        this.errorState = container.querySelector('.error-state');
        this.loadingState = container.querySelector('.loading-state');
        this.contentContainer = container.querySelector('.content-container');
        
        this.setupRetryButton();
    }

    showLoading(message = null) {
        this.hideAll();
        this.loadingState.classList.remove('d-none');
        if (message) {
            this.loadingState.querySelector('.loading-text').textContent = message;
        }
    }

    showError(title = null, description = null) {
        this.hideAll();
        this.errorState.classList.remove('d-none');
        if (title) {
            this.errorState.querySelector('.error-state-title').textContent = title;
        }
        if (description) {
            this.errorState.querySelector('.error-state-description').textContent = description;
        }
    }

    showEmpty(title = null, description = null) {
        this.hideAll();
        this.emptyState.classList.remove('d-none');
        if (title) {
            this.emptyState.querySelector('.empty-state-title').textContent = title;
        }
        if (description) {
            this.emptyState.querySelector('.empty-state-description').textContent = description;
        }
    }

    showContent() {
        this.hideAll();
        if (this.contentContainer) {
            this.contentContainer.classList.remove('d-none');
        }
    }

    hideAll() {
        [this.emptyState, this.errorState, this.loadingState, this.contentContainer]
            .filter(el => el)
            .forEach(el => el.classList.add('d-none'));
    }

    setupRetryButton() {
        const retryButton = this.errorState.querySelector('.retry-button');
        if (retryButton && this.onRetry) {
            retryButton.addEventListener('click', () => this.onRetry());
        }
    }

    setRetryCallback(callback) {
        this.onRetry = callback;
        this.setupRetryButton();
    }
}

// Gestionnaire de notifications toast
class ToastManager {
    constructor() {
        this.container = document.querySelector('.toast-container');
        if (!this.container) {
            this.createContainer();
        }
    }

    createContainer() {
        this.container = document.createElement('div');
        this.container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        document.body.appendChild(this.container);
    }

    show(message, type = 'info', duration = 5000) {
        const toast = this.createToast(message, type);
        this.container.appendChild(toast);
        
        const bsToast = new bootstrap.Toast(toast, {
            delay: duration
        });
        
        bsToast.show();

        toast.addEventListener('hidden.bs.toast', () => {
            toast.remove();
        });
    }

    createToast(message, type) {
        const toast = document.createElement('div');
        toast.className = 'toast';
        toast.setAttribute('role', 'alert');
        toast.setAttribute('aria-live', 'assertive');
        toast.setAttribute('aria-atomic', 'true');

        toast.innerHTML = `
            <div class="toast-header bg-${type} text-white">
                <i class="fas fa-info-circle me-2"></i>
                <strong class="me-auto">${this.getTypeTitle(type)}</strong>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        `;

        return toast;
    }

    getTypeTitle(type) {
        const titles = {
            success: 'Succès',
            error: 'Erreur',
            warning: 'Attention',
            info: 'Information'
        };
        return titles[type] || 'Information';
    }
}

// Initialisation
document.addEventListener('DOMContentLoaded', function() {
    // Initialiser les gestionnaires d'état pour chaque conteneur
    document.querySelectorAll('[data-state-container]').forEach(container => {
        const stateManager = new StateManager(container);
        container.stateManager = stateManager;
    });

    // Initialiser le gestionnaire de notifications
    window.toastManager = new ToastManager();
}); 