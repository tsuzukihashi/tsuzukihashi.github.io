/**
 * Component Loader for tsuzuki817 Website
 * Dynamically loads HTML components and injects them into the page
 */

class ComponentLoader {
    constructor() {
        this.baseLevel = this.calculateBaseLevel();
        this.basePath = this.baseLevel > 0 ? '../'.repeat(this.baseLevel) : './';
    }

    /**
     * Calculate how many levels deep the current page is
     */
    calculateBaseLevel() {
        const path = window.location.pathname;
        const segments = path.split('/').filter(segment => segment !== '');
        
        // Remove filename if present
        if (segments.length > 0 && segments[segments.length - 1].includes('.')) {
            segments.pop();
        }
        
        // Calculate depth from root (excluding domain)
        return segments.length;
    }

    /**
     * Load and inject a component
     */
    async loadComponent(componentName, targetSelector) {
        try {
            const componentPath = `${this.basePath}components/${componentName}.html`;
            const response = await fetch(componentPath);
            
            if (!response.ok) {
                console.warn(`Failed to load component: ${componentName}`);
                return false;
            }
            
            const html = await response.text();
            const targetElement = document.querySelector(targetSelector);
            
            if (!targetElement) {
                console.warn(`Target element not found: ${targetSelector}`);
                return false;
            }
            
            // Process the HTML to adjust relative paths
            const processedHtml = this.processRelativePaths(html);
            targetElement.innerHTML = processedHtml;
            
            return true;
        } catch (error) {
            console.error(`Error loading component ${componentName}:`, error);
            return false;
        }
    }

    /**
     * Process HTML to adjust relative paths based on current page depth
     */
    processRelativePaths(html) {
        // Replace relative paths in href and src attributes
        return html
            .replace(/href="(?!http|#|\/)/g, `href="${this.basePath}`)
            .replace(/src="(?!http|\/)/g, `src="${this.basePath}`)
            .replace(/\$\{BASE_PATH\}/g, this.basePath);
    }

    /**
     * Set active navigation link
     */
    setActiveNavigation() {
        const currentPath = window.location.pathname;
        const navLinks = document.querySelectorAll('.nav-link');
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            const href = link.getAttribute('href');
            
            // Check if this link matches the current page
            if (this.isCurrentPage(href, currentPath)) {
                link.classList.add('active');
            }
        });
    }

    /**
     * Check if the href matches the current page
     */
    isCurrentPage(href, currentPath) {
        // Handle root/home page
        if ((href === '#' || href === '../' || href === './') && 
            (currentPath === '/' || currentPath.endsWith('/index.html') || currentPath.endsWith('/tsuzuki817/'))) {
            return true;
        }
        
        // Handle portfolio page
        if (href.includes('portfolio') && currentPath.includes('/portfolio')) {
            return true;
        }
        
        // Handle blog page
        if (href.includes('blog') && currentPath.includes('/blog')) {
            return true;
        }
        
        // Handle about page
        if (href.includes('about') && currentPath.includes('/about')) {
            return true;
        }
        
        // Handle contact page
        if (href.includes('contact') && currentPath.includes('/contact')) {
            return true;
        }
        
        return false;
    }

    /**
     * Load all components for the page
     */
    async loadAllComponents() {
        const components = [
            { name: 'header', selector: '[data-component="header"]' },
            { name: 'footer', selector: '[data-component="footer"]' },
            { name: 'back-to-top', selector: '[data-component="back-to-top"]' }
        ];

        for (const component of components) {
            await this.loadComponent(component.name, component.selector);
        }

        // Set active navigation after header is loaded
        this.setActiveNavigation();
    }
}

// Auto-initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', async () => {
    const loader = new ComponentLoader();
    await loader.loadAllComponents();
});

// Export for manual usage if needed
window.ComponentLoader = ComponentLoader;