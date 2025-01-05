class CommentManager {
    constructor(container) {
        this.container = container;
        this.commentList = container.querySelector('[data-comment-list]');
        this.commentForm = container.querySelector('[data-comment-form]');
        
        this.setupEventListeners();
    }

    setupEventListeners() {
        // Gestion du formulaire de commentaire
        if (this.commentForm) {
            this.commentForm.addEventListener('submit', (e) => this.handleCommentSubmit(e));
        }

        // Gestion des boutons de réponse
        this.container.querySelectorAll('[data-reply-toggle]').forEach(button => {
            button.addEventListener('click', (e) => this.toggleReplyForm(e));
        });

        // Gestion des boutons d'annulation de réponse
        this.container.querySelectorAll('[data-reply-cancel]').forEach(button => {
            button.addEventListener('click', (e) => this.hideReplyForm(e));
        });

        // Gestion de la suppression des commentaires
        this.container.querySelectorAll('[data-delete-comment]').forEach(button => {
            button.addEventListener('click', (e) => this.handleCommentDelete(e));
        });

        // Gestion de la suppression des réponses
        this.container.querySelectorAll('[data-delete-reply]').forEach(button => {
            button.addEventListener('click', (e) => this.handleReplyDelete(e));
        });
    }

    async handleCommentSubmit(e) {
        e.preventDefault();
        const form = e.target;
        const content = form.querySelector('textarea').value;

        try {
            const response = await fetch(form.action, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCsrfToken()
                },
                body: JSON.stringify({ content })
            });

            if (response.ok) {
                const comment = await response.json();
                this.addCommentToList(comment);
                form.reset();
                window.toastManager.show('Commentaire publié avec succès', 'success');
            } else {
                throw new Error('Erreur lors de la publication du commentaire');
            }
        } catch (error) {
            window.toastManager.show(error.message, 'error');
        }
    }

    toggleReplyForm(e) {
        const commentItem = e.target.closest('.comment-item');
        const replyForm = commentItem.querySelector('[data-reply-form]');
        
        // Cacher tous les autres formulaires de réponse
        this.container.querySelectorAll('[data-reply-form]').forEach(form => {
            if (form !== replyForm) {
                form.classList.add('d-none');
            }
        });

        replyForm.classList.toggle('d-none');
        replyForm.querySelector('textarea').focus();
    }

    hideReplyForm(e) {
        const replyForm = e.target.closest('[data-reply-form]');
        replyForm.classList.add('d-none');
        replyForm.querySelector('form').reset();
    }

    async handleCommentDelete(e) {
        const commentId = e.target.dataset.commentId;
        
        if (confirm('Êtes-vous sûr de vouloir supprimer ce commentaire ?')) {
            try {
                const response = await fetch(`/api/comments/${commentId}/`, {
                    method: 'DELETE',
                    headers: {
                        'X-CSRFToken': this.getCsrfToken()
                    }
                });

                if (response.ok) {
                    const commentItem = e.target.closest('.comment-item');
                    commentItem.remove();
                    window.toastManager.show('Commentaire supprimé avec succès', 'success');
                } else {
                    throw new Error('Erreur lors de la suppression du commentaire');
                }
            } catch (error) {
                window.toastManager.show(error.message, 'error');
            }
        }
    }

    async handleReplyDelete(e) {
        const replyId = e.target.dataset.replyId;
        
        if (confirm('Êtes-vous sûr de vouloir supprimer cette réponse ?')) {
            try {
                const response = await fetch(`/api/comments/replies/${replyId}/`, {
                    method: 'DELETE',
                    headers: {
                        'X-CSRFToken': this.getCsrfToken()
                    }
                });

                if (response.ok) {
                    const replyItem = e.target.closest('.reply-item');
                    replyItem.remove();
                    window.toastManager.show('Réponse supprimée avec succès', 'success');
                } else {
                    throw new Error('Erreur lors de la suppression de la réponse');
                }
            } catch (error) {
                window.toastManager.show(error.message, 'error');
            }
        }
    }

    addCommentToList(comment) {
        const commentHtml = this.createCommentHtml(comment);
        this.commentList.insertAdjacentHTML('afterbegin', commentHtml);
        
        // Réinitialiser les écouteurs d'événements pour le nouveau commentaire
        const newComment = this.commentList.firstElementChild;
        this.setupCommentEventListeners(newComment);
    }

    createCommentHtml(comment) {
        // Création du HTML pour un nouveau commentaire
        return `
            <div class="comment-item" data-comment-id="${comment.id}">
                <!-- Structure du commentaire similaire au template -->
            </div>
        `;
    }

    setupCommentEventListeners(commentElement) {
        // Réinitialiser les écouteurs d'événements pour un commentaire spécifique
        const replyButton = commentElement.querySelector('[data-reply-toggle]');
        if (replyButton) {
            replyButton.addEventListener('click', (e) => this.toggleReplyForm(e));
        }
        // ... autres écouteurs d'événements
    }

    getCsrfToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }
}

// Initialisation
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('[data-comment-container]').forEach(container => {
        new CommentManager(container);
    });
}); 