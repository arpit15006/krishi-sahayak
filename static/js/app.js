// Krishi Sahayak - Main Application JavaScript

// Global app state
const KrishiSahayak = {
    isOnline: navigator.onLine,
    currentUser: null,
    weatherData: null,
    marketData: null
};

// Remove external icon dependencies
const removeExternalDependencies = () => {
    // Remove any external icon script tags
    const externalScripts = document.querySelectorAll('script[src*="heroicons"], script[src*="unpkg"]');
    externalScripts.forEach(script => script.remove());
};

// Call immediately
removeExternalDependencies();

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    registerServiceWorker();
    setupEventListeners();
    checkOnlineStatus();
});

// Initialize application
function initializeApp() {
    console.log('🌱 Krishi Sahayak initializing...');
    
    // Add fade-in animation to main content
    const mainContent = document.querySelector('.main-content');
    if (mainContent) {
        mainContent.classList.add('fade-in');
    }
    
    // Initialize components based on current page
    const currentPage = getCurrentPage();
    
    switch(currentPage) {
        case 'dashboard':
            initializeDashboard();
            break;
        case 'scanner':
            initializeScanner();
            break;
        case 'weather':
            initializeWeatherPage();
            break;
        case 'market':
            initializeMarketPage();
            break;
        case 'passport':
            initializePassportPage();
            break;
        default:
            initializeHomePage();
    }
}

// Get current page identifier
function getCurrentPage() {
    const path = window.location.pathname;
    if (path.includes('dashboard')) return 'dashboard';
    if (path.includes('scanner')) return 'scanner';
    if (path.includes('weather')) return 'weather';
    if (path.includes('market')) return 'market';
    if (path.includes('passport')) return 'passport';
    return 'home';
}

// Register Service Worker for PWA
function registerServiceWorker() {
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/static/js/sw.js')
            .then(registration => {
                console.log('✅ Service Worker registered:', registration);
            })
            .catch(error => {
                console.log('❌ Service Worker registration failed:', error);
            });
    }
}

// Setup global event listeners
function setupEventListeners() {
    // Online/offline status
    window.addEventListener('online', handleOnlineStatus);
    window.addEventListener('offline', handleOfflineStatus);
    
    // Form submissions with loading states
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', handleFormSubmission);
    });
    
    // File upload handling
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', handleFileSelection);
    });
    
    // Quick action buttons
    const actionBtns = document.querySelectorAll('.action-btn');
    actionBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            this.style.transform = 'translateY(-2px)';
            setTimeout(() => {
                this.style.transform = '';
            }, 150);
        });
    });
    
    // Back button handling
    const backButtons = document.querySelectorAll('.btn-back');
    backButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            window.history.back();
        });
    });
}

// Check online status
function checkOnlineStatus() {
    KrishiSahayak.isOnline = navigator.onLine;
    updateUIForConnectivity();
}

function handleOnlineStatus() {
    KrishiSahayak.isOnline = true;
    showNotification('🌐 Back online! All features are available.', 'success');
    updateUIForConnectivity();
}

function handleOfflineStatus() {
    KrishiSahayak.isOnline = false;
    showNotification('📵 You are offline. Some features may be limited.', 'warning');
    updateUIForConnectivity();
}

function updateUIForConnectivity() {
    const offlineElements = document.querySelectorAll('.requires-online');
    offlineElements.forEach(el => {
        if (KrishiSahayak.isOnline) {
            el.classList.remove('disabled');
            el.removeAttribute('disabled');
        } else {
            el.classList.add('disabled');
            el.setAttribute('disabled', 'disabled');
        }
    });
}

// Form submission handling
function handleFormSubmission(e) {
    const form = e.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    
    if (submitBtn) {
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<div class="spinner"></div> Processing...';
        submitBtn.disabled = true;
        
        // Reset button after form submission (handled by page redirect usually)
        setTimeout(() => {
            if (submitBtn) {
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            }
        }, 5000);
    }
}

// File selection handling
function handleFileSelection(e) {
    const file = e.target.files[0];
    if (!file) return;
    
    // Validate file type
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif'];
    if (!allowedTypes.includes(file.type)) {
        showNotification('❌ Please select a valid image file (JPG, PNG, GIF)', 'error');
        e.target.value = '';
        return;
    }
    
    // Validate file size (max 16MB)
    const maxSize = 16 * 1024 * 1024;
    if (file.size > maxSize) {
        showNotification('❌ File size too large. Please select an image under 16MB.', 'error');
        e.target.value = '';
        return;
    }
    
    // Show preview if it's an image
    if (file.type.startsWith('image/')) {
        showImagePreview(file, e.target);
    }
    
    showNotification('✅ Image selected successfully!', 'success');
}

// Show image preview
function showImagePreview(file, input) {
    const reader = new FileReader();
    reader.onload = function(e) {
        // Find or create preview container
        let preview = input.parentNode.querySelector('.image-preview');
        if (!preview) {
            preview = document.createElement('div');
            preview.className = 'image-preview mt-3';
            input.parentNode.appendChild(preview);
        }
        
        preview.innerHTML = `
            <img src="${e.target.result}" 
                 alt="Preview" 
                 style="max-width: 200px; max-height: 200px; border-radius: 8px; object-fit: cover;">
            <p class="mt-2 text-muted">Ready to analyze: ${file.name}</p>
        `;
    };
    reader.readAsDataURL(file);
}

// Initialize Dashboard
function initializeDashboard() {
    console.log('📊 Initializing dashboard...');
    
    // Animate cards on load
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.classList.add('slide-up');
        }, index * 100);
    });
    
    // Initialize weather widget
    updateWeatherWidget();
    
    // Initialize market ticker
    updateMarketTicker();
    
    // Set up auto-refresh for real-time data
    setInterval(updateMarketTicker, 60000); // Update every minute
    setInterval(updateWeatherWidget, 300000); // Update every 5 minutes
}

// Initialize Scanner
function initializeScanner() {
    console.log('📸 Initializing scanner...');
    
    const uploadArea = document.querySelector('.upload-area');
    const fileInput = document.querySelector('.file-input');
    
    if (uploadArea && fileInput) {
        // Drag and drop functionality
        uploadArea.addEventListener('dragover', function(e) {
            e.preventDefault();
            this.classList.add('dragover');
        });
        
        uploadArea.addEventListener('dragleave', function(e) {
            e.preventDefault();
            this.classList.remove('dragover');
        });
        
        uploadArea.addEventListener('drop', function(e) {
            e.preventDefault();
            this.classList.remove('dragover');
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                fileInput.files = files;
                fileInput.dispatchEvent(new Event('change'));
            }
        });
        
        // Click to upload
        uploadArea.addEventListener('click', function() {
            fileInput.click();
        });
    }
    
    // Camera access for mobile devices
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        const cameraBtn = document.getElementById('camera-btn');
        if (cameraBtn) {
            cameraBtn.style.display = 'inline-block';
            cameraBtn.addEventListener('click', openCamera);
        }
    }
}

// Open camera for image capture
async function openCamera() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ 
            video: { facingMode: 'environment' } // Use back camera
        });
        
        // Create camera modal
        const modal = document.createElement('div');
        modal.className = 'camera-modal';
        modal.innerHTML = `
            <div class="camera-container">
                <video id="camera-video" autoplay playsinline></video>
                <canvas id="camera-canvas" style="display: none;"></canvas>
                <div class="camera-controls">
                    <button class="btn btn-primary" id="capture-btn">📷 Capture</button>
                    <button class="btn btn-secondary" id="close-camera-btn">❌ Close</button>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        const video = document.getElementById('camera-video');
        const canvas = document.getElementById('camera-canvas');
        const ctx = canvas.getContext('2d');
        
        video.srcObject = stream;
        
        // Capture button functionality
        document.getElementById('capture-btn').addEventListener('click', function() {
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            ctx.drawImage(video, 0, 0);
            
            // Convert to blob and create file
            canvas.toBlob(function(blob) {
                const file = new File([blob], 'captured-image.jpg', { type: 'image/jpeg' });
                const fileInput = document.querySelector('.file-input');
                
                // Create FileList object
                const dt = new DataTransfer();
                dt.items.add(file);
                fileInput.files = dt.files;
                
                fileInput.dispatchEvent(new Event('change'));
                
                // Close camera
                stream.getTracks().forEach(track => track.stop());
                document.body.removeChild(modal);
            }, 'image/jpeg', 0.8);
        });
        
        // Close button functionality
        document.getElementById('close-camera-btn').addEventListener('click', function() {
            stream.getTracks().forEach(track => track.stop());
            document.body.removeChild(modal);
        });
        
    } catch (error) {
        console.error('Camera access error:', error);
        showNotification('❌ Camera access denied or not available', 'error');
    }
}

// Initialize Weather Page
function initializeWeatherPage() {
    console.log('🌤️ Initializing weather page...');
    
    // Animate weather cards
    const weatherCards = document.querySelectorAll('.forecast-day');
    weatherCards.forEach((card, index) => {
        setTimeout(() => {
            card.classList.add('slide-up');
        }, index * 100);
    });
}

// Initialize Market Page
function initializeMarketPage() {
    console.log('💰 Initializing market page...');
    
    // Animate price cards
    const priceCards = document.querySelectorAll('.price-card');
    priceCards.forEach((card, index) => {
        setTimeout(() => {
            card.classList.add('fade-in');
        }, index * 50);
    });
}

// Initialize Passport Page
function initializePassportPage() {
    console.log('🎫 Initializing passport page...');
    
    // Mock blockchain functionality
    const createPassportBtn = document.querySelector('.create-passport-btn');
    if (createPassportBtn) {
        createPassportBtn.addEventListener('click', function() {
            // Simulate blockchain transaction
            this.innerHTML = '<div class="spinner"></div> Creating on blockchain...';
            this.disabled = true;
            
            setTimeout(() => {
                showNotification('✅ Digital passport created successfully on blockchain!', 'success');
                setTimeout(() => {
                    window.location.reload();
                }, 1500);
            }, 3000);
        });
    }
    
    // Weather shield simulation
    const shieldBtn = document.querySelector('.weather-shield-btn');
    if (shieldBtn) {
        shieldBtn.addEventListener('click', function() {
            showNotification('⚡ Weather Shield activated! Parametric insurance is now monitoring your crops.', 'success');
        });
    }
    
    const simulateBtn = document.querySelector('.simulate-weather-btn');
    if (simulateBtn) {
        simulateBtn.addEventListener('click', function() {
            this.innerHTML = '<div class="spinner"></div> Simulating weather event...';
            this.disabled = true;
            
            setTimeout(() => {
                showNotification('💰 Payout Triggered! 0.1 MATIC has been sent to your wallet.', 'success');
                this.innerHTML = 'Simulate Extreme Weather Event';
                this.disabled = false;
            }, 2000);
        });
    }
}

// Initialize Home Page
function initializeHomePage() {
    console.log('🏠 Initializing home page...');
    
    // Animate hero section
    const hero = document.querySelector('.hero-section');
    if (hero) {
        hero.classList.add('fade-in');
    }
}

// Update Weather Widget
function updateWeatherWidget() {
    const weatherWidget = document.querySelector('.weather-widget');
    if (!weatherWidget) return;
    
    // Add loading state
    const currentTemp = weatherWidget.querySelector('.weather-temp');
    if (currentTemp && currentTemp.textContent === 'Loading...') {
        currentTemp.innerHTML = '<div class="spinner"></div>';
    }
}

// Update Market Ticker
function updateMarketTicker() {
    const ticker = document.querySelector('.ticker-content');
    if (!ticker) return;
    
    // Animate price changes
    const priceItems = ticker.querySelectorAll('.price-item');
    priceItems.forEach(item => {
        const changeElement = item.querySelector('.price-change');
        if (changeElement) {
            // Add subtle animation to price changes
            changeElement.style.transition = 'all 0.3s ease';
        }
    });
}

// Notification system
function showNotification(message, type = 'info', duration = 5000) {
    // Remove existing notifications
    const existingNotifications = document.querySelectorAll('.toast-notification');
    existingNotifications.forEach(notification => notification.remove());
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `toast-notification alert alert-${type} position-fixed`;
    notification.style.cssText = `
        top: 20px;
        right: 20px;
        z-index: 9999;
        max-width: 400px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        animation: slideIn 0.3s ease;
    `;
    
    notification.innerHTML = `
        <div class="d-flex align-items-center">
            <span class="flex-grow-1">${message}</span>
            <button type="button" class="btn-close" aria-label="Close"></button>
        </div>
    `;
    
    // Add close functionality
    const closeBtn = notification.querySelector('.btn-close');
    closeBtn.addEventListener('click', () => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    });
    
    // Auto-remove after duration
    setTimeout(() => {
        if (notification.parentNode) {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }
    }, duration);
    
    document.body.appendChild(notification);
}

// Add notification animations to CSS
const notificationStyles = document.createElement('style');
notificationStyles.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
    
    .camera-modal {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.9);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10000;
    }
    
    .camera-container {
        background: white;
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        max-width: 90%;
        max-height: 90%;
    }
    
    #camera-video {
        max-width: 100%;
        max-height: 70vh;
        border-radius: 8px;
    }
    
    .camera-controls {
        margin-top: 1rem;
        display: flex;
        gap: 1rem;
        justify-content: center;
    }
    
    .upload-area.dragover {
        border-color: var(--secondary-green);
        background: var(--light-blue);
        transform: scale(1.02);
    }
    
    .disabled {
        opacity: 0.6;
        pointer-events: none;
    }
`;

document.head.appendChild(notificationStyles);

// Utility functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR',
        minimumFractionDigits: 0
    }).format(amount);
}

function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('en-IN', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Export for testing purposes
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { KrishiSahayak, showNotification, formatCurrency };
}
