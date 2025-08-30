#!/usr/bin/env python3
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = "krishi-sahayak-demo-key"
app.config['UPLOAD_FOLDER'] = 'uploads'

from services.weather_service import get_weather_data
from services.ai_service import analyze_plant_image
from services.market_service import get_market_prices

demo_user = {
    'id': 1,
    'full_name': 'Demo Farmer',
    'village_city': 'Demo Village', 
    'pin_code': '110001',
    'main_crops': ['Rice', 'Wheat']
}

@app.route('/')
def index():
    session['user_id'] = 1
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    weather_data = get_weather_data('110001')
    market_data = get_market_prices(['Rice', 'Wheat', 'Cotton'])
    return render_template('dashboard.html', user=demo_user, weather=weather_data, market_data=market_data)

@app.route('/scanner', methods=['GET', 'POST'])
def scanner():
    if request.method == 'POST':
        file = request.files.get('plant_image')
        if file and file.filename:
            os.makedirs('uploads', exist_ok=True)
            filename = secure_filename(file.filename)
            filepath = os.path.join('uploads', filename)
            file.save(filepath)
            
            try:
                analysis = analyze_plant_image(filepath)
                session['scan_result'] = analysis
                return redirect(url_for('results'))
            except Exception as e:
                flash(f'Analysis error: {str(e)}', 'error')
    
    return render_template('scanner.html')

@app.route('/results')
def results():
    result = session.get('scan_result', {'diagnosis': 'No scan found', 'treatment': 'Please scan a plant image first'})
    return render_template('results.html', result=result)

@app.route('/weather')
def weather():
    weather_data = get_weather_data('110001')
    return render_template('weather.html', weather=weather_data, user=demo_user)

@app.route('/market')
def market():
    market_data = get_market_prices(['Rice', 'Wheat', 'Cotton', 'Onion', 'Potato'])
    return render_template('market.html', market_data=market_data, user_crops=['Rice', 'Wheat'])

@app.route('/passport')
def passport():
    return render_template('passport.html', user_crops=['Rice', 'Wheat'], passports=[])

if __name__ == '__main__':
    print("🌱 Krishi Sahayak starting on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)