// Component loader function
async function loadComponent(componentPath, containerId) {
    try {
        const response = await fetch(componentPath);
        const html = await response.text();
        const container = document.getElementById(containerId);
        if (container) {
            container.innerHTML = html;
        }
    } catch (error) {
        console.error('Error loading component:', error);
    }
}

// Load shared components based on current page
function loadSharedComponents() {
    const currentPath = window.location.pathname;
    let headerPath, footerPath;
    
    // Determine which header/footer to load based on current path
    if (currentPath.includes('/en/')) {
        // For English pages
        if (currentPath.includes('/legal/')) {
            headerPath = '../../components/header-legal-en.html';
            footerPath = '../../components/footer-legal-en.html';
        } else if (currentPath.includes('/portfolio/apps/')) {
            headerPath = '../../../components/header-page-en.html';
            footerPath = '../../../components/footer-page-en.html';
        } else if (currentPath.includes('/about/') || currentPath.includes('/contact/') || currentPath.includes('/portfolio/')) {
            headerPath = '../components/header-page-en.html';
            footerPath = '../components/footer-page-en.html';
        } else {
            headerPath = '../components/header-en.html';
            footerPath = '../components/footer-en.html';
        }
    } else if (currentPath.includes('/ko/')) {
        // For Korean pages
        if (currentPath.includes('/legal/')) {
            headerPath = '../../components/header-legal-ko.html';
            footerPath = '../../components/footer-legal-ko.html';
        } else if (currentPath.includes('/portfolio/apps/')) {
            headerPath = '../../../components/header-page-ko.html';
            footerPath = '../../../components/footer-page-ko.html';
        } else if (currentPath.includes('/about/') || currentPath.includes('/contact/') || currentPath.includes('/portfolio/')) {
            headerPath = '../components/header-page-ko.html';
            footerPath = '../components/footer-page-ko.html';
        } else {
            headerPath = '../components/header-ko.html';
            footerPath = '../components/footer-ko.html';
        }
    } else {
        // Default to Japanese
        if (currentPath.includes('/legal/')) {
            headerPath = '../components/header-legal.html';
            footerPath = '../components/footer-legal.html';
        } else if (currentPath.includes('/portfolio/apps/')) {
            headerPath = '../../components/header-page.html';
            footerPath = '../../components/footer-page.html';
        } else if (currentPath.includes('/about/') || currentPath.includes('/contact/') || currentPath.includes('/portfolio/')) {
            headerPath = '../components/header-page.html';
            footerPath = '../components/footer-page.html';
        } else {
            headerPath = 'components/header.html';
            footerPath = 'components/footer.html';
        }
    }
    
    // Load header and footer
    loadComponent(headerPath, 'header-container');
    loadComponent(footerPath, 'footer-container');
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

// NOT A HOTEL inspired minimalist interactions
document.addEventListener('DOMContentLoaded', function() {
    // Load shared components first
    loadSharedComponents();
    
    // Setup language switcher for legal pages after components are loaded
    setTimeout(() => {
        setupLanguageSwitcher();
    }, 100);
    // Smooth scrolling for navigation links
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                targetSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Mobile navigation toggle
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');
    
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            navToggle.classList.toggle('active');
        });
    }
    
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