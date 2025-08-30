import logging
from datetime import datetime
from services.agmarknet_api import get_real_market_prices

logger = logging.getLogger(__name__)

def get_market_prices(crops_list):
    """Get real market prices from AGMARKNET API with fallback"""
    try:
        # Try to get real market data first
        real_data = get_real_market_prices(crops_list)
        if real_data and real_data.get('prices'):
            return real_data
        
        # If real API fails, return mock data to prevent infinite loading
        mock_prices = []
        base_prices = {
            'Rice': 2500, 'Wheat': 2200, 'Sugarcane': 350, 'Cotton': 6500,
            'Maize': 1800, 'Onion': 2800, 'Potato': 1500, 'Tomato': 3200,
            'Soybean': 4200, 'Groundnut': 5800, 'Turmeric': 8500, 'Chili': 12000,
            'Garlic': 15000
        }
        
        # Specific market locations for each crop
        market_locations = {
            'Rice': ['Karnal Mandi, Haryana', 'Thanjavur Mandi, Tamil Nadu', 'Cuttack Mandi, Odisha'],
            'Wheat': ['Indore Mandi, Madhya Pradesh', 'Ludhiana Mandi, Punjab', 'Meerut Mandi, UP'],
            'Cotton': ['Akola Mandi, Maharashtra', 'Rajkot Mandi, Gujarat', 'Guntur Mandi, Andhra Pradesh'],
            'Onion': ['Lasalgaon Mandi, Maharashtra', 'Bangalore Mandi, Karnataka', 'Nashik Mandi, Maharashtra'],
            'Potato': ['Agra Mandi, UP', 'Hooghly Mandi, West Bengal', 'Shimla Mandi, Himachal Pradesh'],
            'Tomato': ['Kolar Mandi, Karnataka', 'Pune Mandi, Maharashtra', 'Chennai Mandi, Tamil Nadu'],
            'Sugarcane': ['Muzaffarnagar Mandi, UP', 'Kolhapur Mandi, Maharashtra', 'Coimbatore Mandi, Tamil Nadu'],
            'Maize': ['Davangere Mandi, Karnataka', 'Nizamabad Mandi, Telangana', 'Bharuch Mandi, Gujarat'],
            'Soybean': ['Indore Mandi, Madhya Pradesh', 'Latur Mandi, Maharashtra', 'Rajkot Mandi, Gujarat'],
            'Groundnut': ['Junagadh Mandi, Gujarat', 'Kurnool Mandi, Andhra Pradesh', 'Anantapur Mandi, Andhra Pradesh'],
            'Turmeric': ['Erode Mandi, Tamil Nadu', 'Sangli Mandi, Maharashtra', 'Nizamabad Mandi, Telangana'],
            'Chili': ['Guntur Mandi, Andhra Pradesh', 'Warangal Mandi, Telangana', 'Khammam Mandi, Telangana']
        }
        
        for i, crop in enumerate(crops_list[:10]):
            base_price = base_prices.get(crop, 2000)
            # Get specific market for this crop
            markets = market_locations.get(crop, ['Local Mandi, India'])
            selected_market = markets[i % len(markets)]  # Rotate through markets
            
            mock_prices.append({
                'crop': crop,
                'current_price': base_price,
                'min_price': int(base_price * 0.9),
                'max_price': int(base_price * 1.1),
                'market': selected_market,
                'state': selected_market.split(', ')[-1],
                'date': datetime.now().strftime('%Y-%m-%d'),
                'unit': 'per quintal',
                'trend': 'stable'
            })
        
        return {
            'prices': mock_prices,
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'source': 'Estimated Market Prices (Live data temporarily unavailable)'
        }
        
    except Exception as e:
        logger.error(f"Error fetching market prices: {str(e)}")
        return {
            'prices': [],
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'source': 'Market service error',
            'error': f'Market data service error: {str(e)}'
        }



def get_price_alerts(crops_list, user_preferences=None):
    """Get price alerts based on real market data"""
    try:
        alerts = []
        
        # Get current market data
        market_data = get_market_prices(crops_list)
        
        if market_data.get('error'):
            alerts.append({
                'type': 'service_error',
                'message': 'Market data service is currently unavailable. Please check back later.',
                'priority': 'medium'
            })
        
        return alerts
        
    except Exception as e:
        logger.error(f"Error generating price alerts: {str(e)}")
        return []
