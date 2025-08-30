import os
import requests
import json
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class EnhancedVoiceAssistant:
    def __init__(self):
        self.gemini_key = os.getenv('GEMINI_API_KEY', 'AIzaSyCVchsFQ9RyH4wdM2qrVZqRBJyQ5g9qOKg')
        self.context_memory = {}
        self.farmer_knowledge_base = self._load_farmer_knowledge()
    
    def _load_farmer_knowledge(self):
        """Load comprehensive farming knowledge base"""
        return {
            'crops': {
                'Rice': {
                    'seasons': ['Kharif', 'Rabi'],
                    'diseases': ['Blast', 'Sheath Blight', 'Brown Spot'],
                    'pests': ['Stem Borer', 'Leaf Folder', 'BPH'],
                    'fertilizers': ['Urea', 'DAP', 'Potash'],
                    'growth_stages': ['Seedling', 'Tillering', 'Flowering', 'Maturity']
                },
                'Wheat': {
                    'seasons': ['Rabi'],
                    'diseases': ['Rust', 'Smut', 'Blight'],
                    'pests': ['Aphids', 'Termites', 'Cut Worm'],
                    'fertilizers': ['Urea', 'DAP', 'NPK'],
                    'growth_stages': ['Germination', 'Tillering', 'Jointing', 'Heading']
                },
                'Cotton': {
                    'seasons': ['Kharif'],
                    'diseases': ['Wilt', 'Boll Rot', 'Leaf Curl'],
                    'pests': ['Bollworm', 'Whitefly', 'Thrips'],
                    'fertilizers': ['Urea', 'DAP', 'Potash'],
                    'growth_stages': ['Squaring', 'Flowering', 'Boll Formation', 'Maturity']
                }
            },
            'weather_advice': {
                'rain': 'बारिश से पहले छिड़काव न करें। जल निकासी का ध्यान रखें।',
                'drought': 'पानी की बचत करें। ड्रिप सिंचाई का उपयोग करें।',
                'heat': 'सुबह-शाम पानी दें। दोपहर में काम न करें।',
                'cold': 'पाला से बचाव करें। धुआं करें या स्प्रिंकलर चलाएं।'
            },
            'market_timing': {
                'Rice': 'नवंबर-दिसंबर में बेचें। त्योहारों के समय अच्छे दाम मिलते हैं।',
                'Wheat': 'अप्रैल-मई में बेचें। सरकारी खरीद का इंतजार करें।',
                'Cotton': 'दिसंबर-जनवरी में बेचें। निर्यात मांग अच्छी रहती है।'
            }
        }
    
    def process_contextual_query(self, query, language, user_crops, pin_code, scan_result=None, weather_data=None, market_data=None):
        """Enhanced contextual query processing with comprehensive context"""
        
        try:
            # Build comprehensive context
            context = self._build_enhanced_context(query, user_crops, pin_code, scan_result, weather_data, market_data)
            
            # Detect query intent and category
            intent = self._detect_query_intent(query)
            
            # Generate contextual prompt based on intent
            prompt = self._generate_contextual_prompt(query, intent, context, language)
            
            # Get AI response
            response = self._get_ai_response(prompt)
            
            # Post-process response for better context
            enhanced_response = self._enhance_response_with_context(response, intent, context)
            
            # Store context for future queries
            self._update_context_memory(query, enhanced_response, user_crops)
            
            return enhanced_response
            
        except Exception as e:
            logger.error(f"Enhanced voice assistant error: {str(e)}")
            return self._get_fallback_response(query, language)
    
    def _build_enhanced_context(self, query, user_crops, pin_code, scan_result, weather_data, market_data):
        """Build comprehensive context from all available data"""
        
        context = {
            'user_profile': {
                'crops': user_crops,
                'location': pin_code,
                'farming_experience': 'experienced'  # Could be enhanced with user data
            },
            'current_season': self._get_current_season(),
            'recent_queries': self.context_memory.get('recent_queries', []),
            'crop_knowledge': {}
        }
        
        # Add crop-specific knowledge
        for crop in user_crops:
            if crop in self.farmer_knowledge_base['crops']:
                context['crop_knowledge'][crop] = self.farmer_knowledge_base['crops'][crop]
        
        # Add scan result context
        if scan_result:
            context['plant_diagnosis'] = {
                'disease': scan_result.get('diagnosis', ''),
                'treatment': scan_result.get('treatment', ''),
                'confidence': scan_result.get('confidence', 'medium')
            }
        
        # Add weather context
        if weather_data:
            context['weather'] = {
                'current_temp': weather_data.get('current', {}).get('temperature'),
                'conditions': weather_data.get('current', {}).get('description'),
                'forecast': weather_data.get('forecast', [])
            }
        
        # Add market context
        if market_data:
            context['market'] = {
                'prices': market_data.get('prices', []),
                'trends': 'stable'  # Could be enhanced with trend analysis
            }
        
        return context
    
    def _detect_query_intent(self, query):
        """Detect the intent/category of the user query"""
        
        query_lower = query.lower()
        
        # Disease and pest related
        if any(word in query_lower for word in ['बीमारी', 'रोग', 'कीड़े', 'कीट', 'disease', 'pest', 'problem', 'समस्या']):
            return 'disease_pest'
        
        # Weather related
        elif any(word in query_lower for word in ['मौसम', 'बारिश', 'धूप', 'ठंड', 'weather', 'rain', 'temperature']):
            return 'weather'
        
        # Market and pricing
        elif any(word in query_lower for word in ['दाम', 'कीमत', 'बाजार', 'बेचना', 'price', 'market', 'sell']):
            return 'market'
        
        # Fertilizer and nutrition
        elif any(word in query_lower for word in ['खाद', 'उर्वरक', 'पोषण', 'fertilizer', 'nutrition', 'feeding']):
            return 'fertilizer'
        
        # Irrigation and water
        elif any(word in query_lower for word in ['पानी', 'सिंचाई', 'water', 'irrigation', 'watering']):
            return 'irrigation'
        
        # Planting and sowing
        elif any(word in query_lower for word in ['बुआई', 'रोपाई', 'बीज', 'planting', 'sowing', 'seed']):
            return 'planting'
        
        # Harvesting
        elif any(word in query_lower for word in ['कटाई', 'फसल', 'harvest', 'crop']):
            return 'harvesting'
        
        # General farming
        else:
            return 'general'
    
    def _generate_contextual_prompt(self, query, intent, context, language):
        """Generate highly contextual prompts based on intent and available context"""
        
        base_context = f"""
आप एक अनुभवी कृषि विशेषज्ञ हैं जो भारतीय किसानों की मदद करते हैं।

किसान की जानकारी:
- मुख्य फसलें: {', '.join(context['user_profile']['crops'])}
- स्थान: {context['user_profile']['location']}
- मौसम: {context['current_season']}
"""
        
        # Add weather context if available
        if context.get('weather'):
            weather = context['weather']
            base_context += f"\nवर्तमान मौसम: {weather.get('current_temp', 'N/A')}°C, {weather.get('conditions', 'सामान्य')}"
        
        # Add plant diagnosis context if available
        if context.get('plant_diagnosis'):
            diagnosis = context['plant_diagnosis']
            base_context += f"\nपौधे की समस्या: {diagnosis.get('disease', 'कोई विशेष समस्या नहीं')}"
        
        # Intent-specific prompts
        intent_prompts = {
            'disease_pest': f"""
{base_context}

किसान का सवाल: {query}

कृपया निम्नलिखित के आधार पर विस्तृत सलाह दें:
1. रोग/कीट की पहचान और कारण
2. तत्काल उपचार (जैविक और रासायनिक दोनों)
3. रोकथाम के उपाय
4. मौसम के अनुसार सावधानियां
5. लागत प्रभावी समाधान

सिर्फ हिंदी में 3-4 वाक्यों में व्यावहारिक सलाह दें।
""",
            
            'weather': f"""
{base_context}

किसान का सवाल: {query}

मौसम के आधार पर सलाह दें:
1. आज के मौसम के अनुसार खेती के काम
2. आने वाले दिनों की तैयारी
3. फसल सुरक्षा के उपाय
4. सिंचाई और छिड़काव का समय

हिंदी में व्यावहारिक सलाह दें।
""",
            
            'market': f"""
{base_context}

किसान का सवाल: {query}

बाजार की सलाह दें:
1. वर्तमान कीमतों का विश्लेषण
2. बेचने का सही समय
3. बाजार की मांग और आपूर्ति
4. मुनाफा बढ़ाने के तरीके

हिंदी में स्पष्ट सलाह दें।
""",
            
            'fertilizer': f"""
{base_context}

किसान का सवाल: {query}

खाद-उर्वरक की सलाह:
1. फसल की वर्तमान अवस्था के अनुसार पोषण
2. जैविक और रासायनिक विकल्प
3. मात्रा और समय
4. मिट्टी की जांच की सलाह

हिंदी में सटीक मार्गदर्शन दें।
""",
            
            'irrigation': f"""
{base_context}

किसान का सवाल: {query}

सिंचाई की सलाह:
1. पानी की मात्रा और समय
2. मौसम के अनुसार सिंचाई
3. पानी की बचत के तरीके
4. फसल की अवस्था के अनुसार पानी

हिंदी में व्यावहारिक सुझाव दें।
""",
            
            'general': f"""
{base_context}

किसान का सवाल: {query}

कृपया किसान के सवाल का विस्तृत और व्यावहारिक जवाब दें। 
स्थानीय परिस्थितियों, मौसम, और फसल के अनुसार सलाह दें।

हिंदी में सरल भाषा में जवाब दें।
"""
        }
        
        return intent_prompts.get(intent, intent_prompts['general'])
    
    def _get_ai_response(self, prompt):
        """Get response from Gemini AI with enhanced parameters"""
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_key}"
        headers = {"Content-Type": "application/json"}
        
        data = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 200,
                "topP": 0.8,
                "topK": 40
            }
        }
        
        response = requests.post(url, json=data, headers=headers, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            if 'candidates' in result and len(result['candidates']) > 0:
                return result['candidates'][0]['content']['parts'][0]['text'].strip()
        
        raise Exception("No response from AI")
    
    def _enhance_response_with_context(self, response, intent, context):
        """Enhance AI response with additional contextual information"""
        
        enhanced_response = response
        
        # Add weather-specific enhancements
        if intent == 'weather' and context.get('weather'):
            weather = context['weather']
            if weather.get('current_temp', 0) > 35:
                enhanced_response += " गर्मी के कारण दोपहर 12-3 बजे तक काम न करें।"
            elif weather.get('current_temp', 0) < 10:
                enhanced_response += " ठंड से फसल को बचाने के लिए धुआं करें।"
        
        # Add crop-specific enhancements
        if context.get('crop_knowledge'):
            for crop in context['user_profile']['crops']:
                if crop in context['crop_knowledge'] and intent == 'disease_pest':
                    crop_diseases = context['crop_knowledge'][crop]['diseases']
                    enhanced_response += f" {crop} में आम बीमारियां: {', '.join(crop_diseases[:2])}।"
                    break
        
        # Add seasonal advice
        season = context.get('current_season')
        if season == 'Monsoon' and intent in ['irrigation', 'disease_pest']:
            enhanced_response += " मानसून में जल निकासी का विशेष ध्यान रखें।"
        elif season == 'Winter' and intent == 'planting':
            enhanced_response += " रबी फसल के लिए उपयुक्त समय है।"
        
        return enhanced_response
    
    def _update_context_memory(self, query, response, user_crops):
        """Update context memory for future queries"""
        
        if 'recent_queries' not in self.context_memory:
            self.context_memory['recent_queries'] = []
        
        # Store recent query with timestamp
        query_record = {
            'query': query,
            'response': response,
            'timestamp': datetime.now().isoformat(),
            'crops': user_crops
        }
        
        self.context_memory['recent_queries'].append(query_record)
        
        # Keep only last 5 queries
        if len(self.context_memory['recent_queries']) > 5:
            self.context_memory['recent_queries'] = self.context_memory['recent_queries'][-5:]
    
    def _get_current_season(self):
        """Determine current agricultural season"""
        
        month = datetime.now().month
        
        if month in [6, 7, 8, 9]:
            return 'Kharif'  # Monsoon season
        elif month in [10, 11, 12, 1, 2, 3]:
            return 'Rabi'    # Winter season
        else:
            return 'Zaid'    # Summer season
    
    def _get_fallback_response(self, query, language):
        """Enhanced fallback responses based on query analysis"""
        
        query_lower = query.lower()
        
        # Disease/pest fallbacks
        if any(word in query_lower for word in ['बीमारी', 'रोग', 'कीड़े', 'disease', 'pest']):
            return "पौधे की बीमारी के लिए नीम का तेल (10 मिली प्रति लीटर) का छिड़काव करें। स्थानीय कृषि विशेषज्ञ से भी सलाह लें।"
        
        # Weather fallbacks
        elif any(word in query_lower for word in ['मौसम', 'बारिश', 'weather', 'rain']):
            return "मौसम के अनुसार खेती करें। बारिश से पहले छिड़काव न करें। सुबह-शाम का समय काम के लिए बेहतर है।"
        
        # Market fallbacks
        elif any(word in query_lower for word in ['दाम', 'कीमत', 'बाजार', 'price', 'market']):
            return "बाजार की कीमतें रोज बदलती रहती हैं। स्थानीय मंडी से संपर्क करें या हमारे मार्केट सेक्शन में देखें।"
        
        # General fallback
        else:
            return "आपके सवाल के लिए स्थानीय कृषि विशेषज्ञ से संपर्क करें। हमारे ऐप में और भी जानकारी उपलब्ध है।"

# Initialize enhanced voice assistant
enhanced_voice_assistant = EnhancedVoiceAssistant()