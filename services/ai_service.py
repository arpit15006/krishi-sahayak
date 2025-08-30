import os
import requests
import base64
import logging
from services.weather_service import check_rain_forecast
from services.huggingface_vision import analyze_plant_with_huggingface

logger = logging.getLogger(__name__)

def format_farmer_response(ai_response):
    """Format AI response for better farmer readability"""
    try:
        # This function is now simplified since diagnosis extraction is handled in analyze_plant_image
        formatted_treatment = format_treatment_text(ai_response)
        return {
            'diagnosis': "🔍 पौधे का विश्लेषण पूरा (Plant Analysis Complete)",
            'treatment': formatted_treatment
        }
        
    except Exception as e:
        logger.error(f"Error formatting farmer response: {str(e)}")
        return {
            'diagnosis': "🔍 पौधे का विश्लेषण पूरा (Plant Analysis Complete)",
            'treatment': ai_response
        }

def format_treatment_text(text):
    """Format treatment text with better structure and emojis"""
    try:
        # Split into sections and add proper formatting
        sections = text.split('\n\n')
        formatted_sections = []
        
        for section in sections:
            if not section.strip():
                continue
                
            # Add emojis based on content
            if any(keyword in section.lower() for keyword in ['organic', 'जैविक', 'neem', 'नीम']):
                if not section.startswith('🌿'):
                    section = f"🌿 **जैविक उपचार (Organic Treatment):**\n{section}"
            elif any(keyword in section.lower() for keyword in ['chemical', 'रासायनिक', 'pesticide', 'fungicide']):
                if not section.startswith('💊'):
                    section = f"💊 **रासायनिक उपचार (Chemical Treatment):**\n{section}"
            elif any(keyword in section.lower() for keyword in ['prevention', 'रोकथाम', 'avoid', 'बचाव']):
                if not section.startswith('🛡️'):
                    section = f"🛡️ **रोकथाम (Prevention):**\n{section}"
            elif any(keyword in section.lower() for keyword in ['timing', 'time', 'समय', 'when']):
                if not section.startswith('⏰'):
                    section = f"⏰ **सही समय (Best Timing):**\n{section}"
            elif any(keyword in section.lower() for keyword in ['cost', 'price', 'लागत', 'खर्च']):
                if not section.startswith('💰'):
                    section = f"💰 **लागत (Cost Information):**\n{section}"
            elif any(keyword in section.lower() for keyword in ['disease', 'pest', 'रोग', 'कीट']):
                if not section.startswith('🔍'):
                    section = f"🔍 **समस्या की पहचान (Problem Identification):**\n{section}"
            
            formatted_sections.append(section.strip())
        
        # Join sections with proper spacing
        formatted = '\n\n'.join(formatted_sections)
        
        # Add final note if no cost information
        if not any(keyword in formatted.lower() for keyword in ['cost', 'लागत', 'खर्च']):
            formatted += "\n\n💰 **लागत की जानकारी:** स्थानीय कृषि विशेषज्ञ से संपर्क करें।"
        
        return formatted.strip()
        
    except Exception as e:
        logger.error(f"Error formatting treatment text: {str(e)}")
        return text

def analyze_plant_image(image_path, weather_data=None):
    """Analyze plant image using Gemini Vision API as primary method"""
    
    # Use Gemini Vision API as primary method
    gemini_key = os.getenv('GEMINI_API_KEY', 'AIzaSyCVchsFQ9RyH4wdM2qrVZqRBJyQ5g9qOKg')
    
    try:
        # Read and encode image
        with open(image_path, 'rb') as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
        
        # Detect image format
        from PIL import Image
        img = Image.open(image_path)
        img_format = img.format.lower()
        mime_type = f"image/{img_format}" if img_format in ['jpeg', 'jpg', 'png', 'webp'] else "image/jpeg"
        
        # Clean Hindi-only structured prompt
        prompt = """इस पौधे की तस्वीर का विश्लेषण करें और बिल्कुल इसी फॉर्मेट में जवाब दें:

🔍 **समस्या की पहचान:**
कीट के अंडे या सफेद मक्खी की समस्या दिख रही है

🌿 **जैविक उपचार:**
• नीम का तेल: 10 मिली प्रति लीटर पानी में मिलाकर छिड़काव करें
• गोबर का घोल: 1 किलो गोबर को 10 लीटर पानी में घोलकर छानें
• हरी पत्तियों का काढ़ा: नीम, तुलसी की पत्तियां उबालकर छिड़काव करें

💊 **रासायनिक उपचार:**
• इमिडाक्लोप्रिड: लेबल के अनुसार मात्रा का प्रयोग करें
• क्लोरोपायरिफॉस: भारत में उपलब्ध है
• स्थानीय कृषि दुकान से सलाह लें

⏰ **सही समय:**
• सुबह जल्दी या शाम के समय छिड़काव करें
• धूप तेज न हो तब करें
• बारिश से पहले न करें

🛡️ **रोकथाम:**
• फसल चक्र अपनाएं
• खरपतवार नियंत्रण करें
• खेत की सफाई रखें
• नियमित निगरानी करें

💰 **लागत:**
• अनुमानित खर्च: ₹500-1000 प्रति एकड़
• जैविक उपचार सस्ता है

सिर्फ हिंदी में सरल भाषा में जवाब दें।"""
        
        # Use Gemini 1.5 Flash Vision API
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
        headers = {"Content-Type": "application/json"}
        
        data = {
            "contents": [{
                "parts": [
                    {"text": prompt},
                    {
                        "inline_data": {
                            "mime_type": mime_type,
                            "data": image_data
                        }
                    }
                ]
            }]
        }
        
        response = requests.post(url, json=data, headers=headers, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            
            if 'candidates' in result and len(result['candidates']) > 0:
                candidate = result['candidates'][0]
                
                if 'content' in candidate and 'parts' in candidate['content']:
                    ai_response = candidate['content']['parts'][0]['text']
                    
                    # Extract diagnosis - look for content after problem identification
                    lines = ai_response.split('\n')
                    diagnosis = ""
                    treatment = ai_response
                    
                    # Find the line after problem identification header
                    for i, line in enumerate(lines):
                        if '🔍' in line and ('समस्या' in line or 'पहचान' in line):
                            # Get the next non-empty line as diagnosis
                            for j in range(i+1, len(lines)):
                                next_line = lines[j].strip()
                                if next_line and not next_line.startswith('🔍') and not next_line.startswith('**'):
                                    diagnosis = next_line
                                    break
                            break
                    
                    # Fallback: look for any meaningful content about pest/disease
                    if not diagnosis:
                        for line in lines:
                            line_clean = line.strip()
                            if ('कीड़' in line_clean or 'कीट' in line_clean or 'रोग' in line_clean or 'बीमारी' in line_clean) and len(line_clean) > 20:
                                diagnosis = line_clean
                                break
                    
                    # Final fallback
                    if not diagnosis:
                        diagnosis = "🔍 पौधे का विश्लेषण पूरा (Plant Analysis Complete)"
                    
                    return {
                        'diagnosis': diagnosis,
                        'treatment': treatment,
                        'confidence': 'उच्च (High)',
                        'model': 'Gemini 1.5 Flash Vision'
                    }
                else:
                    return get_fallback_analysis()
            else:
                return get_fallback_analysis()
        else:
            logger.error(f"Gemini API error: {response.status_code} - {response.text}")
            
            if response.status_code == 429:
                return {
                    'diagnosis': "API quota exceeded",
                    'treatment': "Gemini API quota limit reached. Please wait or try again later.",
                    'error': 'Gemini API quota exceeded'
                }
            return get_fallback_analysis()
            
    except Exception as e:
        logger.error(f"Gemini Vision API failed: {str(e)}")
        return get_fallback_analysis()

    # Fallback to Hugging Face if Gemini fails
    try:
        result = analyze_plant_with_huggingface(image_path)
        if not result.get('error'):
            if weather_data:
                has_rain, rain_message = check_rain_forecast(weather_data)
                if has_rain:
                    result['weather_warning'] = f"⚠️ Weather Alert: {rain_message}. Avoid spraying treatments before rain."
            return result
    except Exception as e:
        logger.warning(f"Hugging Face fallback failed: {str(e)}")

    # Final fallback
    return get_ai_error()

def parse_ai_response(ai_response):
    """Parse AI response into structured format"""
    try:
        # Split response into sections
        sections = ai_response.split('\n\n')
        
        diagnosis = ""
        treatment = ""
        
        # Extract diagnosis (usually in first section)
        for section in sections:
            if any(keyword in section.lower() for keyword in ['disease', 'pest', 'identification', 'diagnosis']):
                diagnosis = section.strip()
                break
        
        if not diagnosis and sections:
            diagnosis = sections[0].strip()
        
        # Extract treatment advice (combine organic and chemical sections)
        treatment_sections = []
        for section in sections:
            if any(keyword in section.lower() for keyword in ['treatment', 'organic', 'chemical', 'remedy', 'control']):
                treatment_sections.append(section.strip())
        
        treatment = '\n\n'.join(treatment_sections) if treatment_sections else ai_response
        
        return {
            'diagnosis': diagnosis or "Analysis completed - see treatment recommendations",
            'treatment': treatment or ai_response,
            'confidence': 'High'  # Default confidence
        }
        
    except Exception as e:
        logger.error(f"Error parsing AI response: {str(e)}")
        return {
            'diagnosis': "Plant health analysis completed",
            'treatment': ai_response,
            'confidence': 'Medium'
        }

def process_contextual_query(query, language, user_crops, pin_code, scan_result=None, weather_data=None, market_data=None):
    """Enhanced contextual query processing with comprehensive context awareness"""
    
    try:
        from services.enhanced_voice_assistant import enhanced_voice_assistant
        
        # Use enhanced voice assistant for better contextual responses
        response = enhanced_voice_assistant.process_contextual_query(
            query=query,
            language=language,
            user_crops=user_crops,
            pin_code=pin_code,
            scan_result=scan_result,
            weather_data=weather_data,
            market_data=market_data
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Enhanced contextual query error: {str(e)}")
        
        # Fallback to original implementation
        try:
            gemini_key = os.getenv('GEMINI_API_KEY', 'AIzaSyCVchsFQ9RyH4wdM2qrVZqRBJyQ5g9qOKg')
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
            headers = {"Content-Type": "application/json"}
            
            # Build context from scan result
            context = ""
            if scan_result and scan_result.get('diagnosis'):
                context = f"पौधे की समस्या: {scan_result.get('diagnosis', '')}\nसुझाया गया इलाज: {scan_result.get('treatment', '')}\n"
                if scan_result.get('weather_warning'):
                    context += f"मौसम चेतावनी: {scan_result.get('weather_warning')}\n"
            
            # Create contextual prompt
            prompt = f"""{context}
किसान का सवाल: {query}

ऊपर दी गई पौधे की समस्या और इलाज के आधार पर किसान के सवाल का जवाब दें। सिर्फ हिंदी में 2-3 वाक्यों में व्यावहारिक सलाह दें।"""
            
            data = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.7, "maxOutputTokens": 150}
            }
            
            response = requests.post(url, json=data, headers=headers, timeout=15)
            
            if response.status_code == 200:
                result = response.json()
                if 'candidates' in result and len(result['candidates']) > 0:
                    return result['candidates'][0]['content']['parts'][0]['text'].strip()
            
            raise Exception("No response from AI")
            
        except Exception as fallback_error:
            logger.error(f"Fallback contextual query error: {str(fallback_error)}")
            return "इस समस्या के बारे में अधिक जानकारी के लिए स्थानीय कृषि विशेषज्ञ से संपर्क करें।"

def process_voice_query(query, language, user_crops, pin_code, weather_data=None, market_data=None):
    """Enhanced voice query processing with comprehensive context"""
    
    try:
        from services.enhanced_voice_assistant import enhanced_voice_assistant
        
        # Use enhanced voice assistant for better responses
        response = enhanced_voice_assistant.process_contextual_query(
            query=query,
            language=language,
            user_crops=user_crops,
            pin_code=pin_code,
            scan_result=None,
            weather_data=weather_data,
            market_data=market_data
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Enhanced voice query error: {str(e)}")
        
        # Fallback to original implementation
        try:
            # Use Gemini API for chatbot
            gemini_key = os.getenv('GEMINI_API_KEY', 'AIzaSyCVchsFQ9RyH4wdM2qrVZqRBJyQ5g9qOKg')
            
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
            headers = {"Content-Type": "application/json"}
            
            # Enhanced context-aware prompts for scanner results page
            query_lower = query.lower()
            
            if any(word in query_lower for word in ['often', 'frequency', 'कितनी बार', 'how many times']):
                prompt = f"""किसान पूछ रहा है कि इलाज कितनी बार करना चाहिए: {query}

जैविक उपचार के लिए: हर 7-10 दिन में एक बार। रासायनिक उपचार के लिए: लेबल के अनुसार, आमतौर पर 10-14 दिन का अंतराल। सुबह या शाम का समय बेहतर है। सिर्फ हिंदी में 2-3 वाक्यों में जवाब दें।"""
            
            elif any(word in query_lower for word in ['neem', 'नीम', 'organic', 'जैविक']):
                prompt = f"""किसान नीम या जैविक उपचार के बारे में पूछ रहा है: {query}

नीम का तेल 10 मिली प्रति लीटर पानी में मिलाएं। हफ्ते में एक बार छिड़काव करें। अन्य जैविक विकल्प: गोबर का घोल, हल्दी का पेस्ट, लहसुन-मिर्च का घोल। सिर्फ हिंदी में जवाब दें।"""
            
            else:
                # General farming question
                prompt = f"""आप एक अनुभवी कृषि विशेषज्ञ हैं। किसान का सवाल: {query}

कृपया इस सवाल का व्यावहारिक और उपयोगी जवाब हिंदी में दें। सरल भाषा में 2-3 वाक्यों में जवाब दें जो एक किसान आसानी से समझ सके।"""
            
            data = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }],
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 150
                }
            }
            
            response = requests.post(url, json=data, headers=headers, timeout=15)
            
            if response.status_code == 200:
                result = response.json()
                if 'candidates' in result and len(result['candidates']) > 0:
                    ai_response = result['candidates'][0]['content']['parts'][0]['text']
                    return ai_response.strip()
                else:
                    raise Exception("No response from Gemini")
            else:
                logger.error(f"Gemini API error: {response.status_code} - {response.text}")
                raise Exception(f"Gemini API error: {response.status_code}")
                
        except Exception as fallback_error:
            logger.error(f"Fallback voice query error: {str(fallback_error)}")
            # Provide contextual fallback responses
            if any(word in query.lower() for word in ['neem', 'नीम']):
                return "नीम का तेल 10 मिली प्रति लीटर पानी में मिलाकर छिड़काव करें। सुबह या शाम का समय बेहतर है।"
            elif any(word in query.lower() for word in ['time', 'समय']):
                return "सुबह 6-9 बजे या शाम 5-7 बजे छिड़काव करें। दोपहर की धूप में न करें।"
            else:
                return "कुछ तकनीकी समस्या है। कृपया दोबारा कोशिश करें या स्थानीय कृषि विशेषज्ञ से संपर्क करें।"

def get_groq_response(prompt):
    """Get response using Gemini API"""
    return process_voice_query(prompt, 'hi-IN', [], '110001')

def get_fallback_analysis():
    """Return basic plant health advice when AI fails"""
    return {
        'diagnosis': "पौधे की स्वास्थ्य जांच - बुनियादी विश्लेषण (Plant Health Check - Basic Analysis)",
        'treatment': """🌿 **जैविक देखभाल (Organic Care):**
• नीम का तेल (10 मिली प्रति लीटर पानी) - साप्ताहिक छिड़काव
• पीले, धब्बेदार, या मुरझाने वाले पत्तों की जांच करें
• उचित पानी दें - मिट्टी नम हो लेकिन जलभराव न हो
• मरे या रोगग्रस्त भागों को तुरंत हटा दें

💊 **रासायनिक विकल्प (Chemical Options):**
• कॉपर सल्फेट घोल (2 ग्राम प्रति लीटर) फंगल समस्याओं के लिए
• स्थानीय कृषि विस्तार अधिकारी से संपर्क करें

🛡️ **रोकथाम (Prevention):**
• मिट्टी के स्तर पर पानी दें, पत्तियों को गीला करने से बचें
• पौधों के आसपास अच्छा हवा प्रवाह सुनिश्चित करें
• समस्या की शुरुआती पहचान के लिए नियमित जांच करें

📝 **नोट:** सटीक निदान के लिए, कृपया तस्वीर दोबारा अपलोड करें या स्थानीय कृषि विशेषज्ञ से सलाह लें।""",
        'confidence': 'बुनियादी (Basic)',
        'model': 'Fallback Analysis'
    }

def get_ai_error():
    """Return error when AI service fails"""
    return {
        'diagnosis': "एआई विश्लेषण सेवा अनुपलब्ध (AI analysis service unavailable)",
        'treatment': "इस समय पौधे की तस्वीर का विश्लेषण नहीं हो सका। कृपया अपने इंटरनेट कनेक्शन की जांच करें और बाद में पुन: प्रयास करें।",
        'error': 'AI service temporarily unavailable. Please try again later.'
    }