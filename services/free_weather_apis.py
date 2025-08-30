import requests
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

def get_weather_from_weatherapi(lat, lon, city="Unknown", pin_code="000000"):
    """WeatherAPI.com - 1M free calls/month"""
    try:
        api_key = "f409459a878745ecacc62516252208"
        url = f"http://api.weatherapi.com/v1/forecast.json"
        params = {
            'key': api_key,
            'q': f"{lat},{lon}",
            'days': 3,
            'aqi': 'no',
            'alerts': 'no'
        }
        
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            current = data['current']
            location = data['location']
            
            forecast = []
            for day in data['forecast']['forecastday']:
                forecast.append({
                    'date': day['date'],
                    'day_name': datetime.strptime(day['date'], '%Y-%m-%d').strftime('%A'),
                    'high_temp': int(day['day']['maxtemp_c']),
                    'low_temp': int(day['day']['mintemp_c']),
                    'description': day['day']['condition']['text'],
                    'rain_probability': int(day['day']['daily_chance_of_rain']),
                    'wind_speed': int(day['day']['maxwind_kph'])
                })
            
            return {
                'city': location['name'],
                'pin_code': pin_code,
                'current': {
                    'temperature': int(current['temp_c']),
                    'description': current['condition']['text'],
                    'humidity': current['humidity'],
                    'wind_speed': int(current['wind_kph']),
                    'pressure': int(current['pressure_mb'])
                },
                'forecast': forecast,
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'source': 'WeatherAPI.com'
            }
    except Exception as e:
        logger.error(f"WeatherAPI error: {str(e)}")
    return None

def get_weather_from_openweather_free(lat, lon, city="Unknown", pin_code="000000"):
    """OpenWeatherMap - 1000 free calls/day"""
    try:
        # Sign up at openweathermap.org for free API key
        api_key = "YOUR_FREE_OPENWEATHER_KEY"  # Replace with actual key
        
        # Current weather
        current_url = f"http://api.openweathermap.org/data/2.5/weather"
        current_params = {
            'lat': lat,
            'lon': lon,
            'appid': api_key,
            'units': 'metric'
        }
        
        current_response = requests.get(current_url, params=current_params, timeout=10)
        if current_response.status_code == 200:
            current_data = current_response.json()
            
            # 5-day forecast
            forecast_url = f"http://api.openweathermap.org/data/2.5/forecast"
            forecast_params = {
                'lat': lat,
                'lon': lon,
                'appid': api_key,
                'units': 'metric'
            }
            
            forecast = []
            forecast_response = requests.get(forecast_url, params=forecast_params, timeout=10)
            if forecast_response.status_code == 200:
                forecast_data = forecast_response.json()
                
                # Group by days
                daily_data = {}
                for item in forecast_data['list'][:24]:  # 3 days
                    date = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
                    if date not in daily_data:
                        daily_data[date] = {
                            'temps': [],
                            'descriptions': [],
                            'wind_speeds': [],
                            'rain_prob': 0
                        }
                    
                    daily_data[date]['temps'].append(item['main']['temp'])
                    daily_data[date]['descriptions'].append(item['weather'][0]['description'])
                    daily_data[date]['wind_speeds'].append(item['wind']['speed'] * 3.6)
                    
                    if 'rain' in item:
                        daily_data[date]['rain_prob'] = 70
                
                for date, data in list(daily_data.items())[:3]:
                    forecast.append({
                        'date': date,
                        'day_name': datetime.strptime(date, '%Y-%m-%d').strftime('%A'),
                        'high_temp': int(max(data['temps'])),
                        'low_temp': int(min(data['temps'])),
                        'description': data['descriptions'][0].title(),
                        'rain_probability': data['rain_prob'],
                        'wind_speed': int(sum(data['wind_speeds']) / len(data['wind_speeds']))
                    })
            
            return {
                'city': current_data['name'],
                'pin_code': pin_code,
                'current': {
                    'temperature': int(current_data['main']['temp']),
                    'description': current_data['weather'][0]['description'].title(),
                    'humidity': current_data['main']['humidity'],
                    'wind_speed': int(current_data['wind']['speed'] * 3.6),
                    'pressure': current_data['main']['pressure']
                },
                'forecast': forecast,
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'source': 'OpenWeatherMap'
            }
    except Exception as e:
        logger.error(f"OpenWeatherMap error: {str(e)}")
    return None

def get_weather_from_visualcrossing(lat, lon, city="Unknown", pin_code="000000"):
    """Visual Crossing - 1000 free calls/day"""
    try:
        api_key = "YOUR_VISUAL_CROSSING_KEY"  # Get from visualcrossing.com
        url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{lat},{lon}"
        params = {
            'key': api_key,
            'unitGroup': 'metric',
            'include': 'days,current',
            'elements': 'temp,humidity,windspeed,pressure,conditions,precipprob'
        }
        
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            current = data['currentConditions']
            
            forecast = []
            for day in data['days'][:3]:
                forecast.append({
                    'date': day['datetime'],
                    'day_name': datetime.strptime(day['datetime'], '%Y-%m-%d').strftime('%A'),
                    'high_temp': int(day['tempmax']),
                    'low_temp': int(day['tempmin']),
                    'description': day['conditions'],
                    'rain_probability': int(day.get('precipprob', 0)),
                    'wind_speed': int(day['windspeed'])
                })
            
            return {
                'city': city,
                'pin_code': pin_code,
                'current': {
                    'temperature': int(current['temp']),
                    'description': current['conditions'],
                    'humidity': int(current['humidity']),
                    'wind_speed': int(current['windspeed']),
                    'pressure': int(current.get('pressure', 1013))
                },
                'forecast': forecast,
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'source': 'Visual Crossing'
            }
    except Exception as e:
        logger.error(f"Visual Crossing error: {str(e)}")
    return None