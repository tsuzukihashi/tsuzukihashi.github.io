// Portfolio-specific JavaScript

class PortfolioManager {
    constructor() {
        this.currentFilter = 'all';
        this.apps = [];
        this.init();
    }

    init() {
        this.setupFilterButtons();
        this.setupShowMoreButton();
        this.collectApps();
        this.addPortfolioStyles();
        this.setupAppCardInteractions();
    }

    setupFilterButtons() {
        const filterButtons = document.querySelectorAll('.filter-btn');
        const appsGrid = document.getElementById('apps-grid');
        const noResults = document.getElementById('no-results');

        filterButtons.forEach(button => {
            button.addEventListener('click', () => {
                const filter = button.getAttribute('data-filter');
                
                // Update active button
                filterButtons.forEach(btn => btn.classList.remove('active'));
                button.classList.add('active');
                
                // Filter apps
                this.filterApps(filter, appsGrid, noResults);
                this.currentFilter = filter;
            });
        });
    }

    setupShowMoreButton() {
        const showMoreBtn = document.getElementById('show-more-apps');
        const additionalApps = document.getElementById('additional-apps');
        
        if (!showMoreBtn || !additionalApps) return;

        showMoreBtn.addEventListener('click', () => {
            const isExpanded = additionalApps.classList.contains('show');
            const showMoreText = showMoreBtn.querySelector('.show-more-text');
            const showMoreIcon = showMoreBtn.querySelector('.show-more-icon');
            
            if (isExpanded) {
                // Hide additional apps
                additionalApps.classList.remove('show');
                showMoreText.textContent = 'さらに表示 (22個のアプリ)';
                showMoreIcon.textContent = '↓';
                showMoreBtn.classList.remove('expanded');
            } else {
                // Show additional apps
                additionalApps.classList.add('show');
                showMoreText.textContent = '表示を減らす';
                showMoreIcon.textContent = '↑';
                showMoreBtn.classList.add('expanded');
                
                // Smooth scroll to first additional app
                setTimeout(() => {
                    const firstAdditionalApp = additionalApps.querySelector('.app-card');
                    if (firstAdditionalApp) {
                        firstAdditionalApp.scrollIntoView({ 
                            behavior: 'smooth', 
                            block: 'center' 
                        });
                    }
                }, 100);
            }
        });
    }

    filterApps(filter, appsGrid, noResults) {
        const appCards = appsGrid.querySelectorAll('.app-card');
        const additionalApps = document.getElementById('additional-apps');
        const showMoreContainer = document.querySelector('.show-more-container');
        let visibleCount = 0;

        appCards.forEach((card, index) => {
            // Skip cards that are inside additional-apps container when it's hidden
            const isInAdditionalApps = card.closest('#additional-apps');
            if (isInAdditionalApps && !additionalApps.classList.contains('show')) {
                return;
            }

            const categories = card.getAttribute('data-category').split(' ');
            const shouldShow = filter === 'all' || categories.includes(filter);

            if (shouldShow) {
                card.style.display = 'block';
                card.style.animation = `fadeInScale 0.5s ease-out ${index * 0.1}s forwards`;
                visibleCount++;
            } else {
                card.style.display = 'none';
            }
        });

        // Show/hide show more button based on filter
        if (showMoreContainer) {
            if (filter === 'all') {
                showMoreContainer.style.display = 'flex';
            } else {
                showMoreContainer.style.display = 'none';
                // Reset additional apps when filtering
                additionalApps.classList.remove('show');
                const showMoreBtn = document.getElementById('show-more-apps');
                if (showMoreBtn) {
                    const showMoreText = showMoreBtn.querySelector('.show-more-text');
                    const showMoreIcon = showMoreBtn.querySelector('.show-more-icon');
                    showMoreText.textContent = 'さらに表示 (22個のアプリ)';
                    showMoreIcon.textContent = '↓';
                    showMoreBtn.classList.remove('expanded');
                }
            }
        }

        // Show/hide no results message
        if (visibleCount === 0) {
            noResults.style.display = 'flex';
            noResults.style.animation = 'fadeIn 0.3s ease-out forwards';
        } else {
            noResults.style.display = 'none';
        }

        // Update URL hash
        if (filter !== 'all') {
            window.history.pushState(null, null, `#${filter}`);
        } else {
            window.history.pushState(null, null, window.location.pathname);
        }
    }

    collectApps() {
        const appCards = document.querySelectorAll('.app-card');
        this.apps = Array.from(appCards).map(card => ({
            element: card,
            title: card.querySelector('.app-title').textContent,
            description: card.querySelector('.app-description').textContent,
            categories: card.getAttribute('data-category').split(' ')
        }));
    }

    setupAppCardInteractions() {
        const appCards = document.querySelectorAll('.app-card');
        
        appCards.forEach(card => {
            // Add enhanced hover effects
            card.addEventListener('mouseenter', this.onCardHover.bind(this));
            card.addEventListener('mouseleave', this.onCardLeave.bind(this));
            
            // Add click analytics (if needed)
            card.addEventListener('click', (e) => {
                const appTitle = card.querySelector('.app-title').textContent;
                console.log(`App clicked: ${appTitle}`);
                
                // You can add analytics tracking here
                // gtag('event', 'app_view', { app_name: appTitle });
            });

            // Add keyboard navigation
            card.setAttribute('tabindex', '0');
            card.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    const link = card.querySelector('a[href*="apps/"]');
                    if (link) {
                        link.click();
                    }
                }
            });
        });

        // Setup overlay actions
        this.setupOverlayActions();
    }

    setupOverlayActions() {
        const overlayButtons = document.querySelectorAll('.btn-icon-round');
        
        overlayButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.stopPropagation();
                
                // Add ripple effect
                this.addRippleEffect(button, e);
            });
        });
    }

    onCardHover(e) {
        const card = e.target.closest('.app-card');
        const overlay = card.querySelector('.app-overlay');
        const image = card.querySelector('.app-image img, .placeholder-image');
        
        if (overlay) {
            overlay.style.opacity = '1';
        }
        
        if (image) {
            image.style.transform = 'scale(1.1)';
        }

        // Add subtle glow effect
        card.style.boxShadow = '0 20px 40px rgba(37, 99, 235, 0.15)';
    }

    onCardLeave(e) {
        const card = e.target.closest('.app-card');
        const overlay = card.querySelector('.app-overlay');
        const image = card.querySelector('.app-image img, .placeholder-image');
        
        if (overlay) {
            overlay.style.opacity = '';
        }
        
        if (image) {
            image.style.transform = '';
        }

        card.style.boxShadow = '';
    }

    addRippleEffect(button, e) {
        const ripple = document.createElement('span');
        const rect = button.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;
        
        ripple.style.cssText = `
            position: absolute;
            width: ${size}px;
            height: ${size}px;
            left: ${x}px;
            top: ${y}px;
            background: rgba(255, 255, 255, 0.6);
            border-radius: 50%;
            transform: scale(0);
            animation: ripple 0.6s ease-out;
            pointer-events: none;
        `;
        
        button.style.position = 'relative';
        button.style.overflow = 'hidden';
        button.appendChild(ripple);
        
        setTimeout(() => {
            if (ripple.parentNode) {
                ripple.parentNode.removeChild(ripple);
            }
        }, 600);
    }

    addPortfolioStyles() {
        if (document.getElementById('portfolio-styles')) return;

        const style = document.createElement('style');
        style.id = 'portfolio-styles';
        style.textContent = `
            /* Portfolio-specific styles */
            .portfolio-main {
                padding-top: var(--header-height);
            }

            .portfolio-hero {
                padding: var(--space-20) 0;
                background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            }
            
            @media (prefers-color-scheme: dark) {
                .portfolio-hero {
                    background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
                }
                
                .filter-btn {
                    background: var(--background-secondary);
                    border-color: var(--border-color);
                    color: var(--text-primary);
                }
                
                .filter-btn:hover,
                .filter-btn.active {
                    background: var(--gradient-primary);
                    color: white;
                    border-color: var(--primary-color);
                }
                
                .stat-item {
                    color: var(--text-primary);
                }
                
                .tech-tag {
                    background: var(--background-dark);
                    color: var(--text-secondary);
                    border-color: var(--border-color);
                }
            }

            .portfolio-hero .hero-title {
                font-size: var(--font-size-5xl);
                text-align: center;
                margin-bottom: var(--space-6);
            }

            .portfolio-hero .hero-subtitle {
                text-align: center;
                max-width: 600px;
                margin: 0 auto var(--space-8);
                color: var(--text-secondary);
                font-size: var(--font-size-lg);
            }

            .filter-buttons {
                display: flex;
                justify-content: center;
                gap: var(--space-3);
                flex-wrap: wrap;
                margin-bottom: var(--space-4);
            }

            .filter-btn {
                padding: var(--space-2) var(--space-4);
                border: 2px solid var(--border-color);
                border-radius: var(--radius-lg);
                background: white;
                color: var(--text-primary);
                font-weight: 600;
                cursor: pointer;
                transition: all var(--transition-base);
            }

            .filter-btn:hover,
            .filter-btn.active {
                border-color: var(--primary-color);
                color: var(--primary-color);
                background: rgba(37, 99, 235, 0.05);
                transform: translateY(-2px);
            }

            .apps-showcase {
                padding: var(--space-20) 0;
            }

            .portfolio-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
                gap: var(--space-8);
            }

            .app-overlay {
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0, 0, 0, 0.7);
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                padding: var(--space-4);
                opacity: 0;
                transition: all var(--transition-base);
            }

            .app-actions-overlay {
                display: flex;
                gap: var(--space-2);
                justify-content: flex-end;
            }

            .btn-icon-round {
                width: 40px;
                height: 40px;
                border-radius: 50%;
                background: rgba(255, 255, 255, 0.9);
                display: flex;
                align-items: center;
                justify-content: center;
                text-decoration: none;
                transition: all var(--transition-base);
                backdrop-filter: blur(10px);
            }

            .btn-icon-round:hover {
                background: white;
                transform: scale(1.1);
            }

            .app-meta {
                display: flex;
                justify-content: space-between;
                align-items: flex-end;
                margin-top: var(--space-4);
                padding-top: var(--space-4);
                border-top: 1px solid var(--border-color);
            }

            .app-stats {
                display: flex;
                gap: var(--space-3);
            }

            .stat-item {
                display: flex;
                align-items: center;
                gap: var(--space-1);
                font-size: var(--font-size-sm);
                color: var(--text-primary);
            }

            .stat-icon {
                font-size: var(--font-size-base);
            }

            .app-tech {
                display: flex;
                gap: var(--space-2);
                flex-wrap: wrap;
            }

            .tech-tag {
                padding: var(--space-1) var(--space-2);
                background: var(--background-secondary);
                color: var(--text-primary);
                border-radius: var(--radius-sm);
                font-size: var(--font-size-xs);
                font-weight: 600;
                border: 1px solid #e2e8f0;
            }

            .tag {
                padding: var(--space-1) var(--space-3);
                border-radius: var(--radius-md);
                font-size: var(--font-size-sm);
                font-weight: 500;
                backdrop-filter: blur(10px);
            }

            .tag-travel {
                background: rgba(37, 99, 235, 0.9);
                color: white;
            }

            .tag-map {
                background: rgba(6, 214, 160, 0.9);
                color: white;
            }

            .placeholder-content {
                text-align: center;
            }

            .placeholder-icon {
                font-size: var(--font-size-4xl);
                margin-bottom: var(--space-2);
            }

            .placeholder-subtitle {
                font-size: var(--font-size-sm);
                color: var(--text-light);
                margin-top: var(--space-1);
            }

            .gradient-bg {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }

            .gradient-bg-2 {
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            }

            .gradient-bg-3 {
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            }

            .gradient-bg-4 {
                background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
            }

            .gradient-bg-5 {
                background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
            }

            .gradient-bg-6 {
                background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            }

            .no-results {
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 300px;
                grid-column: 1 / -1;
            }

            .no-results-content {
                text-align: center;
                color: var(--text-light);
            }

            .no-results-icon {
                font-size: var(--font-size-5xl);
                margin-bottom: var(--space-4);
                opacity: 0.5;
            }

            .development-process {
                padding: var(--space-24) 0;
                background: var(--background-secondary);
            }

            .process-timeline {
                max-width: 800px;
                margin: 0 auto;
                position: relative;
            }

            .process-timeline::before {
                content: '';
                position: absolute;
                left: 50%;
                top: 0;
                bottom: 0;
                width: 2px;
                background: var(--gradient-primary);
                transform: translateX(-50%);
            }

            .timeline-item {
                display: flex;
                align-items: center;
                margin-bottom: var(--space-16);
                position: relative;
            }

            .timeline-item:nth-child(even) {
                flex-direction: row-reverse;
            }

            .timeline-icon {
                width: 60px;
                height: 60px;
                border-radius: 50%;
                background: var(--gradient-primary);
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: var(--font-size-xl);
                color: white;
                margin: 0 var(--space-8);
                z-index: 2;
                position: relative;
            }

            .timeline-content {
                flex: 1;
                max-width: 300px;
                background: white;
                padding: var(--space-6);
                border-radius: var(--radius-xl);
                box-shadow: var(--shadow-md);
            }

            .timeline-content h3 {
                color: var(--text-primary);
                margin-bottom: var(--space-3);
            }

            .timeline-content p {
                color: var(--text-secondary);
                margin: 0;
            }

            /* Mobile styles */
            @media (max-width: 768px) {
                .filter-buttons {
                    gap: var(--space-2);
                }

                .filter-btn {
                    padding: var(--space-2) var(--space-3);
                    font-size: var(--font-size-sm);
                }

                .portfolio-grid {
                    grid-template-columns: 1fr;
                    gap: var(--space-6);
                }

                .app-meta {
                    flex-direction: column;
                    align-items: flex-start;
                    gap: var(--space-3);
                }

                .process-timeline::before {
                    left: 30px;
                }

                .timeline-item {
                    flex-direction: row !important;
                    padding-left: var(--space-16);
                }

                .timeline-item:nth-child(even) {
                    flex-direction: row !important;
                }

                .timeline-icon {
                    position: absolute;
                    left: 0;
                    margin: 0;
                    width: 50px;
                    height: 50px;
                }

                .timeline-content {
                    max-width: none;
                }
            }
        `;
        
        document.head.appendChild(style);
    }

    // Public methods
    searchApps(query) {
        const results = this.apps.filter(app => 
            app.title.toLowerCase().includes(query.toLowerCase()) ||
            app.description.toLowerCase().includes(query.toLowerCase()) ||
            app.categories.some(cat => cat.toLowerCase().includes(query.toLowerCase()))
        );
        
        return results;
    }

    getAppsByCategory(category) {
        return this.apps.filter(app => app.categories.includes(category));
    }

    // Initialize from URL hash
    initFromURL() {
        const hash = window.location.hash.slice(1);
        if (hash && hash !== 'all') {
            const filterButton = document.querySelector(`[data-filter="${hash}"]`);
            if (filterButton) {
                filterButton.click();
            }
        }
    }
}

// Initialize portfolio manager when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const portfolioManager = new PortfolioManager();
    
    // Initialize from URL hash if present
    portfolioManager.initFromURL();
    
    // Handle browser back/forward
    window.addEventListener('popstate', () => {
        portfolioManager.initFromURL();
    });
    
    // Make available globally for debugging
    window.portfolioManager = portfolioManager;
});

// Add additional portfolio-specific functionality
document.addEventListener('DOMContentLoaded', () => {
    // Add lazy loading for images
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                        imageObserver.unobserve(img);
                    }
                }
            });
        });

        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }

    // Add share functionality for apps
    if (navigator.share) {
        const shareButtons = document.querySelectorAll('.share-app');
        shareButtons.forEach(button => {
            button.addEventListener('click', async (e) => {
                e.preventDefault();
                const appCard = button.closest('.app-card');
                const appTitle = appCard.querySelector('.app-title').textContent;
                const appDescription = appCard.querySelector('.app-description').textContent;
                
                try {
                    await navigator.share({
                        title: appTitle,
                        text: appDescription,
                        url: window.location.href
                    });
                } catch (err) {
                    console.log('Error sharing:', err);
                }
            });
        });
    }
});