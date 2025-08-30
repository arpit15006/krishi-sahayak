#!/usr/bin/env python3
import os
import requests
import json
from datetime import datetime

class ResourceOptimizer:
    def __init__(self):
        self.groq_api_key = os.getenv('GROQ_API_KEY')

    def calculate_resources(self, crop_data, soil_data, weather_data, farm_area):
        """Calculate water and fertilizer requirements using AI"""
        try:
            # Create comprehensive prompt for AI
            prompt = self._create_optimization_prompt(crop_data, soil_data, weather_data, farm_area)
            
            # Get AI recommendations
            ai_response = self._get_groq_response(prompt)
            
            # Parse and structure the response
            recommendations = self._parse_ai_response(ai_response)
            
            return {
                'success': True,
                'recommendations': recommendations,
                'is_ai_generated': True,
                'input_data': {
                    'crop': crop_data,
                    'soil': soil_data,
                    'weather': weather_data,
                    'area': farm_area
                }
            }
            
        except Exception as e:
            fallback_data = self._get_fallback_recommendations(crop_data['crop_type'], farm_area)
            fallback_data['is_ai_generated'] = False
            return {
                'success': False,
                'error': str(e),
                'fallback': fallback_data
            }

    def _create_optimization_prompt(self, crop_data, soil_data, weather_data, farm_area):
        """Create detailed prompt for AI optimization"""
        
        weather_summary = f"Temperature: {weather_data.get('temperature', 'N/A')}°C, " \
                         f"Humidity: {weather_data.get('humidity', 'N/A')}%, " \
                         f"Rainfall: {weather_data.get('rainfall', 'N/A')}mm"
        
        prompt = f"""आप एक कृषि संसाधन विशेषज्ञ हैं। निम्नलिखित जानकारी के आधार पर पानी और उर्वरक की सटीक मात्रा की गणना करें:

फसल की जानकारी:
- फसल: {crop_data.get('crop_type', 'धान')}
- किस्म: {crop_data.get('variety', 'सामान्य')}
- बुआई की तारीख: {crop_data.get('sowing_date', 'N/A')}
- फसल की अवस्था: {crop_data.get('growth_stage', 'वानस्पतिक')}

मिट्टी की जानकारी:
- मिट्टी का प्रकार: {soil_data.get('soil_type', 'दोमट')}
- pH स्तर: {soil_data.get('ph_level', '6.5')}
- जैविक कार्बन: {soil_data.get('organic_carbon', 'मध्यम')}
- नाइट्रोजन स्तर: {soil_data.get('nitrogen', 'मध्यम')}
- फास्फोरस स्तर: {soil_data.get('phosphorus', 'मध्यम')}
- पोटाश स्तर: {soil_data.get('potash', 'मध्यम')}

मौसम की जानकारी:
- {weather_summary}
- अगले 3 दिन का पूर्वानुमान: {weather_data.get('forecast', 'सामान्य')}

खेत का क्षेत्रफल: {farm_area} एकड़

कृपया निम्नलिखित की सटीक गणना करें:
1. दैनिक पानी की आवश्यकता (लीटर/एकड़)
2. सप्ताहिक सिंचाई की आवृत्ति
3. आवश्यक उर्वरक (NPK) की मात्रा (किग्रा/एकड़)
4. जैविक खाद की सिफारिश
5. लागत अनुमान (₹/एकड़)
6. पर्यावरण प्रभाव कम करने के उपाय

JSON format में उत्तर दें:
{{
  "water": {{
    "daily_requirement": "संख्या",
    "irrigation_frequency": "दिनों में",
    "method": "सिंचाई विधि"
  }},
  "fertilizer": {{
    "nitrogen": "किग्रा/एकड़",
    "phosphorus": "किग्रा/एकड़", 
    "potash": "किग्रा/एकड़",
    "organic": "टन/एकड़"
  }},
  "cost": {{
    "water_cost": "₹/एकड़",
    "fertilizer_cost": "₹/एकड़",
    "total_cost": "₹/एकड़"
  }},
  "schedule": "सप्ताह के अनुसार कार्यक्रम",
  "tips": ["पर्यावरण अनुकूल सुझाव"]
}}"""

        return prompt

    def _get_groq_response(self, prompt):
        """Get response from Groq AI"""
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.groq_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "llama3-8b-8192",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1000,
            "temperature": 0.3
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            raise Exception(f"Groq API error: {response.status_code}")

    def _parse_ai_response(self, ai_response):
        """Parse AI response and extract structured data"""
        try:
            # Try to extract JSON from response
            start_idx = ai_response.find('{')
            end_idx = ai_response.rfind('}') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = ai_response[start_idx:end_idx]
                return json.loads(json_str)
            else:
                # Fallback parsing
                return self._parse_text_response(ai_response)
                
        except json.JSONDecodeError:
            return self._parse_text_response(ai_response)

    def _parse_text_response(self, response):
        """Parse text response when JSON parsing fails"""
        return {
            "water": {
                "daily_requirement": "2000-3000 लीटर/एकड़",
                "irrigation_frequency": "3-4 दिन",
                "method": "ड्रिप सिंचाई"
            },
            "fertilizer": {
                "nitrogen": "40-60 किग्रा/एकड़",
                "phosphorus": "20-30 किग्रा/एकड़",
                "potash": "20-25 किग्रा/एकड़",
                "organic": "2-3 टन/एकड़"
            },
            "cost": {
                "water_cost": "₹1500-2000/एकड़",
                "fertilizer_cost": "₹3000-4000/एकड़",
                "total_cost": "₹4500-6000/एकड़"
            },
            "schedule": "सप्ताह 1-2: बुआई और प्रारंभिक देखभाल\nसप्ताह 3-6: वानस्पतिक वृद्धि\nसप्ताह 7-12: फूल और फल विकास",
            "tips": [
                "मिट्टी की नमी बनाए रखें",
                "जैविक खाद का उपयोग करें",
                "ड्रिप सिंचाई से पानी बचाएं",
                "मौसम के अनुसार सिंचाई करें"
            ],
            "ai_advice": response[:200] + "..." if len(response) > 200 else response
        }

    def _get_fallback_recommendations(self, crop_type, area):
        """Provide fallback recommendations when AI fails"""
        crop_defaults = {
            'Rice': {
                'water_daily': 3000,
                'irrigation_days': 3,
                'nitrogen': 50,
                'phosphorus': 25,
                'potash': 25
            },
            'Wheat': {
                'water_daily': 2000,
                'irrigation_days': 4,
                'nitrogen': 40,
                'phosphorus': 20,
                'potash': 20
            },
            'Cotton': {
                'water_daily': 2500,
                'irrigation_days': 5,
                'nitrogen': 60,
                'phosphorus': 30,
                'potash': 30
            }
        }
        
        defaults = crop_defaults.get(crop_type, crop_defaults['Rice'])
        
        return {
            "water": {
                "daily_requirement": f"{defaults['water_daily']} लीटर/एकड़",
                "irrigation_frequency": f"{defaults['irrigation_days']} दिन",
                "method": "ड्रिप सिंचाई अनुशंसित"
            },
            "fertilizer": {
                "nitrogen": f"{defaults['nitrogen']} किग्रा/एकड़",
                "phosphorus": f"{defaults['phosphorus']} किग्रा/एकड़",
                "potash": f"{defaults['potash']} किग्रा/एकड़",
                "organic": "2-3 टन/एकड़"
            },
            "cost": {
                "total_cost": "₹5000-7000/एकड़"
            },
            "tips": ["मिट्टी परीक्षण कराएं", "जैविक खाद का उपयोग करें"]
        }

# Global instance
resource_optimizer = ResourceOptimizer()