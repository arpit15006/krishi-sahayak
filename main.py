#!/usr/bin/env python3
import os
import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, current_app, Blueprint
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "krishi-sahayak-secret-key")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///krishi_sahayak.db")
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

db = SQLAlchemy(app)

# Models
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    village_city = db.Column(db.String(100), nullable=False)
    pin_code = db.Column(db.String(6), nullable=False)
    main_crops = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_verified = db.Column(db.Boolean, default=False)

class ScanResult(db.Model):
    __tablename__ = 'scan_results'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    image_filename = db.Column(db.String(255), nullable=False)
    diagnosis = db.Column(db.Text, nullable=False)
    treatment_advice = db.Column(db.Text, nullable=False)
    weather_warning = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class DigitalPassport(db.Model):
    __tablename__ = 'digital_passports'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    crop_type = db.Column(db.String(100), nullable=False)
    season = db.Column(db.String(50), nullable=False)
    nft_token_id = db.Column(db.String(100))
    ipfs_hash = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Services
from services.weather_service import get_weather_data, get_weather_by_coordinates, get_weather_by_current_location
from services.ai_service import analyze_plant_image
from services.market_service import get_market_prices

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Routes
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

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
        # Fallback to legacy user system if Supabase fails
        user = User.query.get(session['user_id'])
        if not user:
            return redirect(url_for('login'))
        
        weather_data = get_weather_by_current_location()
        if weather_data.get('error'):
            weather_data = get_weather_data(user.pin_code)
        
        user_crops = json.loads(user.main_crops)
        all_crops = user_crops + ['Cotton', 'Maize', 'Onion', 'Potato', 'Tomato']
        unique_crops = list(dict.fromkeys(all_crops))
        market_data = get_market_prices(unique_crops[:10])
        
        return render_template('dashboard.html', user=user, weather=weather_data, market_data=market_data)

@app.route('/scanner', methods=['GET', 'POST'])
def scanner():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        if 'plant_image' not in request.files:
            flash('No image selected', 'error')
            return render_template('scanner.html')
        
        file = request.files['plant_image']
        if file.filename == '':
            flash('No image selected', 'error')
            return render_template('scanner.html')
        
        if file and allowed_file(file.filename):
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
                
                user = User.query.get(session['user_id'])
                weather_data = get_weather_data(user.pin_code)
                analysis_result = analyze_plant_image(filepath, weather_data)
                
                scan_result = ScanResult(
                    user_id=session['user_id'],
                    image_filename=filename,
                    diagnosis=analysis_result['diagnosis'],
                    treatment_advice=analysis_result['treatment'],
                    weather_warning=analysis_result.get('weather_warning')
                )
                
                db.session.add(scan_result)
                db.session.commit()
                
                return redirect(url_for('results', scan_id=scan_result.id))
                
            except Exception as e:
                app.logger.error(f"Error processing image: {str(e)}")
                flash('Error processing image. Please try again.', 'error')
        else:
            flash('Invalid file type. Please upload a valid image.', 'error')
    
    return render_template('scanner.html')

@app.route('/results/<int:scan_id>')
def results(scan_id):
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    scan_result = ScanResult.query.filter_by(id=scan_id, user_id=session['user_id']).first()
    if not scan_result:
        flash('Scan result not found', 'error')
        return redirect(url_for('scanner'))
    
    return render_template('results.html', result=scan_result)

@app.route('/login')
def login():
    clerk_publishable_key = os.environ.get('CLERK_PUBLISHABLE_KEY')
    return render_template('clerk_auth.html', clerk_publishable_key=clerk_publishable_key)

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
    if 'clerk_user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        from supabase_models.farmer import Farmer
        
        farmer_data = {
            'clerk_user_id': session['clerk_user_id'],
            'name': request.form.get('full_name'),
            'phone': session.get('clerk_phone') or request.form.get('phone_number'),
            'email': session.get('clerk_email') or request.form.get('email', ''),
            'place': request.form.get('village_city'),
            'district': request.form.get('district', ''),
            'state': request.form.get('state', ''),
            'pincode': request.form.get('pin_code'),
            'farm_size_acres': float(request.form.get('farm_size_acres', 0)),
            'farming_experience_years': int(request.form.get('farming_experience_years', 0)),
            'preferred_language': request.form.get('preferred_language', 'en')
        }
        
        farmer = Farmer.create(farmer_data)
        if farmer:
            session['user_id'] = farmer.id
            flash('Profile created successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Error creating profile. Please try again.', 'error')
    
    crops_list = ['Rice', 'Wheat', 'Sugarcane', 'Cotton', 'Jute', 'Maize', 'Barley', 'Bajra', 'Jowar', 'Ragi', 'Potato', 'Onion', 'Tomato', 'Brinjal', 'Cabbage', 'Cauliflower', 'Okra', 'Chili', 'Turmeric', 'Ginger', 'Garlic', 'Coriander', 'Cumin', 'Mustard', 'Groundnut', 'Sesame', 'Sunflower', 'Soybean', 'Black gram', 'Green gram', 'Chickpea', 'Pigeon pea', 'Banana', 'Mango', 'Papaya', 'Guava', 'Coconut']
    return render_template('profile.html', crops_list=crops_list)

@app.route('/weather')
def weather():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    user = User.query.get(session['user_id'])
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
            weather_data = get_weather_data(user.pin_code)
    
    return render_template('weather.html', weather=weather_data, user=user)

@app.route('/market')
def market():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    user = User.query.get(session['user_id'])
    user_crops = json.loads(user.main_crops)
    all_crops = user_crops + ['Cotton', 'Maize', 'Onion', 'Potato', 'Tomato', 'Soybean', 'Groundnut', 'Turmeric', 'Chili', 'Garlic', 'Mustard', 'Sesame', 'Sunflower']
    unique_crops = list(dict.fromkeys(all_crops))
    market_data = get_market_prices(unique_crops[:13])
    
    return render_template('market.html', market_data=market_data, user_crops=user_crops)

@app.route('/passport', methods=['GET', 'POST'])
def passport():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        crop_type = request.form.get('crop_type')
        season = request.form.get('season')
        
        if not all([crop_type, season]):
            flash('All fields are required', 'error')
            return render_template('passport.html')
        
        passport = DigitalPassport(
            user_id=session['user_id'],
            crop_type=crop_type,
            season=season,
            nft_token_id=f"KS-{session['user_id']}-{crop_type[:3].upper()}-{season[:4].upper()}",
            ipfs_hash=f"Qm{hash(str(session.get('user_id')) + crop_type + season) % 10000000000000000000000000000000000000000000000}"
        )
        
        db.session.add(passport)
        db.session.commit()
        
        flash('Digital passport created successfully!', 'success')
    
    user = User.query.get(session['user_id'])
    user_crops = json.loads(user.main_crops)
    passports = DigitalPassport.query.filter_by(user_id=session['user_id']).all()
    
    return render_template('passport.html', user_crops=user_crops, passports=passports)

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'info')
    return redirect(url_for('index'))

# Supabase API routes
try:
    from routes.farmer_routes import farmer_bp
    app.register_blueprint(farmer_bp)
except ImportError:
    pass

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=9000, debug=True)