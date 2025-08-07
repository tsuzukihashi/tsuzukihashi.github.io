/**
 * Language Manager for multi-language support
 * This script manages language switching and text translations across the site
 */

class LanguageManager {
    constructor() {
        this.currentLang = this.detectCurrentLanguage();
        this.translations = window.translations || {};
        this.init();
    }
    
    /**
     * Detect current language from URL
     */
    detectCurrentLanguage() {
        const savedLang = localStorage.getItem('preferredLanguage');
        
        // Check URL for language (for initial page load)
        const path = window.location.pathname;
        if (path.startsWith('/en/')) return 'en';
        if (path.startsWith('/ko/')) return 'ko';
        
        // Use saved preference or default to Japanese
        return savedLang || 'ja';
    }
    
    /**
     * Initialize language manager
     */
    init() {
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.applyTranslations());
        } else {
            this.applyTranslations();
        }
        
        // Listen for language changes
        window.addEventListener('languageChanged', (e) => {
            this.currentLang = e.detail.language;
            this.applyTranslations();
        });
    }
    
    /**
     * Apply translations to all elements with data-i18n attribute
     */
    applyTranslations() {
        const elements = document.querySelectorAll('[data-i18n]');
        
        elements.forEach(element => {
            const key = element.getAttribute('data-i18n');
            const translation = this.getTranslation(key);
            
            if (translation) {
                // Check if it's an input element
                if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
                    if (element.hasAttribute('placeholder')) {
                        element.placeholder = translation;
                    } else {
                        element.value = translation;
                    }
                } else if (element.tagName === 'META') {
                    element.content = translation;
                } else {
                    element.textContent = translation;
                }
            }
        });
        
        // Apply HTML content translations (for rich text)
        const htmlElements = document.querySelectorAll('[data-i18n-html]');
        htmlElements.forEach(element => {
            const key = element.getAttribute('data-i18n-html');
            const translation = this.getTranslation(key);
            
            if (translation) {
                element.innerHTML = translation;
            }
        });
        
        // Update document attributes
        document.documentElement.lang = this.currentLang;
    }
    
    /**
     * Get translation for a given key
     * @param {string} key - Translation key (e.g., 'portfolio.title')
     * @returns {string|null} - Translated text or null if not found
     */
    getTranslation(key) {
        if (!this.translations[this.currentLang]) {
            console.warn(`Language '${this.currentLang}' not found in translations`);
            return null;
        }
        
        const keys = key.split('.');
        let translation = this.translations[this.currentLang];
        
        for (const k of keys) {
            if (translation && typeof translation === 'object') {
                translation = translation[k];
            } else {
                console.warn(`Translation key '${key}' not found for language '${this.currentLang}'`);
                return null;
            }
        }
        
        return translation;
    }
    
    /**
     * Change language and redirect if necessary
     * @param {string} lang - Language code (ja, en, ko)
     */
    changeLanguage(lang) {
        if (!['ja', 'en', 'ko'].includes(lang)) {
            console.error(`Invalid language code: ${lang}`);
            return;
        }
        
        // Save preference
        localStorage.setItem('preferredLanguage', lang);
        
        // Get current page path without language prefix
        let path = window.location.pathname;
        if (path.startsWith('/en/')) {
            path = path.replace(/^\/en/, '');
        } else if (path.startsWith('/ko/')) {
            path = path.replace(/^\/ko/, '');
        }
        
        // Build new URL
        let newPath = path;
        if (lang !== 'ja') {
            newPath = '/' + lang + path;
        }
        
        // Redirect if path changed
        if (newPath !== window.location.pathname) {
            window.location.href = newPath;
        } else {
            // Same page, just update translations
            this.currentLang = lang;
            this.applyTranslations();
            
            // Dispatch event for other components
            window.dispatchEvent(new CustomEvent('languageChanged', {
                detail: { language: lang }
            }));
        }
    }
    
    /**
     * Get current language
     * @returns {string} Current language code
     */
    getCurrentLanguage() {
        return this.currentLang;
    }
    
    /**
     * Get all available languages
     * @returns {object} Available languages
     */
    getAvailableLanguages() {
        return {
            ja: '日本語',
            en: 'English',
            ko: '한국어'
        };
    }
}

// Initialize language manager when script loads
window.languageManager = new LanguageManager();

// Expose global function for easy access
window.changeLanguage = function(lang) {
    window.languageManager.changeLanguage(lang);
};

// Function to translate a key programmatically
window.t = function(key) {
    return window.languageManager.getTranslation(key);
};