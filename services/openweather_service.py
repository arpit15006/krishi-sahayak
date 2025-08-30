import requests
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def get_weather_with_openweather(lat, lon, city="Unknown"):
    """Get weather using OpenWeatherMap free API"""
    try:
        # Free OpenWeatherMap API key (demo key)
        api_key = "b6907d289e10d714a6e88b30761fae22"  # Free demo key
        
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
            
            # Forecast
            forecast_url = f"http://api.openweathermap.org/data/2.5/forecast"
            forecast_params = {
                'lat': lat,
                'lon': lon,
                'appid': api_key,
                'units': 'metric',
                'cnt': 24  # 3 days (8 forecasts per day)
            }
            
            forecast = []
            try:
                forecast_response = requests.get(forecast_url, params=forecast_params, timeout=10)
                if forecast_response.status_code == 200:
                    forecast_data = forecast_response.json()
                    
                    # Group by days and get daily summary
                    daily_data = {}
                    for item in forecast_data['list'][:24]:
                        date = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
                        day_name = datetime.fromtimestamp(item['dt']).strftime('%A')
                        
                        if date not in daily_data:
                            daily_data[date] = {
                                'date': date,
                                'day_name': day_name,
                                'temps': [],
                                'descriptions': [],
                                'rain_prob': 0,
                                'wind_speeds': []
                            }
                        
                        daily_data[date]['temps'].append(item['main']['temp'])
                        daily_data[date]['descriptions'].append(item['weather'][0]['description'])
                        daily_data[date]['wind_speeds'].append(item['wind']['speed'])
                        
                        # Rain probability (simplified)
                        if 'rain' in item:
                            daily_data[date]['rain_prob'] = max(daily_data[date]['rain_prob'], 70)
                        elif 'clouds' in item['weather'][0]['description'].lower():
                            daily_data[date]['rain_prob'] = max(daily_data[date]['rain_prob'], 30)
                    
                    # Convert to forecast format
                    for date, data in list(daily_data.items())[:3]:
                        forecast.append({
                            'date': date,
                            'day_name': data['day_name'],
                            'high_temp': int(max(data['temps'])),
                            'low_temp': int(min(data['temps'])),
                            'description': data['descriptions'][0].title(),
                            'rain_probability': data['rain_prob'],
                            'wind_speed': int(sum(data['wind_speeds']) / len(data['wind_speeds']))
                        })
            except:
                pass
            
            return {
                'city': current_data.get('name', city),
                'pin_code': '000000',
                'current': {
                    'temperature': round(current_data['main']['temp']),
                    'description': current_data['weather'][0]['description'].title(),
                    'humidity': current_data['main']['humidity'],
                    'wind_speed': round(current_data['wind']['speed'] * 3.6),  # Convert m/s to km/h
                    'pressure': current_data['main']['pressure']
                },
                'forecast': forecast,
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'source': 'OpenWeatherMap'
            }
        
    except Exception as e:
        logger.error(f"OpenWeather API error: {str(e)}")
    
    return None