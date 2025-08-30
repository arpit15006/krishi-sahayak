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

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login')
def login():
    clerk_publishable_key = os.environ.get('CLERK_PUBLISHABLE_KEY')
    return render_template('clerk_auth.html', clerk_publishable_key=clerk_publishable_key)

@app.route('/simple-login', methods=['GET', 'POST'])
def simple_login():
    if request.method == 'POST':
        phone_number = request.form.get('phone_number')
        
        if not phone_number:
            flash('Phone number is required', 'error')
            return render_template('simple_login.html')
        
        try:
            from supabase_models.farmer import Farmer
            farmer = Farmer.get_by_phone(phone_number)
            
            if farmer:
                session['user_id'] = farmer.id
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                # New user, redirect to profile setup
                session['temp_phone'] = phone_number
                flash('Please complete your profile setup', 'info')
                return redirect(url_for('profile'))
                
        except Exception as e:
            print(f"Login error: {e}")
            flash('Login failed. Please try again.', 'error')
    
    return render_template('simple_login.html')

@app.route('/auth/session', methods=['POST'])
def create_session():
    data = request.get_json()
    clerk_user_id = data.get('clerk_user_id')
    
    if clerk_user_id:
        try:
            from supabase_models.farmer import Farmer
            farmer = Farmer.get_by_clerk_id(clerk_user_id)
            
            if farmer:
                session['user_id'] = farmer.id
                session['clerk_user_id'] = clerk_user_id
                return jsonify({'redirect': '/dashboard'})
            else:
                session['clerk_user_id'] = clerk_user_id
                session['clerk_email'] = data.get('email')
                session['clerk_phone'] = data.get('phone')
                return jsonify({'redirect': '/profile'})
                
        except Exception as e:
            print(f"Session creation error: {e}")
            return jsonify({'error': 'Session creation failed'}), 500
    
    return jsonify({'error': 'Invalid request'}), 400

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'clerk_user_id' not in session and 'temp_phone' not in session and 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        from supabase_models.farmer import Farmer
        
        farmer_data = {
            'clerk_user_id': session.get('clerk_user_id'),
            'name': request.form.get('full_name'),
            'phone': session.get('clerk_phone') or session.get('temp_phone') or request.form.get('phone_number'),
            'email': session.get('clerk_email') or request.form.get('email', ''),
            'place': request.form.get('village_city'),
            'district': request.form.get('district', ''),
            'state': request.form.get('state', ''),
            'pincode': request.form.get('pin_code'),
            'farm_size_acres': float(request.form.get('farm_size_acres', 1)),
            'farming_experience_years': int(request.form.get('farming_experience_years', 5)),
            'preferred_language': request.form.get('preferred_language', 'hi')
        }
        
        try:
            farmer = Farmer.create(farmer_data)
            if farmer:
                session['user_id'] = farmer.id
                session.pop('temp_phone', None)
                session.pop('clerk_user_id', None)
                session.pop('clerk_email', None)
                session.pop('clerk_phone', None)
                
                # Add crops
                main_crops = request.form.getlist('main_crops')
                if main_crops:
                    from supabase_models.crop import Crop
                    for crop_name in main_crops:
                        Crop.create({
                            'farmer_id': farmer.id,
                            'crop_name': crop_name,
                            'season': 'Current'
                        })
                
                flash('Profile created successfully!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Error creating profile. Please try again.', 'error')
        except Exception as e:
            print(f"Profile creation error: {e}")
            flash('Error creating profile. Please try again.', 'error')
    
    crops_list = ['Rice', 'Wheat', 'Sugarcane', 'Cotton', 'Jute', 'Maize', 'Barley', 'Bajra', 'Jowar', 'Ragi', 'Potato', 'Onion', 'Tomato', 'Brinjal', 'Cabbage', 'Cauliflower', 'Okra', 'Chili', 'Turmeric', 'Ginger', 'Garlic', 'Coriander', 'Cumin', 'Mustard', 'Groundnut', 'Sesame', 'Sunflower', 'Soybean', 'Black gram', 'Green gram', 'Chickpea', 'Pigeon pea', 'Banana', 'Mango', 'Papaya', 'Guava', 'Coconut']
    return render_template('profile.html', crops_list=crops_list)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        from supabase_models.farmer import Farmer
        farmer = Farmer.get_by_id(session['user_id'])
        if not farmer:
            return redirect(url_for('profile'))
        
        weather_data = get_weather_by_current_location()
        if weather_data.get('error'):
            weather_data = get_weather_data(farmer.pincode)
        
        crops = farmer.get_crops()
        crop_names = [crop['crop_name'] for crop in crops] if crops else ['Rice', 'Wheat']
        all_crops = crop_names + ['Cotton', 'Maize', 'Onion', 'Potato', 'Tomato']
        unique_crops = list(dict.fromkeys(all_crops))
        market_data = get_market_prices(unique_crops[:10])
        
        return render_template('dashboard.html', user=farmer, weather=weather_data, market_data=market_data)
        
    except Exception as e:
        print(f"Dashboard error: {e}")
        flash('Error loading dashboard. Please try again.', 'error')
        return redirect(url_for('login'))

@app.route('/scanner', methods=['GET', 'POST'])
def scanner():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
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
            
            from supabase_models.farmer import Farmer
            farmer = Farmer.get_by_id(session['user_id'])
            weather_data = get_weather_data(farmer.pincode if farmer else '110001')
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
        return redirect(url_for('login'))
    
    try:
        from supabase_models.farmer import Farmer
        farmer = Farmer.get_by_id(session['user_id'])
        
        lat = request.args.get('lat')
        lon = request.args.get('lon')
        pin_code = request.args.get('pin')
        
        if lat and lon:
            weather_data = get_weather_by_coordinates(float(lat), float(lon))
        elif pin_code:
            weather_data = get_weather_data(pin_code)
        else:
            weather_data = get_weather_by_current_location()
            if weather_data.get('error') and farmer:
                weather_data = get_weather_data(farmer.pincode)
        
        return render_template('weather.html', weather=weather_data, user=farmer)
    except Exception as e:
        print(f"Weather error: {e}")
        return render_template('weather.html', weather={'error': 'Weather data unavailable'}, user=None)

@app.route('/market')
def market():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        from supabase_models.farmer import Farmer
        farmer = Farmer.get_by_id(session['user_id'])
        
        crops = farmer.get_crops() if farmer else []
        crop_names = [crop['crop_name'] for crop in crops] if crops else ['Rice', 'Wheat']
        all_crops = crop_names + ['Cotton', 'Maize', 'Onion', 'Potato', 'Tomato', 'Soybean']
        unique_crops = list(dict.fromkeys(all_crops))
        market_data = get_market_prices(unique_crops[:10])
        
        return render_template('market.html', market_data=market_data, user_crops=crop_names)
    except Exception as e:
        print(f"Market error: {e}")
        return render_template('market.html', market_data={'error': 'Market data unavailable'}, user_crops=[])

@app.route('/passport')
def passport():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        from supabase_models.farmer import Farmer
        farmer = Farmer.get_by_id(session['user_id'])
        crops = farmer.get_crops() if farmer else []
        crop_names = [crop['crop_name'] for crop in crops]
        
        return render_template('passport.html', user_crops=crop_names, passports=[])
    except Exception as e:
        print(f"Passport error: {e}")
        return render_template('passport.html', user_crops=[], passports=[])

@app.route('/api/voice-query', methods=['POST'])
def voice_query():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        language = data.get('language', 'hi-IN')
        
        if not query:
            return jsonify({'success': False, 'error': 'No query provided'})
        
        # Get user context
        from supabase_models.farmer import Farmer
        farmer = Farmer.get_by_id(session['user_id'])
        
        if farmer:
            crops = farmer.get_crops()
            user_crops = [crop['crop_name'] for crop in crops] if crops else ['Rice', 'Wheat']
            pin_code = farmer.pincode
        else:
            user_crops = ['Rice', 'Wheat']
            pin_code = '110001'
        
        # Process voice query with AI
        from services.ai_service import process_voice_query
        response = process_voice_query(query, language, user_crops, pin_code)
        
        return jsonify({
            'success': True,
            'response': response,
            'language': language
        })
        
    except Exception as e:
        app.logger.error(f"Voice query error: {str(e)}")
        return jsonify({
            'success': False, 
            'error': 'माफ करें, कुछ तकनीकी समस्या है।' if language == 'hi-IN' else 'Sorry, there was a technical issue.'
        }), 500

@app.route('/weather_shield')
def weather_shield():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('weather_shield.html')

@app.route('/yield_prediction')
def yield_prediction():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('yield_prediction.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)