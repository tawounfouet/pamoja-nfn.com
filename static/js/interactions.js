class FavoriteManager {
    constructor() {
        this.setupEventListeners();
    }

    setupEventListeners() {
        document.querySelectorAll('[data-favorite-toggle]').forEach(button => {
            button.addEventListener('click', (e) => this.handleFavoriteToggle(e));
        });
    }

    async handleFavoriteToggle(e) {
        const button = e.currentTarget;
        
        // Si l'utilisateur n'est pas connecté, le modal de connexion s'affichera automatiquement
        if (!button.hasAttribute('data-bs-toggle')) {
            const itemId = button.dataset.itemId;
            const itemType = button.dataset.itemType;

            try {
                const response = await fetch('/api/favorites/toggle/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': this.getCsrfToken()
                    },
                    body: JSON.stringify({
                        item_id: itemId,
                        item_type: itemType
                    })
                });

                if (response.ok) {
                    const data = await response.json();
                    this.updateFavoriteButton(button, data);
                } else {
                    throw new Error('Erreur lors de la mise à jour des favoris');
                }
            } catch (error) {
                window.toastManager.show(error.message, 'error');
            }
        }
    }

    updateFavoriteButton(button, data) {
        const icon = button.querySelector('i');
        const count = button.querySelector('.favorite-count');
        const tooltip = button.querySelector('.favorite-tooltip');

        if (data.is_favorite) {
            button.classList.add('active');
            icon.classList.replace('far', 'fas');
            tooltip.textContent = 'Retirer des favoris';
        } else {
            button.classList.remove('active');
            icon.classList.replace('fas', 'far');
            tooltip.textContent = 'Ajouter aux favoris';
        }

        count.textContent = data.favorite_count;
    }

    getCsrfToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }
}

class RatingWidget {
    constructor(container) {
        this.container = container;
        this.stars = container.querySelectorAll('.star');
        this.form = container.querySelector('[data-rating-form]');
        this.ratingInput = container.querySelector('[data-rating-value]');
        
        this.setupEventListeners();
    }

    setupEventListeners() {
        this.stars.forEach(star => {
            star.addEventListener('click', (e) => this.handleStarClick(e));
        });

        if (this.form) {
            this.form.addEventListener('submit', (e) => this.handleRatingSubmit(e));
        }
    }

    handleStarClick(e) {
        const star = e.currentTarget;
        const rating = star.dataset.rating;

        this.stars.forEach(s => {
            s.classList.toggle('active', s.dataset.rating <= rating);
        });

        if (this.ratingInput) {
            this.ratingInput.value = rating;
        }

        // Si pas de formulaire, soumettre directement
        if (!this.form) {
            this.submitRating(rating);
        }
    }

    async handleRatingSubmit(e) {
        e.preventDefault();
        const formData = new FormData(this.form);
        
        try {
            const response = await fetch(this.form.action, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': this.getCsrfToken()
                },
                body: formData
            });

            if (response.ok) {
                const data = await response.json();
                this.updateAverageRating(data);
                window.toastManager.show('Merci pour votre évaluation !', 'success');
            } else {
                throw new Error('Erreur lors de l\'envoi de l\'évaluation');
            }
        } catch (error) {
            window.toastManager.show(error.message, 'error');
        }
    }

    async submitRating(rating) {
        try {
            const response = await fetch(this.container.dataset.ratingUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCsrfToken()
                },
                body: JSON.stringify({ rating })
            });

            if (response.ok) {
                const data = await response.json();
                this.updateAverageRating(data);
                window.toastManager.show('Merci pour votre évaluation !', 'success');
            } else {
                throw new Error('Erreur lors de l\'envoi de l\'évaluation');
            }
        } catch (error) {
            window.toastManager.show(error.message, 'error');
        }
    }

    updateAverageRating(data) {
        const averageElement = this.container.querySelector('.average-value');
        const countElement = this.container.querySelector('.rating-count');
        
        if (averageElement) {
            averageElement.textContent = parseFloat(data.average_rating).toFixed(1);
        }
        if (countElement) {
            countElement.textContent = `(${data.rating_count} avis)`;
        }
    }

    getCsrfToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }
}

// Initialisation
document.addEventListener('DOMContentLoaded', function() {
    // Initialiser le gestionnaire de favoris
    new FavoriteManager();

    // Initialiser les widgets de notation
    document.querySelectorAll('[data-rating-widget]').forEach(container => {
        new RatingWidget(container);
    });
}); 