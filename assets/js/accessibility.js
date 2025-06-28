// Global Accessibility Enhancement Script

class AccessibilityManager {
    constructor() {
        this.init();
    }

    init() {
        this.addSkipLinks();
        this.enhanceKeyboardNavigation();
        this.initFocusManagement();
        this.addAriaLabels();
        this.handleReducedMotion();
        this.initBackToTop();
        this.announcePageChanges();
        this.setupFormAccessibility();
        this.initTooltips();
        
        // Initialize on page load
        document.addEventListener('DOMContentLoaded', () => {
            this.announcePageLoad();
        });
    }

    // Add skip links for better navigation
    addSkipLinks() {
        if (document.querySelector('.skip-links')) return; // Already exists
        
        const skipLinksHtml = `
            <div class="skip-links" role="navigation" aria-label="Skip navigation">
                <a href="#main-content" class="skip-link">Skip to main content</a>
                <a href="#navigation" class="skip-link">Skip to navigation</a>
                <a href="#footer" class="skip-link">Skip to footer</a>
            </div>
        `;
        
        document.body.insertAdjacentHTML('afterbegin', skipLinksHtml);
    }

    // Enhanced keyboard navigation
    enhanceKeyboardNavigation() {
        // Handle escape key for closing modals/menus
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeAllModals();
                this.closeMobileMenu();
            }
        });

        // Add keyboard support for mobile menu
        const navToggle = document.getElementById('nav-toggle');
        if (navToggle) {
            navToggle.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    navToggle.click();
                }
            });
        }

        // Enhance navigation with arrow keys
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach((link, index) => {
            link.addEventListener('keydown', (e) => {
                if (e.key === 'ArrowDown' || e.key === 'ArrowRight') {
                    e.preventDefault();
                    const nextIndex = (index + 1) % navLinks.length;
                    navLinks[nextIndex].focus();
                } else if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') {
                    e.preventDefault();
                    const prevIndex = (index - 1 + navLinks.length) % navLinks.length;
                    navLinks[prevIndex].focus();
                }
            });
        });
    }

    // Focus management
    initFocusManagement() {
        let lastFocusedElement = null;

        // Store last focused element before modal opens
        document.addEventListener('focusin', (e) => {
            if (!e.target.closest('.modal') && !e.target.closest('.skip-links')) {
                lastFocusedElement = e.target;
            }
        });

        // Return focus when modal closes
        this.returnFocus = () => {
            if (lastFocusedElement) {
                lastFocusedElement.focus();
            }
        };

        // Trap focus in modals
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Tab') {
                this.trapFocus(e);
            }
        });
    }

    // Trap focus within modal or dropdown
    trapFocus(e) {
        const modal = document.querySelector('.modal.active');
        if (!modal) return;

        const focusableElements = modal.querySelectorAll(
            'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        
        if (focusableElements.length === 0) return;

        const firstElement = focusableElements[0];
        const lastElement = focusableElements[focusableElements.length - 1];

        if (e.shiftKey) {
            if (document.activeElement === firstElement) {
                e.preventDefault();
                lastElement.focus();
            }
        } else {
            if (document.activeElement === lastElement) {
                e.preventDefault();
                firstElement.focus();
            }
        }
    }

    // Add appropriate ARIA labels
    addAriaLabels() {
        // Add landmarks
        const main = document.querySelector('main');
        if (main && !main.id) {
            main.id = 'main-content';
            main.setAttribute('role', 'main');
        }

        const nav = document.querySelector('nav');
        if (nav && !nav.id) {
            nav.id = 'navigation';
            nav.setAttribute('role', 'navigation');
            nav.setAttribute('aria-label', 'Main navigation');
        }

        const footer = document.querySelector('footer');
        if (footer && !footer.id) {
            footer.id = 'footer';
            footer.setAttribute('role', 'contentinfo');
        }

        // Add ARIA labels to buttons without text
        const buttons = document.querySelectorAll('button:not([aria-label]):not([aria-labelledby])');
        buttons.forEach(button => {
            const text = button.textContent.trim();
            if (!text) {
                // Try to determine button purpose from class or context
                if (button.classList.contains('nav-toggle')) {
                    button.setAttribute('aria-label', 'Toggle navigation menu');
                    button.setAttribute('aria-expanded', 'false');
                } else if (button.classList.contains('back-to-top')) {
                    button.setAttribute('aria-label', 'Return to top of page');
                } else if (button.classList.contains('close')) {
                    button.setAttribute('aria-label', 'Close');
                }
            }
        });

        // Add ARIA labels to links without text
        const links = document.querySelectorAll('a:not([aria-label]):not([aria-labelledby])');
        links.forEach(link => {
            const text = link.textContent.trim();
            if (!text && link.querySelector('img')) {
                const img = link.querySelector('img');
                if (img.alt) {
                    link.setAttribute('aria-label', img.alt);
                }
            }
        });

        // Enhance form accessibility
        this.enhanceFormAccessibility();
    }

    // Enhanced form accessibility
    enhanceFormAccessibility() {
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            // Associate labels with inputs
            const inputs = form.querySelectorAll('input, textarea, select');
            inputs.forEach(input => {
                if (!input.id) {
                    input.id = 'input-' + Math.random().toString(36).substr(2, 9);
                }

                // Find associated label
                let label = form.querySelector(`label[for="${input.id}"]`);
                if (!label) {
                    label = input.closest('label');
                }

                if (label && !input.getAttribute('aria-labelledby')) {
                    if (!label.id) {
                        label.id = 'label-' + Math.random().toString(36).substr(2, 9);
                    }
                    input.setAttribute('aria-labelledby', label.id);
                }

                // Add required indicator
                if (input.required && !input.getAttribute('aria-required')) {
                    input.setAttribute('aria-required', 'true');
                }

                // Add invalid state handling
                input.addEventListener('invalid', () => {
                    input.setAttribute('aria-invalid', 'true');
                    this.announceError(input);
                });

                input.addEventListener('input', () => {
                    if (input.checkValidity()) {
                        input.removeAttribute('aria-invalid');
                    }
                });
            });
        });
    }

    // Setup form accessibility
    setupFormAccessibility() {
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            form.addEventListener('submit', (e) => {
                const firstInvalidField = form.querySelector(':invalid');
                if (firstInvalidField) {
                    e.preventDefault();
                    firstInvalidField.focus();
                    this.announceError(firstInvalidField);
                }
            });
        });
    }

    // Handle reduced motion preference
    handleReducedMotion() {
        if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
            // Disable animations for users who prefer reduced motion
            document.documentElement.style.setProperty('--transition-base', '0ms');
            document.documentElement.style.setProperty('--transition-slow', '0ms');
            
            // Remove scroll reveal animations
            const scrollElements = document.querySelectorAll('.scroll-reveal');
            scrollElements.forEach(el => {
                el.style.opacity = '1';
                el.style.transform = 'none';
            });
        }
    }

    // Enhanced back to top functionality
    initBackToTop() {
        const backToTop = document.querySelector('.back-to-top');
        if (!backToTop) {
            // Create back to top button if it doesn't exist
            const button = document.createElement('button');
            button.className = 'back-to-top';
            button.innerHTML = '<span class="back-to-top-icon">↑</span>';
            button.setAttribute('aria-label', 'Return to top of page');
            document.body.appendChild(button);
        }

        const backToTopBtn = document.querySelector('.back-to-top');
        
        // Show/hide based on scroll position
        window.addEventListener('scroll', () => {
            if (window.scrollY > 300) {
                backToTopBtn?.classList.add('visible');
            } else {
                backToTopBtn?.classList.remove('visible');
            }
        });

        // Smooth scroll to top
        backToTopBtn?.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
            
            // Announce to screen readers
            this.announce('Returned to top of page');
        });
    }

    // Announce page changes for screen readers
    announcePageChanges() {
        // Listen for navigation changes
        window.addEventListener('popstate', () => {
            this.announcePageLoad();
        });
    }

    // Announce page load
    announcePageLoad() {
        const pageTitle = document.title || 'Page loaded';
        const announcement = document.createElement('div');
        announcement.setAttribute('aria-live', 'polite');
        announcement.setAttribute('aria-atomic', 'true');
        announcement.className = 'sr-only';
        announcement.textContent = `${pageTitle} loaded`;
        
        document.body.appendChild(announcement);
        
        setTimeout(() => {
            announcement.remove();
        }, 1000);
    }

    // Initialize tooltips
    initTooltips() {
        const tooltipElements = document.querySelectorAll('[data-tooltip]');
        tooltipElements.forEach(element => {
            const tooltipText = element.getAttribute('data-tooltip');
            
            element.setAttribute('aria-describedby', 'tooltip-' + Math.random().toString(36).substr(2, 9));
            element.setAttribute('role', 'button');
            element.setAttribute('tabindex', '0');
            
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip-content';
            tooltip.textContent = tooltipText;
            tooltip.id = element.getAttribute('aria-describedby');
            element.appendChild(tooltip);
        });
    }

    // Utility functions
    closeAllModals() {
        const modals = document.querySelectorAll('.modal');
        modals.forEach(modal => {
            modal.classList.remove('active');
        });
        this.returnFocus();
    }

    closeMobileMenu() {
        const navToggle = document.getElementById('nav-toggle');
        const navMenu = document.getElementById('nav-menu');
        
        if (navToggle && navMenu) {
            navToggle.classList.remove('active');
            navMenu.classList.remove('active');
            document.body.classList.remove('nav-open');
            navToggle.setAttribute('aria-expanded', 'false');
        }
    }

    // Announce messages to screen readers
    announce(message, priority = 'polite') {
        const announcement = document.createElement('div');
        announcement.setAttribute('aria-live', priority);
        announcement.setAttribute('aria-atomic', 'true');
        announcement.className = 'sr-only';
        announcement.textContent = message;
        
        document.body.appendChild(announcement);
        
        setTimeout(() => {
            announcement.remove();
        }, 1000);
    }

    // Announce form errors
    announceError(field) {
        const errorMessage = field.validationMessage || 'Invalid input';
        this.announce(`Error: ${errorMessage}`, 'assertive');
    }

    // Color contrast checker (for development)
    checkContrast(foreground, background) {
        // Simple contrast ratio calculation
        const getRGB = (color) => {
            const div = document.createElement('div');
            div.style.color = color;
            document.body.appendChild(div);
            const rgb = window.getComputedStyle(div).color;
            document.body.removeChild(div);
            return rgb.match(/\d+/g).map(Number);
        };

        const getLuminance = (rgb) => {
            const [r, g, b] = rgb.map(c => {
                c = c / 255;
                return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
            });
            return 0.2126 * r + 0.7152 * g + 0.0722 * b;
        };

        const fgRGB = getRGB(foreground);
        const bgRGB = getRGB(background);
        const fgLum = getLuminance(fgRGB);
        const bgLum = getLuminance(bgRGB);
        
        const ratio = (Math.max(fgLum, bgLum) + 0.05) / (Math.min(fgLum, bgLum) + 0.05);
        
        return {
            ratio: ratio,
            AA: ratio >= 4.5,
            AAA: ratio >= 7,
            AA_Large: ratio >= 3
        };
    }
}

// Initialize accessibility manager
const accessibilityManager = new AccessibilityManager();

// Add keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Alt + 1: Skip to main content
    if (e.altKey && e.key === '1') {
        e.preventDefault();
        const main = document.getElementById('main-content');
        if (main) {
            main.focus();
            main.scrollIntoView({ behavior: 'smooth' });
        }
    }
    
    // Alt + 2: Skip to navigation
    if (e.altKey && e.key === '2') {
        e.preventDefault();
        const nav = document.getElementById('navigation');
        if (nav) {
            const firstLink = nav.querySelector('a, button');
            if (firstLink) {
                firstLink.focus();
            }
        }
    }
    
    // Alt + 3: Skip to footer
    if (e.altKey && e.key === '3') {
        e.preventDefault();
        const footer = document.getElementById('footer');
        if (footer) {
            footer.scrollIntoView({ behavior: 'smooth' });
            footer.focus();
        }
    }
});

// Export for use in other scripts
window.AccessibilityManager = AccessibilityManager;
window.accessibilityManager = accessibilityManager;