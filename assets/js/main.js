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
        } else {
            headerPath = '../components/header-en.html';
            footerPath = '../components/footer-en.html';
        }
    } else if (currentPath.includes('/ko/')) {
        // For Korean pages
        if (currentPath.includes('/legal/')) {
            headerPath = '../../components/header-legal-ko.html';
            footerPath = '../../components/footer-legal-ko.html';
        } else {
            headerPath = '../components/header-ko.html';
            footerPath = '../components/footer-ko.html';
        }
    } else {
        // Default to Japanese
        if (currentPath.includes('/legal/')) {
            headerPath = '../components/header-legal.html';
            footerPath = '../components/footer-legal.html';
        } else {
            headerPath = 'components/header.html';
            footerPath = 'components/footer.html';
        }
    }
    
    // Load header and footer
    loadComponent(headerPath, 'header-container');
    loadComponent(footerPath, 'footer-container');
}

// NOT A HOTEL inspired minimalist interactions
document.addEventListener('DOMContentLoaded', function() {
    // Load shared components first
    loadSharedComponents();
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
    
    // Parallax effect for hero section
    window.addEventListener('scroll', function() {
        const scrollY = window.scrollY;
        const heroVisual = document.querySelector('.hero-visual');
        
        if (heroVisual) {
            const translateY = scrollY * 0.5;
            heroVisual.style.transform = `translateY(${translateY}px)`;
        }
    });
    
    // Intersection Observer for animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);
    
    // Observe elements for animation
    const animateElements = document.querySelectorAll('.work-item, .stat, .visual-card');
    animateElements.forEach(element => {
        observer.observe(element);
    });
    
    // Add CSS for animations
    const style = document.createElement('style');
    style.textContent = `
        .work-item,
        .stat,
        .visual-card {
            opacity: 0;
            transform: translateY(20px);
            transition: opacity 0.6s ease, transform 0.6s ease;
        }
        
        .work-item.animate-in,
        .stat.animate-in,
        .visual-card.animate-in {
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

// Add subtle hover effects to interactive elements
const interactiveElements = document.querySelectorAll('a, button, .work-item, .visual-card');
interactiveElements.forEach(element => {
    element.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-2px)';
    });
    
    element.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0)';
    });
});