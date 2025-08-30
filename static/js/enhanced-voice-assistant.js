// Enhanced Voice Assistant with Advanced Context Awareness
class EnhancedVoiceAssistant {
    constructor() {
        this.recognition = null;
        this.synthesis = window.speechSynthesis;
        this.isListening = false;
        this.currentLanguage = 'hi-IN';
        this.conversationHistory = [];
        this.contextMemory = {};
        this.init();
    }

    init() {
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            this.recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            this.setupRecognition();
        }
        
        // Load conversation history from localStorage
        this.loadConversationHistory();
    }

    setupRecognition() {
        this.recognition.continuous = false;
        this.recognition.interimResults = false;
        this.recognition.lang = this.currentLanguage;
        this.recognition.maxAlternatives = 3;

        this.recognition.onstart = () => {
            this.isListening = true;
            this.updateVoiceButton(true);
            this.showListeningAnimation();
            this.showContextualHints();
        };

        this.recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            console.log('Voice transcript:', transcript);
            this.processEnhancedVoiceInput(transcript);
        };

        this.recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            let errorMessage = 'माफ करें, आवाज़ समझने में समस्या हुई।';
            
            switch(event.error) {
                case 'no-speech':
                    errorMessage = 'कोई आवाज़ नहीं सुनाई दी। कृपया दोबारा कोशिश करें।';
                    break;
                case 'audio-capture':
                    errorMessage = 'माइक्रोफोन की समस्या। कृपया अनुमति दें।';
                    break;
                case 'not-allowed':
                    errorMessage = 'माइक्रोफोन की अनुमति दें।';
                    break;
            }
            
            this.displayResponse('', errorMessage);
            this.stopListening();
        };

        this.recognition.onend = () => {
            this.stopListening();
        };
    }

    async processEnhancedVoiceInput(transcript) {
        console.log('Enhanced voice input:', transcript);
        
        // Show processing
        this.showProcessingAnimation();
        
        try {
            // Enhance query with conversation context
            const enhancedQuery = this.enhanceQueryWithHistory(transcript);
            
            // Get comprehensive context
            const context = await this.gatherComprehensiveContext();
            
            // Send to backend for AI processing with enhanced context
            const response = await fetch('/api/voice-query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    query: enhancedQuery,
                    language: this.currentLanguage,
                    scan_result: context.scanResult,
                    conversation_history: this.conversationHistory.slice(-3) // Last 3 exchanges
                })
            });

            const result = await response.json();
            
            if (result.success) {
                // Store conversation
                this.addToConversationHistory(transcript, result.response);
                
                // Speak the response with enhanced voice
                this.speakEnhancedResponse(result.response);
                
                // Show enhanced text response
                this.displayEnhancedResponse(transcript, result.response);
                
                // Update context memory
                this.updateContextMemory(transcript, result.response);
                
            } else {
                const fallbackResponse = this.getContextualFallback(transcript);
                this.speakEnhancedResponse(fallbackResponse);
                this.displayEnhancedResponse(transcript, fallbackResponse);
            }
        } catch (error) {
            console.error('Enhanced voice processing error:', error);
            const errorResponse = this.getIntelligentErrorResponse(transcript);
            this.speakEnhancedResponse(errorResponse);
            this.displayEnhancedResponse(transcript, errorResponse);
        }
        
        this.hideProcessingAnimation();
    }

    enhanceQueryWithHistory(query) {
        // Add context from recent conversation
        if (this.conversationHistory.length > 0) {
            const lastExchange = this.conversationHistory[this.conversationHistory.length - 1];
            
            // If query is a follow-up (short or uses pronouns)
            if (query.length < 20 || this.isFollowUpQuery(query)) {
                return `पिछला सवाल: ${lastExchange.query}\nपिछला जवाब: ${lastExchange.response}\nनया सवाल: ${query}`;
            }
        }
        
        return query;
    }

    isFollowUpQuery(query) {
        const followUpIndicators = [
            'इसका', 'उसका', 'यह', 'वह', 'कैसे', 'क्यों', 'कब', 'कहाँ',
            'this', 'that', 'it', 'how', 'why', 'when', 'where',
            'और', 'फिर', 'अब', 'then', 'now', 'also'
        ];
        
        return followUpIndicators.some(indicator => 
            query.toLowerCase().includes(indicator.toLowerCase())
        );
    }

    async gatherComprehensiveContext() {
        const context = {
            scanResult: null,
            weather: null,
            market: null,
            userProfile: null
        };

        // Try to get scan result from page
        try {
            const diagnosisElement = document.querySelector('.diagnosis-result');
            const treatmentElement = document.querySelector('.treatment-advice');
            
            if (diagnosisElement && treatmentElement) {
                context.scanResult = {
                    diagnosis: diagnosisElement.textContent.trim(),
                    treatment: treatmentElement.textContent.trim()
                };
            }
        } catch (e) {
            console.log('No scan result context available');
        }

        return context;
    }

    speakEnhancedResponse(text) {
        if (this.synthesis) {
            // Cancel any ongoing speech
            this.synthesis.cancel();
            
            // Clean text for better speech
            const cleanText = this.cleanTextForSpeech(text);
            
            const utterance = new SpeechSynthesisUtterance(cleanText);
            utterance.lang = this.currentLanguage;
            utterance.rate = 0.85; // Slightly slower for better comprehension
            utterance.pitch = 1.1;  // Slightly higher pitch for friendliness
            utterance.volume = 0.9;
            
            // Enhanced voice selection
            const setEnhancedVoice = () => {
                const voices = this.synthesis.getVoices();
                let selectedVoice = null;
                
                if (this.currentLanguage === 'hi-IN') {
                    // Prefer Hindi voices
                    selectedVoice = voices.find(voice => 
                        voice.lang.includes('hi') || 
                        voice.name.toLowerCase().includes('hindi') ||
                        voice.name.toLowerCase().includes('indian')
                    );
                }
                
                if (!selectedVoice) {
                    // Fallback to English Indian voices
                    selectedVoice = voices.find(voice => 
                        voice.lang.includes('en-IN') ||
                        voice.name.toLowerCase().includes('indian')
                    );
                }
                
                if (selectedVoice) {
                    utterance.voice = selectedVoice;
                }
                
                // Add speech events
                utterance.onstart = () => {
                    this.showSpeakingAnimation();
                };
                
                utterance.onend = () => {
                    this.hideSpeakingAnimation();
                };
                
                this.synthesis.speak(utterance);
            };
            
            if (this.synthesis.getVoices().length === 0) {
                this.synthesis.addEventListener('voiceschanged', setEnhancedVoice, { once: true });
            } else {
                setEnhancedVoice();
            }
        }
    }

    cleanTextForSpeech(text) {
        // Remove markdown formatting
        let cleanText = text.replace(/\*\*(.*?)\*\*/g, '$1');
        cleanText = cleanText.replace(/\*(.*?)\*/g, '$1');
        
        // Remove emojis for better speech
        cleanText = cleanText.replace(/[\u{1F600}-\u{1F64F}]|[\u{1F300}-\u{1F5FF}]|[\u{1F680}-\u{1F6FF}]|[\u{1F1E0}-\u{1F1FF}]|[\u{2600}-\u{26FF}]|[\u{2700}-\u{27BF}]/gu, '');
        
        // Replace common symbols with spoken equivalents
        cleanText = cleanText.replace(/₹/g, 'रुपए');
        cleanText = cleanText.replace(/%/g, 'प्रतिशत');
        cleanText = cleanText.replace(/°C/g, 'डिग्री सेल्सियस');
        
        return cleanText.trim();
    }

    displayEnhancedResponse(query, response) {
        const container = document.getElementById('voice-response') || 
                         document.getElementById('voice-response-results');
        
        if (container) {
            // Enhanced response display with better formatting
            const enhancedResponse = this.formatResponseForDisplay(response);
            
            container.innerHTML = `
                <div class="voice-conversation enhanced">
                    <div class="user-query">
                        <div class="query-header">
                            <span class="query-icon">🗣️</span>
                            <strong>आपने पूछा:</strong>
                        </div>
                        <div class="query-text">${query}</div>
                    </div>
                    <div class="ai-response">
                        <div class="response-header">
                            <span class="ai-icon">🤖</span>
                            <strong>AI कृषि विशेषज्ञ:</strong>
                        </div>
                        <div class="response-text">${enhancedResponse}</div>
                        <div class="response-actions">
                            <button class="btn btn-sm btn-outline-light" onclick="enhancedVoiceAssistant.speakEnhancedResponse('${response.replace(/'/g, "\\'")}')">
                                🔊 दोबारा सुनें
                            </button>
                            <button class="btn btn-sm btn-outline-light" onclick="enhancedVoiceAssistant.askFollowUp()">
                                ❓ और पूछें
                            </button>
                            <button class="btn btn-sm btn-outline-light" onclick="enhancedVoiceAssistant.saveResponse('${response.replace(/'/g, "\\'")}')">
                                💾 सेव करें
                            </button>
                        </div>
                    </div>
                </div>
            `;
            container.style.display = 'block';
            
            // Keep AI assistant expanded - prevent auto-collapse
            const aiAssistant = document.querySelector('.ai-assistant-prominent');
            if (aiAssistant) {
                aiAssistant.classList.add('conversation-active');
                aiAssistant.style.minHeight = 'auto';
            }
            
            // Scroll to response
            container.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
    }

    formatResponseForDisplay(response) {
        // Add visual formatting to response
        let formatted = response;
        
        // Highlight important farming terms
        const farmingTerms = {
            'नीम': '🌿 नीम',
            'पानी': '💧 पानी',
            'खाद': '🌱 खाद',
            'बीज': '🌰 बीज',
            'फसल': '🌾 फसल',
            'मिट्टी': '🏔️ मिट्टी',
            'बारिश': '🌧️ बारिश',
            'धूप': '☀️ धूप'
        };
        
        Object.entries(farmingTerms).forEach(([term, replacement]) => {
            const regex = new RegExp(`\\b${term}\\b`, 'g');
            formatted = formatted.replace(regex, replacement);
        });
        
        // Add line breaks for better readability
        formatted = formatted.replace(/\. /g, '.<br>');
        
        return formatted;
    }

    addToConversationHistory(query, response) {
        const exchange = {
            query: query,
            response: response,
            timestamp: new Date().toISOString(),
            language: this.currentLanguage
        };
        
        this.conversationHistory.push(exchange);
        
        // Keep only last 10 exchanges
        if (this.conversationHistory.length > 10) {
            this.conversationHistory = this.conversationHistory.slice(-10);
        }
        
        // Save to localStorage
        this.saveConversationHistory();
    }

    saveConversationHistory() {
        try {
            localStorage.setItem('krishi_voice_history', JSON.stringify(this.conversationHistory));
        } catch (e) {
            console.log('Could not save conversation history');
        }
    }

    loadConversationHistory() {
        try {
            const saved = localStorage.getItem('krishi_voice_history');
            if (saved) {
                this.conversationHistory = JSON.parse(saved);
            }
        } catch (e) {
            console.log('Could not load conversation history');
            this.conversationHistory = [];
        }
    }

    updateContextMemory(query, response) {
        // Extract and store important context
        const queryLower = query.toLowerCase();
        
        if (queryLower.includes('फसल') || queryLower.includes('crop')) {
            this.contextMemory.lastCropQuery = { query, response, timestamp: Date.now() };
        }
        
        if (queryLower.includes('बीमारी') || queryLower.includes('disease')) {
            this.contextMemory.lastDiseaseQuery = { query, response, timestamp: Date.now() };
        }
        
        if (queryLower.includes('मौसम') || queryLower.includes('weather')) {
            this.contextMemory.lastWeatherQuery = { query, response, timestamp: Date.now() };
        }
    }

    getContextualFallback(query) {
        const queryLower = query.toLowerCase();
        
        // Use context memory for better fallbacks
        if (queryLower.includes('यह') || queryLower.includes('इसका')) {
            if (this.contextMemory.lastDiseaseQuery) {
                return "आपका सवाल पिछली बीमारी के बारे में है। कृपया अधिक स्पष्ट करें कि आप क्या जानना चाहते हैं।";
            }
        }
        
        // Intent-based fallbacks
        if (queryLower.includes('बीमारी') || queryLower.includes('रोग')) {
            return "पौधे की बीमारी के लिए नीम का तेल (10 मिली प्रति लीटर) का छिड़काव करें। फोटो भेजें तो बेहतर सलाह दे सकूंगा।";
        }
        
        if (queryLower.includes('मौसम') || queryLower.includes('बारिश')) {
            return "मौसम के अनुसार खेती करें। बारिश से पहले छिड़काव न करें। मौसम सेक्शन में विस्तृत जानकारी देखें।";
        }
        
        if (queryLower.includes('दाम') || queryLower.includes('कीमत')) {
            return "बाजार की कीमतें रोज बदलती हैं। मार्केट सेक्शन में आज के भाव देखें या स्थानीय मंडी से संपर्क करें।";
        }
        
        return "कृपया अपना सवाल और स्पष्ट करें। मैं आपकी खेती से जुड़ी हर समस्या में मदद कर सकता हूं।";
    }

    getIntelligentErrorResponse(query) {
        const responses = [
            "नेटवर्क की समस्या है। कृपया दोबारा कोशिश करें।",
            "कुछ तकनीकी समस्या है। थोड़ी देर बाद पूछें।",
            "सर्वर व्यस्त है। कृपया धैर्य रखें और दोबारा कोशिश करें।"
        ];
        
        return responses[Math.floor(Math.random() * responses.length)];
    }

    showContextualHints() {
        // Show relevant hints based on current page
        const hints = this.getContextualHints();
        if (hints.length > 0) {
            this.displayHints(hints);
        }
    }

    getContextualHints() {
        const currentPath = window.location.pathname;
        
        if (currentPath.includes('results')) {
            return [
                "इस पौधे की क्या समस्या है?",
                "इलाज कितनी बार करना है?",
                "नीम का तेल कैसे इस्तेमाल करें?"
            ];
        } else if (currentPath.includes('market')) {
            return [
                "आज के भाव क्या हैं?",
                "कब बेचना चाहिए?",
                "कीमत कैसी रहेगी?"
            ];
        } else if (currentPath.includes('weather')) {
            return [
                "आज मौसम कैसा है?",
                "बारिश होगी क्या?",
                "खेत में काम कर सकते हैं?"
            ];
        } else {
            return [
                "मेरी फसल की समस्या बताएं",
                "आज का मौसम कैसा है?",
                "बाजार के भाव क्या हैं?"
            ];
        }
    }

    displayHints(hints) {
        // Create or update hints display
        let hintsContainer = document.getElementById('voice-hints');
        if (!hintsContainer) {
            hintsContainer = document.createElement('div');
            hintsContainer.id = 'voice-hints';
            hintsContainer.className = 'voice-hints mt-2';
            
            const voiceContainer = document.querySelector('.ai-assistant-prominent') || 
                                 document.querySelector('.ai-assistant-results');
            if (voiceContainer) {
                voiceContainer.appendChild(hintsContainer);
            }
        }
        
        hintsContainer.innerHTML = `
            <div class="hints-header">💡 आप यह पूछ सकते हैं:</div>
            <div class="hints-list">
                ${hints.map(hint => `
                    <button class="hint-btn" onclick="enhancedVoiceAssistant.askHintQuestion('${hint}')">
                        "${hint}"
                    </button>
                `).join('')}
            </div>
        `;
        
        // Auto-hide after 10 seconds
        setTimeout(() => {
            if (hintsContainer) {
                hintsContainer.style.display = 'none';
            }
        }, 10000);
    }

    askHintQuestion(question) {
        // Simulate voice input with hint question
        this.processEnhancedVoiceInput(question);
        
        // Hide hints
        const hintsContainer = document.getElementById('voice-hints');
        if (hintsContainer) {
            hintsContainer.style.display = 'none';
        }
    }

    askFollowUp() {
        const followUpQuestions = [
            'इसके बारे में और बताएं',
            'कितना समय लगेगा?',
            'कोई और तरीका है?',
            'लागत कितनी आएगी?',
            'कब तक असर दिखेगा?'
        ];
        
        const randomQuestion = followUpQuestions[Math.floor(Math.random() * followUpQuestions.length)];
        this.processEnhancedVoiceInput(randomQuestion);
    }

    saveResponse(response) {
        try {
            const savedResponses = JSON.parse(localStorage.getItem('krishi_saved_responses') || '[]');
            savedResponses.push({
                response: response,
                timestamp: new Date().toISOString(),
                page: window.location.pathname
            });
            
            // Keep only last 20 saved responses
            if (savedResponses.length > 20) {
                savedResponses.splice(0, savedResponses.length - 20);
            }
            
            localStorage.setItem('krishi_saved_responses', JSON.stringify(savedResponses));
            
            if (typeof showNotification === 'function') {
                showNotification('💾 जवाब सेव हो गया!', 'success');
            } else {
                alert('💾 जवाब सेव हो गया!');
            }
        } catch (e) {
            console.error('Could not save response:', e);
        }
    }

    // Animation methods
    showSpeakingAnimation() {
        const voiceButton = document.getElementById('voice-button') || 
                           document.getElementById('voice-button-results');
        if (voiceButton) {
            voiceButton.classList.add('speaking');
        }
    }

    hideSpeakingAnimation() {
        const voiceButton = document.getElementById('voice-button') || 
                           document.getElementById('voice-button-results');
        if (voiceButton) {
            voiceButton.classList.remove('speaking');
        }
    }

    startListening() {
        if (this.recognition && !this.isListening) {
            this.recognition.start();
        }
    }

    stopListening() {
        this.isListening = false;
        this.updateVoiceButton(false);
        this.hideListeningAnimation();
    }

    updateVoiceButton(listening) {
        const button = document.getElementById('voice-button') || 
                      document.getElementById('voice-button-results');
        const icon = document.getElementById('voice-icon') || 
                    document.getElementById('voice-icon-results');
        const text = document.getElementById('voice-text') || 
                    document.getElementById('voice-text-results');
        
        if (button) {
            if (listening) {
                button.classList.add('listening');
                if (icon) icon.innerHTML = '🎤';
                if (text) text.textContent = 'सुन रहा हूँ...';
            } else {
                button.classList.remove('listening');
                if (icon) icon.innerHTML = '🗣️';
                if (text) text.textContent = 'बोलिए';
            }
        }
    }

    showListeningAnimation() {
        const animation = document.getElementById('listening-animation') || 
                         document.getElementById('listening-animation-results');
        if (animation) {
            animation.style.display = 'block';
        }
    }

    hideListeningAnimation() {
        const animation = document.getElementById('listening-animation') || 
                         document.getElementById('listening-animation-results');
        if (animation) {
            animation.style.display = 'none';
        }
    }

    showProcessingAnimation() {
        const processing = document.getElementById('processing-animation') || 
                          document.getElementById('processing-animation-results');
        if (processing) {
            processing.style.display = 'block';
        }
    }

    hideProcessingAnimation() {
        const processing = document.getElementById('processing-animation') || 
                          document.getElementById('processing-animation-results');
        if (processing) {
            processing.style.display = 'none';
        }
    }

    toggleLanguage() {
        this.currentLanguage = this.currentLanguage === 'hi-IN' ? 'en-IN' : 'hi-IN';
        if (this.recognition) {
            this.recognition.lang = this.currentLanguage;
        }
        
        const langButton = document.getElementById('language-toggle') || 
                          document.getElementById('language-toggle-results');
        if (langButton) {
            langButton.textContent = this.currentLanguage === 'hi-IN' ? 'हिं' : 'EN';
        }
    }
}

// Initialize enhanced voice assistant
const enhancedVoiceAssistant = new EnhancedVoiceAssistant();

// Global functions for compatibility
function startVoiceInput() {
    enhancedVoiceAssistant.startListening();
}

function startVoiceInputResults() {
    enhancedVoiceAssistant.startListening();
}

function toggleLanguage() {
    enhancedVoiceAssistant.toggleLanguage();
}

function toggleLanguageResults() {
    enhancedVoiceAssistant.toggleLanguage();
}

// Enhanced CSS for better UI
const enhancedStyles = `
<style>
.voice-conversation.enhanced {
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    border-radius: 15px;
    padding: 20px;
    margin: 15px 0;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

.query-header, .response-header {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
    font-weight: 600;
}

.query-icon, .ai-icon {
    font-size: 1.2rem;
    margin-right: 8px;
}

.query-text, .response-text {
    background: white;
    padding: 15px;
    border-radius: 10px;
    border-left: 4px solid #28a745;
    margin-bottom: 15px;
    line-height: 1.6;
}

.response-actions {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}

.response-actions .btn {
    font-size: 0.85rem;
    padding: 5px 12px;
    border-radius: 20px;
}

.voice-hints {
    background: rgba(255,255,255,0.1);
    border-radius: 10px;
    padding: 15px;
    margin-top: 15px;
    backdrop-filter: blur(10px);
}

.hints-header {
    font-size: 0.9rem;
    margin-bottom: 10px;
    color: rgba(255,255,255,0.9);
}

.hints-list {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.hint-btn {
    background: rgba(255,255,255,0.2);
    border: 1px solid rgba(255,255,255,0.3);
    color: white;
    padding: 5px 12px;
    border-radius: 15px;
    font-size: 0.8rem;
    cursor: pointer;
    transition: all 0.3s ease;
}

.hint-btn:hover {
    background: rgba(255,255,255,0.3);
    transform: translateY(-1px);
}

.voice-btn-prominent.speaking {
    background: linear-gradient(45deg, #17a2b8, #20c997);
    animation: speaking-pulse 1s infinite;
}

@keyframes speaking-pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.02); }
    100% { transform: scale(1); }
}

.ai-assistant-prominent.conversation-active {
    min-height: auto !important;
    height: auto !important;
    display: block !important;
    visibility: visible !important;
}

.ai-assistant-prominent.conversation-active #voice-response {
    display: block !important;
    opacity: 1 !important;
}
</style>
`;

// Inject enhanced styles
document.head.insertAdjacentHTML('beforeend', enhancedStyles);