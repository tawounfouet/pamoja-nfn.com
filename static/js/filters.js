document.addEventListener('DOMContentLoaded', function() {
    const filterForm = document.getElementById('filterForm');
    const clearFiltersBtn = document.querySelector('.clear-filters');

    // Mise à jour automatique lors du changement de filtre
    filterForm.querySelectorAll('input, select').forEach(input => {
        input.addEventListener('change', function() {
            if (this.type !== 'text') {  // Ne pas soumettre sur changement de texte
                filterForm.submit();
            }
        });
    });

    // Réinitialisation des filtres
    if (clearFiltersBtn) {
        clearFiltersBtn.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Réinitialiser tous les champs
            filterForm.querySelectorAll('input, select').forEach(input => {
                if (input.type === 'checkbox' || input.type === 'radio') {
                    input.checked = false;
                } else {
                    input.value = '';
                }
            });

            // Soumettre le formulaire
            filterForm.submit();
        });
    }

    // Gestion de la recherche avec debounce
    const searchInput = filterForm.querySelector('input[name="q"]');
    if (searchInput) {
        let timeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(timeout);
            timeout = setTimeout(() => {
                filterForm.submit();
            }, 500);  // Attendre 500ms après la dernière frappe
        });
    }

    // Mise à jour de l'URL sans rechargement
    filterForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        const searchParams = new URLSearchParams(formData);
        
        // Mettre à jour l'URL
        const newUrl = `${window.location.pathname}?${searchParams.toString()}`;
        window.history.pushState({}, '', newUrl);

        // Charger les résultats via AJAX
        fetchFilteredResults(searchParams);
    });
});

async function fetchFilteredResults(searchParams) {
    try {
        const response = await fetch(`/api/listings/filter/?${searchParams.toString()}`);
        const data = await response.json();
        
        // Mettre à jour la liste des résultats
        const resultsContainer = document.querySelector('.results-container');
        resultsContainer.innerHTML = data.html;
        
        // Mettre à jour le compteur de résultats
        const resultsCount = document.querySelector('.results-count');
        if (resultsCount) {
            resultsCount.textContent = `${data.total} résultat${data.total > 1 ? 's' : ''}`;
        }
    } catch (error) {
        console.error('Erreur lors du filtrage:', error);
    }
} 