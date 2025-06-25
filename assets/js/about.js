// About page specific JavaScript

class AboutManager {
    constructor() {
        this.init();
    }

    init() {
        this.setupSkillBars();
        this.addAboutStyles();
        this.setupTimelineAnimations();
        this.initializeCounters();
        this.setupInteractiveElements();
    }

    setupSkillBars() {
        const skillBars = document.querySelectorAll('.skill-progress');
        
        const animateSkillBar = (bar) => {
            const progress = bar.getAttribute('data-progress');
            const duration = 1500; // 1.5 seconds
            const steps = 60; // 60 FPS
            const stepValue = progress / steps;
            let currentProgress = 0;
            
            const timer = setInterval(() => {
                currentProgress += stepValue;
                if (currentProgress >= progress) {
                    currentProgress = progress;
                    clearInterval(timer);
                }
                bar.style.width = `${currentProgress}%`;
            }, duration / steps);
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !entry.target.classList.contains('animated')) {
                    entry.target.classList.add('animated');
                    setTimeout(() => {
                        animateSkillBar(entry.target);
                    }, 300);
                }
            });
        }, {
            threshold: 0.5
        });

        skillBars.forEach(bar => {
            observer.observe(bar);
        });
    }

    setupTimelineAnimations() {
        const timelineItems = document.querySelectorAll('.timeline-item');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                }
            });
        }, {
            threshold: 0.3
        });

        timelineItems.forEach(item => {
            observer.observe(item);
        });
    }

    initializeCounters() {
        const counterElements = document.querySelectorAll('[data-count]');
        
        const animateCounter = (element) => {
            const target = parseInt(element.getAttribute('data-count'));
            const duration = 2000; // 2 seconds
            const step = target / (duration / 16); // 60fps
            let current = 0;
            
            const timer = setInterval(() => {
                current += step;
                if (current >= target) {
                    current = target;
                    clearInterval(timer);
                }
                
                // Format number with commas for thousands
                const formattedNumber = Math.floor(current).toLocaleString();
                element.textContent = formattedNumber + (target >= 1000 ? '+' : '');
            }, 16);
        };

        const counterObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !entry.target.classList.contains('counted')) {
                    entry.target.classList.add('counted');
                    animateCounter(entry.target);
                }
            });
        }, {
            threshold: 0.5
        });

        counterElements.forEach(el => {
            counterObserver.observe(el);
        });
    }

    setupInteractiveElements() {
        // Add hover effects to value items
        const valueItems = document.querySelectorAll('.value-item');
        valueItems.forEach(item => {
            item.addEventListener('mouseenter', () => {
                const icon = item.querySelector('.value-icon');
                if (icon) {
                    icon.style.transform = 'scale(1.2) rotate(10deg)';
                }
            });
            
            item.addEventListener('mouseleave', () => {
                const icon = item.querySelector('.value-icon');
                if (icon) {
                    icon.style.transform = '';
                }
            });
        });

        // Add click effects to achievement items
        const achievementItems = document.querySelectorAll('.achievement-item');
        achievementItems.forEach(item => {
            item.addEventListener('click', () => {
                item.style.transform = 'scale(0.95)';
                setTimeout(() => {
                    item.style.transform = '';
                }, 150);
            });
        });

        // Add parallax effect to profile avatar
        const avatar = document.querySelector('.avatar-placeholder');
        if (avatar) {
            window.addEventListener('scroll', () => {
                const scrolled = window.pageYOffset;
                const rate = scrolled * -0.5;
                avatar.style.transform = `translateY(${rate}px)`;
            }, { passive: true });
        }
    }

    addAboutStyles() {
        if (document.getElementById('about-styles')) return;

        const style = document.createElement('style');
        style.id = 'about-styles';
        style.textContent = `
            /* About page specific styles */
            .about-main {
                padding-top: var(--header-height);
            }

            .about-hero {
                padding: var(--space-20) 0;
                background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            }

            .profile-section {
                display: flex;
                align-items: center;
                gap: var(--space-8);
                margin-bottom: var(--space-8);
            }

            .profile-avatar {
                flex-shrink: 0;
            }

            .avatar-placeholder {
                width: 120px;
                height: 120px;
                border-radius: 50%;
                background: var(--gradient-primary);
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: var(--shadow-xl);
                transition: all var(--transition-base);
            }

            .avatar-placeholder:hover {
                transform: scale(1.05);
                box-shadow: 0 25px 50px rgba(37, 99, 235, 0.3);
            }

            .avatar-icon {
                font-size: var(--font-size-4xl);
                color: white;
            }

            .profile-info {
                flex: 1;
            }

            .profile-name {
                font-size: var(--font-size-4xl);
                font-weight: 700;
                margin-bottom: var(--space-2);
                background: var(--gradient-primary);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }

            .profile-title {
                font-size: var(--font-size-xl);
                color: var(--text-secondary);
                margin-bottom: var(--space-4);
            }

            .profile-status {
                display: flex;
                align-items: center;
                gap: var(--space-2);
                padding: var(--space-2) var(--space-4);
                background: rgba(34, 197, 94, 0.1);
                color: #059669;
                border-radius: var(--radius-lg);
                font-size: var(--font-size-sm);
                font-weight: 500;
                width: fit-content;
            }

            .status-indicator {
                width: 8px;
                height: 8px;
                background: #10b981;
                border-radius: 50%;
                animation: pulse 2s infinite;
            }

            .hero-description {
                text-align: center;
                max-width: 700px;
                margin: 0 auto var(--space-12);
            }

            .description-text {
                font-size: var(--font-size-lg);
                color: var(--text-secondary);
                line-height: 1.7;
            }

            .hero-stats {
                display: flex;
                justify-content: center;
                gap: var(--space-8);
            }

            .hero-stats .stat-item {
                text-align: center;
                padding: var(--space-6);
                background: white;
                border-radius: var(--radius-xl);
                box-shadow: var(--shadow-md);
                min-width: 120px;
            }

            .hero-stats .stat-number {
                font-size: var(--font-size-3xl);
                font-weight: 800;
                background: var(--gradient-primary);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin-bottom: var(--space-2);
            }

            .hero-stats .stat-label {
                font-size: var(--font-size-sm);
                color: var(--text-light);
                font-weight: 500;
            }

            /* Skills Section */
            .skills-section {
                padding: var(--space-24) 0;
                background: var(--background-secondary);
            }

            .skills-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
                gap: var(--space-8);
            }

            .skill-category {
                background: white;
                border-radius: var(--radius-xl);
                padding: var(--space-8);
                box-shadow: var(--shadow-md);
                transition: all var(--transition-base);
            }

            .skill-category:hover {
                transform: translateY(-8px);
                box-shadow: var(--shadow-xl);
            }

            .category-icon {
                font-size: var(--font-size-3xl);
                text-align: center;
                margin-bottom: var(--space-4);
            }

            .category-title {
                font-size: var(--font-size-xl);
                font-weight: 600;
                text-align: center;
                margin-bottom: var(--space-6);
                color: var(--text-primary);
            }

            .skills-list {
                display: flex;
                flex-direction: column;
                gap: var(--space-4);
            }

            .skill-item {
                margin-bottom: var(--space-4);
            }

            .skill-info {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: var(--space-2);
            }

            .skill-name {
                font-weight: 600;
                color: var(--text-primary);
            }

            .skill-level {
                font-size: var(--font-size-sm);
                color: var(--text-light);
            }

            .skill-bar {
                height: 8px;
                background: var(--background-secondary);
                border-radius: 4px;
                overflow: hidden;
            }

            .skill-progress {
                height: 100%;
                background: var(--gradient-primary);
                border-radius: 4px;
                width: 0%;
                transition: width 0.1s ease-out;
            }

            /* Experience Section */
            .experience-section {
                padding: var(--space-24) 0;
            }

            .timeline {
                max-width: 800px;
                margin: 0 auto;
                position: relative;
            }

            .timeline::before {
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
                opacity: 0;
                transform: translateY(30px);
                transition: all 0.8s ease-out;
            }

            .timeline-item.visible {
                opacity: 1;
                transform: translateY(0);
            }

            .timeline-item:nth-child(even) {
                flex-direction: row-reverse;
            }

            .timeline-date {
                width: 80px;
                text-align: center;
                font-weight: 700;
                font-size: var(--font-size-lg);
                color: var(--primary-color);
                margin: 0 var(--space-8);
                background: white;
                border: 2px solid var(--primary-color);
                border-radius: var(--radius-lg);
                padding: var(--space-2);
                z-index: 2;
                position: relative;
            }

            .timeline-content {
                flex: 1;
                max-width: 350px;
                background: white;
                padding: var(--space-6);
                border-radius: var(--radius-xl);
                box-shadow: var(--shadow-md);
                position: relative;
            }

            .timeline-content::before {
                content: '';
                position: absolute;
                top: 20px;
                width: 0;
                height: 0;
                border-style: solid;
            }

            .timeline-item:nth-child(odd) .timeline-content::before {
                right: -12px;
                border-color: transparent transparent transparent white;
                border-width: 12px 0 12px 12px;
            }

            .timeline-item:nth-child(even) .timeline-content::before {
                left: -12px;
                border-color: transparent white transparent transparent;
                border-width: 12px 12px 12px 0;
            }

            .timeline-icon {
                font-size: var(--font-size-xl);
                margin-bottom: var(--space-3);
            }

            .timeline-content h3 {
                font-size: var(--font-size-lg);
                font-weight: 600;
                margin-bottom: var(--space-3);
                color: var(--text-primary);
            }

            .timeline-content p {
                color: var(--text-secondary);
                line-height: 1.6;
                margin: 0;
            }

            /* Philosophy Section */
            .philosophy-section {
                padding: var(--space-24) 0;
                background: var(--background-secondary);
            }

            .philosophy-content {
                max-width: 900px;
                margin: 0 auto;
            }

            .philosophy-text {
                text-align: center;
                margin-bottom: var(--space-16);
            }

            .philosophy-title {
                font-size: var(--font-size-4xl);
                font-weight: 700;
                margin-bottom: var(--space-6);
                background: var(--gradient-primary);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }

            .philosophy-description {
                font-size: var(--font-size-lg);
                color: var(--text-secondary);
                line-height: 1.7;
                max-width: 700px;
                margin: 0 auto;
            }

            .philosophy-description p {
                margin-bottom: var(--space-4);
            }

            .philosophy-values {
                background: white;
                border-radius: var(--radius-2xl);
                padding: var(--space-8);
                box-shadow: var(--shadow-lg);
            }

            .values-title {
                font-size: var(--font-size-2xl);
                font-weight: 600;
                text-align: center;
                margin-bottom: var(--space-8);
                color: var(--text-primary);
            }

            .values-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: var(--space-6);
            }

            .value-item {
                text-align: center;
                padding: var(--space-6);
                border-radius: var(--radius-lg);
                background: var(--background-secondary);
                transition: all var(--transition-base);
            }

            .value-item:hover {
                transform: translateY(-4px);
                box-shadow: var(--shadow-md);
            }

            .value-icon {
                font-size: var(--font-size-3xl);
                margin-bottom: var(--space-3);
                transition: all var(--transition-base);
            }

            .value-item h4 {
                font-size: var(--font-size-lg);
                font-weight: 600;
                margin-bottom: var(--space-2);
                color: var(--text-primary);
            }

            .value-item p {
                color: var(--text-secondary);
                font-size: var(--font-size-sm);
                line-height: 1.5;
                margin: 0;
            }

            /* Achievements Section */
            .achievements-section {
                padding: var(--space-24) 0;
            }

            .achievements-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: var(--space-8);
            }

            .achievement-item {
                display: flex;
                gap: var(--space-4);
                padding: var(--space-6);
                background: white;
                border-radius: var(--radius-xl);
                box-shadow: var(--shadow-md);
                transition: all var(--transition-base);
                cursor: pointer;
            }

            .achievement-item:hover {
                transform: translateY(-4px);
                box-shadow: var(--shadow-lg);
            }

            .achievement-icon {
                font-size: var(--font-size-3xl);
                flex-shrink: 0;
            }

            .achievement-content h3 {
                font-size: var(--font-size-lg);
                font-weight: 600;
                margin-bottom: var(--space-2);
                color: var(--text-primary);
            }

            .achievement-content p {
                color: var(--text-secondary);
                line-height: 1.6;
                margin: 0;
            }

            /* Interests Section */
            .interests-section {
                padding: var(--space-24) 0;
                background: var(--background-secondary);
            }

            .interests-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: var(--space-6);
            }

            .interest-item {
                text-align: center;
                padding: var(--space-8);
                background: white;
                border-radius: var(--radius-xl);
                box-shadow: var(--shadow-md);
                transition: all var(--transition-base);
            }

            .interest-icon {
                font-size: var(--font-size-4xl);
                margin-bottom: var(--space-4);
            }

            .interest-item h3 {
                font-size: var(--font-size-xl);
                font-weight: 600;
                margin-bottom: var(--space-3);
                color: var(--text-primary);
            }

            .interest-item p {
                color: var(--text-secondary);
                line-height: 1.6;
                margin: 0;
            }

            /* CTA Section */
            .cta-section {
                padding: var(--space-24) 0;
            }

            .cta-content {
                text-align: center;
                max-width: 600px;
                margin: 0 auto;
            }

            .cta-icon {
                font-size: var(--font-size-5xl);
                margin-bottom: var(--space-6);
            }

            .cta-title {
                font-size: var(--font-size-4xl);
                font-weight: 700;
                margin-bottom: var(--space-4);
                background: var(--gradient-primary);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }

            .cta-description {
                font-size: var(--font-size-lg);
                color: var(--text-secondary);
                margin-bottom: var(--space-8);
                line-height: 1.6;
            }

            .cta-actions {
                display: flex;
                gap: var(--space-4);
                justify-content: center;
                flex-wrap: wrap;
            }

            /* Mobile styles */
            @media (max-width: 768px) {
                .profile-section {
                    flex-direction: column;
                    text-align: center;
                    gap: var(--space-6);
                }

                .profile-name {
                    font-size: var(--font-size-3xl);
                }

                .hero-stats {
                    flex-direction: column;
                    align-items: center;
                    gap: var(--space-4);
                }

                .skills-grid {
                    grid-template-columns: 1fr;
                }

                .timeline::before {
                    left: 30px;
                }

                .timeline-item {
                    flex-direction: row !important;
                    padding-left: var(--space-16);
                }

                .timeline-item:nth-child(even) {
                    flex-direction: row !important;
                }

                .timeline-date {
                    position: absolute;
                    left: 0;
                    margin: 0;
                    width: 60px;
                    font-size: var(--font-size-sm);
                    padding: var(--space-1);
                }

                .timeline-content {
                    max-width: none;
                }

                .timeline-content::before {
                    display: none;
                }

                .values-grid {
                    grid-template-columns: 1fr;
                }

                .achievements-grid {
                    grid-template-columns: 1fr;
                }

                .interests-grid {
                    grid-template-columns: repeat(2, 1fr);
                }

                .cta-actions {
                    flex-direction: column;
                    align-items: center;
                }
            }

            @media (max-width: 480px) {
                .interests-grid {
                    grid-template-columns: 1fr;
                }
            }
        `;
        
        document.head.appendChild(style);
    }

    // Public methods
    triggerSkillAnimation(skillName) {
        const skillItems = document.querySelectorAll('.skill-item');
        skillItems.forEach(item => {
            const name = item.querySelector('.skill-name').textContent;
            if (name.toLowerCase().includes(skillName.toLowerCase())) {
                const progressBar = item.querySelector('.skill-progress');
                if (progressBar && !progressBar.classList.contains('animated')) {
                    progressBar.classList.add('animated');
                    this.setupSkillBars();
                }
            }
        });
    }

    scrollToSection(sectionClass) {
        const section = document.querySelector(`.${sectionClass}`);
        if (section) {
            const headerHeight = document.querySelector('.header').offsetHeight;
            const targetPosition = section.offsetTop - headerHeight - 20;
            
            window.scrollTo({
                top: targetPosition,
                behavior: 'smooth'
            });
        }
    }
}

// Initialize about manager
document.addEventListener('DOMContentLoaded', () => {
    const aboutManager = new AboutManager();
    
    // Make available globally for debugging
    window.aboutManager = aboutManager;
    
    // Add keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        // Alt + S: Scroll to skills
        if (e.altKey && e.key === 's') {
            e.preventDefault();
            aboutManager.scrollToSection('skills-section');
        }
        
        // Alt + E: Scroll to experience
        if (e.altKey && e.key === 'e') {
            e.preventDefault();
            aboutManager.scrollToSection('experience-section');
        }
        
        // Alt + C: Scroll to contact CTA
        if (e.altKey && e.key === 'c') {
            e.preventDefault();
            aboutManager.scrollToSection('cta-section');
        }
    });
    
    // Add enhanced scroll effects
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        const windowHeight = window.innerHeight;
        
        // Parallax effect for hero elements
        const heroElements = document.querySelectorAll('.hero-stats .stat-item');
        heroElements.forEach((element, index) => {
            const speed = 0.5 + (index * 0.1);
            const yPos = -(scrolled * speed);
            element.style.transform = `translateY(${yPos}px)`;
        });
    }, { passive: true });
});