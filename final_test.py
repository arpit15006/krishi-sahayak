#!/usr/bin/env python3
"""Final comprehensive test"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_groq():
    from services.ai_service import analyze_plant_image
    print("🤖 Testing Groq API...")
    
    # Create a dummy image file for testing
    with open('test_image.jpg', 'w') as f:
        f.write('dummy')
    
    try:
        result = analyze_plant_image('test_image.jpg')
        if result and 'diagnosis' in result:
            print("✅ Groq API working")
            return True
        else:
            print("❌ Groq API failed")
            return False
    except Exception as e:
        print(f"❌ Groq error: {str(e)}")
        return False
    finally:
        if os.path.exists('test_image.jpg'):
            os.remove('test_image.jpg')

def test_weather():
    from services.weather_service import get_weather_data
    print("🌤️ Testing AccuWeather API...")
    
    try:
        weather = get_weather_data("110001")  # Delhi
        if weather and weather.get('current'):
            temp = weather['current']['temperature']
            city = weather['city']
            print(f"✅ Weather working: {temp}°C in {city}")
            return True
        else:
            print("❌ Weather failed")
            return False
    except Exception as e:
        print(f"❌ Weather error: {str(e)}")
        return False

def test_app():
    print("🌱 Testing Flask App...")
    try:
        from app import app
        with app.test_client() as client:
            response = client.get('/')
            if response.status_code in [200, 302]:  # 302 for redirect
                print("✅ Flask app working")
                return True
            else:
                print(f"❌ Flask app failed: {response.status_code}")
                return False
    except Exception as e:
        print(f"❌ Flask error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧪 Final Krishi Sahayak Test\n")
    
    results = []
    results.append(test_groq())
    print()
    results.append(test_weather())
    print()
    results.append(test_app())
    
    print(f"\n📊 Final Results: {sum(results)}/{len(results)} tests passed")
    
    if all(results):
        print("🎉 Krishi Sahayak is fully functional!")
        print("🚀 Run: python3 run.py")
    else:
        print("⚠️ Some issues detected")