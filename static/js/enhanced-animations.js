/**
 * Enhanced Animations for Krishi Sahayak
 * Farmer-friendly interactions and visual feedback
 */

class KrishiAnimations {
    constructor() {
        this.init();
    }

    init() {
        this.setupIntersectionObserver();
        this.setupClickAnimations();
        this.setupHoverEffects();
        this.setupLoadingStates();
        this.setupNotifications();
        this.setupProgressIndicators();
        this.setupParallaxEffects();
    }

    // Intersection Observer for scroll animations
    setupIntersectionObserver() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                    
                    // Stagger child animations
                    const children = entry.target.querySelectorAll('.stagger-child');
                    children.forEach((child, index) => {
                        setTimeout(() => {
                            child.classList.add('animate-in');
                        }, index * 100);
                    });
                }
            });
        }, observerOptions);

        // Observe all cards and sections
        document.querySelectorAll('.card, .action-btn, .weather-widget, .market-ticker').forEach(el => {
            observer.observe(el);
        });
    }

    // Enhanced click animations
    setupClickAnimations() {
        document.addEventListener('click', (e) => {
            const button = e.target.closest('.btn, .action-btn, .nav-link');
            if (button) {
                this.createRippleEffect(button, e);
                this.addClickFeedback(button);
            }
        });
    }

    // Ripple effect on click
    createRippleEffect(element, event) {
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
            background: rgba(255, 255, 255, 0.6);
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

    // Click feedback animation
    addClickFeedback(element) {
        element.style.transform = 'scale(0.95)';
        setTimeout(() => {
            element.style.transform = '';
        }, 150);
    }

    // Enhanced hover effects
    setupHoverEffects() {
        // Magnetic effect for buttons
        document.querySelectorAll('.btn, .action-btn').forEach(btn => {
            btn.addEventListener('mousemove', (e) => {
                const rect = btn.getBoundingClientRect();
                const x = e.clientX - rect.left - rect.width / 2;
                const y = e.clientY - rect.top - rect.height / 2;
                
                btn.style.transform = `translate(${x * 0.1}px, ${y * 0.1}px)`;
            });

            btn.addEventListener('mouseleave', () => {
                btn.style.transform = '';
            });
        });

        // Tilt effect for cards
        document.querySelectorAll('.card').forEach(card => {
            card.addEventListener('mousemove', (e) => {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                const centerX = rect.width / 2;
                const centerY = rect.height / 2;
                const rotateX = (y - centerY) / 10;
                const rotateY = (centerX - x) / 10;

                card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateZ(10px)`;
            });

            card.addEventListener('mouseleave', () => {
                card.style.transform = '';
            });
        });
    }

    // Loading states with animations
    setupLoadingStates() {
        window.showLoading = (element, text = 'Loading...') => {
            const originalContent = element.innerHTML;
            element.innerHTML = `
                <div class="d-flex align-items-center justify-content-center">
                    <div class="spinner me-2"></div>
                    <span class="loading-dots">${text}</span>
                </div>
            `;
            element.disabled = true;
            
            return () => {
                element.innerHTML = originalContent;
                element.disabled = false;
            };
        };

        // Auto-loading for forms
        document.querySelectorAll('form').forEach(form => {
            form.addEventListener('submit', (e) => {
                const submitBtn = form.querySelector('button[type="submit"], input[type="submit"]');
                if (submitBtn) {
                    const stopLoading = this.showLoading(submitBtn, 'Processing...');
                    
                    // Auto-stop after 30 seconds
                    setTimeout(stopLoading, 30000);
                }
            });
        });
    }

    // Enhanced notifications
    setupNotifications() {
        window.showNotification = (message, type = 'info', duration = 5000) => {
            const notification = document.createElement('div');
            notification.className = `notification notification-${type}`;
            
            const icons = {
                success: '✅',
                error: '❌',
                warning: '⚠️',
                info: 'ℹ️'
            };

            notification.innerHTML = `
                <div class="d-flex align-items-start">
                    <div class="farmer-icon me-3">
                        ${icons[type] || icons.info}
                    </div>
                    <div class="flex-grow-1">
                        <div class="fw-bold mb-1">${type.charAt(0).toUpperCase() + type.slice(1)}</div>
                        <div>${message}</div>
                    </div>
                    <button class="btn-close ms-3" onclick="this.closest('.notification').remove()"></button>
                </div>
            `;

            document.body.appendChild(notification);

            // Auto-remove
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.style.animation = 'slideOutRight 0.3s ease-in';
                    setTimeout(() => notification.remove(), 300);
                }
            }, duration);

            return notification;
        };

        // Success feedback for actions
        window.showSuccess = (message) => {
            this.showNotification(message, 'success');
            this.celebrateSuccess();
        };

        window.showError = (message) => {
            this.showNotification(message, 'error');
            this.shakeScreen();
        };
    }

    // Celebration animation
    celebrateSuccess() {
        // Create confetti effect
        for (let i = 0; i < 50; i++) {
            setTimeout(() => {
                this.createConfetti();
            }, i * 20);
        }
    }

    createConfetti() {
        const confetti = document.createElement('div');
        confetti.style.cssText = `
            position: fixed;
            width: 10px;
            height: 10px;
            background: ${['#4ade80', '#0ea5e9', '#eab308', '#f97316'][Math.floor(Math.random() * 4)]};
            left: ${Math.random() * 100}vw;
            top: -10px;
            border-radius: 50%;
            pointer-events: none;
            z-index: 9999;
            animation: confetti-fall 3s ease-out forwards;
        `;

        document.body.appendChild(confetti);

        setTimeout(() => {
            confetti.remove();
        }, 3000);
    }

    // Shake animation for errors
    shakeScreen() {
        document.body.style.animation = 'shake 0.5s ease-in-out';
        setTimeout(() => {
            document.body.style.animation = '';
        }, 500);
    }

    // Progress indicators
    setupProgressIndicators() {
        window.updateProgress = (element, percentage) => {
            const circle = element.querySelector('.progress-ring-circle');
            if (circle) {
                const circumference = 2 * Math.PI * 30; // radius = 30
                const offset = circumference - (percentage / 100) * circumference;
                circle.style.strokeDashoffset = offset;
            }
        };

        // Auto-progress for uploads
        document.querySelectorAll('input[type="file"]').forEach(input => {
            input.addEventListener('change', () => {
                if (input.files.length > 0) {
                    this.simulateUploadProgress();
                }
            });
        });
    }

    simulateUploadProgress() {
        const progressBar = document.createElement('div');
        progressBar.className = 'progress-bar';
        progressBar.innerHTML = `
            <div class="progress-fill" style="width: 0%; transition: width 0.3s ease;"></div>
            <div class="progress-text">Uploading... 0%</div>
        `;

        document.body.appendChild(progressBar);

        let progress = 0;
        const interval = setInterval(() => {
            progress += Math.random() * 15;
            if (progress >= 100) {
                progress = 100;
                clearInterval(interval);
                setTimeout(() => {
                    progressBar.remove();
                    this.showSuccess('Upload completed successfully!');
                }, 500);
            }

            const fill = progressBar.querySelector('.progress-fill');
            const text = progressBar.querySelector('.progress-text');
            fill.style.width = `${progress}%`;
            text.textContent = `Uploading... ${Math.round(progress)}%`;
        }, 200);
    }

    // Parallax effects
    setupParallaxEffects() {
        window.addEventListener('scroll', () => {
            const scrolled = window.pageYOffset;
            const parallaxElements = document.querySelectorAll('.parallax');
            
            parallaxElements.forEach(element => {
                const speed = element.dataset.speed || 0.5;
                element.style.transform = `translateY(${scrolled * speed}px)`;
            });
        });
    }

    // Weather animation effects
    static createWeatherEffect(type) {
        const effects = {
            rain: () => {
                for (let i = 0; i < 100; i++) {
                    setTimeout(() => {
                        const drop = document.createElement('div');
                        drop.className = 'rain-drop';
                        drop.style.cssText = `
                            position: fixed;
                            width: 2px;
                            height: 20px;
                            background: linear-gradient(to bottom, transparent, #0ea5e9);
                            left: ${Math.random() * 100}vw;
                            top: -20px;
                            pointer-events: none;
                            z-index: 1000;
                            animation: rain-fall 1s linear forwards;
                        `;
                        document.body.appendChild(drop);
                        setTimeout(() => drop.remove(), 1000);
                    }, i * 10);
                }
            },
            
            sunny: () => {
                const sun = document.querySelector('.weather-temp');
                if (sun) {
                    sun.style.animation = 'glow 2s ease-in-out infinite';
                }
            },
            
            cloudy: () => {
                // Add floating cloud animation
                const clouds = document.querySelectorAll('.weather-widget');
                clouds.forEach(cloud => {
                    cloud.style.animation = 'float 4s ease-in-out infinite';
                });
            }
        };

        if (effects[type]) {
            effects[type]();
        }
    }

    // Voice interaction feedback
    static setupVoiceAnimations() {
        window.startVoiceAnimation = () => {
            const voiceBtn = document.getElementById('voice-button');
            if (voiceBtn) {
                voiceBtn.classList.add('listening');
                voiceBtn.innerHTML = '<span class="pulse-ring"></span>🎤 Listening...';
            }
        };

        window.stopVoiceAnimation = () => {
            const voiceBtn = document.getElementById('voice-button');
            if (voiceBtn) {
                voiceBtn.classList.remove('listening');
                voiceBtn.innerHTML = '🗣️ Speak';
            }
        };
    }

    // Market price animations
    static animatePriceChange(element, oldPrice, newPrice) {
        const isIncrease = newPrice > oldPrice;
        const changeClass = isIncrease ? 'price-increase' : 'price-decrease';
        
        element.classList.add(changeClass);
        element.style.animation = 'pulse 0.5s ease-in-out';
        
        setTimeout(() => {
            element.classList.remove(changeClass);
            element.style.animation = '';
        }, 1000);
    }

    // Crop growth animation
    static animateCropGrowth(container) {
        const stages = ['🌱', '🌿', '🌾', '🌽'];
        let currentStage = 0;
        
        const growthInterval = setInterval(() => {
            const icon = container.querySelector('.crop-icon');
            if (icon) {
                icon.textContent = stages[currentStage];
                icon.style.animation = 'bounce 0.5s ease-in-out';
                
                currentStage++;
                if (currentStage >= stages.length) {
                    clearInterval(growthInterval);
                }
            }
        }, 1000);
    }
}

// CSS animations to be injected
const animationStyles = `
<style>
@keyframes ripple {
    to {
        transform: scale(4);
        opacity: 0;
    }
}

@keyframes slideOutRight {
    to {
        transform: translateX(100%);
        opacity: 0;
    }
}

@keyframes confetti-fall {
    to {
        transform: translateY(100vh) rotate(720deg);
        opacity: 0;
    }
}

@keyframes shake {
    0%, 100% { transform: translateX(0); }
    10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
    20%, 40%, 60%, 80% { transform: translateX(5px); }
}

@keyframes rain-fall {
    to {
        transform: translateY(100vh);
        opacity: 0;
    }
}

.animate-in {
    animation: fadeInUp 0.6s ease-out forwards;
}

.price-increase {
    color: #16a34a !important;
    background: rgba(22, 163, 74, 0.1) !important;
}

.price-decrease {
    color: #dc2626 !important;
    background: rgba(220, 38, 38, 0.1) !important;
}

.pulse-ring {
    position: absolute;
    width: 100%;
    height: 100%;
    border: 2px solid #4ade80;
    border-radius: 50%;
    animation: pulse-ring 1.5s ease-out infinite;
}

@keyframes pulse-ring {
    0% {
        transform: scale(0.8);
        opacity: 1;
    }
    100% {
        transform: scale(2);
        opacity: 0;
    }
}

.progress-bar {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 300px;
    height: 60px;
    background: white;
    border-radius: 15px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    z-index: 9999;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #4ade80, #16a34a);
    border-radius: 15px;
    transition: width 0.3s ease;
}

.progress-text {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-weight: 600;
    color: #1f2937;
}

.listening {
    position: relative;
    background: linear-gradient(45deg, #ff6b6b, #ee5a24) !important;
    animation: pulse 1.5s infinite !important;
}
</style>
`;

// Initialize animations when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Inject animation styles
    document.head.insertAdjacentHTML('beforeend', animationStyles);
    
    // Initialize animation system
    new KrishiAnimations();
    
    // Setup voice animations
    KrishiAnimations.setupVoiceAnimations();
    
    // Add stagger classes to elements
    document.querySelectorAll('.quick-actions .action-btn').forEach((btn, index) => {
        btn.classList.add('stagger-child');
        btn.style.animationDelay = `${index * 0.1}s`;
    });
    
    // Weather effect based on current weather
    const weatherDesc = document.querySelector('.weather-description');
    if (weatherDesc) {
        const description = weatherDesc.textContent.toLowerCase();
        if (description.includes('rain')) {
            KrishiAnimations.createWeatherEffect('rain');
        } else if (description.includes('sun') || description.includes('clear')) {
            KrishiAnimations.createWeatherEffect('sunny');
        } else if (description.includes('cloud')) {
            KrishiAnimations.createWeatherEffect('cloudy');
        }
    }
    
    // Add floating action button
    const fab = document.createElement('button');
    fab.className = 'fab';
    fab.innerHTML = '💬';
    fab.title = 'Quick Help';
    fab.onclick = () => {
        showNotification('🌾 Need help? Use the voice assistant or scan a plant!', 'info');
    };
    document.body.appendChild(fab);
    
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Add loading states to all buttons
    document.querySelectorAll('.btn').forEach(btn => {
        btn.addEventListener('click', function() {
            if (this.type !== 'button' && !this.classList.contains('no-loading')) {
                const stopLoading = showLoading(this);
                setTimeout(stopLoading, 2000); // Auto-stop after 2 seconds
            }
        });
    });
});

// Export for global use
window.KrishiAnimations = KrishiAnimations;