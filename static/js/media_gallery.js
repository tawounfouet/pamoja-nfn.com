document.addEventListener('DOMContentLoaded', function() {
    // Gestion du modal média
    const mediaModal = document.getElementById('mediaModal');
    if (mediaModal) {
        mediaModal.addEventListener('show.bs.modal', function(event) {
            const button = event.relatedTarget;
            const mediaUrl = button.getAttribute('data-media-url');
            const mediaType = button.getAttribute('data-media-type');
            const mediaTitle = button.getAttribute('data-media-title');
            const mediaDescription = button.getAttribute('data-media-description');

            const modalTitle = this.querySelector('.modal-title');
            const mediaContainer = this.querySelector('.media-container');
            const descriptionElement = this.querySelector('.media-description');

            modalTitle.textContent = mediaTitle;
            mediaContainer.innerHTML = '';

            if (mediaType === 'video') {
                const video = document.createElement('video');
                video.src = mediaUrl;
                video.controls = true;
                mediaContainer.appendChild(video);
            } else {
                const img = document.createElement('img');
                img.src = mediaUrl;
                img.alt = mediaTitle;
                mediaContainer.appendChild(img);
            }

            if (mediaDescription) {
                descriptionElement.textContent = mediaDescription;
                descriptionElement.style.display = 'block';
            } else {
                descriptionElement.style.display = 'none';
            }
        });
    }

    // Gestion de la suppression des médias
    document.querySelectorAll('.delete-media').forEach(button => {
        button.addEventListener('click', async function(e) {
            e.preventDefault();
            const mediaId = this.getAttribute('data-media-id');
            
            if (confirm('Êtes-vous sûr de vouloir supprimer ce média ?')) {
                try {
                    const response = await fetch(`/api/media/${mediaId}/`, {
                        method: 'DELETE',
                        headers: {
                            'X-CSRFToken': getCookie('csrftoken')
                        }
                    });

                    if (response.ok) {
                        const galleryItem = this.closest('.gallery-item');
                        galleryItem.remove();
                    }
                } catch (error) {
                    console.error('Erreur lors de la suppression du média:', error);
                }
            }
        });
    });

    // Gestion de l'image principale
    document.querySelectorAll('.set-primary').forEach(button => {
        button.addEventListener('click', async function(e) {
            e.preventDefault();
            const mediaId = this.getAttribute('data-media-id');
            
            try {
                const response = await fetch(`/api/media/${mediaId}/set-primary/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken')
                    }
                });

                if (response.ok) {
                    // Réinitialiser tous les boutons
                    document.querySelectorAll('.set-primary').forEach(btn => {
                        btn.disabled = false;
                    });
                    // Désactiver le bouton cliqué
                    this.disabled = true;
                }
            } catch (error) {
                console.error('Erreur lors de la définition de l\'image principale:', error);
            }
        });
    });
}); 