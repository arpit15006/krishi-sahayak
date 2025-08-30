/**
 * Multilingual Support for Krishi Sahayak
 * Handles dynamic language switching and text updates
 */

// Language translations for dynamic content
const translations = {
    'en': {
        'loading': 'Loading...',
        'error': 'Error',
        'success': 'Success',
        'warning': 'Warning',
        'info': 'Information',
        'submit': 'Submit',
        'cancel': 'Cancel',
        'save': 'Save',
        'edit': 'Edit',
        'delete': 'Delete',
        'view': 'View',
        'download': 'Download',
        'print': 'Print',
        'share': 'Share',
        'search': 'Search',
        'filter': 'Filter',
        'sort': 'Sort',
        'calculate': 'Calculate',
        'results': 'Results',
        'recommendations': 'Recommendations',
        'cost_analysis': 'Cost Analysis',
        'seed_required': 'Seed Required',
        'total_cost': 'Total Cost',
        'estimated_cost': 'Estimated Cost',
        'farm_area': 'Farm Area',
        'crop_type': 'Crop Type',
        'variety': 'Variety',
        'season': 'Season',
        'sowing_method': 'Sowing Method',
        'soil_type': 'Soil Type',
        'organic': 'Organic',
        'sustainable': 'Sustainable',
        'drip_irrigation': 'Drip Irrigation',
        'broadcasting': 'Broadcasting',
        'line_sowing': 'Line Sowing',
        'transplanting': 'Transplanting',
        'dibbling': 'Dibbling',
        'acres': 'Acres',
        'hectares': 'Hectares',
        'bigha': 'Bigha',
        'katha': 'Katha',
        'kharif': 'Kharif',
        'rabi': 'Rabi',
        'summer': 'Summer',
        'parametric_weather_insurance': 'Parametric weather insurance',
        'ai_powered_crop_yield': 'AI-powered crop yield forecasting',
        'farming_guides_tutorials': 'Farming guides, tutorials & tools',
        'smart_protection': 'Smart Protection',
        'accurate': 'Accurate',
        'guides': '50+ Guides',
        'blockchain_secured': 'Blockchain Secured',
        'live_prices': 'Live Prices',
        'accuracy': '95% Accuracy',
        'weather_shield': 'Weather Shield',
        'yield_prediction': 'Yield Prediction',
        'resources': 'Resources'
    },
    'hi': {
        'loading': 'लोड हो रहा है...',
        'error': 'त्रुटि',
        'success': 'सफलता',
        'warning': 'चेतावनी',
        'info': 'जानकारी',
        'submit': 'जमा करें',
        'cancel': 'रद्द करें',
        'save': 'सेव करें',
        'edit': 'संपादित करें',
        'delete': 'हटाएं',
        'view': 'देखें',
        'download': 'डाउनलोड करें',
        'print': 'प्रिंट करें',
        'share': 'साझा करें',
        'search': 'खोजें',
        'filter': 'फिल्टर करें',
        'sort': 'क्रमबद्ध करें',
        'calculate': 'गणना करें',
        'results': 'परिणाम',
        'recommendations': 'सुझाव',
        'cost_analysis': 'लागत विश्लेषण',
        'seed_required': 'बीज की आवश्यकता',
        'total_cost': 'कुल लागत',
        'estimated_cost': 'अनुमानित लागत',
        'farm_area': 'खेत का क्षेत्रफल',
        'crop_type': 'फसल का प्रकार',
        'variety': 'किस्म',
        'season': 'मौसम',
        'sowing_method': 'बुवाई की विधि',
        'soil_type': 'मिट्टी का प्रकार',
        'organic': 'जैविक',
        'sustainable': 'टिकाऊ',
        'drip_irrigation': 'ड्रिप सिंचाई',
        'broadcasting': 'छिड़काव विधि',
        'line_sowing': 'कतार में बुवाई',
        'transplanting': 'रोपाई',
        'dibbling': 'गड्ढा विधि',
        'acres': 'एकड़',
        'hectares': 'हेक्टेयर',
        'bigha': 'बीघा',
        'katha': 'कठा',
        'kharif': 'खरीफ',
        'rabi': 'रबी',
        'summer': 'गर्मी',
        'parametric_weather_insurance': 'पैरामेट्रिक मौसम बीमा',
        'ai_powered_crop_yield': 'AI-संचालित फसल उत्पादन पूर्वानुमान',
        'farming_guides_tutorials': 'कृषि गाइड, ट्यूटोरियल और उपकरण',
        'smart_protection': 'स्मार्ट सुरक्षा',
        'accurate': 'सटीक',
        'guides': '50+ गाइड',
        'blockchain_secured': 'ब्लॉकचेन सुरक्षित',
        'live_prices': 'लाइव कीमतें',
        'accuracy': '95% सटीकता',
        'weather_shield': 'मौसम सुरक्षा',
        'yield_prediction': 'उत्पादन पूर्वानुमान',
        'resources': 'संसाधन'
    },
    'gu': {
        'loading': 'લોડ થઈ રહ્યું છે...',
        'error': 'ભૂલ',
        'success': 'સફળતા',
        'warning': 'ચેતવણી',
        'info': 'માહિતી',
        'submit': 'સબમિટ કરો',
        'cancel': 'રદ કરો',
        'save': 'સેવ કરો',
        'edit': 'સંપાદિત કરો',
        'delete': 'કાઢી નાખો',
        'view': 'જુઓ',
        'download': 'ડાઉનલોડ કરો',
        'print': 'પ્રિન્ટ કરો',
        'share': 'શેર કરો',
        'search': 'શોધો',
        'filter': 'ફિલ્ટર કરો',
        'sort': 'ક્રમમાં ગોઠવો',
        'calculate': 'ગણતરી કરો',
        'results': 'પરિણામો',
        'recommendations': 'સુઝાવો',
        'cost_analysis': 'ખર્ચ વિશ્લેષણ',
        'seed_required': 'બીજની જરૂરિયાત',
        'total_cost': 'કુલ ખર્ચ',
        'estimated_cost': 'અંદાજિત ખર્ચ',
        'farm_area': 'ખેતરનો વિસ્તાર',
        'crop_type': 'પાકનો પ્રકાર',
        'variety': 'જાત',
        'season': 'મોસમ',
        'sowing_method': 'વાવણીની પદ્ધતિ',
        'soil_type': 'માટીનો પ્રકાર',
        'organic': 'જૈવિક',
        'sustainable': 'ટકાઉ',
        'drip_irrigation': 'ડ્રિપ સિંચાઈ',
        'broadcasting': 'છાંટવાની પદ્ધતિ',
        'line_sowing': 'લાઈનમાં વાવણી',
        'transplanting': 'રોપણી',
        'dibbling': 'ખાડા પદ્ધતિ',
        'acres': 'એકર',
        'hectares': 'હેક્ટર',
        'bigha': 'બીઘા',
        'katha': 'કઠા',
        'kharif': 'ખરીફ',
        'rabi': 'રબી',
        'summer': 'ઉનાળો',
        'parametric_weather_insurance': 'પેરામેટ્રિક હવામાન વીમો',
        'ai_powered_crop_yield': 'AI-સંચાલિત પાક ઉત્પાદન આગાહી',
        'farming_guides_tutorials': 'ખેતી માર્ગદર્શિકાઓ, ટ્યુટોરિયલ અને સાધનો',
        'smart_protection': 'સ્માર્ટ સુરક્ષા',
        'accurate': 'સચોટ',
        'guides': '50+ માર્ગદર્શિકાઓ',
        'blockchain_secured': 'બ્લોકચેન સુરક્ષિત',
        'live_prices': 'લાઇવ કિંમતો',
        'accuracy': '95% સચોટતா',
        'weather_shield': 'હવામાન સુરક્ષા',
        'yield_prediction': 'ઉત્પાદન આગાહી',
        'resources': 'સંસાધનો',
        'parametric_weather_insurance': 'પેરામેટ્રિક હવામાન વીમો',
        'ai_powered_crop_yield': 'AI-સંચાલિત પાક ઉત્પાદન આગાહી',
        'farming_guides_tutorials': 'ખેતી માર્ગદર્શિકાઓ, ટ્યુટોરિયલ અને સાધનો',
        'smart_protection': 'સ્માર્ટ સુરક્ષા',
        'accurate': 'સચોટ',
        'guides': '50+ માર્ગદર્શિકાઓ',
        'blockchain_secured': 'બ્લોકચેન સુરક્ષિત',
        'live_prices': 'લાઇવ કિંમતો',
        'accuracy': '95% સચોટતા',
        'weather_shield': 'હવામાન સુરક્ષા',
        'yield_prediction': 'ઉત્પાદન આગાહી',
        'resources': 'સંસાધનો'
    },
    'mr': {
        'loading': 'लोड होत आहे...',
        'error': 'त्रुटी',
        'success': 'यश',
        'warning': 'चेतावणी',
        'info': 'माहिती',
        'submit': 'सबमिट करा',
        'cancel': 'रद्द करा',
        'save': 'सेव्ह करा',
        'calculate': 'गणना करा',
        'results': 'परिणाम',
        'recommendations': 'शिफारसी',
        'cost_analysis': 'खर्च विश्लेषण',
        'seed_required': 'बीजाची गरज',
        'total_cost': 'एकूण खर्च',
        'estimated_cost': 'अंदाजित खर्च',
        'farm_area': 'शेताचे क्षेत्रफळ',
        'crop_type': 'पिकाचा प्रकार',
        'variety': 'जात',
        'season': 'हंगाम',
        'sowing_method': 'पेरणीची पद्धत',
        'soil_type': 'मातीचा प्रकार',
        'organic': 'सेंद्रिय',
        'sustainable': 'टिकाऊ',
        'drip_irrigation': 'ठिबक सिंचन',
        'broadcasting': 'पसरवणी पद्धत',
        'line_sowing': 'रांगेत पेरणी',
        'transplanting': 'रोपणी',
        'dibbling': 'खड्डा पद्धत',
        'acres': 'एकर',
        'hectares': 'हेक्टर',
        'bigha': 'बीघा',
        'katha': 'कठा',
        'kharif': 'खरीप',
        'rabi': 'रब्बी',
        'summer': 'उन्हाळा'
    },
    'te': {
        'loading': 'లోడ్ అవుతోంది...',
        'error': 'లోపం',
        'success': 'విజయం',
        'warning': 'హెచ్చరిక',
        'info': 'సమాచారం',
        'submit': 'సమర్పించండి',
        'cancel': 'రద్దు చేయండి',
        'save': 'సేవ్ చేయండి',
        'calculate': 'గణించండి',
        'results': 'ఫలితాలు',
        'recommendations': 'సలహాలు',
        'cost_analysis': 'ఖర్చు విశ్లేషణ',
        'seed_required': 'విత్తన అవసరం',
        'total_cost': 'మొత్తం ఖర్చు',
        'estimated_cost': 'అనుమానిత ఖర్చు',
        'farm_area': 'వ్యవసాయ భూమి వైశాల్యం',
        'crop_type': 'పంట రకం',
        'variety': 'రకం',
        'season': 'సీజన్',
        'sowing_method': 'విత్తన పద్ధతి',
        'soil_type': 'మిట్టి రకం',
        'organic': 'సేంద్రీయ',
        'sustainable': 'స్థిరమైన',
        'drip_irrigation': 'డ్రిప్ సించన',
        'broadcasting': 'వితరణ పద్ధతి',
        'line_sowing': 'వరుసలో విత్తన',
        'transplanting': 'రోపణ',
        'dibbling': 'గ్రూపు పద్ధతి',
        'acres': 'ఎకరాలు',
        'hectares': 'హెక్టర్లు',
        'bigha': 'బీఘా',
        'katha': 'కథా',
        'kharif': 'ఖరీఫ్',
        'rabi': 'రబీ',
        'summer': 'వేసవి'
    },
    'ta': {
        'loading': 'ஏறுகிறது...',
        'error': 'பிழை',
        'success': 'வெற்றி',
        'warning': 'எச்சரிக்கை',
        'info': 'தகவல்',
        'submit': 'சமர்ப்பிக்கவும்',
        'cancel': 'ரத்து செய்யவும்',
        'save': 'சேமிக்கவும்',
        'calculate': 'கணக்கீடு செய்யவும்',
        'results': 'முடிவுகள்',
        'recommendations': 'பரிந்துரைகள்',
        'cost_analysis': 'செலவு பகுப்பாய்வு',
        'seed_required': 'விதை தேவை',
        'total_cost': 'முழு செலவு',
        'estimated_cost': 'அனுமான செலவு',
        'farm_area': 'பண்ணை பரப்பளவு',
        'crop_type': 'பயிர் வகை',
        'variety': 'வகை',
        'season': 'பருவம்',
        'sowing_method': 'விதைப்பு முறை',
        'soil_type': 'மண் வகை',
        'organic': 'இயற்கை',
        'sustainable': 'நிலையான',
        'drip_irrigation': 'துளி நீர்ப்பாசனம்',
        'broadcasting': 'விதரல் முறை',
        'line_sowing': 'வரிசை விதைப்பு',
        'transplanting': 'நடவு',
        'dibbling': 'குழி முறை',
        'acres': 'ஏக்கர்',
        'hectares': 'ஹெக்டர்',
        'bigha': 'பீகா',
        'katha': 'கதா',
        'kharif': 'கரீப்',
        'rabi': 'ரபி',
        'summer': 'கோடை'
    }
};

// Current language
let currentLanguage = 'en';

// Language names mapping
const languageNames = {
    'en': 'English',
    'hi': 'हिंदी',
    'gu': 'ગુજરાતી',
    'mr': 'मराठी',
    'te': 'తెలుగు',
    'ta': 'தமிழ்'
};

// Initialize multilingual support
function initMultilingual() {
    // Get current language from HTML lang attribute or default to 'en'
    currentLanguage = document.documentElement.lang || 'en';
    
    // Update dynamic content
    updateDynamicContent();
    
    // Set up language change listeners
    setupLanguageListeners();
}

// Update dynamic content based on current language
function updateDynamicContent() {
    const lang = translations[currentLanguage] || translations['en'];
    
    // Update elements with data-translate attribute
    document.querySelectorAll('[data-translate]').forEach(element => {
        const key = element.getAttribute('data-translate');
        if (lang[key]) {
            element.textContent = lang[key];
        }
    });
    
    // Update placeholders
    document.querySelectorAll('[data-translate-placeholder]').forEach(element => {
        const key = element.getAttribute('data-translate-placeholder');
        if (lang[key]) {
            element.placeholder = lang[key];
        }
    });
    
    // Update titles
    document.querySelectorAll('[data-translate-title]').forEach(element => {
        const key = element.getAttribute('data-translate-title');
        if (lang[key]) {
            element.title = lang[key];
        }
    });
}

// Set up language change listeners
function setupLanguageListeners() {
    // Listen for language dropdown changes
    document.querySelectorAll('.language-selector').forEach(selector => {
        selector.addEventListener('change', function() {
            changeLanguage(this.value);
        });
    });
    
    // Listen for language links
    document.querySelectorAll('[data-lang]').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            changeLanguage(this.getAttribute('data-lang'));
        });
    });
}

// Change language
function changeLanguage(newLang) {
    if (translations[newLang]) {
        currentLanguage = newLang;
        
        // Update HTML lang attribute
        document.documentElement.lang = newLang;
        
        // Update dynamic content
        updateDynamicContent();
        
        // Save to localStorage
        localStorage.setItem('krishi_language', newLang);
        
        // Redirect to set language in session
        window.location.href = `/set-language/${newLang}`;
    }
}

// Get translated text
function getText(key, lang = null) {
    const targetLang = lang || currentLanguage;
    return translations[targetLang]?.[key] || translations['en']?.[key] || key;
}

// Show notification with translation
function showNotification(messageKey, type = 'info', params = {}) {
    const message = getText(messageKey);
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; max-width: 300px;';
    
    notification.innerHTML = `
        ${message}
        <button type=\"button\" class=\"btn-close\" data-bs-dismiss=\"alert\"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// Update form validation messages
function updateValidationMessages() {
    const lang = translations[currentLanguage] || translations['en'];
    
    // Update required field messages
    document.querySelectorAll('input[required], select[required], textarea[required]').forEach(field => {
        field.addEventListener('invalid', function() {
            if (this.validity.valueMissing) {
                this.setCustomValidity(lang['required_field'] || 'This field is required');
            }
        });
        
        field.addEventListener('input', function() {
            this.setCustomValidity('');
        });
    });
}

// Format numbers according to language
function formatNumber(number, lang = null) {
    const targetLang = lang || currentLanguage;
    
    try {
        return new Intl.NumberFormat(targetLang === 'hi' ? 'hi-IN' : 'en-IN').format(number);
    } catch (e) {
        return number.toString();
    }
}

// Format currency according to language
function formatCurrency(amount, lang = null) {
    const targetLang = lang || currentLanguage;
    
    try {
        return new Intl.NumberFormat(targetLang === 'hi' ? 'hi-IN' : 'en-IN', {
            style: 'currency',
            currency: 'INR'
        }).format(amount);
    } catch (e) {
        return `₹${amount}`;
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Load saved language preference
    const savedLang = localStorage.getItem('krishi_language');
    if (savedLang && translations[savedLang]) {
        currentLanguage = savedLang;
    }
    
    initMultilingual();
    updateValidationMessages();
});

// Export functions for global use
window.KrishiLang = {
    getText,
    changeLanguage,
    showNotification,
    formatNumber,
    formatCurrency,
    updateDynamicContent
};