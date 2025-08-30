import json
import logging
from datetime import datetime, timedelta
from services.market_service import get_market_prices

logger = logging.getLogger(__name__)

def check_price_alerts(user_crops, user_id):
    """Check for price alerts based on user's crops"""
    
    try:
        # Get current market prices
        market_data = get_market_prices(user_crops)
        alerts = []
        
        if not market_data.get('prices'):
            return []
        
        prices = market_data.get('prices', {})
        if isinstance(prices, list):
            # Handle list format
            for price_item in prices:
                crop_name = price_item.get('commodity', '')
                if crop_name in user_crops:
                    current_price = price_item.get('modal_price', 0)
                    alert = generate_price_alert(crop_name, price_item, current_price)
                    if alert:
                        alerts.append(alert)
        elif isinstance(prices, dict):
            # Handle dict format
            for crop_name, crop_data in prices.items():
                if crop_name in user_crops:
                    current_price = crop_data.get('modal_price', 0)
                    alert = generate_price_alert(crop_name, crop_data, current_price)
                    if alert:
                        alerts.append(alert)
        
        return alerts
        
    except Exception as e:
        logger.error(f"Error checking price alerts: {str(e)}")
        return []

def generate_price_alert(crop_name, crop_data, current_price):
    """Generate alert based on price analysis"""
    
    try:
        min_price = crop_data.get('min_price', current_price)
        max_price = crop_data.get('max_price', current_price)
        
        # Calculate price position (0-100%)
        if max_price > min_price:
            price_position = ((current_price - min_price) / (max_price - min_price)) * 100
        else:
            price_position = 50  # Default middle position
        
        alert = None
        
        # High price alert (good for selling)
        if price_position >= 80:
            alert = {
                'type': 'high_price',
                'crop': crop_name,
                'message': f"🟢 {crop_name} की कीमत अच्छी है! ₹{current_price}/क्विंटल - बेचने का अच्छा समय",
                'price': current_price,
                'action': 'sell',
                'urgency': 'high',
                'timestamp': datetime.now().isoformat()
            }
        
        # Low price alert (good for buying)
        elif price_position <= 30:
            alert = {
                'type': 'low_price',
                'crop': crop_name,
                'message': f"🔴 {crop_name} की कीमत कम है - ₹{current_price}/क्विंटल - खरीदने का समय",
                'price': current_price,
                'action': 'buy',
                'urgency': 'medium',
                'timestamp': datetime.now().isoformat()
            }
        
        # Moderate price alert
        elif 60 <= price_position <= 75:
            alert = {
                'type': 'moderate_price',
                'crop': crop_name,
                'message': f"🟡 {crop_name} की कीमत स्थिर है - ₹{current_price}/क्विंटल - बाजार की निगरानी करें",
                'price': current_price,
                'action': 'monitor',
                'urgency': 'low',
                'timestamp': datetime.now().isoformat()
            }
        
        return alert
        
    except Exception as e:
        logger.error(f"Error generating alert for {crop_name}: {str(e)}")
        return None

def get_market_trends(crop_name):
    """Get market trend analysis for a crop"""
    
    try:
        # Simulate trend analysis (in real app, this would use historical data)
        trends = {
            'Rice': {'trend': 'up', 'change': '+5%', 'forecast': 'बढ़ने की संभावना'},
            'Wheat': {'trend': 'stable', 'change': '0%', 'forecast': 'स्थिर रहने की संभावना'},
            'Cotton': {'trend': 'down', 'change': '-3%', 'forecast': 'गिरने की संभावना'},
            'Sugarcane': {'trend': 'up', 'change': '+8%', 'forecast': 'तेजी से बढ़ने की संभावना'},
            'Onion': {'trend': 'volatile', 'change': '±10%', 'forecast': 'अस्थिर बाजार'}
        }
        
        return trends.get(crop_name, {
            'trend': 'stable',
            'change': '0%',
            'forecast': 'सामान्य बाजार'
        })
        
    except Exception as e:
        logger.error(f"Error getting trends for {crop_name}: {str(e)}")
        return {'trend': 'unknown', 'change': '0%', 'forecast': 'डेटा उपलब्ध नहीं'}

def create_alert_summary(alerts):
    """Create a summary of all alerts"""
    
    if not alerts:
        return {
            'total_alerts': 0,
            'high_priority': 0,
            'summary': 'कोई नई अलर्ट नहीं है। सभी कीमतें सामान्य हैं।'
        }
    
    high_priority = len([a for a in alerts if a.get('urgency') == 'high'])
    sell_opportunities = len([a for a in alerts if a.get('action') == 'sell'])
    
    summary = f"{len(alerts)} नई अलर्ट मिली हैं। "
    
    if sell_opportunities > 0:
        summary += f"{sell_opportunities} फसलों की अच्छी कीमत मिल रही है। "
    
    if high_priority > 0:
        summary += "तुरंत कार्रवाई की जरूरत है!"
    
    return {
        'total_alerts': len(alerts),
        'high_priority': high_priority,
        'sell_opportunities': sell_opportunities,
        'summary': summary
    }

def get_demo_alerts():
    """Generate demo alerts for testing"""
    
    return [
        {
            'type': 'high_price',
            'crop': 'Rice',
            'message': '🟢 धान की कीमत अच्छी है! ₹2,150/क्विंटल - बेचने का अच्छा समय',
            'price': 2150,
            'action': 'sell',
            'urgency': 'high',
            'timestamp': datetime.now().isoformat()
        },
        {
            'type': 'low_price',
            'crop': 'Wheat',
            'message': '🔴 गेहूं की कीमत कम है - ₹1,800/क्विंटल - खरीदने का समय',
            'price': 1800,
            'action': 'buy',
            'urgency': 'medium',
            'timestamp': datetime.now().isoformat()
        },
        {
            'type': 'trend_alert',
            'crop': 'Cotton',
            'message': '📈 कपास की कीमत बढ़ने की संभावना - अगले सप्ताह तक इंतजार करें',
            'price': 5200,
            'action': 'wait',
            'urgency': 'low',
            'timestamp': datetime.now().isoformat()
        }
    ]