// Legal pages specific JavaScript

class LegalManager {
    constructor() {
        this.init();
    }

    init() {
        this.setupTableOfContents();
        this.addLegalStyles();
        this.setupSmoothScrolling();
        this.setupReadingProgress();
        this.setupPrintOptimization();
        this.addAccessibilityFeatures();
    }

    setupTableOfContents() {
        const tocLinks = document.querySelectorAll('.toc-link');
        const sections = document.querySelectorAll('.policy-section[id]');
        
        if (!tocLinks.length || !sections.length) return;

        // Add click handlers for TOC links
        tocLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const targetId = link.getAttribute('href').substring(1);
                const targetSection = document.getElementById(targetId);
                
                if (targetSection) {
                    const headerHeight = document.querySelector('.header').offsetHeight;
                    const targetPosition = targetSection.offsetTop - headerHeight - 20;
                    
                    window.scrollTo({
                        top: targetPosition,
                        behavior: 'smooth'
                    });
                }
            });
        });

        // Highlight current section in TOC
        const updateActiveTocItem = () => {
            const scrollPosition = window.scrollY;
            const headerHeight = document.querySelector('.header').offsetHeight;
            
            let currentSection = '';
            
            sections.forEach(section => {
                const sectionTop = section.offsetTop - headerHeight - 100;
                const sectionBottom = sectionTop + section.offsetHeight;
                
                if (scrollPosition >= sectionTop && scrollPosition < sectionBottom) {
                    currentSection = section.getAttribute('id');
                }
            });
            
            tocLinks.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === `#${currentSection}`) {
                    link.classList.add('active');
                }
            });
        };

        // Throttled scroll listener
        let ticking = false;
        const handleScroll = () => {
            if (!ticking) {
                requestAnimationFrame(() => {
                    updateActiveTocItem();
                    ticking = false;
                });
                ticking = true;
            }
        };

        window.addEventListener('scroll', handleScroll, { passive: true });
    }

    setupSmoothScrolling() {
        // Enhance smooth scrolling for all anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                const href = this.getAttribute('href');
                if (href === '#') return;
                
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    const headerHeight = document.querySelector('.header').offsetHeight;
                    const targetPosition = target.offsetTop - headerHeight - 20;
                    
                    window.scrollTo({
                        top: targetPosition,
                        behavior: 'smooth'
                    });
                }
            });
        });
    }

    setupReadingProgress() {
        // Create reading progress bar
        const progressBar = document.createElement('div');
        progressBar.className = 'reading-progress';
        progressBar.innerHTML = '<div class="reading-progress-bar"></div>';
        document.body.appendChild(progressBar);

        const progressBarFill = progressBar.querySelector('.reading-progress-bar');
        
        const updateReadingProgress = () => {
            const windowHeight = window.innerHeight;
            const documentHeight = document.documentElement.scrollHeight;
            const scrollTop = window.scrollY;
            const scrollableHeight = documentHeight - windowHeight;
            const progress = (scrollTop / scrollableHeight) * 100;
            
            progressBarFill.style.width = `${Math.min(progress, 100)}%`;
        };

        window.addEventListener('scroll', updateReadingProgress, { passive: true });
        updateReadingProgress(); // Initial call
    }

    setupPrintOptimization() {
        // Add print-specific optimizations
        const handleBeforePrint = () => {
            // Expand all collapsed sections for printing
            document.querySelectorAll('.collapsed').forEach(el => {
                el.classList.add('print-expanded');
                el.classList.remove('collapsed');
            });
            
            // Add print timestamp
            const printInfo = document.createElement('div');
            printInfo.className = 'print-info';
            printInfo.innerHTML = `
                <p>印刷日時: ${new Date().toLocaleString('ja-JP')}</p>
                <p>URL: ${window.location.href}</p>
            `;
            document.body.appendChild(printInfo);
        };

        const handleAfterPrint = () => {
            // Restore collapsed state
            document.querySelectorAll('.print-expanded').forEach(el => {
                el.classList.remove('print-expanded');
                el.classList.add('collapsed');
            });
            
            // Remove print info
            const printInfo = document.querySelector('.print-info');
            if (printInfo) {
                printInfo.remove();
            }
        };

        window.addEventListener('beforeprint', handleBeforePrint);
        window.addEventListener('afterprint', handleAfterPrint);
    }

    addAccessibilityFeatures() {
        // Add keyboard navigation for TOC
        const tocLinks = document.querySelectorAll('.toc-link');
        tocLinks.forEach((link, index) => {
            link.addEventListener('keydown', (e) => {
                if (e.key === 'ArrowDown' && index < tocLinks.length - 1) {
                    e.preventDefault();
                    tocLinks[index + 1].focus();
                } else if (e.key === 'ArrowUp' && index > 0) {
                    e.preventDefault();
                    tocLinks[index - 1].focus();
                }
            });
        });

        // Add skip links for better navigation
        const skipLinks = document.createElement('div');
        skipLinks.className = 'skip-links';
        skipLinks.innerHTML = `
            <a href="#main-content" class="skip-link">メインコンテンツにスキップ</a>
            <a href="#table-of-contents" class="skip-link">目次にスキップ</a>
        `;
        document.body.insertBefore(skipLinks, document.body.firstChild);

        // Add landmarks
        const main = document.querySelector('main');
        if (main && !main.id) {
            main.id = 'main-content';
        }

        const toc = document.querySelector('.table-of-contents');
        if (toc && !toc.id) {
            toc.id = 'table-of-contents';
        }
    }

    addLegalStyles() {
        if (document.getElementById('legal-styles')) return;

        const style = document.createElement('style');
        style.id = 'legal-styles';
        style.textContent = `
            /* Legal pages specific styles */
            .legal-main {
                padding-top: var(--header-height);
            }

            .legal-hero {
                padding: var(--space-20) 0 var(--space-16);
                background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            }

            .breadcrumb {
                display: flex;
                align-items: center;
                gap: var(--space-2);
                margin-bottom: var(--space-8);
                font-size: var(--font-size-sm);
                color: var(--text-light);
            }

            .breadcrumb a {
                color: var(--primary-color);
                text-decoration: none;
                transition: all var(--transition-base);
            }

            .breadcrumb a:hover {
                text-decoration: underline;
            }

            .breadcrumb-separator {
                color: var(--text-light);
            }

            .breadcrumb-current {
                color: var(--text-secondary);
                font-weight: 500;
            }

            .legal-icon {
                font-size: var(--font-size-5xl);
                text-align: center;
                margin-bottom: var(--space-4);
            }

            .legal-hero .hero-title {
                font-size: var(--font-size-5xl);
                text-align: center;
                margin-bottom: var(--space-6);
            }

            .legal-hero .hero-subtitle {
                text-align: center;
                max-width: 600px;
                margin: 0 auto var(--space-6);
                color: var(--text-secondary);
                font-size: var(--font-size-lg);
            }

            .last-updated {
                text-align: center;
                padding: var(--space-4);
                background: rgba(255, 255, 255, 0.8);
                border-radius: var(--radius-lg);
                border: 1px solid var(--border-color);
                max-width: 300px;
                margin: 0 auto;
            }

            .update-label {
                color: var(--text-light);
                font-size: var(--font-size-sm);
                margin-right: var(--space-2);
            }

            .update-date {
                color: var(--text-primary);
                font-weight: 600;
            }

            .table-of-contents {
                padding: var(--space-16) 0;
            }

            .toc-card {
                background: white;
                border-radius: var(--radius-xl);
                padding: var(--space-8);
                box-shadow: var(--shadow-md);
                max-width: 600px;
                margin: 0 auto;
            }

            .toc-title {
                font-size: var(--font-size-2xl);
                font-weight: 600;
                margin-bottom: var(--space-6);
                text-align: center;
                color: var(--text-primary);
            }

            .toc-list {
                list-style: none;
                padding: 0;
                margin: 0;
            }

            .toc-list li {
                margin-bottom: var(--space-2);
            }

            .toc-link {
                display: block;
                padding: var(--space-3) var(--space-4);
                color: var(--text-secondary);
                text-decoration: none;
                border-radius: var(--radius-md);
                transition: all var(--transition-base);
                border-left: 3px solid transparent;
            }

            .toc-link:hover,
            .toc-link.active {
                background: rgba(37, 99, 235, 0.05);
                color: var(--primary-color);
                border-left-color: var(--primary-color);
                transform: translateX(4px);
            }

            .policy-content {
                padding: var(--space-20) 0;
                background: var(--background-secondary);
            }

            .content-wrapper {
                max-width: 800px;
                margin: 0 auto;
            }

            .policy-section {
                background: white;
                border-radius: var(--radius-xl);
                padding: var(--space-8);
                margin-bottom: var(--space-8);
                box-shadow: var(--shadow-md);
            }

            .section-icon {
                font-size: var(--font-size-3xl);
                text-align: center;
                margin-bottom: var(--space-4);
            }

            .section-title {
                font-size: var(--font-size-2xl);
                font-weight: 600;
                margin-bottom: var(--space-6);
                color: var(--text-primary);
                text-align: center;
            }

            .section-content {
                line-height: 1.7;
                color: var(--text-secondary);
            }

            .section-content p {
                margin-bottom: var(--space-4);
                font-size: var(--font-size-base);
            }

            .section-content h4 {
                font-size: var(--font-size-lg);
                font-weight: 600;
                margin: var(--space-6) 0 var(--space-3);
                color: var(--text-primary);
            }

            .section-content h5 {
                font-size: var(--font-size-base);
                font-weight: 600;
                margin: var(--space-4) 0 var(--space-2);
                color: var(--text-primary);
            }

            .section-content ul,
            .section-content ol {
                margin: var(--space-4) 0;
                padding-left: var(--space-6);
            }

            .section-content li {
                margin-bottom: var(--space-2);
                line-height: 1.6;
            }

            /* Highlight boxes */
            .highlight-box,
            .detail-box,
            .note-box,
            .preamble-box {
                background: rgba(37, 99, 235, 0.05);
                border: 1px solid rgba(37, 99, 235, 0.2);
                border-radius: var(--radius-lg);
                padding: var(--space-6);
                margin: var(--space-6) 0;
            }

            .preamble-box {
                background: rgba(6, 214, 160, 0.05);
                border-color: rgba(6, 214, 160, 0.2);
            }

            .note-box {
                background: rgba(245, 158, 11, 0.05);
                border-color: rgba(245, 158, 11, 0.2);
            }

            .consequences-box,
            .limitation-box,
            .communication-protection {
                background: rgba(239, 68, 68, 0.05);
                border: 1px solid rgba(239, 68, 68, 0.2);
                border-radius: var(--radius-lg);
                padding: var(--space-6);
                margin: var(--space-6) 0;
            }

            /* Grid layouts */
            .purpose-grid,
            .prohibited-grid,
            .security-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: var(--space-4);
                margin: var(--space-6) 0;
            }

            .purpose-item,
            .prohibited-item,
            .security-item {
                background: var(--background-secondary);
                border-radius: var(--radius-lg);
                padding: var(--space-4);
                text-align: center;
                transition: all var(--transition-base);
            }

            .purpose-item:hover,
            .prohibited-item:hover,
            .security-item:hover {
                transform: translateY(-4px);
                box-shadow: var(--shadow-lg);
            }

            .purpose-icon,
            .prohibited-icon,
            .security-icon {
                font-size: var(--font-size-2xl);
                margin-bottom: var(--space-2);
            }

            /* Exception list */
            .exception-list {
                margin: var(--space-6) 0;
            }

            .exception-item {
                display: flex;
                gap: var(--space-4);
                margin-bottom: var(--space-6);
                padding: var(--space-4);
                background: var(--background-secondary);
                border-radius: var(--radius-lg);
            }

            .exception-number {
                width: 40px;
                height: 40px;
                background: var(--primary-color);
                color: white;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: 600;
                flex-shrink: 0;
            }

            .exception-content h4 {
                margin: 0 0 var(--space-2);
                color: var(--text-primary);
            }

            .exception-content p {
                margin: 0;
                font-size: var(--font-size-sm);
            }

            /* Process flows */
            .inquiry-process,
            .registration-flow,
            .delivery-flow {
                margin: var(--space-6) 0;
            }

            .process-step,
            .flow-step {
                display: flex;
                align-items: center;
                gap: var(--space-4);
                margin-bottom: var(--space-4);
                padding: var(--space-4);
                background: var(--background-secondary);
                border-radius: var(--radius-lg);
            }

            .step-number {
                width: 40px;
                height: 40px;
                background: var(--gradient-primary);
                color: white;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: 600;
                flex-shrink: 0;
            }

            .step-content h4 {
                margin: 0 0 var(--space-1);
                font-size: var(--font-size-base);
            }

            .step-content p {
                margin: 0;
                font-size: var(--font-size-sm);
                color: var(--text-light);
            }

            /* Business info section */
            .business-info {
                padding: var(--space-16) 0;
            }

            .info-card {
                background: white;
                border-radius: var(--radius-xl);
                padding: var(--space-8);
                box-shadow: var(--shadow-lg);
            }

            .card-title {
                font-size: var(--font-size-3xl);
                font-weight: 600;
                text-align: center;
                margin-bottom: var(--space-8);
                color: var(--text-primary);
            }

            .info-grid {
                display: grid;
                gap: var(--space-6);
            }

            .info-item {
                display: flex;
                gap: var(--space-4);
                padding: var(--space-6);
                background: var(--background-secondary);
                border-radius: var(--radius-lg);
            }

            .info-icon {
                font-size: var(--font-size-2xl);
                flex-shrink: 0;
            }

            .info-content h3 {
                margin: 0 0 var(--space-2);
                font-size: var(--font-size-lg);
                color: var(--text-primary);
            }

            .info-content p {
                margin: 0 0 var(--space-2);
            }

            .note {
                font-size: var(--font-size-sm);
                color: var(--text-light);
                font-style: italic;
            }

            /* Reading progress */
            .reading-progress {
                position: fixed;
                top: var(--header-height);
                left: 0;
                width: 100%;
                height: 3px;
                background: rgba(37, 99, 235, 0.1);
                z-index: var(--z-fixed);
            }

            .reading-progress-bar {
                height: 100%;
                background: var(--gradient-primary);
                width: 0%;
                transition: width 0.3s ease-out;
            }

            /* Skip links for accessibility */
            .skip-links {
                position: absolute;
                top: -100px;
                left: 0;
                z-index: 10000;
            }

            .skip-link {
                position: absolute;
                top: 100px;
                left: var(--space-4);
                background: var(--primary-color);
                color: white;
                padding: var(--space-2) var(--space-4);
                border-radius: var(--radius-md);
                text-decoration: none;
                font-weight: 500;
                transform: translateY(-100px);
                transition: transform var(--transition-base);
            }

            .skip-link:focus {
                transform: translateY(0);
            }

            /* Contact sections */
            .terms-contact,
            .commercial-contact,
            .policy-updates {
                padding: var(--space-16) 0;
            }

            .contact-card,
            .updates-card {
                background: white;
                border-radius: var(--radius-2xl);
                padding: var(--space-12);
                box-shadow: var(--shadow-xl);
                text-align: center;
                max-width: 600px;
                margin: 0 auto;
            }

            .contact-icon,
            .updates-icon {
                font-size: var(--font-size-4xl);
                margin-bottom: var(--space-4);
            }

            .contact-title,
            .updates-title {
                font-size: var(--font-size-2xl);
                font-weight: 600;
                margin-bottom: var(--space-4);
                color: var(--text-primary);
            }

            .contact-description,
            .updates-description {
                color: var(--text-secondary);
                margin-bottom: var(--space-6);
                font-size: var(--font-size-lg);
                line-height: 1.6;
            }

            .contact-actions,
            .updates-action {
                display: flex;
                gap: var(--space-4);
                justify-content: center;
                flex-wrap: wrap;
            }

            /* Mobile optimizations */
            @media (max-width: 768px) {
                .legal-hero {
                    padding: var(--space-16) 0 var(--space-12);
                }

                .legal-hero .hero-title {
                    font-size: var(--font-size-4xl);
                }

                .toc-card {
                    margin: 0 var(--space-4);
                }

                .content-wrapper {
                    padding: 0 var(--space-4);
                }

                .policy-section {
                    padding: var(--space-6);
                    margin-bottom: var(--space-6);
                }

                .purpose-grid,
                .prohibited-grid,
                .security-grid {
                    grid-template-columns: 1fr;
                }

                .exception-item,
                .process-step,
                .flow-step {
                    flex-direction: column;
                    text-align: center;
                }

                .exception-number,
                .step-number {
                    align-self: center;
                }

                .info-item {
                    flex-direction: column;
                    text-align: center;
                }

                .contact-actions,
                .updates-action {
                    flex-direction: column;
                    align-items: center;
                }
            }

            /* Print styles */
            @media print {
                .reading-progress,
                .skip-links,
                .back-to-top {
                    display: none !important;
                }

                .policy-section {
                    break-inside: avoid;
                    page-break-inside: avoid;
                }

                .section-title {
                    page-break-after: avoid;
                }

                .print-info {
                    position: fixed;
                    bottom: 0;
                    left: 0;
                    right: 0;
                    padding: var(--space-2);
                    background: #f8f9fa;
                    border-top: 1px solid #ddd;
                    font-size: 10pt;
                    color: #666;
                }
            }
        `;
        
        document.head.appendChild(style);
    }

    // Public methods
    scrollToSection(sectionId) {
        const section = document.getElementById(sectionId);
        if (section) {
            const headerHeight = document.querySelector('.header').offsetHeight;
            const targetPosition = section.offsetTop - headerHeight - 20;
            
            window.scrollTo({
                top: targetPosition,
                behavior: 'smooth'
            });
        }
    }

    highlightText(query) {
        if (!query) return;
        
        const walker = document.createTreeWalker(
            document.body,
            NodeFilter.SHOW_TEXT,
            null,
            false
        );

        const textNodes = [];
        let node;
        
        while (node = walker.nextNode()) {
            if (node.parentElement.tagName !== 'SCRIPT' && 
                node.parentElement.tagName !== 'STYLE') {
                textNodes.push(node);
            }
        }

        textNodes.forEach(textNode => {
            const text = textNode.textContent;
            if (text.toLowerCase().includes(query.toLowerCase())) {
                const regex = new RegExp(`(${query})`, 'gi');
                const highlightedText = text.replace(regex, '<mark>$1</mark>');
                
                const wrapper = document.createElement('span');
                wrapper.innerHTML = highlightedText;
                textNode.parentNode.replaceChild(wrapper, textNode);
            }
        });
    }

    clearHighlights() {
        const marks = document.querySelectorAll('mark');
        marks.forEach(mark => {
            const parent = mark.parentNode;
            parent.replaceChild(document.createTextNode(mark.textContent), mark);
            parent.normalize();
        });
    }
}

// Initialize legal manager
document.addEventListener('DOMContentLoaded', () => {
    const legalManager = new LegalManager();
    
    // Make available globally for debugging
    window.legalManager = legalManager;
    
    // Add keyboard shortcuts for legal pages
    document.addEventListener('keydown', (e) => {
        // Ctrl/Cmd + F: Focus search (if available)
        if ((e.ctrlKey || e.metaKey) && e.key === 'f' && !e.defaultPrevented) {
            // Let browser handle default search
        }
        
        // Ctrl/Cmd + P: Optimize for printing
        if ((e.ctrlKey || e.metaKey) && e.key === 'p') {
            // Print optimization will be handled by print event listeners
        }
        
        // Alt + T: Scroll to table of contents
        if (e.altKey && e.key === 't') {
            e.preventDefault();
            const toc = document.getElementById('table-of-contents');
            if (toc) {
                legalManager.scrollToSection('table-of-contents');
            }
        }
    });
});