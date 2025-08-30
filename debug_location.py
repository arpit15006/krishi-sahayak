#!/usr/bin/env python3
"""Debug location weather issue"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.weather_service import get_current_location, get_weather_by_coordinates, get_weather_data

def debug_location_weather():
    print("🔍 Debugging Location Weather...")
    
    # Step 1: Get location
    location = get_current_location()
    if not location:
        print("❌ No location data")
        return
    
    print(f"📍 Location: {location}")
    
    # Step 2: Try coordinates
    if location['latitude'] and location['longitude']:
        print(f"🌐 Trying coordinates: {location['latitude']}, {location['longitude']}")
        weather = get_weather_by_coordinates(location['latitude'], location['longitude'])
        if weather and not weather.get('error'):
            print(f"✅ Weather by coordinates: {weather['current']['temperature']}°C")
            return weather
        else:
            print(f"❌ Weather by coordinates failed: {weather}")
    
    # Step 3: Try postal code
    if location.get('postal'):
        print(f"📮 Trying postal code: {location['postal']}")
        weather = get_weather_data(location['postal'])
        if weather and not weather.get('error'):
            print(f"✅ Weather by postal: {weather['current']['temperature']}°C")
            return weather
        else:
            print(f"❌ Weather by postal failed: {weather}")
    
    print("❌ All methods failed")
    return None

if __name__ == "__main__":
    debug_location_weather()