// Blog-specific JavaScript

class BlogManager {
    constructor() {
        this.posts = [];
        this.filteredPosts = [];
        this.currentFilter = 'all';
        this.currentSearch = '';
        this.init();
    }

    init() {
        this.collectPosts();
        this.setupSearch();
        this.setupCategoryFilter();
        this.addBlogStyles();
        this.setupPostInteractions();
        this.initializeAnimations();
    }

    collectPosts() {
        const postCards = document.querySelectorAll('.post-card');
        this.posts = Array.from(postCards).map(card => ({
            element: card,
            title: card.querySelector('.post-title').textContent,
            excerpt: card.querySelector('.post-excerpt').textContent,
            category: card.querySelector('.post-category').textContent,
            categories: card.getAttribute('data-category').split(' '),
            tags: Array.from(card.querySelectorAll('.tag')).map(tag => tag.textContent)
        }));
        this.filteredPosts = [...this.posts];
    }

    setupSearch() {
        const searchInput = document.getElementById('blog-search');
        if (!searchInput) return;

        const debounce = (func, wait) => {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    clearTimeout(timeout);
                    func(...args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        };

        const handleSearch = debounce((query) => {
            this.currentSearch = query.toLowerCase();
            this.filterAndDisplayPosts();
        }, 300);

        searchInput.addEventListener('input', (e) => {
            handleSearch(e.target.value);
        });

        // Add search animation
        searchInput.addEventListener('focus', () => {
            searchInput.parentElement.classList.add('focused');
        });

        searchInput.addEventListener('blur', () => {
            if (!searchInput.value) {
                searchInput.parentElement.classList.remove('focused');
            }
        });
    }

    setupCategoryFilter() {
        const categoryFilter = document.getElementById('category-filter');
        if (!categoryFilter) return;

        categoryFilter.addEventListener('change', (e) => {
            this.currentFilter = e.target.value;
            this.filterAndDisplayPosts();
        });
    }

    filterAndDisplayPosts() {
        const postsGrid = document.getElementById('posts-grid');
        const noResults = document.getElementById('blog-no-results');
        
        // Filter posts
        this.filteredPosts = this.posts.filter(post => {
            const matchesCategory = this.currentFilter === 'all' || 
                                  post.categories.includes(this.currentFilter);
            
            const matchesSearch = !this.currentSearch || 
                                post.title.toLowerCase().includes(this.currentSearch) ||
                                post.excerpt.toLowerCase().includes(this.currentSearch) ||
                                post.tags.some(tag => tag.toLowerCase().includes(this.currentSearch));
            
            return matchesCategory && matchesSearch;
        });

        // Hide all posts first
        this.posts.forEach(post => {
            post.element.style.display = 'none';
            post.element.style.opacity = '0';
        });

        // Show filtered posts with animation
        if (this.filteredPosts.length > 0) {
            noResults.style.display = 'none';
            this.filteredPosts.forEach((post, index) => {
                post.element.style.display = 'block';
                setTimeout(() => {
                    post.element.style.opacity = '1';
                    post.element.style.transform = 'translateY(0)';
                }, index * 100);
            });
        } else {
            noResults.style.display = 'flex';
            noResults.style.animation = 'fadeIn 0.3s ease-out forwards';
        }

        // Update results count
        this.updateResultsCount();
    }

    updateResultsCount() {
        const existingCount = document.querySelector('.results-count');
        if (existingCount) {
            existingCount.remove();
        }

        if (this.currentSearch || this.currentFilter !== 'all') {
            const postsGrid = document.getElementById('posts-grid');
            const count = document.createElement('div');
            count.className = 'results-count';
            count.textContent = `${this.filteredPosts.length}件の記事が見つかりました`;
            postsGrid.parentElement.insertBefore(count, postsGrid);
        }
    }

    setupPostInteractions() {
        const postCards = document.querySelectorAll('.post-card');
        
        postCards.forEach(card => {
            // Add enhanced hover effects
            card.addEventListener('mouseenter', this.onPostHover.bind(this));
            card.addEventListener('mouseleave', this.onPostLeave.bind(this));
            
            // Add click handling for future navigation
            card.addEventListener('click', (e) => {
                const postTitle = card.querySelector('.post-title').textContent;
                console.log(`Post clicked: ${postTitle}`);
                
                // Show coming soon notification
                this.showComingSoonNotification();
            });

            // Add keyboard navigation
            card.setAttribute('tabindex', '0');
            card.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    card.click();
                }
            });
        });
    }

    onPostHover(e) {
        const card = e.target.closest('.post-card');
        const image = card.querySelector('.placeholder-image');
        
        if (image) {
            image.style.transform = 'scale(1.05)';
        }

        // Add subtle glow effect
        card.style.boxShadow = '0 20px 40px rgba(37, 99, 235, 0.15)';
        
        // Animate post icon
        const icon = card.querySelector('.post-icon');
        if (icon) {
            icon.style.transform = 'scale(1.2)';
        }
    }

    onPostLeave(e) {
        const card = e.target.closest('.post-card');
        const image = card.querySelector('.placeholder-image');
        
        if (image) {
            image.style.transform = '';
        }

        card.style.boxShadow = '';
        
        // Reset post icon
        const icon = card.querySelector('.post-icon');
        if (icon) {
            icon.style.transform = '';
        }
    }

    showComingSoonNotification() {
        // Create notification
        const notification = document.createElement('div');
        notification.className = 'blog-notification';
        notification.innerHTML = `
            <div class="notification-content">
                <div class="notification-icon">📝</div>
                <div class="notification-text">
                    <h4>記事は準備中です</h4>
                    <p>現在執筆中です。公開開始時はTwitterでお知らせいたします。</p>
                </div>
                <button class="notification-close">&times;</button>
            </div>
        `;
        
        // Add to DOM
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.classList.add('show');
        }, 10);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            this.removeNotification(notification);
        }, 5000);
        
        // Close button
        const closeBtn = notification.querySelector('.notification-close');
        closeBtn.addEventListener('click', () => {
            this.removeNotification(notification);
        });
        
        // Click outside to close
        notification.addEventListener('click', (e) => {
            if (e.target === notification) {
                this.removeNotification(notification);
            }
        });
    }

    removeNotification(notification) {
        notification.classList.remove('show');
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }

    initializeAnimations() {
        // Add stagger animation to post cards
        const postCards = document.querySelectorAll('.post-card');
        postCards.forEach((card, index) => {
            card.style.animationDelay = `${index * 0.1}s`;
            card.style.transform = 'translateY(20px)';
            card.style.opacity = '0';
            
            setTimeout(() => {
                card.style.transition = 'all 0.6s ease-out';
                card.style.transform = 'translateY(0)';
                card.style.opacity = '1';
            }, 100 + (index * 100));
        });

        // Animate newsletter floating elements
        const floatingItems = document.querySelectorAll('.floating-item');
        floatingItems.forEach((item, index) => {
            item.style.animationDelay = `${index * 0.5}s`;
        });
    }

    addBlogStyles() {
        if (document.getElementById('blog-styles')) return;

        const style = document.createElement('style');
        style.id = 'blog-styles';
        style.textContent = `
            /* Blog-specific styles */
            .blog-main {
                padding-top: var(--header-height);
            }

            .blog-hero {
                padding: var(--space-20) 0;
                background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            }

            .blog-hero .hero-title {
                font-size: var(--font-size-5xl);
                text-align: center;
                margin-bottom: var(--space-6);
            }

            .blog-hero .hero-subtitle {
                text-align: center;
                max-width: 600px;
                margin: 0 auto var(--space-8);
                color: var(--text-secondary);
                font-size: var(--font-size-lg);
            }

            .blog-controls {
                display: flex;
                gap: var(--space-4);
                justify-content: center;
                align-items: center;
                flex-wrap: wrap;
                max-width: 600px;
                margin: 0 auto;
            }

            .search-box {
                position: relative;
                flex: 1;
                min-width: 250px;
            }

            .search-input {
                width: 100%;
                padding: var(--space-3) var(--space-4) var(--space-3) var(--space-12);
                border: 2px solid var(--border-color);
                border-radius: var(--radius-lg);
                font-size: var(--font-size-base);
                transition: all var(--transition-base);
                background: white;
            }

            .search-input:focus {
                outline: none;
                border-color: var(--primary-color);
                box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
            }

            .search-icon {
                position: absolute;
                left: var(--space-4);
                top: 50%;
                transform: translateY(-50%);
                color: var(--text-light);
                font-size: var(--font-size-lg);
            }

            .search-box.focused .search-icon {
                color: var(--primary-color);
            }

            .filter-select {
                padding: var(--space-3) var(--space-4);
                border: 2px solid var(--border-color);
                border-radius: var(--radius-lg);
                font-size: var(--font-size-base);
                background: white;
                cursor: pointer;
                transition: all var(--transition-base);
            }

            .filter-select:focus {
                outline: none;
                border-color: var(--primary-color);
                box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
            }

            .featured-post {
                padding: var(--space-16) 0;
            }

            .featured-card {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: var(--space-8);
                background: white;
                border-radius: var(--radius-2xl);
                overflow: hidden;
                box-shadow: var(--shadow-xl);
                transition: all var(--transition-base);
            }

            .featured-card:hover {
                transform: translateY(-8px);
                box-shadow: 0 30px 60px rgba(0, 0, 0, 0.12);
            }

            .featured-image {
                position: relative;
                min-height: 300px;
            }

            .blog-featured-bg {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                height: 100%;
                display: flex;
                align-items: center;
                justify-content: center;
            }

            .featured-content {
                text-align: center;
                color: white;
            }

            .featured-icon {
                font-size: var(--font-size-5xl);
                margin-bottom: var(--space-4);
            }

            .featured-badge {
                background: rgba(255, 255, 255, 0.2);
                color: white;
                padding: var(--space-2) var(--space-4);
                border-radius: var(--radius-lg);
                font-weight: 600;
                backdrop-filter: blur(10px);
            }

            .featured-text {
                padding: var(--space-8);
                display: flex;
                flex-direction: column;
                justify-content: center;
            }

            .featured-title {
                font-size: var(--font-size-3xl);
                font-weight: 700;
                margin-bottom: var(--space-4);
                line-height: 1.3;
            }

            .featured-excerpt {
                font-size: var(--font-size-lg);
                color: var(--text-secondary);
                margin-bottom: var(--space-6);
                line-height: 1.6;
            }

            .featured-tags {
                display: flex;
                flex-wrap: wrap;
                gap: var(--space-2);
                margin-bottom: var(--space-6);
            }

            .featured-action .btn.disabled {
                opacity: 0.6;
                cursor: not-allowed;
                pointer-events: none;
            }

            .blog-posts {
                padding: var(--space-20) 0;
                background: var(--background-secondary);
            }

            .posts-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
                gap: var(--space-8);
            }

            .post-card {
                background: white;
                border-radius: var(--radius-xl);
                overflow: hidden;
                box-shadow: var(--shadow-md);
                transition: all var(--transition-base);
                cursor: pointer;
            }

            .post-image {
                position: relative;
                height: 200px;
                overflow: hidden;
            }

            .post-placeholder {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100%;
                color: white;
                text-align: center;
            }

            .post-icon {
                font-size: var(--font-size-4xl);
                margin-bottom: var(--space-3);
                transition: transform var(--transition-base);
            }

            .status-badge {
                background: rgba(255, 255, 255, 0.2);
                color: white;
                padding: var(--space-1) var(--space-3);
                border-radius: var(--radius-md);
                font-size: var(--font-size-sm);
                font-weight: 500;
                backdrop-filter: blur(10px);
            }

            .post-bg-1 { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
            .post-bg-2 { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
            .post-bg-3 { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }
            .post-bg-4 { background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); }
            .post-bg-5 { background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); }
            .post-bg-6 { background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); }

            .post-content {
                padding: var(--space-6);
            }

            .post-meta {
                display: flex;
                align-items: center;
                gap: var(--space-3);
                margin-bottom: var(--space-4);
                font-size: var(--font-size-sm);
                color: var(--text-light);
            }

            .post-category {
                background: var(--primary-color);
                color: white;
                padding: var(--space-1) var(--space-2);
                border-radius: var(--radius-sm);
                font-weight: 500;
            }

            .read-time {
                color: var(--text-light);
            }

            .post-title {
                font-size: var(--font-size-xl);
                font-weight: 600;
                margin-bottom: var(--space-3);
                line-height: 1.4;
            }

            .post-excerpt {
                color: var(--text-secondary);
                margin-bottom: var(--space-4);
                line-height: 1.6;
            }

            .post-tags {
                display: flex;
                flex-wrap: wrap;
                gap: var(--space-2);
            }

            .tag {
                padding: var(--space-1) var(--space-3);
                background: var(--background-secondary);
                color: var(--text-secondary);
                border-radius: var(--radius-md);
                font-size: var(--font-size-sm);
                font-weight: 500;
            }

            .results-count {
                text-align: center;
                color: var(--text-light);
                margin-bottom: var(--space-6);
                font-size: var(--font-size-sm);
            }

            .newsletter {
                padding: var(--space-20) 0;
            }

            .newsletter-card {
                background: white;
                border-radius: var(--radius-2xl);
                padding: var(--space-12);
                box-shadow: var(--shadow-xl);
                display: grid;
                grid-template-columns: 1fr auto;
                gap: var(--space-8);
                align-items: center;
            }

            .newsletter-content {
                text-align: center;
            }

            .newsletter-icon {
                font-size: var(--font-size-4xl);
                margin-bottom: var(--space-4);
            }

            .newsletter-title {
                font-size: var(--font-size-2xl);
                font-weight: 600;
                margin-bottom: var(--space-3);
            }

            .newsletter-description {
                color: var(--text-secondary);
                margin-bottom: var(--space-6);
                font-size: var(--font-size-lg);
            }

            .newsletter-visual {
                position: relative;
                width: 200px;
                height: 200px;
            }

            .floating-elements {
                position: relative;
                width: 100%;
                height: 100%;
            }

            .floating-item {
                position: absolute;
                font-size: var(--font-size-3xl);
                animation: float 6s ease-in-out infinite;
            }

            .floating-item:nth-child(1) {
                top: 0;
                left: 0;
                animation-delay: 0s;
            }

            .floating-item:nth-child(2) {
                top: 0;
                right: 0;
                animation-delay: 1.5s;
            }

            .floating-item:nth-child(3) {
                bottom: 0;
                left: 0;
                animation-delay: 3s;
            }

            .floating-item:nth-child(4) {
                bottom: 0;
                right: 0;
                animation-delay: 4.5s;
            }

            .blog-notification {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0, 0, 0, 0.5);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 10000;
                opacity: 0;
                visibility: hidden;
                transition: all var(--transition-base);
            }

            .blog-notification.show {
                opacity: 1;
                visibility: visible;
            }

            .notification-content {
                background: white;
                border-radius: var(--radius-xl);
                padding: var(--space-8);
                max-width: 400px;
                margin: var(--space-4);
                position: relative;
                text-align: center;
                transform: scale(0.8);
                transition: transform var(--transition-base);
            }

            .blog-notification.show .notification-content {
                transform: scale(1);
            }

            .notification-icon {
                font-size: var(--font-size-4xl);
                margin-bottom: var(--space-4);
            }

            .notification-close {
                position: absolute;
                top: var(--space-4);
                right: var(--space-4);
                width: 30px;
                height: 30px;
                border: none;
                background: var(--background-secondary);
                border-radius: 50%;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: var(--font-size-lg);
                transition: all var(--transition-base);
            }

            .notification-close:hover {
                background: var(--border-color);
            }

            /* Mobile styles */
            @media (max-width: 768px) {
                .blog-controls {
                    flex-direction: column;
                    align-items: stretch;
                }

                .search-box {
                    min-width: auto;
                }

                .featured-card {
                    grid-template-columns: 1fr;
                }

                .featured-image {
                    min-height: 200px;
                }

                .posts-grid {
                    grid-template-columns: 1fr;
                    gap: var(--space-6);
                }

                .newsletter-card {
                    grid-template-columns: 1fr;
                    text-align: center;
                }

                .newsletter-visual {
                    width: 150px;
                    height: 150px;
                    margin: 0 auto;
                }
            }
        `;
        
        document.head.appendChild(style);
    }

    // Public methods
    searchPosts(query) {
        this.currentSearch = query.toLowerCase();
        this.filterAndDisplayPosts();
    }

    filterByCategory(category) {
        this.currentFilter = category;
        const categorySelect = document.getElementById('category-filter');
        if (categorySelect) {
            categorySelect.value = category;
        }
        this.filterAndDisplayPosts();
    }

    resetFilters() {
        this.currentFilter = 'all';
        this.currentSearch = '';
        const searchInput = document.getElementById('blog-search');
        const categorySelect = document.getElementById('category-filter');
        
        if (searchInput) searchInput.value = '';
        if (categorySelect) categorySelect.value = 'all';
        
        this.filterAndDisplayPosts();
    }
}

// Initialize blog manager
document.addEventListener('DOMContentLoaded', () => {
    const blogManager = new BlogManager();
    
    // Make available globally for debugging
    window.blogManager = blogManager;
    
    // Add keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        // Ctrl/Cmd + F: Focus search
        if ((e.ctrlKey || e.metaKey) && e.key === 'f') {
            e.preventDefault();
            const searchInput = document.getElementById('blog-search');
            if (searchInput) {
                searchInput.focus();
            }
        }
        
        // Escape: Clear search
        if (e.key === 'Escape') {
            const searchInput = document.getElementById('blog-search');
            if (searchInput && document.activeElement === searchInput) {
                searchInput.blur();
                if (searchInput.value) {
                    searchInput.value = '';
                    blogManager.searchPosts('');
                }
            }
        }
    });
});