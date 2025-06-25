// Contact page specific JavaScript

class ContactManager {
    constructor() {
        this.form = null;
        this.submitButton = null;
        this.isSubmitting = false;
        this.init();
    }

    init() {
        this.setupForm();
        this.setupFAQ();
        this.addContactStyles();
        this.setupInteractiveElements();
        this.setupFormValidation();
        this.setupAccessibilityFeatures();
    }

    setupForm() {
        this.form = document.getElementById('contact-form-element');
        this.submitButton = document.getElementById('submit-btn');
        
        if (!this.form || !this.submitButton) return;

        this.form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleFormSubmit();
        });

        // Real-time validation
        const inputs = this.form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('blur', () => this.validateField(input));
            input.addEventListener('input', () => {
                if (input.classList.contains('error')) {
                    this.validateField(input);
                }
            });
        });
    }

    setupFAQ() {
        const faqItems = document.querySelectorAll('.faq-item');
        
        faqItems.forEach(item => {
            const question = item.querySelector('.faq-question');
            const answer = item.querySelector('.faq-answer');
            const icon = item.querySelector('.faq-icon');
            
            if (!question || !answer || !icon) return;

            question.addEventListener('click', () => {
                const isExpanded = item.classList.contains('expanded');
                
                // Close other FAQ items
                faqItems.forEach(otherItem => {
                    if (otherItem !== item) {
                        otherItem.classList.remove('expanded');
                        const otherIcon = otherItem.querySelector('.faq-icon');
                        if (otherIcon) otherIcon.textContent = '+';
                    }
                });
                
                // Toggle current item
                if (isExpanded) {
                    item.classList.remove('expanded');
                    icon.textContent = '+';
                } else {
                    item.classList.add('expanded');
                    icon.textContent = '−';
                }
            });

            // Keyboard accessibility
            question.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    question.click();
                }
            });

            // Make focusable
            question.setAttribute('tabindex', '0');
            question.setAttribute('role', 'button');
            question.setAttribute('aria-expanded', 'false');
        });
    }

    setupFormValidation() {
        if (!this.form) return;

        const validators = {
            name: (value) => {
                if (!value.trim()) return 'お名前を入力してください';
                if (value.trim().length < 2) return 'お名前は2文字以上で入力してください';
                return null;
            },
            email: (value) => {
                if (!value.trim()) return 'メールアドレスを入力してください';
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!emailRegex.test(value)) return '有効なメールアドレスを入力してください';
                return null;
            },
            subject: (value) => {
                if (!value) return '件名を選択してください';
                return null;
            },
            message: (value) => {
                if (!value.trim()) return 'メッセージを入力してください';
                if (value.trim().length < 10) return 'メッセージは10文字以上で入力してください';
                return null;
            },
            privacy: (checked) => {
                if (!checked) return 'プライバシーポリシーに同意してください';
                return null;
            }
        };

        this.validators = validators;
    }

    validateField(field) {
        const fieldName = field.name;
        const fieldValue = field.type === 'checkbox' ? field.checked : field.value;
        const errorElement = document.getElementById(`${fieldName}-error`);
        
        if (!this.validators[fieldName] || !errorElement) return true;

        const error = this.validators[fieldName](fieldValue);
        
        if (error) {
            field.classList.add('error');
            errorElement.textContent = error;
            errorElement.style.display = 'block';
            return false;
        } else {
            field.classList.remove('error');
            errorElement.textContent = '';
            errorElement.style.display = 'none';
            return true;
        }
    }

    validateForm() {
        const formData = new FormData(this.form);
        let isValid = true;
        
        // Validate all fields
        ['name', 'email', 'subject', 'message'].forEach(fieldName => {
            const field = this.form.querySelector(`[name="${fieldName}"]`);
            if (field && !this.validateField(field)) {
                isValid = false;
            }
        });

        // Validate privacy checkbox
        const privacyField = this.form.querySelector('[name="privacy"]');
        if (privacyField && !this.validateField(privacyField)) {
            isValid = false;
        }

        return isValid;
    }

    async handleFormSubmit() {
        if (this.isSubmitting) return;

        if (!this.validateForm()) {
            this.showFormError('入力内容に誤りがあります。確認してください。');
            return;
        }

        this.isSubmitting = true;
        this.setSubmitButtonLoading(true);

        try {
            // Simulate form submission (replace with actual submission logic)
            await this.simulateFormSubmission();
            this.showFormSuccess();
        } catch (error) {
            this.showFormError('送信に失敗しました。しばらく時間をおいて再度お試しください。');
        } finally {
            this.isSubmitting = false;
            this.setSubmitButtonLoading(false);
        }
    }

    async simulateFormSubmission() {
        // Simulate network delay
        return new Promise((resolve) => {
            setTimeout(resolve, 2000);
        });
    }

    setSubmitButtonLoading(loading) {
        const btnText = this.submitButton.querySelector('.btn-text');
        const btnLoader = this.submitButton.querySelector('.btn-loader');
        const btnIcon = this.submitButton.querySelector('.btn-icon');

        if (loading) {
            btnText.style.display = 'none';
            btnIcon.style.display = 'none';
            btnLoader.style.display = 'flex';
            this.submitButton.disabled = true;
        } else {
            btnText.style.display = 'inline';
            btnIcon.style.display = 'inline';
            btnLoader.style.display = 'none';
            this.submitButton.disabled = false;
        }
    }

    showFormSuccess() {
        const formContainer = document.querySelector('.contact-form-container');
        const successElement = document.getElementById('form-success');
        
        if (formContainer && successElement) {
            this.form.style.display = 'none';
            successElement.style.display = 'block';
            
            // Scroll to success message
            successElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
            
            // Reset form after a delay
            setTimeout(() => {
                this.resetForm();
            }, 5000);
        }
    }

    showFormError(message) {
        // Create or update error message
        let errorElement = document.querySelector('.form-general-error');
        
        if (!errorElement) {
            errorElement = document.createElement('div');
            errorElement.className = 'form-general-error';
            this.form.insertBefore(errorElement, this.form.firstChild);
        }
        
        errorElement.textContent = message;
        errorElement.style.display = 'block';
        
        // Scroll to error
        errorElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
        
        // Hide error after 5 seconds
        setTimeout(() => {
            errorElement.style.display = 'none';
        }, 5000);
    }

    resetForm() {
        if (!this.form) return;
        
        this.form.reset();
        this.form.style.display = 'block';
        
        const successElement = document.getElementById('form-success');
        if (successElement) {
            successElement.style.display = 'none';
        }
        
        // Clear all errors
        const errorElements = this.form.querySelectorAll('.form-error');
        errorElements.forEach(el => {
            el.textContent = '';
            el.style.display = 'none';
        });
        
        const inputs = this.form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => input.classList.remove('error'));
    }

    setupInteractiveElements() {
        // Method cards hover effects
        const methodCards = document.querySelectorAll('.method-card');
        methodCards.forEach(card => {
            card.addEventListener('mouseenter', () => {
                const icon = card.querySelector('.method-icon .icon-bg');
                if (icon) {
                    icon.style.transform = 'scale(1.1) rotate(5deg)';
                }
            });
            
            card.addEventListener('mouseleave', () => {
                const icon = card.querySelector('.method-icon .icon-bg');
                if (icon) {
                    icon.style.transform = '';
                }
            });
        });

        // Availability status animation
        const statusIndicator = document.querySelector('.status-indicator.available');
        if (statusIndicator) {
            setInterval(() => {
                statusIndicator.style.opacity = '0.3';
                setTimeout(() => {
                    statusIndicator.style.opacity = '1';
                }, 500);
            }, 2000);
        }

        // Form focus effects
        const formInputs = document.querySelectorAll('.form-input, .form-select, .form-textarea');
        formInputs.forEach(input => {
            input.addEventListener('focus', () => {
                const formGroup = input.closest('.form-group');
                if (formGroup) {
                    formGroup.classList.add('focused');
                }
            });
            
            input.addEventListener('blur', () => {
                const formGroup = input.closest('.form-group');
                if (formGroup) {
                    formGroup.classList.remove('focused');
                }
            });
        });
    }

    setupAccessibilityFeatures() {
        // Add aria-labels to form elements
        const nameInput = document.getElementById('name');
        const emailInput = document.getElementById('email');
        const subjectSelect = document.getElementById('subject');
        const messageTextarea = document.getElementById('message');
        
        if (nameInput) nameInput.setAttribute('aria-describedby', 'name-error');
        if (emailInput) emailInput.setAttribute('aria-describedby', 'email-error');
        if (subjectSelect) subjectSelect.setAttribute('aria-describedby', 'subject-error');
        if (messageTextarea) messageTextarea.setAttribute('aria-describedby', 'message-error');

        // Add skip link to form
        const contactForm = document.getElementById('contact-form');
        if (contactForm && !contactForm.id) {
            contactForm.id = 'contact-form-section';
        }

        // Enhanced keyboard navigation for method cards
        const methodCards = document.querySelectorAll('.method-card');
        methodCards.forEach((card, index) => {
            card.setAttribute('tabindex', '0');
            card.setAttribute('role', 'button');
            
            card.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    const link = card.querySelector('a');
                    if (link) {
                        e.preventDefault();
                        link.click();
                    }
                }
                
                if (e.key === 'ArrowDown' && index < methodCards.length - 1) {
                    e.preventDefault();
                    methodCards[index + 1].focus();
                } else if (e.key === 'ArrowUp' && index > 0) {
                    e.preventDefault();
                    methodCards[index - 1].focus();
                }
            });
        });
    }

    addContactStyles() {
        if (document.getElementById('contact-styles')) return;

        const style = document.createElement('style');
        style.id = 'contact-styles';
        style.textContent = `
            /* Contact page specific styles */
            .contact-main {
                padding-top: var(--header-height);
            }

            .contact-hero {
                padding: var(--space-20) 0;
                background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            }

            .contact-icon {
                font-size: var(--font-size-5xl);
                text-align: center;
                margin-bottom: var(--space-6);
            }

            .hero-title {
                font-size: var(--font-size-5xl);
                font-weight: 700;
                text-align: center;
                margin-bottom: var(--space-6);
                background: var(--gradient-primary);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }

            .hero-subtitle {
                text-align: center;
                color: var(--text-secondary);
                font-size: var(--font-size-lg);
                margin-bottom: var(--space-8);
                line-height: 1.6;
            }

            .response-time {
                display: flex;
                align-items: center;
                justify-content: center;
                gap: var(--space-2);
                padding: var(--space-3) var(--space-6);
                background: rgba(34, 197, 94, 0.1);
                color: #059669;
                border-radius: var(--radius-lg);
                max-width: 350px;
                margin: 0 auto;
                font-size: var(--font-size-sm);
                font-weight: 500;
            }

            .time-icon {
                font-size: var(--font-size-lg);
            }

            /* Contact Methods */
            .contact-methods {
                padding: var(--space-20) 0;
            }

            .methods-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
                gap: var(--space-8);
                margin-top: var(--space-12);
            }

            .method-card {
                background: white;
                border-radius: var(--radius-2xl);
                padding: var(--space-8);
                box-shadow: var(--shadow-md);
                transition: all var(--transition-base);
                border: 1px solid transparent;
            }

            .method-card:hover,
            .method-card:focus {
                transform: translateY(-8px);
                box-shadow: var(--shadow-xl);
                border-color: var(--primary-color);
                outline: none;
            }

            .method-icon {
                text-align: center;
                margin-bottom: var(--space-6);
            }

            .icon-bg {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                width: 80px;
                height: 80px;
                border-radius: 50%;
                font-size: var(--font-size-3xl);
                color: white;
                transition: all var(--transition-base);
            }

            .twitter-bg {
                background: linear-gradient(135deg, #1da1f2 0%, #0d8bd9 100%);
            }

            .github-bg {
                background: linear-gradient(135deg, #333 0%, #24292e 100%);
            }

            .email-bg {
                background: linear-gradient(135deg, #ea4335 0%, #d33b2c 100%);
            }

            .method-content h3 {
                font-size: var(--font-size-xl);
                font-weight: 600;
                margin-bottom: var(--space-4);
                color: var(--text-primary);
            }

            .method-content p {
                color: var(--text-secondary);
                line-height: 1.6;
                margin-bottom: var(--space-6);
            }

            .method-details {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: var(--space-6);
                padding: var(--space-3);
                background: var(--background-secondary);
                border-radius: var(--radius-md);
            }

            .detail-label {
                font-size: var(--font-size-sm);
                color: var(--text-light);
                font-weight: 500;
            }

            .detail-value {
                font-size: var(--font-size-sm);
                color: var(--text-primary);
                font-weight: 600;
            }

            /* Contact Form */
            .contact-form-section {
                padding: var(--space-20) 0;
                background: var(--background-secondary);
            }

            .form-wrapper {
                max-width: 800px;
                margin: 0 auto;
            }

            .form-header {
                text-align: center;
                margin-bottom: var(--space-12);
            }

            .form-title {
                font-size: var(--font-size-4xl);
                font-weight: 700;
                margin-bottom: var(--space-4);
                background: var(--gradient-primary);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }

            .form-subtitle {
                color: var(--text-secondary);
                font-size: var(--font-size-lg);
                line-height: 1.6;
            }

            .contact-form-container {
                background: white;
                border-radius: var(--radius-2xl);
                padding: var(--space-12);
                box-shadow: var(--shadow-lg);
            }

            .contact-form {
                display: flex;
                flex-direction: column;
                gap: var(--space-6);
            }

            .form-row {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: var(--space-6);
            }

            .form-group {
                display: flex;
                flex-direction: column;
                gap: var(--space-2);
                position: relative;
            }

            .form-group.focused .form-label {
                color: var(--primary-color);
            }

            .form-label {
                font-weight: 600;
                color: var(--text-primary);
                font-size: var(--font-size-sm);
                transition: color var(--transition-base);
            }

            .form-input,
            .form-select,
            .form-textarea {
                padding: var(--space-4);
                border: 2px solid var(--border-color);
                border-radius: var(--radius-md);
                font-size: var(--font-size-base);
                background: white;
                transition: all var(--transition-base);
                font-family: inherit;
            }

            .form-input:focus,
            .form-select:focus,
            .form-textarea:focus {
                outline: none;
                border-color: var(--primary-color);
                box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
            }

            .form-input.error,
            .form-select.error,
            .form-textarea.error {
                border-color: #ef4444;
                box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
            }

            .form-textarea {
                resize: vertical;
                min-height: 120px;
            }

            .form-error {
                color: #ef4444;
                font-size: var(--font-size-sm);
                font-weight: 500;
                display: none;
            }

            .form-general-error {
                background: rgba(239, 68, 68, 0.1);
                color: #dc2626;
                padding: var(--space-4);
                border-radius: var(--radius-md);
                border: 1px solid rgba(239, 68, 68, 0.2);
                font-size: var(--font-size-sm);
                font-weight: 500;
                margin-bottom: var(--space-6);
                display: none;
            }

            .checkbox-group {
                display: flex;
                align-items: center;
                gap: var(--space-3);
            }

            .checkbox-group input[type="checkbox"] {
                width: 18px;
                height: 18px;
                accent-color: var(--primary-color);
            }

            .checkbox-label {
                font-size: var(--font-size-sm);
                color: var(--text-secondary);
                line-height: 1.5;
            }

            .checkbox-label a {
                color: var(--primary-color);
                text-decoration: none;
            }

            .checkbox-label a:hover {
                text-decoration: underline;
            }

            .form-submit {
                text-align: center;
                margin-top: var(--space-4);
            }

            .btn-loader {
                display: none;
                align-items: center;
                gap: var(--space-1);
            }

            .loader-dot {
                width: 4px;
                height: 4px;
                background: currentColor;
                border-radius: 50%;
                animation: loader-bounce 1.4s ease-in-out infinite both;
            }

            .loader-dot:nth-child(1) { animation-delay: -0.32s; }
            .loader-dot:nth-child(2) { animation-delay: -0.16s; }

            @keyframes loader-bounce {
                0%, 80%, 100% { transform: scale(0); }
                40% { transform: scale(1); }
            }

            .form-success {
                text-align: center;
                padding: var(--space-12);
                display: none;
            }

            .success-icon {
                font-size: var(--font-size-5xl);
                margin-bottom: var(--space-6);
            }

            .form-success h3 {
                font-size: var(--font-size-2xl);
                font-weight: 600;
                margin-bottom: var(--space-4);
                color: var(--text-primary);
            }

            .form-success p {
                color: var(--text-secondary);
                font-size: var(--font-size-lg);
                line-height: 1.6;
            }

            /* FAQ Section */
            .faq-section {
                padding: var(--space-20) 0;
            }

            .faq-container {
                max-width: 800px;
                margin: 0 auto;
                margin-top: var(--space-12);
            }

            .faq-item {
                background: white;
                border-radius: var(--radius-xl);
                margin-bottom: var(--space-4);
                box-shadow: var(--shadow-md);
                overflow: hidden;
                transition: all var(--transition-base);
            }

            .faq-item:hover {
                box-shadow: var(--shadow-lg);
            }

            .faq-question {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: var(--space-6);
                cursor: pointer;
                background: white;
                border: none;
                width: 100%;
                text-align: left;
                transition: all var(--transition-base);
            }

            .faq-question:hover,
            .faq-question:focus {
                background: var(--background-secondary);
                outline: none;
            }

            .faq-text {
                font-size: var(--font-size-lg);
                font-weight: 600;
                color: var(--text-primary);
            }

            .faq-icon {
                font-size: var(--font-size-xl);
                font-weight: 300;
                color: var(--primary-color);
                transition: transform var(--transition-base);
            }

            .faq-answer {
                max-height: 0;
                overflow: hidden;
                transition: max-height 0.3s ease-out;
            }

            .faq-item.expanded .faq-answer {
                max-height: 200px;
            }

            .faq-item.expanded .faq-icon {
                transform: rotate(45deg);
            }

            .faq-answer p {
                padding: 0 var(--space-6) var(--space-6);
                color: var(--text-secondary);
                line-height: 1.6;
                margin: 0;
            }

            /* Availability Section */
            .availability-section {
                padding: var(--space-20) 0;
                background: var(--background-secondary);
            }

            .availability-card {
                background: white;
                border-radius: var(--radius-2xl);
                padding: var(--space-12);
                box-shadow: var(--shadow-xl);
                max-width: 700px;
                margin: 0 auto;
            }

            .availability-status {
                display: flex;
                align-items: center;
                gap: var(--space-4);
                margin-bottom: var(--space-8);
            }

            .status-indicator {
                width: 12px;
                height: 12px;
                border-radius: 50%;
                flex-shrink: 0;
                transition: opacity var(--transition-base);
            }

            .status-indicator.available {
                background: #10b981;
                box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.2);
            }

            .status-text h3 {
                font-size: var(--font-size-2xl);
                font-weight: 600;
                margin-bottom: var(--space-2);
                color: var(--text-primary);
            }

            .status-text p {
                color: var(--text-secondary);
                font-size: var(--font-size-lg);
                margin: 0;
            }

            .availability-details {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: var(--space-4);
                margin-bottom: var(--space-8);
                padding: var(--space-6);
                background: var(--background-secondary);
                border-radius: var(--radius-lg);
            }

            .detail-item {
                display: flex;
                justify-content: space-between;
                align-items: center;
            }

            .availability-action {
                text-align: center;
            }

            /* Mobile styles */
            @media (max-width: 768px) {
                .contact-hero {
                    padding: var(--space-16) 0;
                }

                .hero-title {
                    font-size: var(--font-size-4xl);
                }

                .methods-grid {
                    grid-template-columns: 1fr;
                    gap: var(--space-6);
                }

                .form-row {
                    grid-template-columns: 1fr;
                    gap: var(--space-4);
                }

                .contact-form-container {
                    padding: var(--space-8);
                    margin: 0 var(--space-4);
                }

                .availability-details {
                    grid-template-columns: 1fr;
                }

                .faq-text {
                    font-size: var(--font-size-base);
                }
            }
        `;
        
        document.head.appendChild(style);
    }

    // Public methods
    focusForm() {
        const firstInput = this.form?.querySelector('input, select, textarea');
        if (firstInput) {
            firstInput.focus();
        }
    }

    scrollToFAQ() {
        const faqSection = document.querySelector('.faq-section');
        if (faqSection) {
            const headerHeight = document.querySelector('.header').offsetHeight;
            const targetPosition = faqSection.offsetTop - headerHeight - 20;
            
            window.scrollTo({
                top: targetPosition,
                behavior: 'smooth'
            });
        }
    }

    expandFAQ(index) {
        const faqItems = document.querySelectorAll('.faq-item');
        if (faqItems[index]) {
            const question = faqItems[index].querySelector('.faq-question');
            if (question) {
                question.click();
            }
        }
    }
}

// Initialize contact manager
document.addEventListener('DOMContentLoaded', () => {
    const contactManager = new ContactManager();
    
    // Make available globally for debugging
    window.contactManager = contactManager;
    
    // Add keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        // Alt + F: Focus form
        if (e.altKey && e.key === 'f') {
            e.preventDefault();
            contactManager.focusForm();
        }
        
        // Alt + Q: Scroll to FAQ
        if (e.altKey && e.key === 'q') {
            e.preventDefault();
            contactManager.scrollToFAQ();
        }
        
        // Ctrl/Cmd + Enter: Submit form (when focused in form)
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            const activeElement = document.activeElement;
            if (activeElement && contactManager.form?.contains(activeElement)) {
                e.preventDefault();
                contactManager.form.dispatchEvent(new Event('submit'));
            }
        }
    });
    
    // Add smooth scroll for contact form links
    document.querySelectorAll('a[href="#contact-form"]').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const formSection = document.getElementById('contact-form');
            if (formSection) {
                const headerHeight = document.querySelector('.header').offsetHeight;
                const targetPosition = formSection.offsetTop - headerHeight - 20;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
                
                // Focus form after scroll
                setTimeout(() => {
                    contactManager.focusForm();
                }, 500);
            }
        });
    });
});