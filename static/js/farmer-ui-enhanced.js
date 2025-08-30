/**
 * 🌾 Krishi Sahayak - Enhanced Farmer UI Interactions
 * Advanced animations and farmer-friendly interactions
 */

class FarmerUIEnhanced {
    constructor() {
        this.isInitialized = false;
        this.animations = new Map();
        this.observers = new Map();
        this.init();
    }

    init() {
        if (this.isInitialized) return;
        
        console.log('🌱 Initializing Enhanced Farmer UI...');
        
        this.setupIntersectionObservers();
        this.setupAdvancedAnimations();
        this.setupInteractiveElements();
        this.setupWeatherEffects();
        this.setupMarketAnimations();
        this.setupVoiceInteractions();
        this.setupGestureControls();
        this.setupAccessibilityFeatures();
        this.setupPerformanceOptimizations();
        
        this.isInitialized = true;
        console.log('✅ Enhanced Farmer UI initialized successfully!');
    }

    // Advanced Intersection Observer for scroll animations
    setupIntersectionObservers() {
        const observerOptions = {
            threshold: [0, 0.1, 0.5, 1],
            rootMargin: '0px 0px -50px 0px'
        };

        // Main content observer
        const mainObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                const element = entry.target;
                const ratio = entry.intersectionRatio;

                if (entry.isIntersecting) {
                    this.animateElementIn(element, ratio);
                } else {
                    this.animateElementOut(element, ratio);
                }
            });
        }, observerOptions);

        // Observe all animatable elements
        const animatableElements = document.querySelectorAll(`
            .card, .action-btn, .weather-widget, .market-ticker,
            .alert-section, .ai-assistant-prominent, .resource-card
        `);

        animatableElements.forEach(el => {
            mainObserver.observe(el);
            el.classList.add('animate-ready');
        });

        this.observers.set('main', mainObserver);
    }

    // Animate elements into view
    animateElementIn(element, ratio) {
        if (element.classList.contains('animated-in')) return;

        const animationType = element.dataset.animation || 'fadeInUp';
        const delay = element.dataset.delay || 0;

        setTimeout(() => {
            element.classList.add('animated-in', animationType);
            
            // Stagger child animations
            const children = element.querySelectorAll('.stagger-child');
            children.forEach((child, index) => {
                setTimeout(() => {
                    child.classList.add('animate-in');
                }, index * 100);
            });

            // Trigger custom animations based on element type
            this.triggerCustomAnimation(element);
        }, delay);
    }

    // Animate elements out of view
    animateElementOut(element, ratio) {
        if (ratio === 0 && element.classList.contains('animated-in')) {
            // Optional: Add exit animations for elements going out of view
            // element.classList.add('animate-out');
        }
    }

    // Trigger custom animations based on element type
    triggerCustomAnimation(element) {
        if (element.classList.contains('weather-widget')) {
            this.animateWeatherWidget(element);
        } else if (element.classList.contains('market-ticker')) {
            this.animateMarketTicker(element);
        } else if (element.classList.contains('action-btn')) {
            this.animateActionButton(element);
        } else if (element.classList.contains('ai-assistant-prominent')) {
            this.animateVoiceAssistant(element);
        }
    }

    // Advanced animation system
    setupAdvancedAnimations() {
        // Parallax scrolling
        this.setupParallaxScrolling();
        
        // Mouse tracking effects
        this.setupMouseTracking();
        
        // Particle effects
        this.setupParticleEffects();
        
        // Morphing animations
        this.setupMorphingAnimations();
        
        // Physics-based animations
        this.setupPhysicsAnimations();
    }

    // Parallax scrolling effects
    setupParallaxScrolling() {
        let ticking = false;

        const updateParallax = () => {
            const scrolled = window.pageYOffset;
            const parallaxElements = document.querySelectorAll('[data-parallax]');
            
            parallaxElements.forEach(element => {
                const speed = parseFloat(element.dataset.parallax) || 0.5;
                const yPos = -(scrolled * speed);
                element.style.transform = `translate3d(0, ${yPos}px, 0)`;
            });
            
            ticking = false;
        };

        const requestTick = () => {
            if (!ticking) {
                requestAnimationFrame(updateParallax);
                ticking = true;
            }
        };

        window.addEventListener('scroll', requestTick, { passive: true });
    }

    // Mouse tracking for interactive elements
    setupMouseTracking() {
        const trackableElements = document.querySelectorAll('.card, .action-btn, .btn');
        
        trackableElements.forEach(element => {
            element.addEventListener('mousemove', (e) => {
                const rect = element.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                const centerX = rect.width / 2;
                const centerY = rect.height / 2;
                
                const rotateX = (y - centerY) / 10;
                const rotateY = (centerX - x) / 10;
                
                element.style.transform = `
                    perspective(1000px) 
                    rotateX(${rotateX}deg) 
                    rotateY(${rotateY}deg) 
                    translateZ(10px)
                `;
            });

            element.addEventListener('mouseleave', () => {
                element.style.transform = '';
            });
        });
    }

    // Particle effects for celebrations
    setupParticleEffects() {
        this.particleSystem = {
            particles: [],
            canvas: null,
            ctx: null,
            
            init() {
                this.canvas = document.createElement('canvas');
                this.canvas.style.cssText = `
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    pointer-events: none;
                    z-index: 9999;
                `;
                this.ctx = this.canvas.getContext('2d');
                document.body.appendChild(this.canvas);
                this.resize();
                
                window.addEventListener('resize', () => this.resize());
            },
            
            resize() {
                this.canvas.width = window.innerWidth;
                this.canvas.height = window.innerHeight;
            },
            
            createParticle(x, y, type = 'success') {
                const colors = {
                    success: ['#10b981', '#16a34a', '#22c55e'],
                    celebration: ['#f59e0b', '#ea580c', '#dc2626'],
                    rain: ['#0ea5e9', '#3b82f6', '#1d4ed8']
                };
                
                return {
                    x: x || Math.random() * this.canvas.width,
                    y: y || Math.random() * this.canvas.height,
                    vx: (Math.random() - 0.5) * 4,
                    vy: (Math.random() - 0.5) * 4,
                    size: Math.random() * 6 + 2,
                    color: colors[type][Math.floor(Math.random() * colors[type].length)],
                    life: 1,
                    decay: Math.random() * 0.02 + 0.01
                };
            },
            
            animate() {
                this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
                
                for (let i = this.particles.length - 1; i >= 0; i--) {
                    const particle = this.particles[i];
                    
                    particle.x += particle.vx;
                    particle.y += particle.vy;
                    particle.life -= particle.decay;
                    
                    if (particle.life <= 0) {
                        this.particles.splice(i, 1);
                        continue;
                    }
                    
                    this.ctx.save();
                    this.ctx.globalAlpha = particle.life;
                    this.ctx.fillStyle = particle.color;
                    this.ctx.beginPath();
                    this.ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
                    this.ctx.fill();
                    this.ctx.restore();
                }
                
                if (this.particles.length > 0) {
                    requestAnimationFrame(() => this.animate());
                }
            },
            
            burst(x, y, count = 30, type = 'success') {
                for (let i = 0; i < count; i++) {
                    this.particles.push(this.createParticle(x, y, type));
                }
                this.animate();
            }
        };
        
        this.particleSystem.init();
    }

    // Morphing animations for dynamic content
    setupMorphingAnimations() {
        const morphElements = document.querySelectorAll('[data-morph]');
        
        morphElements.forEach(element => {
            const morphType = element.dataset.morph;
            
            if (morphType === 'number') {
                this.animateNumber(element);
            } else if (morphType === 'progress') {
                this.animateProgress(element);
            }
        });
    }

    // Animate numbers with counting effect
    animateNumber(element) {
        const finalValue = parseFloat(element.textContent);
        const duration = 2000;
        const startTime = performance.now();
        
        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            const currentValue = finalValue * this.easeOutCubic(progress);
            element.textContent = Math.round(currentValue);
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };
        
        element.textContent = '0';
        requestAnimationFrame(animate);
    }

    // Physics-based animations
    setupPhysicsAnimations() {
        // Spring animations for buttons
        const springElements = document.querySelectorAll('.btn, .action-btn');
        
        springElements.forEach(element => {
            element.addEventListener('click', (e) => {
                this.createSpringEffect(element, e);
            });
        });
    }

    // Create spring effect on click
    createSpringEffect(element, event) {
        const rect = element.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;
        
        // Create ripple effect
        const ripple = document.createElement('div');
        ripple.style.cssText = `
            position: absolute;
            width: 4px;
            height: 4px;
            left: ${x}px;
            top: ${y}px;
            background: rgba(255, 255, 255, 0.6);
            border-radius: 50%;
            transform: scale(0);
            animation: ripple-spring 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            pointer-events: none;
        `;
        
        element.style.position = 'relative';
        element.appendChild(ripple);
        
        setTimeout(() => {
            ripple.remove();
        }, 600);
        
        // Add spring animation to element
        element.style.animation = 'spring-bounce 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55)';
        setTimeout(() => {
            element.style.animation = '';
        }, 400);
    }

    // Interactive elements setup
    setupInteractiveElements() {
        // Enhanced hover effects
        this.setupEnhancedHovers();
        
        // Gesture recognition - handled in setupGestureControls
        // this.setupGestureRecognition();
        
        // Voice feedback - handled in setupVoiceInteractions
        // this.setupVoiceFeedback();
        
        // Haptic feedback (for supported devices) - not implemented yet
        // this.setupHapticFeedback();
    }

    // Enhanced hover effects
    setupEnhancedHovers() {
        const hoverElements = document.querySelectorAll('.action-btn, .card');
        
        hoverElements.forEach(element => {
            let hoverTimeout;
            
            element.addEventListener('mouseenter', () => {
                clearTimeout(hoverTimeout);
                this.animateHoverIn(element);
            });
            
            element.addEventListener('mouseleave', () => {
                hoverTimeout = setTimeout(() => {
                    this.animateHoverOut(element);
                }, 100);
            });
        });
    }

    // Animate hover in
    animateHoverIn(element) {
        element.style.transition = 'all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275)';
        element.style.transform = 'translateY(-8px) scale(1.02)';
        
        // Add glow effect
        const glowElement = document.createElement('div');
        glowElement.className = 'hover-glow';
        glowElement.style.cssText = `
            position: absolute;
            inset: -10px;
            background: linear-gradient(45deg, transparent, rgba(167, 201, 87, 0.3), transparent);
            border-radius: inherit;
            opacity: 0;
            animation: glow-pulse 2s ease-in-out infinite;
            pointer-events: none;
            z-index: -1;
        `;
        
        element.style.position = 'relative';
        element.appendChild(glowElement);
    }

    // Animate hover out
    animateHoverOut(element) {
        element.style.transform = '';
        
        const glowElement = element.querySelector('.hover-glow');
        if (glowElement) {
            glowElement.remove();
        }
    }

    // Weather effects based on current conditions
    setupWeatherEffects() {
        const weatherWidget = document.querySelector('.weather-widget');
        if (!weatherWidget) return;
        
        const weatherDescription = weatherWidget.querySelector('.weather-description');
        if (!weatherDescription) return;
        
        const description = weatherDescription.textContent.toLowerCase();
        
        if (description.includes('rain') || description.includes('shower')) {
            this.createRainEffect();
        } else if (description.includes('sun') || description.includes('clear')) {
            this.createSunEffect();
        } else if (description.includes('cloud')) {
            this.createCloudEffect();
        } else if (description.includes('storm')) {
            this.createStormEffect();
        }
    }

    // Create rain effect
    createRainEffect() {
        const rainContainer = document.createElement('div');
        rainContainer.className = 'rain-effect';
        rainContainer.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 1;
            overflow: hidden;
        `;
        
        document.body.appendChild(rainContainer);
        
        // Create rain drops
        for (let i = 0; i < 100; i++) {
            setTimeout(() => {
                this.createRainDrop(rainContainer);
            }, i * 50);
        }
        
        // Remove after 10 seconds
        setTimeout(() => {
            rainContainer.remove();
        }, 10000);
    }

    // Create individual rain drop
    createRainDrop(container) {
        const drop = document.createElement('div');
        drop.className = 'rain-drop';
        drop.style.cssText = `
            position: absolute;
            width: 2px;
            height: 20px;
            background: linear-gradient(to bottom, transparent, rgba(14, 165, 233, 0.6));
            left: ${Math.random() * 100}%;
            top: -20px;
            animation: rain-fall ${Math.random() * 0.5 + 0.5}s linear forwards;
        `;
        
        container.appendChild(drop);
        
        setTimeout(() => {
            drop.remove();
        }, 1000);
    }

    // Create sun effect
    createSunEffect() {
        const weatherTemp = document.querySelector('.weather-temp');
        if (weatherTemp) {
            weatherTemp.style.animation = 'sun-glow 3s ease-in-out infinite';
            weatherTemp.style.textShadow = '0 0 20px rgba(245, 158, 11, 0.8)';
        }
    }

    // Create cloud effect
    createCloudEffect() {
        const weatherWidget = document.querySelector('.weather-widget');
        if (weatherWidget) {
            weatherWidget.style.animation = 'float-clouds 6s ease-in-out infinite';
        }
    }

    // Create storm effect
    createStormEffect() {
        let flashCount = 0;
        const maxFlashes = 5;
        
        const flash = () => {
            if (flashCount >= maxFlashes) return;
            
            const lightning = document.createElement('div');
            lightning.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(255, 255, 255, 0.9);
                pointer-events: none;
                z-index: 9998;
                animation: lightning-flash 0.1s ease-out;
            `;
            
            document.body.appendChild(lightning);
            
            setTimeout(() => {
                lightning.remove();
                flashCount++;
                
                if (flashCount < maxFlashes) {
                    setTimeout(flash, Math.random() * 2000 + 500);
                }
            }, 100);
        };
        
        setTimeout(flash, 1000);
    }

    // Market animations
    setupMarketAnimations() {
        const priceItems = document.querySelectorAll('.price-item');
        
        priceItems.forEach(item => {
            this.animateMarketItem(item);
        });
        
        // Simulate real-time price updates
        this.simulateMarketUpdates();
    }

    // Animate individual market item
    animateMarketItem(item) {
        const priceElement = item.querySelector('span');
        if (!priceElement) return;
        
        const originalPrice = priceElement.textContent;
        
        // Add pulse animation on hover
        item.addEventListener('mouseenter', () => {
            priceElement.style.animation = 'price-pulse 0.5s ease-in-out';
        });
        
        item.addEventListener('mouseleave', () => {
            priceElement.style.animation = '';
        });
    }

    // Simulate market updates with animations
    simulateMarketUpdates() {
        const priceItems = document.querySelectorAll('.price-item span');
        
        setInterval(() => {
            const randomItem = priceItems[Math.floor(Math.random() * priceItems.length)];
            if (randomItem) {
                this.animatePriceChange(randomItem);
            }
        }, 5000);
    }

    // Animate price change
    animatePriceChange(element) {
        const currentPrice = parseFloat(element.textContent.replace('₹', ''));
        const change = (Math.random() - 0.5) * 20;
        const newPrice = Math.max(0, currentPrice + change);
        const isIncrease = newPrice > currentPrice;
        
        element.style.animation = isIncrease ? 'price-increase 1s ease-out' : 'price-decrease 1s ease-out';
        element.textContent = `₹${Math.round(newPrice)}`;
        
        // Add particle effect
        const rect = element.getBoundingClientRect();
        this.particleSystem.burst(
            rect.left + rect.width / 2,
            rect.top + rect.height / 2,
            10,
            isIncrease ? 'success' : 'celebration'
        );
        
        setTimeout(() => {
            element.style.animation = '';
        }, 1000);
    }

    // Voice interactions
    setupVoiceInteractions() {
        const voiceButton = document.getElementById('voice-button');
        if (!voiceButton) return;
        
        voiceButton.addEventListener('click', () => {
            this.handleVoiceInteraction();
        });
    }

    // Handle voice interaction with enhanced animations
    handleVoiceInteraction() {
        const voiceButton = document.getElementById('voice-button');
        const listeningAnimation = document.getElementById('listening-animation');
        
        if (!voiceButton) return;
        
        // Start listening animation
        voiceButton.classList.add('listening');
        if (listeningAnimation) {
            listeningAnimation.style.display = 'flex';
        }
        
        // Create voice wave effect
        this.createVoiceWaveEffect();
        
        // Simulate voice processing
        setTimeout(() => {
            this.stopVoiceAnimation();
            this.showVoiceResponse();
        }, 3000);
    }

    // Create voice wave effect
    createVoiceWaveEffect() {
        const voiceButton = document.getElementById('voice-button');
        if (!voiceButton) return;
        
        const waves = [];
        for (let i = 0; i < 3; i++) {
            const wave = document.createElement('div');
            wave.className = 'voice-wave';
            wave.style.cssText = `
                position: absolute;
                width: 100%;
                height: 100%;
                border: 2px solid rgba(16, 185, 129, 0.6);
                border-radius: 50%;
                animation: voice-wave-pulse ${1.5 + i * 0.2}s ease-out infinite;
                animation-delay: ${i * 0.2}s;
            `;
            
            voiceButton.style.position = 'relative';
            voiceButton.appendChild(wave);
            waves.push(wave);
        }
        
        // Store waves for cleanup
        this.voiceWaves = waves;
    }

    // Stop voice animation
    stopVoiceAnimation() {
        const voiceButton = document.getElementById('voice-button');
        const listeningAnimation = document.getElementById('listening-animation');
        
        if (voiceButton) {
            voiceButton.classList.remove('listening');
        }
        
        if (listeningAnimation) {
            listeningAnimation.style.display = 'none';
        }
        
        // Clean up voice waves
        if (this.voiceWaves) {
            this.voiceWaves.forEach(wave => wave.remove());
            this.voiceWaves = null;
        }
    }

    // Show voice response with animation
    showVoiceResponse() {
        const responseContainer = document.getElementById('voice-response');
        if (!responseContainer) return;
        
        responseContainer.style.display = 'block';
        responseContainer.innerHTML = `
            <div class="voice-response-content">
                <div class="response-avatar">🤖</div>
                <div class="response-text">
                    <p><strong>AI Assistant:</strong> मैंने आपकी बात सुनी है। आपकी फसल की समस्या के लिए यहाँ कुछ सुझाव हैं...</p>
                </div>
            </div>
        `;
        
        responseContainer.style.animation = 'slide-up-fade 0.5s ease-out';
        
        // Auto-hide after 10 seconds
        setTimeout(() => {
            responseContainer.style.animation = 'fade-out 0.5s ease-out';
            setTimeout(() => {
                responseContainer.style.display = 'none';
            }, 500);
        }, 10000);
    }

    // Gesture controls for mobile
    setupGestureControls() {
        let touchStartX = 0;
        let touchStartY = 0;
        
        document.addEventListener('touchstart', (e) => {
            touchStartX = e.touches[0].clientX;
            touchStartY = e.touches[0].clientY;
        }, { passive: true });
        
        document.addEventListener('touchend', (e) => {
            const touchEndX = e.changedTouches[0].clientX;
            const touchEndY = e.changedTouches[0].clientY;
            
            const deltaX = touchEndX - touchStartX;
            const deltaY = touchEndY - touchStartY;
            
            // Swipe gestures
            if (Math.abs(deltaX) > Math.abs(deltaY) && Math.abs(deltaX) > 50) {
                if (deltaX > 0) {
                    this.handleSwipeRight();
                } else {
                    this.handleSwipeLeft();
                }
            } else if (Math.abs(deltaY) > 50) {
                if (deltaY > 0) {
                    this.handleSwipeDown();
                } else {
                    this.handleSwipeUp();
                }
            }
        }, { passive: true });
    }

    // Handle swipe gestures
    handleSwipeRight() {
        // Navigate back or show previous content
        console.log('Swipe right detected');
    }

    handleSwipeLeft() {
        // Navigate forward or show next content
        console.log('Swipe left detected');
    }

    handleSwipeUp() {
        // Scroll to top or show more content
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    handleSwipeDown() {
        // Refresh content or show menu
        this.refreshContent();
    }

    // Accessibility features
    setupAccessibilityFeatures() {
        // High contrast mode toggle
        this.setupHighContrastMode();
        
        // Font size adjustment
        this.setupFontSizeAdjustment();
        
        // Keyboard navigation
        this.setupKeyboardNavigation();
        
        // Screen reader support
        this.setupScreenReaderSupport();
    }

    // High contrast mode
    setupHighContrastMode() {
        const contrastToggle = document.createElement('button');
        contrastToggle.className = 'contrast-toggle';
        contrastToggle.innerHTML = '🔆';
        contrastToggle.title = 'Toggle High Contrast';
        contrastToggle.style.cssText = `
            position: fixed;
            top: 100px;
            right: 20px;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background: var(--primary-green);
            color: white;
            border: none;
            font-size: 1.2rem;
            cursor: pointer;
            z-index: 1000;
            box-shadow: var(--shadow-md);
        `;
        
        contrastToggle.addEventListener('click', () => {
            document.body.classList.toggle('high-contrast');
            contrastToggle.innerHTML = document.body.classList.contains('high-contrast') ? '🔅' : '🔆';
        });
        
        document.body.appendChild(contrastToggle);
    }

    // Font size adjustment
    setupFontSizeAdjustment() {
        const fontControls = document.createElement('div');
        fontControls.className = 'font-controls';
        fontControls.innerHTML = `
            <button class="font-decrease" title="Decrease Font Size">A-</button>
            <button class="font-increase" title="Increase Font Size">A+</button>
        `;
        fontControls.style.cssText = `
            position: fixed;
            top: 160px;
            right: 20px;
            display: flex;
            flex-direction: column;
            gap: 5px;
            z-index: 1000;
        `;
        
        const buttons = fontControls.querySelectorAll('button');
        buttons.forEach(btn => {
            btn.style.cssText = `
                width: 40px;
                height: 40px;
                border-radius: 50%;
                background: var(--primary-green);
                color: white;
                border: none;
                font-size: 0.9rem;
                cursor: pointer;
                box-shadow: var(--shadow-sm);
            `;
        });
        
        let currentFontSize = 1;
        
        fontControls.querySelector('.font-increase').addEventListener('click', () => {
            if (currentFontSize < 1.5) {
                currentFontSize += 0.1;
                document.documentElement.style.fontSize = `${currentFontSize}rem`;
            }
        });
        
        fontControls.querySelector('.font-decrease').addEventListener('click', () => {
            if (currentFontSize > 0.8) {
                currentFontSize -= 0.1;
                document.documentElement.style.fontSize = `${currentFontSize}rem`;
            }
        });
        
        document.body.appendChild(fontControls);
    }

    // Keyboard navigation
    setupKeyboardNavigation() {
        document.addEventListener('keydown', (e) => {
            switch(e.key) {
                case 'Tab':
                    this.highlightFocusedElement(e.target);
                    break;
                case 'Enter':
                case ' ':
                    if (e.target.classList.contains('action-btn')) {
                        e.preventDefault();
                        e.target.click();
                    }
                    break;
                case 'Escape':
                    this.closeModals();
                    break;
            }
        });
    }

    // Highlight focused element
    highlightFocusedElement(element) {
        // Remove previous highlights
        document.querySelectorAll('.keyboard-focus').forEach(el => {
            el.classList.remove('keyboard-focus');
        });
        
        // Add highlight to current element
        if (element) {
            element.classList.add('keyboard-focus');
        }
    }

    // Screen reader support
    setupScreenReaderSupport() {
        // Add ARIA labels to interactive elements
        const interactiveElements = document.querySelectorAll('.action-btn, .btn, .card');
        
        interactiveElements.forEach(element => {
            if (!element.getAttribute('aria-label')) {
                const text = element.textContent.trim() || element.title || 'Interactive element';
                element.setAttribute('aria-label', text);
            }
            
            if (!element.getAttribute('role')) {
                element.setAttribute('role', 'button');
            }
        });
        
        // Add live region for dynamic content
        const liveRegion = document.createElement('div');
        liveRegion.setAttribute('aria-live', 'polite');
        liveRegion.setAttribute('aria-atomic', 'true');
        liveRegion.className = 'sr-only';
        liveRegion.style.cssText = `
            position: absolute;
            width: 1px;
            height: 1px;
            padding: 0;
            margin: -1px;
            overflow: hidden;
            clip: rect(0, 0, 0, 0);
            white-space: nowrap;
            border: 0;
        `;
        
        document.body.appendChild(liveRegion);
        this.liveRegion = liveRegion;
    }

    // Performance optimizations
    setupPerformanceOptimizations() {
        // Lazy loading for images
        this.setupLazyLoading();
        
        // Debounced scroll events
        this.setupDebouncedEvents();
        
        // Memory management
        this.setupMemoryManagement();
    }

    // Lazy loading for images
    setupLazyLoading() {
        const images = document.querySelectorAll('img[data-src]');
        
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.add('loaded');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    }

    // Debounced events for performance
    setupDebouncedEvents() {
        let scrollTimeout;
        let resizeTimeout;
        
        window.addEventListener('scroll', () => {
            clearTimeout(scrollTimeout);
            scrollTimeout = setTimeout(() => {
                this.handleOptimizedScroll();
            }, 16); // ~60fps
        }, { passive: true });
        
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimeout);
            resizeTimeout = setTimeout(() => {
                this.handleOptimizedResize();
            }, 250);
        });
    }

    // Optimized scroll handler
    handleOptimizedScroll() {
        const scrolled = window.pageYOffset;
        const navbar = document.querySelector('.navbar');
        
        if (navbar) {
            if (scrolled > 100) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        }
    }

    // Optimized resize handler
    handleOptimizedResize() {
        if (this.particleSystem && this.particleSystem.canvas) {
            this.particleSystem.resize();
        }
    }

    // Memory management
    setupMemoryManagement() {
        // Clean up animations when elements are removed
        const mutationObserver = new MutationObserver((mutations) => {
            mutations.forEach(mutation => {
                mutation.removedNodes.forEach(node => {
                    if (node.nodeType === Node.ELEMENT_NODE) {
                        this.cleanupElement(node);
                    }
                });
            });
        });
        
        mutationObserver.observe(document.body, {
            childList: true,
            subtree: true
        });
    }

    // Cleanup element animations and listeners
    cleanupElement(element) {
        // Remove from observers
        this.observers.forEach(observer => {
            observer.unobserve(element);
        });
        
        // Clear animations
        if (this.animations.has(element)) {
            const animation = this.animations.get(element);
            if (animation.cancel) {
                animation.cancel();
            }
            this.animations.delete(element);
        }
    }

    // Utility functions
    easeOutCubic(t) {
        return 1 - Math.pow(1 - t, 3);
    }

    easeInOutCubic(t) {
        return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
    }

    // Refresh content with animation
    refreshContent() {
        const refreshIndicator = document.createElement('div');
        refreshIndicator.className = 'refresh-indicator';
        refreshIndicator.innerHTML = '🔄 Refreshing...';
        refreshIndicator.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: var(--shadow-lg);
            z-index: 9999;
            animation: fade-in 0.3s ease-out;
        `;
        
        document.body.appendChild(refreshIndicator);
        
        setTimeout(() => {
            refreshIndicator.remove();
            // Trigger actual refresh logic here
            window.location.reload();
        }, 1500);
    }

    // Close all modals
    closeModals() {
        const modals = document.querySelectorAll('.modal.show');
        modals.forEach(modal => {
            const modalInstance = bootstrap.Modal.getInstance(modal);
            if (modalInstance) {
                modalInstance.hide();
            }
        });
    }

    // Announce to screen reader
    announceToScreenReader(message) {
        if (this.liveRegion) {
            this.liveRegion.textContent = message;
        }
    }

    // Animate weather widget
    animateWeatherWidget(element) {
        const temp = element.querySelector('.weather-temp');
        if (temp) {
            temp.style.animation = 'number-count 2s ease-out';
        }
    }

    // Animate market ticker
    animateMarketTicker(element) {
        const ticker = element.querySelector('.ticker-content');
        if (ticker) {
            ticker.style.animationPlayState = 'running';
        }
    }

    // Animate action button
    animateActionButton(element) {
        element.style.animation = 'bounce-in 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55)';
    }

    // Animate voice assistant
    animateVoiceAssistant(element) {
        const assistantHeader = element.querySelector('.assistant-header');
        if (assistantHeader) {
            assistantHeader.style.animation = 'glow-pulse 2s ease-in-out infinite';
        }
    }
}

// CSS animations to inject
const enhancedAnimationStyles = `
<style>
@keyframes ripple-spring {
    to {
        transform: scale(100);
        opacity: 0;
    }
}

@keyframes spring-bounce {
    0% { transform: scale(1); }
    50% { transform: scale(0.95); }
    100% { transform: scale(1); }
}

@keyframes glow-pulse {
    0%, 100% { box-shadow: 0 0 20px rgba(167, 201, 87, 0.3); }
    50% { box-shadow: 0 0 40px rgba(167, 201, 87, 0.6); }
}

@keyframes sun-glow {
    0%, 100% { text-shadow: 0 0 20px rgba(245, 158, 11, 0.8); }
    50% { text-shadow: 0 0 40px rgba(245, 158, 11, 1), 0 0 60px rgba(245, 158, 11, 0.8); }
}

@keyframes float-clouds {
    0%, 100% { transform: translateX(0px); }
    50% { transform: translateX(10px); }
}

@keyframes lightning-flash {
    0%, 100% { opacity: 0; }
    50% { opacity: 1; }
}

@keyframes price-pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.1); }
}

@keyframes price-increase {
    0% { background: rgba(16, 185, 129, 0.2); transform: scale(1); }
    50% { background: rgba(16, 185, 129, 0.4); transform: scale(1.05); }
    100% { background: transparent; transform: scale(1); }
}

@keyframes price-decrease {
    0% { background: rgba(239, 68, 68, 0.2); transform: scale(1); }
    50% { background: rgba(239, 68, 68, 0.4); transform: scale(1.05); }
    100% { background: transparent; transform: scale(1); }
}

@keyframes voice-wave-pulse {
    0% { transform: scale(1); opacity: 1; }
    100% { transform: scale(2); opacity: 0; }
}

@keyframes slide-up-fade {
    from { transform: translateY(30px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}

@keyframes fade-out {
    from { opacity: 1; }
    to { opacity: 0; }
}

@keyframes number-count {
    from { transform: scale(0.8); }
    to { transform: scale(1); }
}

@keyframes bounce-in {
    0% { transform: scale(0.3); opacity: 0; }
    50% { transform: scale(1.05); }
    70% { transform: scale(0.9); }
    100% { transform: scale(1); opacity: 1; }
}

.keyboard-focus {
    outline: 3px solid var(--accent-green) !important;
    outline-offset: 2px !important;
}

.high-contrast {
    filter: contrast(150%) brightness(120%);
}

.high-contrast .card {
    border: 2px solid var(--primary-green) !important;
}

.high-contrast .btn {
    border: 2px solid currentColor !important;
}

.animate-ready {
    opacity: 0;
    transform: translateY(30px);
    transition: all 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.animated-in {
    opacity: 1;
    transform: translateY(0);
}

.fadeInUp {
    animation: fadeIn 0.8s ease-out forwards;
}

.voice-response-content {
    display: flex;
    align-items: flex-start;
    gap: 15px;
}

.response-avatar {
    font-size: 2rem;
    animation: bounce 1s ease-in-out infinite;
}

.response-text {
    flex: 1;
}

.refresh-indicator {
    animation: pulse 1s ease-in-out infinite;
}

@media (max-width: 768px) {
    .contrast-toggle,
    .font-controls {
        right: 10px;
    }
    
    .font-controls button {
        width: 35px;
        height: 35px;
        font-size: 0.8rem;
    }
}
</style>
`;

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Inject enhanced animation styles
    document.head.insertAdjacentHTML('beforeend', enhancedAnimationStyles);
    
    // Initialize enhanced UI
    window.farmerUI = new FarmerUIEnhanced();
    
    // Global functions for external use
    window.showSuccess = (message) => {
        window.farmerUI.announceToScreenReader(message);
        window.farmerUI.particleSystem.burst(
            window.innerWidth / 2,
            window.innerHeight / 2,
            50,
            'success'
        );
    };
    
    window.showCelebration = (x, y) => {
        window.farmerUI.particleSystem.burst(x || window.innerWidth / 2, y || window.innerHeight / 2, 100, 'celebration');
    };
    
    window.createWeatherEffect = (type) => {
        if (type === 'rain') {
            window.farmerUI.createRainEffect();
        } else if (type === 'sun') {
            window.farmerUI.createSunEffect();
        } else if (type === 'storm') {
            window.farmerUI.createStormEffect();
        }
    };
    
    console.log('🎉 Enhanced Farmer UI loaded successfully!');
});

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = FarmerUIEnhanced;
}