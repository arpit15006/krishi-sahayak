/**
 * 🏆 Krishi Sahayak - Hackathon Winning Interactions
 * Professional animations and weather-based effects
 */

class HackathonUI {
    constructor() {
        this.init();
    }

    init() {
        this.setupWeatherAnimations();
        this.setupFadeInAnimations();
        this.setupButtonInteractions();
        this.setupScannerEnhancements();
        this.setupMarketTicker();
        this.setupFormEnhancements();
    }

    // Weather-based dashboard animations
    setupWeatherAnimations() {
        const weatherWidget = document.querySelector('.weather-widget');
        if (!weatherWidget) return;

        const description = weatherWidget.querySelector('.weather-description');
        if (!description) return;

        const weatherText = description.textContent.toLowerCase();
        
        // Remove existing weather classes
        weatherWidget.classList.remove('sunny', 'rainy', 'cloudy', 'stormy');
        
        // Add appropriate weather class based on description
        if (weatherText.includes('sun') || weatherText.includes('clear')) {
            weatherWidget.classList.add('sunny');
        } else if (weatherText.includes('rain') || weatherText.includes('shower')) {
            weatherWidget.classList.add('rainy');
        } else if (weatherText.includes('cloud')) {
            weatherWidget.classList.add('cloudy');
        } else if (weatherText.includes('storm') || weatherText.includes('thunder')) {
            weatherWidget.classList.add('stormy');
        }
    }

    // Fade-in animations for page elements
    setupFadeInAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in');
                }
            });
        }, observerOptions);

        // Observe all cards and action elements
        document.querySelectorAll('.card, .action-card, .weather-widget, .market-ticker').forEach(el => {
            observer.observe(el);
        });
    }

    // Enhanced button interactions
    setupButtonInteractions() {
        // Add ripple effect to buttons
        document.addEventListener('click', (e) => {
            const button = e.target.closest('.btn, .action-card');
            if (button) {
                this.createRipple(button, e);
            }
        });

        // Pulse animation for main scan button
        const scanButton = document.querySelector('.btn-pulse');
        if (scanButton) {
            scanButton.addEventListener('mouseenter', () => {
                scanButton.style.animationDuration = '1s';
            });
            
            scanButton.addEventListener('mouseleave', () => {
                scanButton.style.animationDuration = '2s';
            });
        }
    }

    // Create ripple effect
    createRipple(element, event) {
        const ripple = document.createElement('span');
        const rect = element.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = event.clientX - rect.left - size / 2;
        const y = event.clientY - rect.top - size / 2;

        ripple.style.cssText = `
            position: absolute;
            width: ${size}px;
            height: ${size}px;
            left: ${x}px;
            top: ${y}px;
            background: rgba(255, 255, 255, 0.4);
            border-radius: 50%;
            transform: scale(0);
            animation: ripple 0.6s ease-out;
            pointer-events: none;
            z-index: 1;
        `;

        element.style.position = 'relative';
        element.style.overflow = 'hidden';
        element.appendChild(ripple);

        setTimeout(() => {
            ripple.remove();
        }, 600);
    }

    // Scanner enhancements
    setupScannerEnhancements() {
        const uploadArea = document.querySelector('.upload-area');
        const fileInput = document.querySelector('input[type="file"]');
        
        if (!uploadArea || !fileInput) return;

        // Drag and drop enhancements
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.style.borderColor = 'var(--color-accent)';
            uploadArea.style.backgroundColor = 'var(--bg-secondary)';
            uploadArea.style.transform = 'scale(1.02)';
        });

        uploadArea.addEventListener('dragleave', (e) => {
            e.preventDefault();
            uploadArea.style.borderColor = 'var(--color-primary)';
            uploadArea.style.backgroundColor = 'var(--bg-white)';
            uploadArea.style.transform = 'scale(1)';
        });

        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.style.borderColor = 'var(--color-primary)';
            uploadArea.style.backgroundColor = 'var(--bg-white)';
            uploadArea.style.transform = 'scale(1)';

            const files = e.dataTransfer.files;
            if (files.length > 0) {
                fileInput.files = files;
                this.showImagePreview(files[0], uploadArea);
            }
        });

        // File input change handler
        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                this.showImagePreview(e.target.files[0], uploadArea);
            }
        });
    }

    // Show image preview
    showImagePreview(file, container) {
        const reader = new FileReader();
        reader.onload = (e) => {
            container.innerHTML = `
                <img src="${e.target.result}" 
                     alt="Preview" 
                     style="max-width: 200px; max-height: 200px; border-radius: 12px; 
                            object-fit: cover; box-shadow: var(--shadow-md);">
                <p style="margin-top: 1rem; color: var(--color-success); font-weight: 600;">
                    ✓ Ready to analyze: ${file.name}
                </p>
            `;
        };
        reader.readAsDataURL(file);
    }

    // Market ticker enhancements
    setupMarketTicker() {
        const ticker = document.querySelector('.ticker-content');
        if (!ticker) return;

        // Pause animation on hover
        ticker.addEventListener('mouseenter', () => {
            ticker.style.animationPlayState = 'paused';
        });

        ticker.addEventListener('mouseleave', () => {
            ticker.style.animationPlayState = 'running';
        });
    }

    // Form enhancements
    setupFormEnhancements() {
        // Enhanced form validation feedback
        document.querySelectorAll('.form-control').forEach(input => {
            input.addEventListener('blur', () => {
                if (input.value.trim() === '') {
                    input.style.borderColor = 'var(--color-error)';
                } else {
                    input.style.borderColor = 'var(--color-success)';
                }
            });

            input.addEventListener('focus', () => {
                input.style.borderColor = 'var(--color-primary)';
            });
        });

        // Form submission with loading state
        document.querySelectorAll('form').forEach(form => {
            form.addEventListener('submit', (e) => {
                const submitBtn = form.querySelector('button[type="submit"]');
                if (submitBtn) {
                    const originalText = submitBtn.innerHTML;
                    submitBtn.innerHTML = `
                        <div class="spinner" style="width: 20px; height: 20px; margin-right: 8px;"></div>
                        Processing...
                    `;
                    submitBtn.disabled = true;
                }
            });
        });
    }

    // Professional notification system
    static showNotification(message, type = 'info', duration = 5000) {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type}`;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            max-width: 400px;
            animation: slideInRight 0.3s ease-out;
            box-shadow: var(--shadow-lg);
        `;
        
        notification.innerHTML = `
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <span>${message}</span>
                <button onclick="this.parentElement.parentElement.remove()" 
                        style="background: none; border: none; font-size: 1.2rem; cursor: pointer; margin-left: 1rem;">×</button>
            </div>
        `;

        document.body.appendChild(notification);

        setTimeout(() => {
            if (notification.parentNode) {
                notification.style.animation = 'slideOutRight 0.3s ease-in';
                setTimeout(() => notification.remove(), 300);
            }
        }, duration);
    }

    // Weather-specific dashboard updates
    static updateWeatherAnimation(weatherCondition) {
        const weatherWidget = document.querySelector('.weather-widget');
        if (!weatherWidget) return;

        // Remove all weather classes
        weatherWidget.classList.remove('sunny', 'rainy', 'cloudy', 'stormy');
        
        // Add new weather class
        weatherWidget.classList.add(weatherCondition);
    }

    // Professional loading overlay
    static showLoadingOverlay(message = 'Processing...') {
        const overlay = document.createElement('div');
        overlay.id = 'loading-overlay';
        overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(44, 62, 80, 0.8);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            z-index: 10000;
            backdrop-filter: blur(5px);
        `;
        
        overlay.innerHTML = `
            <div class="spinner" style="width: 60px; height: 60px; margin-bottom: 1rem;"></div>
            <p style="color: white; font-size: 1.2rem; font-weight: 600;">${message}</p>
        `;

        document.body.appendChild(overlay);
        return overlay;
    }

    static hideLoadingOverlay() {
        const overlay = document.getElementById('loading-overlay');
        if (overlay) {
            overlay.remove();
        }
    }
}

// CSS animations to inject
const hackathonStyles = `
<style>
@keyframes ripple {
    to {
        transform: scale(4);
        opacity: 0;
    }
}

@keyframes slideInRight {
    from {
        transform: translateX(100%);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}

@keyframes slideOutRight {
    from {
        transform: translateX(0);
        opacity: 1;
    }
    to {
        transform: translateX(100%);
        opacity: 0;
    }
}

/* Professional hover effects */
.action-card {
    position: relative;
    overflow: hidden;
}

.action-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
    transition: left 0.5s ease;
}

.action-card:hover::before {
    left: 100%;
}

/* Enhanced focus states */
.btn:focus-visible,
.action-card:focus-visible {
    outline: 3px solid var(--color-accent);
    outline-offset: 2px;
}

/* Professional loading states */
.btn.loading {
    pointer-events: none;
    opacity: 0.8;
}

.btn.loading::after {
    content: '';
    position: absolute;
    width: 16px;
    height: 16px;
    margin: auto;
    border: 2px solid transparent;
    border-top-color: currentColor;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}
</style>
`;

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Inject hackathon styles
    document.head.insertAdjacentHTML('beforeend', hackathonStyles);
    
    // Initialize hackathon UI
    window.hackathonUI = new HackathonUI();
    
    // Global functions for external use
    window.showNotification = HackathonUI.showNotification;
    window.showLoadingOverlay = HackathonUI.showLoadingOverlay;
    window.hideLoadingOverlay = HackathonUI.hideLoadingOverlay;
    window.updateWeatherAnimation = HackathonUI.updateWeatherAnimation;
    
    console.log('🏆 Hackathon UI initialized successfully!');
});

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = HackathonUI;
}