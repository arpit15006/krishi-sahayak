#!/usr/bin/env python3
import os
import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.utils import secure_filename
from PIL import Image
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "krishi-sahayak-secret-key")
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Import services
from services.weather_service import get_weather_data, get_weather_by_coordinates, get_weather_by_current_location
from services.ai_service import analyze_plant_image
from services.market_service import get_market_prices

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Mock user data for demo
demo_user = {
    'id': 1,
    'phone_number': '9999999999',
    'full_name': 'Demo Farmer',
    'village_city': 'Demo Village',
    'pin_code': '110001',
    'main_crops': ['Rice', 'Wheat', 'Sugarcane']
}

@app.route('/')
def index():
    session['user_id'] = demo_user['id']
    session['phone_number'] = demo_user['phone_number']
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    weather_data = get_weather_by_current_location()
    if weather_data.get('error'):
        weather_data = get_weather_data(demo_user['pin_code'])
    
    all_crops = demo_user['main_crops'] + ['Cotton', 'Maize', 'Onion', 'Potato', 'Tomato']
    unique_crops = list(dict.fromkeys(all_crops))
    market_data = get_market_prices(unique_crops[:10])
    
    return render_template('dashboard.html', user=demo_user, weather=weather_data, market_data=market_data)

@app.route('/scanner', methods=['GET', 'POST'])
def scanner():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        if 'plant_image' not in request.files:
            flash('No image selected', 'error')
            return render_template('scanner.html')
        
        file = request.files['plant_image']
        if file.filename == '' or not allowed_file(file.filename):
            flash('Please upload a valid image', 'error')
            return render_template('scanner.html')
        
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            with Image.open(filepath) as img:
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                max_size = (1024, 1024)
                img.thumbnail(max_size, Image.LANCZOS)
                img.save(filepath, 'JPEG', quality=85)
            
            weather_data = get_weather_data(demo_user['pin_code'])
            analysis_result = analyze_plant_image(filepath, weather_data)
            
            # Store result in session for demo
            session['last_scan'] = {
                'filename': filename,
                'diagnosis': analysis_result['diagnosis'],
                'treatment': analysis_result['treatment'],
                'weather_warning': analysis_result.get('weather_warning')
            }
            
            return redirect(url_for('results'))
            
        except Exception as e:
            app.logger.error(f"Error processing image: {str(e)}")
            flash('Error processing image. Please try again.', 'error')
    
    return render_template('scanner.html')

@app.route('/results')
def results():
    if 'user_id' not in session or 'last_scan' not in session:
        return redirect(url_for('scanner'))
    
    result = session['last_scan']
    return render_template('results.html', result=result)

@app.route('/weather')
def weather():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    pin_code = request.args.get('pin')
    
    if lat and lon:
        weather_data = get_weather_by_coordinates(float(lat), float(lon))
    elif pin_code:
        weather_data = get_weather_data(pin_code)
    else:
        weather_data = get_weather_by_current_location()
        if weather_data.get('error'):
            weather_data = get_weather_data(demo_user['pin_code'])
    
    return render_template('weather.html', weather=weather_data, user=demo_user)

@app.route('/market')
def market():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    all_crops = demo_user['main_crops'] + ['Cotton', 'Maize', 'Onion', 'Potato', 'Tomato', 'Soybean']
    unique_crops = list(dict.fromkeys(all_crops))
    market_data = get_market_prices(unique_crops[:10])
    
    return render_template('market.html', market_data=market_data, user_crops=demo_user['main_crops'])

@app.route('/passport')
def passport():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    return render_template('passport.html', user_crops=demo_user['main_crops'], passports=[])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)