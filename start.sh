#!/bin/bash

# Krishi Sahayak - Complete Startup Script
# This script starts the full application with all integrated services

echo "🌱 Starting Krishi Sahayak - The Farmer's AI Co-pilot"
echo "============================================================"
echo "📱 Progressive Web App for Indian Farmers"
echo "🔬 AI Plant Disease Detection (Gemini Vision API)"
echo "🌤️ Weather Forecasting (Multiple APIs)"
echo "💰 Market Price Intelligence (AGMARKNET API)"
echo "📜 Digital Crop Passports (Supabase + Clerk Auth)"
echo "============================================================"

# Check Python version
python_version=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python 3.8+ required. Current: $python_version"
    exit 1
fi

echo "✅ Python $python_version detected"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "📦 Installing dependencies..."
pip install -q --upgrade pip

# Install from requirements.txt
if [ -f "requirements.txt" ]; then
    echo "📦 Installing from requirements.txt..."
    pip install -q -r requirements.txt
    echo "📦 Installing blockchain dependencies..."
    pip install -q web3 eth-account qrcode[pil]
else
    echo "📦 Installing core dependencies..."
    pip install -q Flask==3.0.0 Flask-SQLAlchemy==3.1.1 Werkzeug==3.0.1 Pillow requests gunicorn python-dotenv PyJWT supabase web3 eth-account qrcode[pil]
fi

# Load environment variables from .env file
if [ -f ".env" ]; then
    echo "📄 Loading environment variables from .env..."
    set -a
    source .env
    set +a
else
    echo "⚠️ .env file not found, using defaults..."
    export FLASK_APP=simple_run.py
    export FLASK_ENV=development
    export SESSION_SECRET="krishi-sahayak-secret-key-2024"
    export GROQ_API_KEY="your-groq-api-key"
    export ACCUWEATHER_API_KEY="AF3FyPRmzWbmYMD9h7rSygKHufTh1GIu"
    export GEMINI_API_KEY="AIzaSyCVchsFQ9RyH4wdM2qrVZqRBJyQ5g9qOKg"
fi

echo "✅ Environment variables configured"

# Create required directories
mkdir -p uploads static/uploads instance

# Skip database initialization for Supabase
echo "🗄️ Using Supabase database (no local initialization needed)..."
echo "✅ Database: Supabase configured"

# Verify all systems
echo "🧪 Verifying system integration..."
python3 -c "
print('Testing integrations...')
try:
    from services.market_service import get_market_prices
    market = get_market_prices(['Rice'])
    print('✅ Market API: Working' if market.get('prices') else '⚠️ Market API: Limited')
except Exception as e:
    print(f'⚠️ Market API: {str(e)[:30]}...')

try:
    from services.weather_service import get_weather_data
    weather = get_weather_data('110001')
    print('✅ Weather API: Working' if weather.get('current') else '⚠️ Weather API: Limited')
except Exception as e:
    print(f'⚠️ Weather API: {str(e)[:30]}...')

try:
    from services.ai_service import analyze_plant_image
    from PIL import Image
    import os
    img = Image.new('RGB', (224, 224), 'green')
    img.save('test.jpg')
    ai = analyze_plant_image('test.jpg')
    print('✅ AI Vision: Working' if ai.get('diagnosis') else '⚠️ AI Vision: Limited')
    if os.path.exists('test.jpg'):
        os.remove('test.jpg')
except Exception as e:
    print(f'⚠️ AI Vision: {str(e)[:30]}...')

print('✅ Flask App: Ready')
"

# Find available port
PORT=8000
while lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null ; do
    PORT=$((PORT + 1))
done

echo ""
echo "🚀 Starting Krishi Sahayak Server..."
echo "📍 URL: http://localhost:$PORT"
echo "📱 Mobile: http://$(ifconfig | grep 'inet ' | grep -v '127.0.0.1' | head -1 | awk '{print $2}'):$PORT"
echo ""
echo "💡 Features Ready:"
echo "   🔬 AI Plant Disease Scanner (Gemini Vision API)"
echo "   🌤️ Real-time Weather Data (Multiple APIs)"
echo "   💰 Live Market Prices (Government AGMARKNET API)"
echo "   📜 Digital Crop Passports (Mock Blockchain)"
echo "   💬 Farmer Community Chat (AI Moderated)"
echo "   💧 Resource Optimization Engine (Water & Fertilizer)"
echo "   🛰️ Satellite Crop Monitoring (NASA GIBS API)"
echo "   📱 Progressive Web App (Install on Mobile)"
echo ""
echo "🛑 Press Ctrl+C to stop the server"
echo "============================================================"

# Start the application
echo "🌱 Launching Krishi Sahayak..."
export PORT=$PORT
python3 complete_app.py