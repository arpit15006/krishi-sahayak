import os
import requests
import logging
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)

def get_current_location():
    """Get current location using IP geolocation"""
    try:
        # Use ipapi.co for free IP geolocation
        response = requests.get('https://ipapi.co/json/', timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                'latitude': data.get('latitude'),
                'longitude': data.get('longitude'),
                'city': data.get('city'),
                'postal': data.get('postal'),
                'country': data.get('country_code')
            }
    except Exception as e:
        logger.error(f"Error getting current location: {str(e)}")
    
    return None

def get_weather_by_current_location():
    """Get weather data using current IP location"""
    try:
        # Get current location
        location_info = get_current_location()
        if not location_info:
            logger.warning("Could not determine current location")
            return get_fallback_weather_data("000000")
        
        lat = location_info['latitude']
        lon = location_info['longitude']
        postal = location_info.get('postal')
        
        logger.info(f"Current location: {location_info['city']}, {postal} ({lat}, {lon})")
        
        if lat and lon:
            return get_weather_by_coordinates(lat, lon)
        elif postal:
            return get_weather_data(postal)
        else:
            return get_fallback_weather_data("000000")
                
    except Exception as e:
        logger.error(f"Error getting weather by current location: {str(e)}")
        return get_fallback_weather_data("000000")

def get_weather_data(pin_code=None):
    """Get weather data from AccuWeather API"""
    api_key = os.getenv('ACCUWEATHER_API_KEY', 'dM1leSojtDVmCX2hn97fMdqVVxh5r5OI')
    
    # If no PIN code provided, try to get current location
    if not pin_code:
        location_info = get_current_location()
        if location_info and location_info.get('postal'):
            pin_code = location_info['postal']
            logger.info(f"Using current location PIN: {pin_code}")
        else:
            pin_code = "110001"  # Default to Delhi
            logger.info("Using default location: Delhi")
    
    # If no API key is available, use fallback data immediately
    if not api_key:
        logger.info("No AccuWeather API key found, using fallback weather data")
        return get_fallback_weather_data(pin_code)
    
    try:
        # First, get location key from PIN code
        location_url = f"http://dataservice.accuweather.com/locations/v1/postalcodes/IN/search"
        location_params = {
            'apikey': api_key,
            'q': pin_code
        }
        
        location_response = requests.get(location_url, params=location_params, timeout=10)
        location_data = location_response.json()
        
        if not location_data:
            logger.warning(f"No location found for PIN code: {pin_code}")
            return get_fallback_weather_data()
        
        location_key = location_data[0]['Key']
        city_name = location_data[0]['LocalizedName']
        
        # Get current weather
        current_url = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}"
        current_params = {
            'apikey': api_key,
            'details': 'true'
        }
        
        current_response = requests.get(current_url, params=current_params, timeout=10)
        current_data = current_response.json()
        
        # Get 3-day forecast
        forecast_url = f"http://dataservice.accuweather.com/forecasts/v1/daily/3day/{location_key}"
        forecast_params = {
            'apikey': api_key,
            'metric': 'true',
            'details': 'true'
        }
        
        forecast_response = requests.get(forecast_url, params=forecast_params, timeout=10)
        
        # Check if forecast API call failed
        if forecast_response.status_code != 200:
            logger.warning(f"Forecast API failed with status {forecast_response.status_code}")
            return get_fallback_weather_data(pin_code)
            
        forecast_data = forecast_response.json()
        
        # Process current weather
        current = current_data[0] if current_data else {}
        
        # Process forecast
        forecast = []
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
        return get_fallback_weather_data(pin_code)

def get_fallback_weather_data(pin_code="000000"):
    """Fallback weather data when API fails"""
    today = datetime.now()
    
    return {
        'city': 'Your Location',
        'pin_code': pin_code,
        'current': {
            'temperature': 28,
            'description': 'Partly Cloudy',
            'humidity': 65,
            'wind_speed': 8,
            'pressure': 1015
        },
        'forecast': [
            {
                'date': (today + timedelta(days=i)).strftime('%Y-%m-%d'),
                'day_name': (today + timedelta(days=i)).strftime('%A'),
                'high_temp': 32 - i,
                'low_temp': 22 - i,
                'description': ['Sunny', 'Partly Cloudy', 'Light Rain'][i],
                'rain_probability': [10, 30, 70][i],
                'wind_speed': 8 + i
            } for i in range(3)
        ],
        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'error': 'Weather service temporarily unavailable'
    }

def get_weather_by_coordinates(lat, lon):
    """Get weather data using GPS coordinates"""
    api_key = os.getenv('ACCUWEATHER_API_KEY', 'dM1leSojtDVmCX2hn97fMdqVVxh5r5OI')
    
    # If no API key is available, use fallback data immediately
    if not api_key:
        logger.info("No AccuWeather API key found, using fallback weather data")
        return get_fallback_weather_data("000000")
    
    try:
        # Get location key from coordinates
        location_url = f"http://dataservice.accuweather.com/locations/v1/cities/geoposition/search"
        location_params = {
            'apikey': api_key,
            'q': f"{lat},{lon}"
        }
        
        location_response = requests.get(location_url, params=location_params, timeout=10)
        
        if location_response.status_code != 200:
            logger.warning(f"Location API failed with status {location_response.status_code}")
            return get_fallback_weather_data("000000")
            
        location_data = location_response.json()
        
        location_key = location_data['Key']
        city_name = location_data['LocalizedName']
        postal_code = location_data.get('PostalCode', '000000')
        
        # Get current weather
        current_url = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}"
        current_params = {
            'apikey': api_key,
            'details': 'true'
        }
        
        current_response = requests.get(current_url, params=current_params, timeout=10)
        current_data = current_response.json()
        
        # Get 3-day forecast
        forecast_url = f"http://dataservice.accuweather.com/forecasts/v1/daily/3day/{location_key}"
        forecast_params = {
            'apikey': api_key,
            'metric': 'true',
            'details': 'true'
        }
        
        forecast_response = requests.get(forecast_url, params=forecast_params, timeout=10)
        
        # Check if forecast API call failed
        if forecast_response.status_code != 200:
            logger.warning(f"Forecast API failed with status {forecast_response.status_code}")
            return get_fallback_weather_data(postal_code)
            
        forecast_data = forecast_response.json()
        
        # Process current weather
        current = current_data[0] if current_data else {}
        
        # Process forecast
        forecast = []
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
        
        return {
            'city': city_name,
            'pin_code': postal_code,
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
        logger.error(f"Error fetching weather data by coordinates: {str(e)}")
        return get_fallback_weather_data("000000")

def check_rain_forecast(weather_data):
    """Check if rain is expected in next 2-3 days"""
    if not weather_data or 'forecast' not in weather_data:
        return False, "Weather data unavailable"
    
    for day in weather_data['forecast'][:3]:
        if day['rain_probability'] > 60:
            return True, f"Heavy rain expected on {day['day_name']} ({day['rain_probability']}% chance)"
    
    return False, "No heavy rain expected"
