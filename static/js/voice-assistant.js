/**
 * Voice Assistant - Hindi + English Support
 */

class VoiceAssistant {
    constructor() {
        this.recognition = null;
        this.synthesis = window.speechSynthesis;
        this.isListening = false;
        this.currentLanguage = 'hi-IN';
        this.init();
    }

    init() {
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            this.recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            this.setupRecognition();
        }
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
        };

        this.recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            console.log('Voice transcript:', transcript);
            this.processVoiceInput(transcript);
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

    async processVoiceInput(transcript) {
        console.log('Voice input:', transcript);
        
        // Show processing
        this.showProcessingAnimation();
        
        try {
            // Send to backend for AI processing
            const response = await fetch('/api/voice-query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    query: transcript,
                    language: this.currentLanguage
                })
            });

            const result = await response.json();
            
            if (result.success) {
                // Speak the response
                this.speakResponse(result.response);
                
                // Show text response
                this.displayResponse(transcript, result.response);
            } else {
                this.speakResponse('माफ करें, मुझे समझने में समस्या हुई है।');
            }
        } catch (error) {
            console.error('Voice processing error:', error);
            this.speakResponse('कुछ तकनीकी समस्या है। कृपया दोबारा कोशिश करें।');
        }
        
        this.hideProcessingAnimation();
    }

    speakResponse(text) {
        if (this.synthesis) {
            // Cancel any ongoing speech
            this.synthesis.cancel();
            
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = this.currentLanguage;
            utterance.rate = 0.9;
            utterance.pitch = 1;
            utterance.volume = 0.8;
            
            // Wait for voices to load and find appropriate voice
            const setVoice = () => {
                const voices = this.synthesis.getVoices();
                let selectedVoice = null;
                
                if (this.currentLanguage === 'hi-IN') {
                    // Try to find Hindi voice
                    selectedVoice = voices.find(voice => 
                        voice.lang.includes('hi') || 
                        voice.name.toLowerCase().includes('hindi')
                    );
                }
                
                if (!selectedVoice) {
                    // Fallback to any Indian English voice
                    selectedVoice = voices.find(voice => 
                        voice.lang.includes('en-IN') ||
                        voice.name.toLowerCase().includes('indian')
                    );
                }
                
                if (selectedVoice) {
                    utterance.voice = selectedVoice;
                }
                
                this.synthesis.speak(utterance);
            };
            
            if (this.synthesis.getVoices().length === 0) {
                this.synthesis.addEventListener('voiceschanged', setVoice, { once: true });
            } else {
                setVoice();
            }
        }
    }

    updateVoiceButton(listening) {
        const button = document.getElementById('voice-button');
        const icon = document.getElementById('voice-icon');
        const text = document.getElementById('voice-text');
        
        if (button) {
            if (listening) {
                button.classList.add('listening');
                icon.innerHTML = '🎤';
                text.textContent = 'सुन रहा हूँ...';
            } else {
                button.classList.remove('listening');
                icon.innerHTML = '🗣️';
                text.textContent = 'बोलिए';
            }
        }
    }

    showListeningAnimation() {
        const animation = document.getElementById('listening-animation');
        if (animation) {
            animation.style.display = 'block';
        }
    }

    hideListeningAnimation() {
        const animation = document.getElementById('listening-animation');
        if (animation) {
            animation.style.display = 'none';
        }
    }

    showProcessingAnimation() {
        const processing = document.getElementById('processing-animation');
        if (processing) {
            processing.style.display = 'block';
        }
    }

    hideProcessingAnimation() {
        const processing = document.getElementById('processing-animation');
        if (processing) {
            processing.style.display = 'none';
        }
    }

    displayResponse(query, response) {
        const container = document.getElementById('voice-response');
        if (container) {
            container.innerHTML = `
                <div class="voice-conversation">
                    <div class="user-query">
                        <strong>आपने पूछा:</strong> ${query}
                    </div>
                    <div class="ai-response">
                        <strong>कृषि सहायक:</strong> ${response}
                    </div>
                </div>
            `;
            container.style.display = 'block';
        }
    }

    toggleLanguage() {
        this.currentLanguage = this.currentLanguage === 'hi-IN' ? 'en-IN' : 'hi-IN';
        if (this.recognition) {
            this.recognition.lang = this.currentLanguage;
        }
        
        const langButton = document.getElementById('language-toggle');
        if (langButton) {
            langButton.textContent = this.currentLanguage === 'hi-IN' ? 'हिं' : 'EN';
        }
    }
}

// Initialize voice assistant
const voiceAssistant = new VoiceAssistant();

// Global functions for buttons
function startVoiceInput() {
    voiceAssistant.startListening();
}

function toggleLanguage() {
    voiceAssistant.toggleLanguage();
}