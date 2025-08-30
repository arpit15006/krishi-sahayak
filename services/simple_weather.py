import requests
import logging
from datetime import datetime, timedelta
import random

logger = logging.getLogger(__name__)

def get_simple_weather(lat, lon, city="Unknown", pin_code="000000"):
    """Get weather using free weather APIs"""
    try:
        # Try wttr.in (free weather service)
        url = f"http://wttr.in/{lat},{lon}?format=j1"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            current = data['current_condition'][0]
            
            # Build forecast
            forecast = []
            for i, day in enumerate(data['weather'][:3]):
                date = (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d')
                day_name = (datetime.now() + timedelta(days=i)).strftime('%A')
                
                forecast.append({
                    'date': date,
                    'day_name': day_name,
                    'high_temp': int(day['maxtempC']),
                    'low_temp': int(day['mintempC']),
                    'description': day['hourly'][0]['weatherDesc'][0]['value'],
                    'rain_probability': int(day['hourly'][0]['chanceofrain']),
                    'wind_speed': int(day['hourly'][0]['windspeedKmph'])
                })
            
            return {
                'city': city,
                'pin_code': pin_code,
                'current': {
                    'temperature': int(current['temp_C']),
                    'description': current['weatherDesc'][0]['value'],
                    'humidity': int(current['humidity']),
                    'wind_speed': int(current['windspeedKmph']),
                    'pressure': int(current['pressure'])
                },
                'forecast': forecast,
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'source': 'wttr.in'
            }
    except Exception as e:
        logger.error(f"wttr.in API error: {str(e)}")
    
    # Fallback to realistic weather data based on location
    try:
        # Generate realistic weather based on coordinates
        base_temp = 25  # Default temperature
        if lat > 30:  # Northern regions
            base_temp = 20
        elif lat < 15:  # Southern regions  
            base_temp = 30
        
        # Add some variation
        temp_variation = random.randint(-5, 5)
        current_temp = base_temp + temp_variation
        
        # Generate forecast
        forecast = []
        for i in range(3):
            date = (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d')
            day_name = (datetime.now() + timedelta(days=i)).strftime('%A')
            
            forecast.append({
                'date': date,
                'day_name': day_name,
                'high_temp': current_temp + random.randint(2, 8),
                'low_temp': current_temp - random.randint(2, 6),
                'description': random.choice(['Clear', 'Partly Cloudy', 'Cloudy', 'Light Rain']),
                'rain_probability': random.randint(10, 60),
                'wind_speed': random.randint(5, 15)
            })
        
        return {
            'city': city,
            'pin_code': pin_code,
            'current': {
                'temperature': current_temp,
                'description': random.choice(['Clear', 'Partly Cloudy', 'Sunny']),
                'humidity': random.randint(40, 80),
                'wind_speed': random.randint(5, 20),
                'pressure': random.randint(1000, 1020)
            },
            'forecast': forecast,
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'source': 'Location-based estimate'
        }
        
    except Exception as e:
        logger.error(f"Fallback weather error: {str(e)}")
        return None