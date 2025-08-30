#!/bin/bash

# Krishi Sahayak - Complete Application Startup Script
echo "🌱 Starting Krishi Sahayak - The Farmer's AI Co-pilot"
echo "=================================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11 or higher."
    exit 1
fi

# Check if pip is installed
if ! command -v pip &> /dev/null; then
    echo "❌ pip is not installed. Please install pip."
    exit 1
fi

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
else
    echo "⚠️  requirements.txt not found. Installing essential packages..."
    pip install flask python-dotenv requests pillow groq supabase qrcode[pil] web3 eth-account python-dateutil
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating template..."
    cat > .env << EOF
# Krishi Sahayak Environment Variables
SESSION_SECRET="krishi-sahayak-secret-key-change-this"
GROQ_API_KEY="your-groq-api-key-here"
ACCUWEATHER_API_KEY="your-accuweather-api-key-here"
CLERK_PUBLISHABLE_KEY="your-clerk-publishable-key-here"
SUPABASE_URL="your-supabase-url-here"
SUPABASE_KEY="your-supabase-anon-key-here"
PINATA_API_KEY="your-pinata-api-key-here"
PINATA_SECRET_KEY="your-pinata-secret-key-here"
MONAD_PRIVATE_KEY="your-monad-private-key-here"
EOF
    echo "📝 Please update .env file with your API keys before running the application."
fi

# Create uploads directory if it doesn't exist
mkdir -p uploads

# Check if complete_app.py exists
if [ ! -f "complete_app.py" ]; then
    echo "❌ complete_app.py not found. Please ensure you're in the correct directory."
    exit 1
fi

# Kill any existing processes on ports 8000, 8001, 5000
echo "🔄 Stopping any existing servers..."
lsof -ti:8000,8001,5000 | xargs kill -9 2>/dev/null || true

# Start the application
echo "🚀 Starting Krishi Sahayak on http://localhost:8000"
echo "📱 For mobile testing, use your local IP address"
echo "🎯 Press Ctrl+C to stop the server"
echo ""

# Export environment variables and start Flask app
export FLASK_APP=complete_app.py
export FLASK_ENV=development
export FLASK_DEBUG=1

# Start the application with proper host and port
python3 complete_app.py

echo ""
echo "👋 Krishi Sahayak server stopped. Thank you for using our platform!"