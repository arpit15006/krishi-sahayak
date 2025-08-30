import os
import requests
import logging
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)

def get_current_location():
    """Get current location using IP geolocation with fallbacks"""
    services = [
        ('http://ip-api.com/json/', lambda d: {
            'latitude': d.get('lat'),
            'longitude': d.get('lon'), 
            'city': d.get('city'),
            'postal': d.get('zip'),
            'country': d.get('countryCode')
        }),
        ('http://ipinfo.io/json', lambda d: {
            'latitude': float(d.get('loc', ',').split(',')[0]) if ',' in d.get('loc', '') else None,
            'longitude': float(d.get('loc', ',').split(',')[1]) if ',' in d.get('loc', '') else None,
            'city': d.get('city'),
            'postal': d.get('postal'),
            'country': d.get('country')
        }),
        ('https://ipapi.co/json/', lambda d: {
            'latitude': d.get('latitude'),
            'longitude': d.get('longitude'),
            'city': d.get('city'),
            'postal': d.get('postal'),
            'country': d.get('country_code')
        })
    ]
    
    for url, parser in services:
        try:
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                data = response.json()
                location = parser(data)
                if location.get('latitude') and location.get('longitude'):
                    return location
        except:
            continue
    
    # Fallback to Delhi coordinates
    return {
        'latitude': 28.6139,
        'longitude': 77.2090,
        'city': 'Delhi',
        'postal': '110001',
        'country': 'IN'
    }

def get_weather_data(pin_code=None):
    """Get weather data with multiple API fallbacks"""
    if not pin_code:
        location_info = get_current_location()
        if location_info and location_info.get('postal'):
            pin_code = location_info['postal']
        else:
            pin_code = "110001"
    
    # Try OpenWeatherMap first for PIN code
    try:
        from services.openweather_service import get_weather_with_openweather
        
        # Always try to get weather using the same method as current location
        try:
            from services.free_weather_apis import get_weather_from_weatherapi
            
            # Convert PIN to coordinates (expanded mapping)
            pin_coords = {
                '110001': (28.6139, 77.2090, 'Delhi'),
                '400001': (19.0760, 72.8777, 'Mumbai'), 
                '560001': (12.9716, 77.5946, 'Bangalore'),
                '600001': (13.0827, 80.2707, 'Chennai'),
                '700001': (22.5726, 88.3639, 'Kolkata'),
                '500001': (17.3850, 78.4867, 'Hyderabad'),
                '411001': (18.5204, 73.8567, 'Pune'),
                '380001': (23.0225, 72.5714, 'Ahmedabad'),
                '497001': (21.2787, 81.8661, 'Raigarh'),
                '390001': (22.3072, 73.1812, 'Vadodara'),
                '390007': (22.3072, 73.1812, 'Vadodara'),
                '390019': (22.3072, 73.1812, 'Vadodara'),
                '391760': (22.2587, 73.0261, 'Waghodia')
            }
            
            if pin_code in pin_coords:
                lat, lon, city = pin_coords[pin_code]
                weather = get_weather_from_weatherapi(lat, lon, city, pin_code)
                if weather:
                    return weather
            
            # For unknown PIN codes, use a generic location but keep the PIN code
            weather = get_weather_from_weatherapi(22.3072, 73.1812, f'PIN {pin_code}', pin_code)
            if weather:
                # Override the city name to show the PIN code location
                weather['city'] = f'PIN {pin_code}'
                return weather
                
        except Exception as e:
            print(f"WeatherAPI failed for PIN {pin_code}: {e}")
    except:
        pass
    
    # Fallback to AccuWeather
    api_key = os.getenv('ACCUWEATHER_API_KEY', 'AF3FyPRmzWbmYMD9h7rSygKHufTh1GIu')
    
    try:
        # Get location key
        location_url = f"http://dataservice.accuweather.com/locations/v1/postalcodes/IN/search"
        location_params = {'apikey': api_key, 'q': pin_code}
        location_response = requests.get(location_url, params=location_params, timeout=10)
        location_data = location_response.json()
        
        if not location_data:
            return get_weather_error(pin_code)
        
        location_key = location_data[0]['Key']
        city_name = location_data[0]['LocalizedName']
        
        # Get current weather
        current_url = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}"
        current_params = {'apikey': api_key, 'details': 'true'}
        current_response = requests.get(current_url, params=current_params, timeout=10)
        
        if current_response.status_code != 200:
            return get_weather_error(pin_code)
            
        current_data = current_response.json()
        current = current_data[0] if current_data else {}
        
        # Try to get forecast (optional)
        forecast = []
        try:
            forecast_url = f"http://dataservice.accuweather.com/forecasts/v1/daily/3day/{location_key}"
            forecast_params = {'apikey': api_key, 'metric': 'true', 'details': 'true'}
            forecast_response = requests.get(forecast_url, params=forecast_params, timeout=10)
            
            if forecast_response.status_code == 200:
                forecast_data = forecast_response.json()
                if forecast_data and 'DailyForecasts' in forecast_data:
                    for day in forecast_data['DailyForecasts']:
                        forecast.append({
                            'date': datetime.fromisoformat(day['Date'].replace('Z', '+00:00')).strftime('%Y-%m-%d'),
                            'day_name': datetime.fromisoformat(day['Date'].replace('Z', '+00:00')).strftime('%A'),
                            'high_temp': day['Temperature']['Maximum']['Value'],
                            'low_temp': day['Temperature']['Minimum']['Value'],
                            'description': day['Day']['IconPhrase'],
                            'rain_probability': day['Day']['RainProbability'],
                            'wind_speed': day['Day']['Wind']['Speed']['Value']
                        })
        except Exception as e:
            logger.warning(f"Forecast unavailable: {str(e)}")
        
        return {
            'city': city_name,
            'pin_code': pin_code,
            'current': {
                'temperature': current.get('Temperature', {}).get('Metric', {}).get('Value', 25),
                'description': current.get('WeatherText', 'Clear'),
                'humidity': current.get('RelativeHumidity', 60),
                'wind_speed': current.get('Wind', {}).get('Speed', {}).get('Metric', {}).get('Value', 5),
                'pressure': current.get('Pressure', {}).get('Metric', {}).get('Value', 1013)
            },
            'forecast': forecast,
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
    except Exception as e:
        logger.error(f"Error fetching weather data: {str(e)}")
        return get_weather_error(pin_code)

def get_weather_by_coordinates(lat, lon):
    """Get weather data using GPS coordinates with WeatherAPI fallback"""
    try:
        # Use WeatherAPI.com for coordinates
        from services.free_weather_apis import get_weather_from_weatherapi
        weather = get_weather_from_weatherapi(lat, lon, "Current Location", "000000")
        if weather:
            return weather
    except Exception as e:
        logger.error(f"WeatherAPI coordinates failed: {str(e)}")
    
    # Fallback to simple weather
    try:
        from services.simple_weather import get_simple_weather
        return get_simple_weather(lat, lon, "Current Location", "000000")
    except Exception as e:
        logger.error(f"Error fetching weather data by coordinates: {str(e)}")
        return get_weather_error("000000")

def get_weather_by_current_location():
    """Get weather data using current IP location"""
    try:
        from services.openweather_service import get_weather_with_openweather
        
        location_info = get_current_location()
        if not location_info:
            return get_weather_error("000000")
        
        lat = location_info['latitude']
        lon = location_info['longitude']
        city = location_info.get('city', 'Unknown')
        postal = location_info.get('postal', '000000')
        
        if lat and lon:
            # Try WeatherAPI.com first (premium free service)
            from services.free_weather_apis import get_weather_from_weatherapi
            weather = get_weather_from_weatherapi(lat, lon, city, postal)
            if weather:
                return weather
            
            # Fallback to simple weather service
            from services.simple_weather import get_simple_weather
            weather = get_simple_weather(lat, lon, city, postal)
            if weather:
                return weather
            
            # Fallback to AccuWeather
            return get_weather_by_coordinates(lat, lon)
        elif postal:
            return get_weather_data(postal)
        else:
            return get_weather_error("000000")
                
    except Exception as e:
        logger.error(f"Error getting weather by current location: {str(e)}")
        return get_weather_error("000000")

def get_weather_error(pin_code="000000"):
    """Return error when weather API fails"""
    return {
        'city': 'Unknown Location',
        'pin_code': pin_code,
        'current': None,
        'forecast': [],
        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'error': 'Weather service unavailable. Please check your internet connection and try again.'
    }

def check_rain_forecast(weather_data):
    """Check if rain is expected in next 2-3 days"""
    if not weather_data or 'forecast' not in weather_data:
        return False, "Weather data unavailable"
    
    for day in weather_data['forecast'][:3]:
        if day['rain_probability'] > 60:
            return True, f"Heavy rain expected on {day['day_name']} ({day['rain_probability']}% chance)"
    
    return False, "No heavy rain expected"