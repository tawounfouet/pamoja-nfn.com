class DynamicForm {
    constructor(container) {
        this.container = container;
        this.form = container.querySelector('form');
        this.steps = container.querySelectorAll('[data-step]');
        this.progressSteps = container.querySelectorAll('.progress-step');
        this.currentStep = 1;
        
        this.setupEventListeners();
        this.setupValidation();
    }

    setupEventListeners() {
        // Navigation entre les étapes
        this.container.querySelectorAll('.next-step').forEach(button => {
            button.addEventListener('click', () => this.validateAndNext());
        });

        this.container.querySelectorAll('.prev-step').forEach(button => {
            button.addEventListener('click', () => this.previousStep());
        });

        // Gestion des uploads de fichiers
        this.container.querySelectorAll('input[type="file"]').forEach(input => {
            input.addEventListener('change', (e) => this.handleFileUpload(e));
        });

        // Soumission du formulaire
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
    }

    setupValidation() {
        // Validation en temps réel des champs
        this.form.querySelectorAll('.form-control').forEach(input => {
            ['input', 'blur'].forEach(eventType => {
                input.addEventListener(eventType, () => {
                    this.validateField(input);
                });
            });
        });
    }

    validateField(input) {
        const fieldGroup = input.closest('[data-field-group]');
        const feedback = fieldGroup.querySelector('.invalid-feedback');
        let isValid = true;
        let errorMessage = '';

        // Validation personnalisée selon le type de champ
        switch (input.type) {
            case 'email':
                isValid = this.validateEmail(input.value);
                errorMessage = 'Veuillez entrer une adresse email valide';
                break;
            case 'tel':
                isValid = this.validatePhone(input.value);
                errorMessage = 'Veuillez entrer un numéro de téléphone valide';
                break;
            case 'password':
                isValid = this.validatePassword(input.value);
                errorMessage = 'Le mot de passe doit contenir au moins 8 caractères';
                break;
            default:
                isValid = input.value.trim() !== '';
                errorMessage = 'Ce champ est requis';
        }

        // Mise à jour de l'état de validation
        input.classList.toggle('is-invalid', !isValid);
        if (feedback) {
            feedback.textContent = !isValid ? errorMessage : '';
        }

        return isValid;
    }

    validateStep(step) {
        const fields = step.querySelectorAll('.form-control');
        let isValid = true;

        fields.forEach(field => {
            if (!this.validateField(field)) {
                isValid = false;
            }
        });

        return isValid;
    }

    validateAndNext() {
        const currentStepElement = this.container.querySelector(`.form-step[data-step="${this.currentStep}"]`);
        
        if (this.validateStep(currentStepElement)) {
            this.nextStep();
        }
    }

    nextStep() {
        if (this.currentStep < this.steps.length) {
            this.updateStep(this.currentStep + 1);
        }
    }

    previousStep() {
        if (this.currentStep > 1) {
            this.updateStep(this.currentStep - 1);
        }
    }

    updateStep(step) {
        // Mettre à jour les classes actives
        this.steps.forEach(s => {
            s.classList.toggle('active', parseInt(s.dataset.step) === step);
        });

        this.progressSteps.forEach(s => {
            const stepNum = parseInt(s.dataset.step);
            s.classList.toggle('active', stepNum === step);
            s.classList.toggle('completed', stepNum < step);
        });

        this.currentStep = step;
    }

    handleFileUpload(e) {
        const input = e.target;
        const preview = input.closest('.file-upload-wrapper').querySelector('.preview-image');
        
        if (input.files && input.files[0]) {
            const reader = new FileReader();
            
            reader.onload = function(e) {
                preview.src = e.target.result;
                preview.classList.remove('d-none');
            }
            
            reader.readAsDataURL(input.files[0]);
        }
    }

    async handleSubmit(e) {
        e.preventDefault();

        if (!this.validateStep(this.container.querySelector(`.form-step[data-step="${this.currentStep}"]`))) {
            return;
        }

        const formData = new FormData(this.form);

        try {
            const response = await fetch(this.form.action, {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const data = await response.json();
                window.toastManager.show('Formulaire envoyé avec succès', 'success');
                
                if (data.redirect_url) {
                    window.location.href = data.redirect_url;
                }
            } else {
                const errors = await response.json();
                this.handleErrors(errors);
            }
        } catch (error) {
            window.toastManager.show('Une erreur est survenue', 'error');
        }
    }

    handleErrors(errors) {
        // Afficher les erreurs de validation
        Object.entries(errors).forEach(([field, messages]) => {
            const fieldGroup = this.container.querySelector(`[data-field-group="${field}"]`);
            if (fieldGroup) {
                const input = fieldGroup.querySelector('.form-control');
                const feedback = fieldGroup.querySelector('.invalid-feedback');
                
                input.classList.add('is-invalid');
                feedback.textContent = messages[0];
                
                // Revenir à l'étape contenant le champ en erreur
                const step = parseInt(fieldGroup.closest('.form-step').dataset.step);
                this.updateStep(step);
            }
        });
    }

    validateEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    validatePhone(phone) {
        return /^(\+\d{1,3}[- ]?)?\d{10}$/.test(phone);
    }

    validatePassword(password) {
        return password.length >= 8;
    }
}

// Initialisation
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('[data-dynamic-form]').forEach(container => {
        new DynamicForm(container);
    });
}); 