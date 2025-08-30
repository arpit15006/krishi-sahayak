#!/bin/bash

echo "🌱 Krishi Sahayak - Quick Start"
echo "================================"

# Remove problematic venv
if [ -d "venv" ]; then
    echo "🗑️ Removing old virtual environment..."
    rm -rf venv
fi

# Create fresh venv
echo "📦 Creating fresh virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install minimal dependencies
echo "📦 Installing core packages..."
pip install --upgrade pip
pip install Flask==3.0.0 Flask-SQLAlchemy==3.1.1 Werkzeug==3.0.1
pip install Pillow requests gunicorn

# Install AI packages
echo "🤖 Installing AI packages..."
pip install --no-deps transformers
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Set environment variables
export FLASK_APP=app.py
export SESSION_SECRET="krishi-sahayak-secret-key-2024"
export DATABASE_URL="sqlite:///krishi_sahayak.db"

# Create directories
mkdir -p uploads static/uploads instance

# Initialize database
echo "🗄️ Initializing database..."
python3 -c "from app import app, db; app.app_context().push(); db.create_all()"

# Start app
echo "🚀 Starting Krishi Sahayak..."
python3 -c "
from app import app
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('', 0))
    port = s.getsockname()[1]

print(f'🌱 Krishi Sahayak: http://localhost:{port}')
app.run(host='0.0.0.0', port=port, debug=True)
"