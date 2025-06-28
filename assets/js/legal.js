// Legal Pages JavaScript - Accessibility & UX Features

document.addEventListener('DOMContentLoaded', function() {
    initLegalPageFeatures();
});

function initLegalPageFeatures() {
    // Initialize all legal page features
    initSmoothScrolling();
    initTableOfContents();
    initKeyboardNavigation();
    initAriaAttributes();
    initPrintOptimization();
    
    // Announce page load for screen readers
    announcePageLoad();
}

// Smooth scrolling for table of contents links
function initSmoothScrolling() {
    const tocLinks = document.querySelectorAll('.toc-link');
    
    tocLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                // Calculate offset for fixed header
                const headerHeight = document.querySelector('.header')?.offsetHeight || 70;
                const targetPosition = targetElement.offsetTop - headerHeight - 20;
                
                // Smooth scroll
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
                
                // Update focus for accessibility
                targetElement.focus();
                
                // Update active link in TOC
                updateActiveTocLink(this);
                
                // Announce to screen readers
                announceNavigation(targetElement);
            }
        });
    });
}

// Table of contents functionality
function initTableOfContents() {
    const sections = document.querySelectorAll('.policy-section[id]');
    const tocLinks = document.querySelectorAll('.toc-link');
    
    if (sections.length === 0 || tocLinks.length === 0) return;
    
    // Highlight current section in TOC based on scroll position
    function updateTocOnScroll() {
        const scrollPosition = window.scrollY + 100;
        
        let currentSection = null;
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            if (scrollPosition >= sectionTop) {
                currentSection = section;
            }
        });
        
        if (currentSection) {
            const activeId = currentSection.getAttribute('id');
            const activeLink = document.querySelector(`.toc-link[href="#${activeId}"]`);
            updateActiveTocLink(activeLink);
        }
    }
    
    // Throttled scroll listener
    let scrollTimeout;
    window.addEventListener('scroll', function() {
        if (scrollTimeout) clearTimeout(scrollTimeout);
        scrollTimeout = setTimeout(updateTocOnScroll, 10);
    });
    
    // Initial check
    updateTocOnScroll();
}

// Update active link in table of contents
function updateActiveTocLink(activeLink) {
    if (!activeLink) return;
    
    // Remove active class from all links
    document.querySelectorAll('.toc-link').forEach(link => {
        link.classList.remove('active');
        link.removeAttribute('aria-current');
    });
    
    // Add active class to current link
    activeLink.classList.add('active');
    activeLink.setAttribute('aria-current', 'location');
}

// Enhanced keyboard navigation
function initKeyboardNavigation() {
    // Add keyboard support for TOC navigation
    const tocLinks = document.querySelectorAll('.toc-link');
    
    tocLinks.forEach((link, index) => {
        link.addEventListener('keydown', function(e) {
            let targetIndex;
            
            switch(e.key) {
                case 'ArrowDown':
                    e.preventDefault();
                    targetIndex = (index + 1) % tocLinks.length;
                    tocLinks[targetIndex].focus();
                    break;
                    
                case 'ArrowUp':
                    e.preventDefault();
                    targetIndex = (index - 1 + tocLinks.length) % tocLinks.length;
                    tocLinks[targetIndex].focus();
                    break;
                    
                case 'Home':
                    e.preventDefault();
                    tocLinks[0].focus();
                    break;
                    
                case 'End':
                    e.preventDefault();
                    tocLinks[tocLinks.length - 1].focus();
                    break;
            }
        });
    });
    
    // Add skip links for better accessibility
    addSkipLinks();
}

// Add skip links for better accessibility
function addSkipLinks() {
    const skipLinksHtml = `
        <div class="skip-links" aria-label="Skip navigation links">
            <a href="#main-content" class="skip-link">Skip to main content</a>
            <a href="#table-of-contents" class="skip-link">Skip to table of contents</a>
        </div>
    `;
    
    document.body.insertAdjacentHTML('afterbegin', skipLinksHtml);
    
    // Add CSS for skip links
    const skipLinksStyle = document.createElement('style');
    skipLinksStyle.textContent = `
        .skip-links {
            position: absolute;
            top: -100px;
            left: 0;
            z-index: 9999;
        }
        
        .skip-link {
            position: absolute;
            top: -100px;
            left: 10px;
            background: var(--primary-color);
            color: white;
            padding: 8px 16px;
            text-decoration: none;
            border-radius: 4px;
            font-weight: 500;
            transition: top 0.2s ease;
        }
        
        .skip-link:focus {
            top: 10px;
        }
    `;
    document.head.appendChild(skipLinksStyle);
}

// Initialize ARIA attributes for better accessibility
function initAriaAttributes() {
    // Add main content landmark
    const mainContent = document.querySelector('.legal-main');
    if (mainContent) {
        mainContent.setAttribute('id', 'main-content');
        mainContent.setAttribute('role', 'main');
        mainContent.setAttribute('aria-label', 'Legal document content');
    }
    
    // Add table of contents landmark
    const toc = document.querySelector('.table-of-contents');
    if (toc) {
        toc.setAttribute('id', 'table-of-contents');
        toc.setAttribute('role', 'navigation');
        toc.setAttribute('aria-label', 'Table of contents');
    }
    
    // Make sections focusable for better navigation
    const sections = document.querySelectorAll('.policy-section[id]');
    sections.forEach(section => {
        section.setAttribute('tabindex', '-1');
        const title = section.querySelector('.section-title');
        if (title) {
            section.setAttribute('aria-labelledby', title.id || generateId('section-title'));
            if (!title.id) {
                title.id = generateId('section-title');
            }
        }
    });
    
    // Add proper heading hierarchy
    ensureHeadingHierarchy();
}

// Ensure proper heading hierarchy for screen readers
function ensureHeadingHierarchy() {
    const h1 = document.querySelector('h1');
    if (h1) {
        h1.setAttribute('tabindex', '-1');
    }
    
    // Ensure section titles are properly nested
    const sectionTitles = document.querySelectorAll('.section-title');
    sectionTitles.forEach(title => {
        if (title.tagName !== 'H2') {
            const h2 = document.createElement('h2');
            h2.className = title.className;
            h2.innerHTML = title.innerHTML;
            h2.id = title.id;
            title.parentNode.replaceChild(h2, title);
        }
    });
}

// Generate unique IDs
function generateId(prefix) {
    return prefix + '-' + Math.random().toString(36).substr(2, 9);
}

// Announce page load for screen readers
function announcePageLoad() {
    const pageTitle = document.querySelector('h1')?.textContent || 'Legal document';
    const announcement = document.createElement('div');
    announcement.setAttribute('aria-live', 'polite');
    announcement.setAttribute('aria-atomic', 'true');
    announcement.className = 'sr-only';
    announcement.textContent = `${pageTitle} loaded. Use the table of contents to navigate sections.`;
    
    document.body.appendChild(announcement);
    
    // Remove announcement after it's been read
    setTimeout(() => {
        announcement.remove();
    }, 3000);
}

// Announce navigation for screen readers
function announceNavigation(targetElement) {
    const sectionTitle = targetElement.querySelector('.section-title')?.textContent || 'Section';
    const announcement = document.createElement('div');
    announcement.setAttribute('aria-live', 'polite');
    announcement.className = 'sr-only';
    announcement.textContent = `Navigated to ${sectionTitle}`;
    
    document.body.appendChild(announcement);
    
    setTimeout(() => {
        announcement.remove();
    }, 2000);
}

// Print optimization
function initPrintOptimization() {
    // Add print button if needed
    const printButton = document.createElement('button');
    printButton.textContent = 'Print this document';
    printButton.className = 'btn btn-outline print-button';
    printButton.setAttribute('aria-label', 'Print this legal document');
    printButton.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 1000;
        display: none;
    `;
    
    printButton.addEventListener('click', function() {
        window.print();
    });
    
    // Show print button on larger screens
    if (window.innerWidth > 768) {
        printButton.style.display = 'block';
        document.body.appendChild(printButton);
    }
    
    // Hide print button when printing
    window.addEventListener('beforeprint', function() {
        printButton.style.display = 'none';
    });
    
    window.addEventListener('afterprint', function() {
        if (window.innerWidth > 768) {
            printButton.style.display = 'block';
        }
    });
}

// Screen reader only class
const srOnlyStyle = document.createElement('style');
srOnlyStyle.textContent = `
    .sr-only {
        position: absolute !important;
        width: 1px !important;
        height: 1px !important;
        padding: 0 !important;
        margin: -1px !important;
        overflow: hidden !important;
        clip: rect(0, 0, 0, 0) !important;
        white-space: nowrap !important;
        border: 0 !important;
    }
`;
document.head.appendChild(srOnlyStyle);

// Handle back to top button integration
document.addEventListener('scroll', function() {
    const backToTopButton = document.querySelector('.back-to-top');
    if (backToTopButton) {
        // Enhanced accessibility for back to top button
        if (!backToTopButton.hasAttribute('aria-label')) {
            backToTopButton.setAttribute('aria-label', 'Return to top of page');
        }
    }
});

// Add focus management for modal-like interactions
function manageFocus() {
    // Store the last focused element before navigation
    let lastFocusedElement = null;
    
    document.addEventListener('focusin', function(e) {
        if (!e.target.closest('.skip-links') && !e.target.closest('.sr-only')) {
            lastFocusedElement = e.target;
        }
    });
    
    // Return focus when needed
    window.returnFocus = function() {
        if (lastFocusedElement) {
            lastFocusedElement.focus();
        }
    };
}

manageFocus();

// Export functions for external use
window.legalPageUtils = {
    updateActiveTocLink,
    announceNavigation,
    generateId
};