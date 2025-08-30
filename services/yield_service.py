import os
import requests
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

def predict_crop_yield(crop_type, area_acres, location_data, weather_data):
    """AI-powered crop yield prediction using Gemini API"""
    
    try:
        gemini_key = os.getenv('GEMINI_API_KEY', 'AIzaSyCVchsFQ9RyH4wdM2qrVZqRBJyQ5g9qOKg')
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
        headers = {"Content-Type": "application/json"}
        
        # Create context-rich prompt for yield prediction
        current_temp = weather_data.get('current', {}).get('temperature', 25)
        rainfall = weather_data.get('forecast', [{}])[0].get('precipitation', 0)
        
        prompt = f"""भारतीय कृषि विशेषज्ञ के रूप में फसल उत्पादन की भविष्यवाणी करें:

फसल: {crop_type}
क्षेत्रफल: {area_acres} एकड़
स्थान: {location_data.get('pin_code', 'भारत')}
वर्तमान तापमान: {current_temp}°C
बारिश: {rainfall}mm

कृपया निम्नलिखित जानकारी दें:
1. अनुमानित उत्पादन (क्विंटल में)
2. उत्पादन की गुणवत्ता (उत्कृष्ट/अच्छी/औसत)
3. मुख्य सुझाव (2-3 बिंदु)
4. जोखिम कारक (यदि कोई हो)

संक्षिप्त और व्यावहारिक उत्तर दें।"""
        
        data = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 300
            }
        }
        
        response = requests.post(url, json=data, headers=headers, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            if 'candidates' in result and len(result['candidates']) > 0:
                ai_response = result['candidates'][0]['content']['parts'][0]['text']
                
                # Parse the response to extract structured data
                return parse_yield_prediction(ai_response, crop_type, area_acres)
            else:
                return get_fallback_prediction(crop_type, area_acres)
        else:
            logger.error(f"Gemini API error: {response.status_code}")
            return get_fallback_prediction(crop_type, area_acres)
            
    except Exception as e:
        logger.error(f"Yield prediction error: {str(e)}")
        return get_fallback_prediction(crop_type, area_acres)

def parse_yield_prediction(ai_response, crop_type, area_acres):
    """Parse AI response into structured yield prediction"""
    
    # Extract yield estimate (basic parsing)
    lines = ai_response.split('\n')
    estimated_yield = f"{area_acres * 15}-{area_acres * 25} क्विंटल"  # Default range
    
    for line in lines:
        if any(keyword in line for keyword in ['उत्पादन', 'क्विंटल', 'टन']):
            if any(char.isdigit() for char in line):
                estimated_yield = line.strip()
                break
    
    return {
        'crop_type': crop_type,
        'area_acres': area_acres,
        'estimated_yield': estimated_yield,
        'prediction_text': ai_response,
        'confidence': 'मध्यम (Medium)',
        'prediction_date': datetime.now().strftime('%Y-%m-%d'),
        'factors': {
            'weather_impact': 'सामान्य',
            'soil_quality': 'अच्छी',
            'season_suitability': 'उपयुक्त'
        }
    }

def get_fallback_prediction(crop_type, area_acres):
    """Fallback prediction when AI fails"""
    
    # Basic yield estimates per acre for common crops
    yield_per_acre = {
        'Rice': 20,
        'Wheat': 25,
        'Sugarcane': 300,
        'Cotton': 8,
        'Maize': 30,
        'Potato': 150,
        'Onion': 200
    }
    
    base_yield = yield_per_acre.get(crop_type, 20)
    estimated_total = base_yield * area_acres
    
    return {
        'crop_type': crop_type,
        'area_acres': area_acres,
        'estimated_yield': f"{estimated_total} क्विंटल (अनुमानित)",
        'prediction_text': f"""🌾 **फसल उत्पादन पूर्वानुमान**

**अनुमानित उत्पादन:** {estimated_total} क्विंटल
**गुणवत्ता:** अच्छी (मानक कृषि पद्धति के साथ)

**मुख्य सुझाव:**
• उचित सिंचाई और उर्वरक का प्रयोग करें
• कीट-रोग नियंत्रण पर ध्यान दें
• मौसम की निगरानी करते रहें

**नोट:** यह अनुमान सामान्य परिस्थितियों पर आधारित है।""",
        'confidence': 'बुनियादी (Basic)',
        'prediction_date': datetime.now().strftime('%Y-%m-%d'),
        'factors': {
            'weather_impact': 'सामान्य',
            'soil_quality': 'औसत',
            'season_suitability': 'उपयुक्त'
        }
    }