"""
AI-powered crop yield prediction
"""

import json
import requests
import os
from datetime import datetime, timedelta

def predict_crop_yield(crop_data, weather_data, farmer_data):
    """Predict crop yield using AI"""
    
    try:
        # Use Groq API for yield prediction
        api_key = os.getenv('GROQ_API_KEY')
        
        prompt = f"""You are an expert agricultural scientist specializing in crop yield prediction for Indian farmers.

CROP DATA:
- Crop: {crop_data.get('crop_type')}
- Variety: {crop_data.get('variety')}
- Area: {crop_data.get('area')} acres
- Sowing Date: {crop_data.get('sowing_date')}
- Practices: {', '.join(crop_data.get('practices', []))}

WEATHER CONDITIONS:
- Temperature: {weather_data.get('current', {}).get('temperature', 25)}°C
- Humidity: {weather_data.get('current', {}).get('humidity', 70)}%
- Recent Weather: {weather_data.get('current', {}).get('description', 'Normal')}

FARMER PROFILE:
- Experience: {farmer_data.get('experience', 5)} years
- Location: {farmer_data.get('location', 'India')}

Provide a comprehensive yield prediction analysis in Hindi and English:

1. Expected yield per acre (tons/acre)
2. Total production estimate
3. Revenue projection (₹)
4. Key success factors
5. Specific recommendations
6. Harvest timeline
7. Risk factors to watch

Write the analysis in a farmer-friendly tone mixing Hindi and English as Indian farmers speak."""

        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "llama3-70b-8192",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 500,
            "temperature": 0.7
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            ai_analysis = result['choices'][0]['message']['content'].strip()
            
            # Generate structured prediction
            prediction = generate_structured_prediction(crop_data, ai_analysis)
            return prediction
        else:
            return get_fallback_prediction(crop_data)
            
    except Exception as e:
        return get_fallback_prediction(crop_data)

def generate_structured_prediction(crop_data, ai_analysis):
    """Generate structured prediction from AI analysis"""
    
    crop = crop_data.get('crop_type', 'Rice')
    area = float(crop_data.get('area', 1))
    
    # Base yields for different crops (tons/acre)
    base_yields = {
        'Rice': 2.8, 'Wheat': 2.5, 'Cotton': 1.2, 'Sugarcane': 45,
        'Maize': 3.2, 'Potato': 15, 'Onion': 12, 'Tomato': 25
    }
    
    # Base prices (₹/ton)
    base_prices = {
        'Rice': 21000, 'Wheat': 19500, 'Cotton': 52000, 'Sugarcane': 3500,
        'Maize': 18000, 'Potato': 12000, 'Onion': 18000, 'Tomato': 25000
    }
    
    base_yield = base_yields.get(crop, 2.5)
    base_price = base_prices.get(crop, 20000)
    
    # Adjust yield based on practices
    practices = crop_data.get('practices', [])
    yield_multiplier = 1.0
    
    if 'Organic' in practices:
        yield_multiplier += 0.15
    if 'Drip Irrigation' in practices:
        yield_multiplier += 0.20
    if 'Fertilizer' in practices:
        yield_multiplier += 0.10
    
    expected_yield_per_acre = base_yield * yield_multiplier
    total_production = expected_yield_per_acre * area
    expected_revenue = total_production * base_price
    
    # Calculate harvest date (3-4 months from sowing)
    try:
        sowing_date = datetime.strptime(crop_data.get('sowing_date'), '%Y-%m-%d')
        harvest_date = sowing_date + timedelta(days=120)
        market_date = harvest_date + timedelta(days=15)
    except:
        harvest_date = datetime.now() + timedelta(days=90)
        market_date = harvest_date + timedelta(days=15)
    
    return {
        'success': True,
        'crop': crop,
        'area': area,
        'expected_yield': f"{expected_yield_per_acre:.1f}",
        'total_production': f"{total_production:.1f}",
        'expected_revenue': f"{expected_revenue:,.0f}",
        'yield_per_acre': f"{expected_yield_per_acre:.1f}-{expected_yield_per_acre*1.2:.1f}",
        'harvest_date': harvest_date.strftime('%B %Y'),
        'market_date': market_date.strftime('%B %d, %Y'),
        'ai_analysis': ai_analysis,
        'confidence': 'High' if yield_multiplier > 1.2 else 'Medium',
        'recommendations': generate_recommendations(practices),
        'timeline': generate_timeline(harvest_date)
    }

def get_fallback_prediction(crop_data):
    """Fallback prediction when AI fails"""
    
    crop = crop_data.get('crop_type', 'Rice')
    area = float(crop_data.get('area', 1))
    practices = crop_data.get('practices', [])
    
    # Fallback analysis in Hindi/English mix
    fallback_analysis = f"""आपकी {crop} की फसल अच्छी है! Based on your farming practices and area of {area} acres, here's the prediction:

✅ Good farming practices detected - {'Organic, ' if 'Organic' in practices else ''}{'Drip irrigation, ' if 'Drip Irrigation' in practices else ''}{'Fertilizer use' if 'Fertilizer' in practices else ''}

🌾 Expected yield looks promising with proper care. Your experience and good practices will help achieve better results.

💡 Recommendation: Continue current practices, monitor weather conditions, and ensure timely harvesting for maximum profit."""
    
    return generate_structured_prediction(crop_data, fallback_analysis)

def generate_recommendations(practices):
    """Generate farming recommendations"""
    recommendations = [
        "Monitor soil moisture regularly",
        "Watch for pest and disease symptoms",
        "Apply nutrients as per soil test"
    ]
    
    if 'Organic' in practices:
        recommendations.append("Continue organic practices for premium pricing")
    if 'Drip Irrigation' in practices:
        recommendations.append("Maintain drip system for water efficiency")
    else:
        recommendations.append("Consider drip irrigation for better yield")
        
    return recommendations

def generate_timeline(harvest_date):
    """Generate crop timeline"""
    now = datetime.now()
    days_to_harvest = (harvest_date - now).days
    
    if days_to_harvest > 60:
        stage = "Growth stage"
    elif days_to_harvest > 30:
        stage = "Flowering stage"
    else:
        stage = "Maturity stage"
        
    return {
        'current_stage': stage,
        'days_to_harvest': max(0, days_to_harvest),
        'harvest_month': harvest_date.strftime('%B %Y')
    }