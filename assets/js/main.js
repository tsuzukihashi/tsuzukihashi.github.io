// Component loader function
async function loadComponent(componentPath, containerId) {
    try {
        const response = await fetch(componentPath);
        const html = await response.text();
        const container = document.getElementById(containerId);
        if (container) {
            container.innerHTML = html;
            
            // Execute scripts in the loaded content
            const scripts = container.querySelectorAll('script');
            scripts.forEach(oldScript => {
                const newScript = document.createElement('script');
                if (oldScript.src) {
                    newScript.src = oldScript.src;
                } else {
                    newScript.textContent = oldScript.textContent;
                }
                oldScript.parentNode.replaceChild(newScript, oldScript);
            });
        }
    } catch (error) {
        console.error('Error loading component:', error);
    }
}

// Load shared components based on current page
async function loadSharedComponents() {
    const currentPath = window.location.pathname;
    const pathParts = currentPath.split('/').filter(Boolean);
    let headerPath, footerPath;
    
    // Calculate base path based on directory depth
    let depth = pathParts.length;
    let basePath = '';
    
    // Generate the correct relative path
    if (depth === 0) {
        basePath = '';
    } else {
        basePath = '../'.repeat(depth);
    }
    
    // Use language-specific header
    if (currentPath.includes('/en/')) {
        headerPath = basePath + 'components/header-en.html';
    } else if (currentPath.includes('/ko/')) {
        headerPath = basePath + 'components/header-ko.html';
    } else {
        headerPath = basePath + 'components/header.html';
    }
    
    // Determine which footer to load based on current path
    if (currentPath.includes('/en/')) {
        // For English pages
        if (currentPath.includes('/legal/')) {
            footerPath = '../../components/footer-legal-en.html';
        } else if (currentPath.includes('/blog/posts/')) {
            footerPath = '../../../components/footer-blog-posts-en.html';
        } else if (currentPath.includes('/portfolio/apps/')) {
            footerPath = '../../../components/footer-page-en.html';
        } else if (currentPath.includes('/about/') || currentPath.includes('/contact/')) {
            footerPath = '../../components/footer-subpage-en.html';
        } else if (currentPath.includes('/portfolio/')) {
            footerPath = '../components/footer-page-en.html';
        } else {
            footerPath = '../components/footer-en.html';
        }
    } else if (currentPath.includes('/ko/')) {
        // For Korean pages
        if (currentPath.includes('/legal/')) {
            footerPath = '../../components/footer-legal-ko.html';
        } else if (currentPath.includes('/blog/posts/')) {
            footerPath = '../../../components/footer-blog-posts-ko.html';
        } else if (currentPath.includes('/portfolio/apps/')) {
            footerPath = '../../../components/footer-page-ko.html';
        } else if (currentPath.includes('/about/') || currentPath.includes('/contact/')) {
            footerPath = '../../components/footer-subpage-ko.html';
        } else if (currentPath.includes('/portfolio/')) {
            footerPath = '../components/footer-page-ko.html';
        } else {
            footerPath = '../components/footer-ko.html';
        }
    } else {
        // Default to Japanese
        if (currentPath.includes('/legal/')) {
            footerPath = '../components/footer-legal.html';
        } else if (currentPath.includes('/blog/posts/')) {
            footerPath = '../../components/footer-blog-posts.html';
        } else if (currentPath.includes('/portfolio/apps/')) {
            footerPath = '../../components/footer-page.html';
        } else if (currentPath.includes('/about/') || currentPath.includes('/contact/') || currentPath.includes('/portfolio/')) {
            footerPath = '../components/footer-page.html';
        } else {
            footerPath = 'components/footer.html';
        }
    }
    
    // Load header and footer
    await loadComponent(headerPath, 'header-container');
    await loadComponent(footerPath, 'footer-container');
}

// Setup language switcher for legal pages
function setupLanguageSwitcher() {
    const currentPath = window.location.pathname;
    const langOptions = document.querySelectorAll('.lang-option[data-lang]');
    
    if (langOptions.length > 0 && currentPath.includes('/legal/')) {
        // Get current page name (e.g., 'privacy-policy.html')
        const currentPage = currentPath.split('/').pop();
        
        langOptions.forEach(option => {
            const lang = option.getAttribute('data-lang');
            let targetPath;
            
            if (lang === 'ja') {
                targetPath = `../../legal/${currentPage}`;
            } else if (lang === 'en') {
                targetPath = `../../en/legal/${currentPage}`;
            } else if (lang === 'ko') {
                targetPath = `../../ko/legal/${currentPage}`;
            }
            
            // Adjust path based on current location
            if (currentPath.includes('/en/legal/')) {
                if (lang === 'ja') {
                    targetPath = `../../legal/${currentPage}`;
                } else if (lang === 'en') {
                    targetPath = currentPage;
                } else if (lang === 'ko') {
                    targetPath = `../../ko/legal/${currentPage}`;
                }
            } else if (currentPath.includes('/ko/legal/')) {
                if (lang === 'ja') {
                    targetPath = `../../legal/${currentPage}`;
                } else if (lang === 'en') {
                    targetPath = `../../en/legal/${currentPage}`;
                } else if (lang === 'ko') {
                    targetPath = currentPage;
                }
            } else {
                // Japanese legal page
                if (lang === 'ja') {
                    targetPath = currentPage;
                } else if (lang === 'en') {
                    targetPath = `../en/legal/${currentPage}`;
                } else if (lang === 'ko') {
                    targetPath = `../ko/legal/${currentPage}`;
                }
            }
            
            option.href = targetPath;
        });
    }
}

// Setup clickable cards functionality
function setupClickableCards() {
    const clickableCards = document.querySelectorAll('.clickable-card');
    
    clickableCards.forEach(card => {
        card.addEventListener('click', function(e) {
            // Don't navigate if the target element has onclick with stopPropagation
            if (e.target.closest('a[onclick*="stopPropagation"]')) {
                return;
            }
            
            const href = this.getAttribute('data-href');
            
            // Only navigate if href exists and is not '#'
            if (href && href !== '#') {
                window.location.href = href;
            }
        });
    });
}

// Setup mobile navigation toggle
function setupMobileNavigation() {
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');
    
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            navToggle.classList.toggle('active');
        });
    }
}

// NOT A HOTEL inspired minimalist interactions
document.addEventListener('DOMContentLoaded', async function() {
    // Load shared components first
    await loadSharedComponents();
    
    // Setup everything after components are loaded
    setupLanguageSwitcher();
    setupClickableCards();
    setupMobileNavigation();
    // Smooth scrolling for anchor links only
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            // Only handle anchor links (starting with #)
            if (href && href.startsWith('#')) {
                e.preventDefault();
                const targetSection = document.querySelector(href);
                
                if (targetSection) {
                    targetSection.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
            // Let normal links work as usual (no preventDefault for external links)
        });
    });
    
    
    // Scroll indicator behavior
    const scrollIndicator = document.querySelector('.scroll-indicator');
    if (scrollIndicator) {
        scrollIndicator.addEventListener('click', function() {
            const workSection = document.querySelector('#work');
            if (workSection) {
                workSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    }
    
    // Parallax effect for hero section - DISABLED
    // window.addEventListener('scroll', function() {
    //     const scrollY = window.scrollY;
    //     const heroVisual = document.querySelector('.hero-visual');
    //     
    //     if (heroVisual) {
    //         const translateY = scrollY * 0.5;
    //         heroVisual.style.transform = `translateY(${translateY}px)`;
    //     }
    // });
    
    // Intersection Observer for animations - DISABLED
    // const observerOptions = {
    //     threshold: 0.1,
    //     rootMargin: '0px 0px -50px 0px'
    // };
    // 
    // const observer = new IntersectionObserver(function(entries) {
    //     entries.forEach(entry => {
    //         if (entry.isIntersecting) {
    //             entry.target.classList.add('animate-in');
    //         }
    //     });
    // }, observerOptions);
    // 
    // // Observe elements for animation
    // const animateElements = document.querySelectorAll('.work-item, .stat, .visual-card');
    // animateElements.forEach(element => {
    //     observer.observe(element);
    // });
    
    // Add CSS for static appearance (no scroll animations)
    const style = document.createElement('style');
    style.textContent = `
        .work-item,
        .stat,
        .visual-card {
            opacity: 1;
            transform: translateY(0);
        }
        
        .nav-toggle.active span:nth-child(1) {
            transform: rotate(45deg) translate(5px, 5px);
        }
        
        .nav-toggle.active span:nth-child(2) {
            opacity: 0;
        }
        
        .nav-toggle.active span:nth-child(3) {
            transform: rotate(-45deg) translate(7px, -6px);
        }
        
        @media (max-width: 768px) {
            .nav-menu {
                position: fixed;
                top: 70px;
                left: 0;
                right: 0;
                background: var(--color-background);
                border-bottom: 1px solid var(--color-border);
                padding: var(--spacing-lg);
                transform: translateY(-100%);
                transition: transform 0.3s ease;
            }
            
            .nav-menu.active {
                transform: translateY(0);
            }
            
            .nav-menu {
                flex-direction: column;
                gap: var(--spacing-lg);
            }
        }
    `;
    document.head.appendChild(style);
});

// Cursor effect for hover states (optional enhancement)
document.addEventListener('mousemove', function(e) {
    const cursor = document.querySelector('.cursor');
    if (cursor) {
        cursor.style.left = e.clientX + 'px';
        cursor.style.top = e.clientY + 'px';
    }
});

// Add subtle hover effects to interactive elements - DISABLED for scroll elements
// const interactiveElements = document.querySelectorAll('a, button, .work-item, .visual-card');
// interactiveElements.forEach(element => {
//     element.addEventListener('mouseenter', function() {
//         this.style.transform = 'translateY(-2px)';
//     });
//     
//     element.addEventListener('mouseleave', function() {
//         this.style.transform = 'translateY(0)';
//     });
// });