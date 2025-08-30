#!/usr/bin/env python3
import os
import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.utils import secure_filename
from PIL import Image
from dotenv import load_dotenv
from translations import get_text, get_available_languages

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "krishi-sahayak-secret-key")
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Language support
@app.context_processor
def inject_language():
    current_lang = session.get('language', 'en')
    return {
        'get_text': lambda key: get_text(key, current_lang),
        'current_lang': current_lang,
        'available_languages': get_available_languages()
    }

# Import services
from services.weather_service import get_weather_data, get_weather_by_coordinates, get_weather_by_current_location
from services.ai_service import analyze_plant_image
from services.market_service import get_market_prices
from services.alert_service import check_price_alerts, get_demo_alerts, create_alert_summary
from services.market_guru import get_ai_market_prediction, get_market_insights
from services.community_service import community_service
from services.resource_optimizer import resource_optimizer
from services.satellite_service import satellite_service
from services.seed_calculator import seed_calculator
from datetime import datetime
import dateutil.parser
import requests

@app.template_filter('format_date')
def format_date(date_str):
    """Format date string for display"""
    if not date_str:
        return 'Unknown'
    try:
        if isinstance(date_str, str):
            dt = dateutil.parser.parse(date_str)
            return dt.strftime('%b %Y')
        elif hasattr(date_str, 'strftime'):
            return date_str.strftime('%b %Y')
        else:
            return str(date_str)[:7]
    except:
        return str(date_str)[:7]

@app.template_filter('time_ago')
def time_ago(date_str):
    """Simple time ago filter"""
    if not date_str:
        return 'अभी'
    try:
        if isinstance(date_str, str):
            dt = dateutil.parser.parse(date_str)
            now = datetime.now()
            diff = now - dt.replace(tzinfo=None)
            
            if diff.days > 0:
                return f'{diff.days} दिन पहले'
            elif diff.seconds > 3600:
                hours = diff.seconds // 3600
                return f'{hours} घंटे पहले'
            elif diff.seconds > 60:
                minutes = diff.seconds // 60
                return f'{minutes} मिनट पहले'
            else:
                return 'अभी'
        return 'अभी'
    except:
        return 'अभी'

# Import passport routes
from routes_package.passport_routes import passport_bp

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class UserWrapper:
    """Wrapper to unify Supabase Farmer and demo user attributes"""
    def __init__(self, user_data):
        if hasattr(user_data, '__dict__'):
            # Supabase Farmer object
            self.id = getattr(user_data, 'id', None)
            self.name = getattr(user_data, 'name', None)
            self.full_name = getattr(user_data, 'name', None)
            self.place = getattr(user_data, 'place', None)
            self.village_city = getattr(user_data, 'place', None)
            self.pincode = getattr(user_data, 'pincode', None)
            self.pin_code = getattr(user_data, 'pincode', None)
            self.phone = getattr(user_data, 'phone', None)
            self.email = getattr(user_data, 'email', None)
            self._original = user_data
        else:
            # Dict object (demo user)
            self.id = user_data.get('id')
            self.name = user_data.get('name') or user_data.get('full_name')
            self.full_name = user_data.get('full_name') or user_data.get('name')
            self.place = user_data.get('place') or user_data.get('village_city')
            self.village_city = user_data.get('village_city') or user_data.get('place')
            self.pincode = user_data.get('pincode') or user_data.get('pin_code')
            self.pin_code = user_data.get('pin_code') or user_data.get('pincode')
            self.phone = user_data.get('phone')
            self.email = user_data.get('email')
            self._original = user_data
    
    def get_crops(self):
        """Get crops with fallback"""
        if hasattr(self._original, 'get_crops'):
            return self._original.get_crops()
        return []

def get_supabase_farmer(user_id):
    """Get farmer from Supabase by ID"""
    try:
        from supabase_models.farmer import Farmer
        farmer = Farmer.get_by_id(user_id)
        return UserWrapper(farmer) if farmer else None
    except Exception as e:
        print(f"Supabase error: {e}")
        return None

def get_supabase_farmer_by_clerk_id(clerk_user_id):
    """Get farmer from Supabase by Clerk ID"""
    try:
        from supabase_models.farmer import Farmer
        farmer = Farmer.get_by_clerk_id(clerk_user_id)
        return UserWrapper(farmer) if farmer else None
    except Exception as e:
        print(f"Supabase error: {e}")
        return None

def create_supabase_farmer(farmer_data):
    """Create farmer in Supabase"""
    try:
        from supabase_models.farmer import Farmer
        
        # Check if farmer already exists
        existing = Farmer.get_by_clerk_id(farmer_data['clerk_user_id'])
        if existing:
            print(f"Farmer already exists with clerk_user_id: {farmer_data['clerk_user_id']}")
            return UserWrapper(existing)
        
        farmer = Farmer.create(farmer_data)
        return UserWrapper(farmer) if farmer else None
    except Exception as e:
        print(f"Supabase create error: {e}")
        raise e



@app.route('/set-language/<lang_code>')
def set_language(lang_code):
    """Set user's preferred language"""
    if lang_code in ['en', 'hi', 'gu', 'mr', 'te', 'ta']:
        session['language'] = lang_code
        # Update user profile if logged in
        if 'user_id' in session:
            try:
                farmer = get_supabase_farmer(session['user_id'])
                if farmer and hasattr(farmer._original, 'update_language'):
                    farmer._original.update_language(lang_code)
            except:
                pass
    return redirect(request.referrer or url_for('dashboard'))

@app.route('/')
def index():
    # Set default language if not set
    if 'language' not in session:
        session['language'] = 'en'
    
    # Check if user is authenticated with Clerk and has profile
    if 'clerk_user_id' in session and 'user_id' in session:
        return redirect(url_for('dashboard'))
    # If authenticated with Clerk but no profile, go to profile setup
    elif 'clerk_user_id' in session:
        return redirect(url_for('profile'))
    # Not authenticated, show landing page
    return render_template('index.html')

@app.route('/login')
def login():
    clerk_publishable_key = os.environ.get('CLERK_PUBLISHABLE_KEY')
    if not clerk_publishable_key:
        flash('Authentication service not configured', 'error')
        return render_template('index.html')
    return render_template('clerk_auth.html', clerk_publishable_key=clerk_publishable_key)

@app.route('/auth/session', methods=['GET', 'POST'])
def create_session():
    if request.method == 'GET':
        return redirect(url_for('dashboard'))
    
    data = request.get_json()
    clerk_user_id = data.get('clerk_user_id')
    
    print(f"Auth session data: {data}")
    
    if clerk_user_id:
        farmer = get_supabase_farmer_by_clerk_id(clerk_user_id)
        
        if farmer:
            session['user_id'] = farmer.id
            session['clerk_user_id'] = clerk_user_id
            print(f"Existing farmer found: {farmer.id}")
            return jsonify({'redirect': '/dashboard'})
        else:
            session['clerk_user_id'] = clerk_user_id
            session['clerk_email'] = data.get('email')
            session['clerk_phone'] = data.get('phone')
            print(f"New user, redirecting to profile: {clerk_user_id}")
            return jsonify({'redirect': '/profile'})
    
    return jsonify({'error': 'Invalid request'}), 400

@app.route('/session')
def session_redirect():
    return redirect(url_for('dashboard'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'clerk_user_id' not in session:
        flash('Please sign in first', 'error')
        return redirect(url_for('login'))
    
    # Check if user already has a profile
    existing_farmer = get_supabase_farmer_by_clerk_id(session['clerk_user_id'])
    if existing_farmer:
        session['user_id'] = existing_farmer.id
        flash('Welcome back! Your profile already exists.', 'info')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        # Validate required fields
        required_fields = ['full_name', 'village_city', 'pin_code']
        for field in required_fields:
            if not request.form.get(field):
                flash(f'Please fill in {field.replace("_", " ").title()}', 'error')
                crops_list = ['Rice', 'Wheat', 'Sugarcane', 'Cotton', 'Jute', 'Maize', 'Barley', 'Bajra', 'Jowar', 'Ragi', 'Potato', 'Onion', 'Tomato', 'Brinjal', 'Cabbage', 'Cauliflower', 'Okra', 'Chili', 'Turmeric', 'Ginger', 'Garlic', 'Coriander', 'Cumin', 'Mustard', 'Groundnut', 'Sesame', 'Sunflower', 'Soybean', 'Black gram', 'Green gram', 'Chickpea', 'Pigeon pea', 'Banana', 'Mango', 'Papaya', 'Guava', 'Coconut']
                return render_template('profile.html', crops_list=crops_list)
        
        # Validate PIN code
        pin_code = request.form.get('pin_code')
        if not pin_code.isdigit() or len(pin_code) != 6:
            flash('Please enter a valid 6-digit PIN code', 'error')
            crops_list = ['Rice', 'Wheat', 'Sugarcane', 'Cotton', 'Jute', 'Maize', 'Barley', 'Bajra', 'Jowar', 'Ragi', 'Potato', 'Onion', 'Tomato', 'Brinjal', 'Cabbage', 'Cauliflower', 'Okra', 'Chili', 'Turmeric', 'Ginger', 'Garlic', 'Coriander', 'Cumin', 'Mustard', 'Groundnut', 'Sesame', 'Sunflower', 'Soybean', 'Black gram', 'Green gram', 'Chickpea', 'Pigeon pea', 'Banana', 'Mango', 'Papaya', 'Guava', 'Coconut']
            return render_template('profile.html', crops_list=crops_list)
        
        farmer_data = {
            'clerk_user_id': session.get('clerk_user_id'),
            'name': request.form.get('full_name'),
            'phone': session.get('clerk_phone') or session.get('temp_phone') or request.form.get('phone_number', ''),
            'email': session.get('clerk_email') or request.form.get('email', ''),
            'place': request.form.get('village_city'),
            'district': request.form.get('district', ''),
            'state': request.form.get('state', ''),
            'pincode': request.form.get('pin_code'),
            'farm_size_acres': float(request.form.get('farm_size_acres', 1.0)),
            'farming_experience_years': int(request.form.get('farming_experience_years', 1)),
            'preferred_language': request.form.get('preferred_language', 'en')
        }
        
        try:
            farmer = create_supabase_farmer(farmer_data)
            if farmer:
                session['user_id'] = farmer.id
                flash('Profile created successfully!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Error creating profile. Please try again.', 'error')
        except Exception as e:
            print(f"Profile creation error: {e}")
            flash(f'Database error: {str(e)}', 'error')
    
    crops_list = ['Rice', 'Wheat', 'Sugarcane', 'Cotton', 'Jute', 'Maize', 'Barley', 'Bajra', 'Jowar', 'Ragi', 'Potato', 'Onion', 'Tomato', 'Brinjal', 'Cabbage', 'Cauliflower', 'Okra', 'Chili', 'Turmeric', 'Ginger', 'Garlic', 'Coriander', 'Cumin', 'Mustard', 'Groundnut', 'Sesame', 'Sunflower', 'Soybean', 'Black gram', 'Green gram', 'Chickpea', 'Pigeon pea', 'Banana', 'Mango', 'Papaya', 'Guava', 'Coconut']
    return render_template('profile.html', crops_list=crops_list)

@app.route('/dashboard')
def dashboard():
    if 'clerk_user_id' not in session:
        flash('Please sign in with Google first', 'error')
        return redirect(url_for('login'))
    
    if 'user_id' not in session:
        flash('Please complete your profile setup', 'info')
        return redirect(url_for('profile'))
    
    # Try to get farmer from Supabase
    farmer = get_supabase_farmer(session['user_id'])
    if not farmer:
        flash('Profile not found. Please complete setup.', 'error')
        return redirect(url_for('profile'))
    
    # Always use farmer's pincode for weather - no fallback to current location
    pincode = getattr(farmer, 'pincode', None) or '110001'
    weather_data = get_weather_data(pincode)
    
    # Ensure the weather shows the farmer's location, not fallback location
    if weather_data and not weather_data.get('error'):
        # Force the city name to match farmer's location if available
        farmer_location = getattr(farmer, 'location', None) or ''
        if farmer_location and pincode:
            weather_data['city'] = f'{farmer_location} ({pincode})'
        elif pincode:
            weather_data['city'] = f'PIN {pincode}'
    else:
        # Only use current location if farmer's pincode completely fails
        weather_data = get_weather_by_current_location()
    
    # Get crops and market data
    try:
        if hasattr(farmer, 'get_crops'):
            crops = farmer.get_crops()
            crop_names = [crop['crop_name'] for crop in crops] if crops else ['Rice', 'Wheat']
        else:
            crop_names = ['Rice', 'Wheat']
    except:
        crop_names = ['Rice', 'Wheat']
    
    all_crops = crop_names + ['Cotton', 'Maize', 'Onion', 'Potato', 'Tomato']
    unique_crops = list(dict.fromkeys(all_crops))
    market_data = get_market_prices(unique_crops[:10])
    
    # Get price alerts for user's crops
    alerts = check_price_alerts(crop_names, session['user_id'])
    alert_summary = create_alert_summary(alerts)
    
    # Get AI market predictions
    market_insights = get_market_insights(crop_names)
    
    return render_template('dashboard.html', user=farmer, weather=weather_data, market_data=market_data, alerts=alerts, alert_summary=alert_summary, market_insights=market_insights)

@app.route('/scanner', methods=['GET', 'POST'])
def scanner():
    if 'clerk_user_id' not in session:
        flash('Please sign in with Google first', 'error')
        return redirect(url_for('login'))
    
    if 'user_id' not in session:
        flash('Please complete your profile setup', 'info')
        return redirect(url_for('profile'))
    
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
            
            farmer = get_supabase_farmer(session['user_id'])
            if not farmer:
                flash('Profile not found. Please complete setup.', 'error')
                return redirect(url_for('profile'))
            pincode = farmer.pincode or '110001'
            weather_data = get_weather_data(pincode)
            analysis_result = analyze_plant_image(filepath, weather_data)
            
            # Store result in session
            from datetime import datetime
            session['last_scan'] = {
                'filename': filename,
                'diagnosis': analysis_result['diagnosis'],
                'treatment': analysis_result['treatment'],
                'treatment_advice': analysis_result['treatment'],
                'weather_warning': analysis_result.get('weather_warning'),
                'created_at': datetime.now()
            }
            
            return redirect(url_for('results'))
            
        except Exception as e:
            app.logger.error(f"Error processing image: {str(e)}")
            flash('Error processing image. Please try again.', 'error')
    
    return render_template('scanner.html')

@app.route('/results')
def results():
    if 'clerk_user_id' not in session:
        flash('Please sign in with Google first', 'error')
        return redirect(url_for('login'))
    
    if 'user_id' not in session or 'last_scan' not in session:
        return redirect(url_for('scanner'))
    
    result = session['last_scan']
    from datetime import datetime
    return render_template('results.html', result=result, moment=datetime.now)

@app.route('/weather')
def weather():
    if 'clerk_user_id' not in session:
        flash('Please sign in with Google first', 'error')
        return redirect(url_for('login'))
    
    if 'user_id' not in session:
        flash('Please complete your profile setup', 'info')
        return redirect(url_for('profile'))
    
    farmer = get_supabase_farmer(session['user_id'])
    if not farmer:
        flash('Profile not found. Please complete setup.', 'error')
        return redirect(url_for('profile'))
    
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
            weather_data = get_weather_data(farmer.pincode or '110001')
    
    return render_template('weather.html', weather=weather_data, user=farmer)

@app.route('/market', methods=['GET', 'POST'])
def market():
    if 'clerk_user_id' not in session:
        flash('Please sign in with Google first', 'error')
        return redirect(url_for('login'))
    
    if 'user_id' not in session:
        flash('Please complete your profile setup', 'info')
        return redirect(url_for('profile'))
    
    if request.method == 'POST':
        # Handle price alert creation
        crop = request.form.get('alert_crop')
        target_price = float(request.form.get('target_price', 0))
        alert_type = request.form.get('alert_type', 'above')
        
        if crop and target_price > 0:
            from services.market_alerts import market_alerts
            alert_id = market_alerts.set_price_alert(
                user_id=session['user_id'],
                crop=crop,
                target_price=target_price,
                alert_type=alert_type
            )
            flash(f'Price alert set for {crop} at ₹{target_price}/kg', 'success')
    
    farmer = get_supabase_farmer(session['user_id'])
    if not farmer:
        flash('Profile not found. Please complete setup.', 'error')
        return redirect(url_for('profile'))
    
    try:
        crops = farmer.get_crops()
        crop_names = [crop['crop_name'] for crop in crops] if crops else ['Rice', 'Wheat']
    except:
        crop_names = ['Rice', 'Wheat']
    
    all_crops = crop_names + ['Cotton', 'Maize', 'Onion', 'Potato', 'Tomato', 'Soybean']
    unique_crops = list(dict.fromkeys(all_crops))
    market_data = get_market_prices(unique_crops[:10])
    
    return render_template('market.html', market_data=market_data, user_crops=crop_names)

@app.route('/passport', methods=['GET', 'POST'])
def passport():
    if 'clerk_user_id' not in session:
        flash('Please sign in with Google first', 'error')
        return redirect(url_for('login'))
    
    if 'user_id' not in session:
        flash('Please complete your profile setup', 'info')
        return redirect(url_for('profile'))
    
    if request.method == 'POST':
        print(f"DEBUG: POST request received with form data: {request.form}")
        from services.blockchain.working_passport_service import working_passport_service as passport_service
        
        crop_type = request.form.get('crop_type')
        season = request.form.get('season')
        sowing_date = request.form.get('sowing_date')
        harvest_date = request.form.get('harvest_date')
        area = request.form.get('area')
        variety = request.form.get('variety')
        practices = request.form.getlist('practices')
        
        print(f"DEBUG: Form fields - crop_type: {crop_type}, season: {season}")
        
        if not all([crop_type, season, sowing_date, harvest_date, area, variety]):
            flash('All fields are required', 'error')
            print("DEBUG: Missing required fields")
        else:
            print("DEBUG: All fields present, creating passport...")
            farmer = get_supabase_farmer(session['user_id'])
            user_data = {
                'full_name': farmer.name,
                'village_city': farmer.place
            }
            
            crop_data = {
                'sowing_date': sowing_date,
                'harvest_date': harvest_date,
                'area': float(area),
                'variety': variety,
                'practices': practices or ['Conventional']
            }
            
            result = passport_service.create_digital_passport(
                user_id=session['user_id'],
                crop_type=crop_type,
                season=season,
                user_data=user_data,
                crop_data=crop_data
            )
            
            print(f"DEBUG: Passport creation result: {result}")
            
            if result['success']:
                flash(result['message'], 'success')
                if result.get('warning'):
                    flash(f"Warning: {result['warning']}", 'warning')
                print("DEBUG: Passport created successfully, redirecting...")
                return redirect(url_for('passport'))
            else:
                flash(result['error'], 'error')
                print(f"DEBUG: Passport creation failed: {result['error']}")
    
    farmer = get_supabase_farmer(session['user_id'])
    if not farmer:
        flash('Profile not found. Please complete setup.', 'error')
        return redirect(url_for('profile'))
    
    try:
        crops = farmer.get_crops()
        crop_names = [crop['crop_name'] for crop in crops] if crops else ['Rice', 'Wheat']
    except:
        crop_names = ['Rice', 'Wheat']
    
    # Get user's existing passports
    from services.blockchain.working_passport_service import working_passport_service as passport_service
    blockchain_status = passport_service.get_blockchain_status()
    
    passports_result = passport_service.get_user_passports(session['user_id'])
    passports = passports_result.get('passports', []) if passports_result['success'] else []
    
    print(f"DEBUG: Found {len(passports)} passports for user {session['user_id']}")
    for i, p in enumerate(passports):
        print(f"  {i+1}. {p.crop_type} {p.season} (Token: {p.nft_token_id})")
    
    # Add cache busting
    import time
    cache_buster = int(time.time())
    
    print(f"DEBUG: Rendering template with {len(passports)} passports")
    
    return render_template('passport.html', 
                         user_crops=crop_names, 
                         passports=passports,
                         blockchain_status=blockchain_status,
                         cache_buster=cache_buster)

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'info')
    return redirect(url_for('index'))

@app.route('/qr/<token_id>')
def generate_qr(token_id):
    """Generate QR code with comprehensive farmer and crop data"""
    try:
        from services.qr_service import generate_qr_code
        from supabase_models.digital_passport import DigitalPassport
        
        # Get passport details
        passport = DigitalPassport.get_by_token_id(token_id)
        if not passport:
            return jsonify({'error': 'Passport not found'}), 404
        
        # Get farmer details
        farmer = get_supabase_farmer(passport.farmer_id)
        if not farmer:
            return jsonify({'error': 'Farmer not found'}), 404
        
        # Create comprehensive data for QR code
        qr_data_content = {
            'passport_id': token_id,
            'farmer': {
                'name': farmer.name,
                'location': farmer.place,
                'district': getattr(farmer, 'district', ''),
                'state': getattr(farmer, 'state', ''),
                'pincode': farmer.pincode,
                'phone': farmer.phone,
                'experience': getattr(farmer, 'farming_experience_years', 0)
            },
            'crop': {
                'type': passport.crop_type,
                'season': passport.season,
                'harvest_date': str(passport.created_at) if passport.created_at else '',
                'area': getattr(passport, 'area', 'N/A'),
                'practices': 'Organic, Sustainable'
            },
            'verification': {
                'blockchain': 'MONAD Testnet',
                'ipfs_hash': passport.ipfs_hash,
                'verified': True,
                'verify_url': f"{request.host_url}verify/{token_id}"
            }
        }
        
        # Create QR code that links directly to PDF certificate
        certificate_url = f"{request.host_url}certificate/{token_id}"
        qr_image = generate_qr_code(certificate_url)
        
        return jsonify({
            'qr_code': qr_image,
            'certificate_url': f"/certificate/{token_id}"
        })
        
    except Exception as e:
        app.logger.error(f"Error generating QR code: {str(e)}")
        return jsonify({'error': f'Failed to generate QR code: {str(e)}'}), 500

@app.route('/verify/<token_id>')
def verify_passport(token_id):
    """Public verification page for passports"""
    from services.blockchain.working_passport_service import working_passport_service
    
    result = working_passport_service.verify_passport(token_id)
    
    if result['success']:
        # Get passport details from database
        from supabase_models.digital_passport import DigitalPassport
        passport = DigitalPassport.get_by_token_id(token_id)
        return render_template('verify.html', passport=passport)
    else:
        return render_template('verify.html', passport=None)

@app.route('/qr-data/<token_id>')
def show_qr_data(token_id):
    """Show what data is embedded in QR code"""
    qr_response = generate_qr(token_id)
    if qr_response.status_code == 200:
        data = qr_response.get_json()['data']
        return render_template('qr_data.html', data=data)
    else:
        flash('Passport not found', 'error')
        return redirect(url_for('passport'))

@app.route('/api/chat', methods=['POST'])
def chat():
    """Real-time chat with AI expert with scan context"""
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        scan_result = data.get('scan_result', {})
        
        if not question:
            return jsonify({'success': False, 'error': 'No question provided'})
        
        # Direct Groq API call
        api_key = os.getenv('GROQ_API_KEY')
        
        # Create context from scan result
        context = ""
        if scan_result:
            diagnosis = scan_result.get('diagnosis', '')
            treatment = scan_result.get('treatment_advice', '') or scan_result.get('treatment', '')
            weather_warning = scan_result.get('weather_warning', '')
            
            if diagnosis:
                context = f"\n\nस्कैन की गई समस्या: {diagnosis[:300]}..."
                if treatment:
                    context += f"\nसुझाया गया इलाज: {treatment[:300]}..."
                if weather_warning:
                    context += f"\nमौसम चेतावनी: {weather_warning}"
        
        # Create farming expert prompt with context
        prompt = f"""आप एक कृषि विशेषज्ञ हैं।{context}

किसान का सवाल: "{question}"

यदि स्कैन रिपोर्ट उपलब्ध है तो उसके आधार पर जवाब दें। हिंदी में व्यावहारिक सलाह दें। 2-3 वाक्यों में जवाब दें।"""
        
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "llama-3.2-90b-text-preview",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 150,
            "temperature": 0.8
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result['choices'][0]['message']['content']
            return jsonify({
                'success': True,
                'response': ai_response
            })
        else:
            return jsonify({
                'success': True,
                'response': get_fallback_answer(question)
            })
        
    except Exception as e:
        return jsonify({
            'success': True,
            'response': get_fallback_answer(question)
        })

def get_fallback_answer(question):
    """Get contextual fallback answer based on question"""
    q = question.lower()
    
    if 'neem' in q or 'नीम' in q:
        return "हां, नीम का तेल बहुत अच्छा है। 10 मिली प्रति लीटर पानी में मिलाकर सप्ताह में 2-3 बार छिड़काव करें। सुबह या शाम के समय करें।"
    elif 'often' in q or 'frequency' in q or 'कितनी बार' in q:
        return "आमतौर पर 7-10 दिन में एक बार छिड़काव करें। जैविक दवा के लिए 5-7 दिन, रासायनिक के लिए 10-14 दिन। सुधार दिखने तक जारी रखें।"
    elif 'worse' in q or 'bad' in q or 'खराब' in q:
        return "अगर समस्या बढ़ रही है तो: 1) छिड़काव की मात्रा बढ़ाएं 2) रोगग्रस्त भाग हटा दें 3) स्थानीय कृषि अधिकारी से संपर्क करें।"
    elif 'time' in q or 'when' in q or 'कब' in q:
        return "सबसे अच्छा समय सुबह 6-9 बजे या शाम 5-7 बजे है। दोपहर की तेज धूप में न करें। बारिश से पहले भी न करें।"
    elif 'cost' in q or 'price' in q or 'लागत' in q:
        return "जैविक उपचार की लागत ₹200-500 प्रति एकड़। रासायनिक दवा की लागत ₹800-1500 प्रति एकड़। नीम का तेल सबसे सस्ता विकल्प है।"
    else:
        return f"आपके सवाल '{question}' के लिए: नीम का तेल और गोबर का घोल उपयोग करें। सुबह या शाम को छिड़काव करें। अधिक जानकारी के लिए स्थानीय कृषि अधिकारी से संपर्क करें।"

@app.route('/api/voice-query', methods=['POST'])
def voice_query():
    """Process voice queries in Hindi/English with scan context"""
    data = request.get_json()
    query = data.get('query', '')
    language = data.get('language', 'hi-IN')
    scan_result = data.get('scan_result', {})
    
    try:
        from services.ai_service import get_groq_response
        
        # Create context-aware prompt with scan result
        context = ""
        if scan_result:
            diagnosis = scan_result.get('diagnosis', '')
            treatment = scan_result.get('treatment', '')
            weather_warning = scan_result.get('weather_warning', '')
            
            if diagnosis:
                context = f"\n\nस्कैन रिपोर्ट:\n- समस्या: {diagnosis[:200]}...\n- इलाज: {treatment[:200]}..."
                if weather_warning:
                    context += f"\n- मौसम चेतावनी: {weather_warning}"
        
        if language.startswith('hi'):
            prompt = f"""आप एक कृषि विशेषज्ञ हैं जो भारतीय किसानों की मदद करते हैं।{context}

किसान का सवाल: "{query}"

कृपया हिंदी में सरल और व्यावहारिक उत्तर दें। यदि स्कैन रिपोर्ट उपलब्ध है तो उसके आधार पर जवाब दें। यदि यह पौधे की बीमारी के बारे में है, तो इलाज बताएं। यदि मौसम के बारे में है, तो सलाह दें।

उत्तर 2-3 वाक्यों में दें।"""
        else:
            prompt = f"""You are an agricultural expert helping Indian farmers.{context}

Farmer's question: "{query}"

Please provide a simple and practical answer in English. If scan report is available, base your answer on it. If it's about plant disease, suggest treatment. If about weather, give advice.

Keep response to 2-3 sentences."""
        
        response = get_groq_response(prompt)
        
        return jsonify({
            'success': True,
            'response': response,
            'query': query,
            'language': language
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/market-alerts', methods=['POST'])
def trigger_market_alerts():
    """Simulate market alert trigger for demo"""
    try:
        from services.market_alerts import market_alerts
        
        # Simulate price changes
        demo_prices = {
            'Rice': 45,
            'Wheat': 32,
            'Cotton': 85,
            'Onion': 25
        }
        
        triggered_alerts = market_alerts.check_price_alerts(demo_prices)
        
        return jsonify({
            'success': True,
            'alerts': triggered_alerts,
            'message': f'{len(triggered_alerts)} alerts triggered'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/yield-prediction')
def yield_prediction():
    """Yield prediction page"""
    if 'clerk_user_id' not in session:
        flash('Please sign in with Google first', 'error')
        return redirect(url_for('login'))
    
    if 'user_id' not in session:
        flash('Please complete your profile setup', 'info')
        return redirect(url_for('profile'))
    
    farmer = get_supabase_farmer(session['user_id'])
    if not farmer:
        flash('Profile not found. Please complete setup.', 'error')
        return redirect(url_for('profile'))
    
    try:
        crops = farmer.get_crops()
        crop_names = [crop['crop_name'] for crop in crops] if crops else ['Rice', 'Wheat']
    except:
        crop_names = ['Rice', 'Wheat']
    
    return render_template('yield_prediction.html', user_crops=crop_names)

@app.route('/api/yield-prediction', methods=['POST'])
def api_yield_prediction():
    """API endpoint for yield prediction"""
    try:
        data = request.get_json()
        
        # Get farmer and weather data
        farmer = get_supabase_farmer(session['user_id'])
        weather_data = get_weather_data(farmer.pincode or '110001')
        
        from services.yield_prediction import predict_crop_yield
        
        crop_data = {
            'crop_type': data.get('crop_type'),
            'variety': data.get('variety'),
            'area': float(data.get('area', 1)),
            'sowing_date': data.get('sowing_date'),
            'practices': data.get('practices', [])
        }
        
        farmer_data = {
            'experience': getattr(farmer, 'farming_experience_years', 5),
            'location': farmer.place
        }
        
        prediction = predict_crop_yield(crop_data, weather_data, farmer_data)
        
        return jsonify({
            'success': True,
            'prediction': prediction
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/weather-shield')
def weather_shield():
    """Weather Shield insurance page"""
    if 'clerk_user_id' not in session:
        flash('Please sign in with Google first', 'error')
        return redirect(url_for('login'))
    
    if 'user_id' not in session:
        flash('Please complete your profile setup', 'info')
        return redirect(url_for('profile'))
    
    return render_template('weather_shield.html')

@app.route('/api/alerts')
def get_alerts():
    """Get current alerts for user"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    try:
        farmer = get_supabase_farmer(session['user_id'])
        if not farmer:
            return jsonify({'success': False, 'error': 'User not found'}), 404
        
        try:
            crops = farmer.get_crops()
            crop_names = [crop['crop_name'] for crop in crops] if crops else ['Rice', 'Wheat']
        except:
            crop_names = ['Rice', 'Wheat']
        
        alerts = check_price_alerts(crop_names, session['user_id'])
        alert_summary = create_alert_summary(alerts)
        
        return jsonify({
            'success': True,
            'alerts': alerts,
            'summary': alert_summary
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/demo-alerts')
def get_demo_alerts_api():
    """Get demo alerts for testing"""
    try:
        alerts = get_demo_alerts()
        alert_summary = create_alert_summary(alerts)
        
        return jsonify({
            'success': True,
            'alerts': alerts,
            'summary': alert_summary
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/market-prediction/<crop_name>')
def get_crop_prediction(crop_name):
    """Get AI market prediction for specific crop"""
    try:
        current_price = float(request.args.get('price', 2000))
        prediction = get_ai_market_prediction(crop_name, current_price)
        
        return jsonify(prediction)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/market-insights')
def get_user_market_insights():
    """Get market insights for user's crops"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    try:
        farmer = get_supabase_farmer(session['user_id'])
        if not farmer:
            return jsonify({'success': False, 'error': 'User not found'}), 404
        
        try:
            crops = farmer.get_crops()
            crop_names = [crop['crop_name'] for crop in crops] if crops else ['Rice', 'Wheat']
        except:
            crop_names = ['Rice', 'Wheat']
        
        insights = get_market_insights(crop_names)
        
        return jsonify({
            'success': True,
            'insights': insights
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Community Chat Routes
@app.route('/community')
def community():
    """Community chat main page"""
    if 'clerk_user_id' not in session:
        flash('Please sign in with Google first', 'error')
        return redirect(url_for('login'))
    
    if 'user_id' not in session:
        flash('Please complete your profile setup', 'info')
        return redirect(url_for('profile'))
    
    # Get categories
    categories_result = community_service.get_categories()
    categories = categories_result.get('categories', []) if categories_result['success'] else []
    
    # Get recent posts
    category = request.args.get('category', 'all')
    posts_result = community_service.get_posts(category=category, limit=10)
    posts = posts_result.get('posts', []) if posts_result['success'] else []
    
    # Add farmer info to posts
    for post in posts:
        farmer_info = community_service.get_farmer_info(post['farmer_id'])
        post['farmer_name'] = farmer_info['name']
        post['farmer_place'] = farmer_info['place']
        post['is_ai'] = farmer_info['is_ai']
    
    return render_template('community.html', posts=posts, categories=categories, current_category=category)

@app.route('/community/post/<post_id>')
def community_post(post_id):
    """Individual post view with replies"""
    if 'clerk_user_id' not in session:
        flash('Please sign in with Google first', 'error')
        return redirect(url_for('login'))
    
    if 'user_id' not in session:
        flash('Please complete your profile setup', 'info')
        return redirect(url_for('profile'))
    
    # Get post details
    result = community_service.get_post_details(post_id)
    if not result['success']:
        flash('Post not found', 'error')
        return redirect(url_for('community'))
    
    post = result['post']
    replies = result['replies']
    
    # Add farmer info
    farmer_info = community_service.get_farmer_info(post['farmer_id'])
    post['farmer_name'] = farmer_info['name']
    post['farmer_place'] = farmer_info['place']
    post['is_ai'] = farmer_info['is_ai']
    
    for reply in replies:
        farmer_info = community_service.get_farmer_info(reply['farmer_id'])
        reply['farmer_name'] = farmer_info['name']
        reply['farmer_place'] = farmer_info['place']
        reply['is_ai'] = farmer_info['is_ai']
    
    return render_template('community_post.html', post=post, replies=replies)

@app.route('/community/new', methods=['GET', 'POST'])
def new_community_post():
    """Create new community post"""
    if 'clerk_user_id' not in session:
        flash('Please sign in with Google first', 'error')
        return redirect(url_for('login'))
    
    if 'user_id' not in session:
        flash('Please complete your profile setup', 'info')
        return redirect(url_for('profile'))
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        category = request.form.get('category', 'general')
        is_question = request.form.get('is_question') == 'on'
        
        if not title or not content:
            flash('Title and content are required', 'error')
        else:
            result = community_service.create_post(
                farmer_id=session['user_id'],
                title=title,
                content=content,
                category=category,
                is_question=is_question
            )
            
            if result['success']:
                flash('Post created successfully!', 'success')
                return redirect(url_for('community'))
            else:
                flash(f'Error creating post: {result["error"]}', 'error')
    
    # Get categories for form
    categories_result = community_service.get_categories()
    categories = categories_result.get('categories', []) if categories_result['success'] else []
    
    return render_template('new_community_post.html', categories=categories)

@app.route('/api/community/reply', methods=['POST'])
def create_community_reply():
    """Create reply to community post"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    data = request.get_json()
    post_id = data.get('post_id')
    content = data.get('content', '').strip()
    
    if not post_id or not content:
        return jsonify({'success': False, 'error': 'Post ID and content required'}), 400
    
    result = community_service.create_reply(
        post_id=post_id,
        farmer_id=session['user_id'],
        content=content
    )
    
    return jsonify(result)

@app.route('/api/community/vote', methods=['POST'])
def vote_community_content():
    """Vote on post or reply"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    data = request.get_json()
    vote_type = data.get('vote_type')  # 'upvote' or 'downvote'
    post_id = data.get('post_id')
    reply_id = data.get('reply_id')
    
    if vote_type not in ['upvote', 'downvote']:
        return jsonify({'success': False, 'error': 'Invalid vote type'}), 400
    
    if post_id:
        result = community_service.vote_post(session['user_id'], post_id, vote_type)
    elif reply_id:
        result = community_service.vote_reply(session['user_id'], reply_id, vote_type)
    else:
        return jsonify({'success': False, 'error': 'Post ID or Reply ID required'}), 400
    
    return jsonify(result)

@app.route('/api/community/search')
def search_community():
    """Search community posts"""
    query = request.args.get('q', '').strip()
    category = request.args.get('category', 'all')
    
    if not query:
        return jsonify({'success': False, 'error': 'Search query required'}), 400
    
    result = community_service.search_posts(query, category)
    
    if result['success']:
        # Add farmer info to posts
        for post in result['posts']:
            farmer_info = community_service.get_farmer_info(post['farmer_id'])
            post['farmer_name'] = farmer_info['name']
            post['farmer_place'] = farmer_info['place']
            post['is_ai'] = farmer_info['is_ai']
    
    return jsonify(result)

# Resource Optimization Routes
@app.route('/resource-optimizer')
def resource_optimizer_page():
    """Resource optimization calculator page"""
    if 'clerk_user_id' not in session:
        flash('Please sign in with Google first', 'error')
        return redirect(url_for('login'))
    
    if 'user_id' not in session:
        flash('Please complete your profile setup', 'info')
        return redirect(url_for('profile'))
    
    farmer = get_supabase_farmer(session['user_id'])
    if not farmer:
        flash('Profile not found. Please complete setup.', 'error')
        return redirect(url_for('profile'))
    
    try:
        crops = farmer.get_crops()
        crop_names = [crop['crop_name'] for crop in crops] if crops else ['Rice', 'Wheat']
    except:
        crop_names = ['Rice', 'Wheat']
    
    return render_template('resource_optimizer.html', user_crops=crop_names)

@app.route('/api/optimize-resources', methods=['POST'])
def optimize_resources():
    """Calculate water and fertilizer requirements"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    try:
        data = request.get_json()
        
        # Get farmer data
        farmer = get_supabase_farmer(session['user_id'])
        if not farmer:
            return jsonify({'success': False, 'error': 'Farmer not found'}), 404
        
        # Get weather data for farmer's location
        weather_data = get_weather_data(farmer.pincode or '110001')
        
        # Prepare input data
        crop_data = {
            'crop_type': data.get('crop_type'),
            'variety': data.get('variety', 'सामान्य'),
            'sowing_date': data.get('sowing_date'),
            'growth_stage': data.get('growth_stage', 'वानस्पतिक')
        }
        
        soil_data = {
            'soil_type': data.get('soil_type'),
            'ph_level': data.get('ph_level', '6.5'),
            'organic_carbon': data.get('organic_carbon', 'मध्यम'),
            'nitrogen': data.get('nitrogen_level', 'मध्यम'),
            'phosphorus': data.get('phosphorus_level', 'मध्यम'),
            'potash': data.get('potash_level', 'मध्यम')
        }
        
        farm_area = float(data.get('farm_area', 1.0))
        
        # Get AI recommendations
        result = resource_optimizer.calculate_resources(
            crop_data, soil_data, weather_data, farm_area
        )
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Satellite Monitoring Routes
@app.route('/satellite-monitor')
def satellite_monitor():
    """Satellite crop monitoring page"""
    if 'clerk_user_id' not in session:
        flash('Please sign in with Google first', 'error')
        return redirect(url_for('login'))
    
    if 'user_id' not in session:
        flash('Please complete your profile setup', 'info')
        return redirect(url_for('profile'))
    
    farmer = get_supabase_farmer(session['user_id'])
    if not farmer:
        flash('Profile not found. Please complete setup.', 'error')
        return redirect(url_for('profile'))
    
    return render_template('satellite_monitor.html')

# Seed Calculator Routes
@app.route('/seed-calculator')
def seed_calculator_page():
    """Seed calculator page"""
    if 'clerk_user_id' not in session:
        flash('Please sign in with Google first', 'error')
        return redirect(url_for('login'))
    
    if 'user_id' not in session:
        flash('Please complete your profile setup', 'info')
        return redirect(url_for('profile'))
    
    return render_template('seed_calculator.html')

@app.route('/api/calculate-seed', methods=['POST'])
def calculate_seed():
    """Calculate seed requirements"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    try:
        from services.seed_calculator import seed_calculator
        
        data = request.get_json()
        result = seed_calculator.calculate_seed_requirement(data)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/satellite-data', methods=['POST'])
def get_satellite_data():
    """Get satellite crop monitoring data"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    try:
        data = request.get_json()
        lat = float(data.get('lat', 0))
        lon = float(data.get('lon', 0))
        farm_area = float(data.get('farm_area', 1))
        
        if not lat or not lon:
            return jsonify({'success': False, 'error': 'Location required'}), 400
        
        # Get satellite data with cache busting
        result = satellite_service.get_crop_health_data(lat, lon, farm_area)
        
        # Add timestamp to force refresh
        if result.get('success') and result.get('vegetation_image'):
            result['cache_buster'] = datetime.now().timestamp()
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/generate-qr', methods=['POST'])
def api_generate_qr():
    """API endpoint to generate QR code for passport"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    try:
        data = request.get_json()
        passport_id = data.get('passport_id')
        crop_type = data.get('crop_type')
        
        if not passport_id:
            return jsonify({'success': False, 'error': 'Passport ID required'}), 400
        
        # Generate QR code directly
        from services.qr_service import generate_qr_code
        from supabase_models.digital_passport import DigitalPassport
        
        # Get passport details
        passport = DigitalPassport.get_by_token_id(passport_id)
        if not passport:
            return jsonify({'success': False, 'error': 'Passport not found'}), 404
        
        # Get farmer details
        farmer = get_supabase_farmer(passport.farmer_id)
        if not farmer:
            return jsonify({'success': False, 'error': 'Farmer not found'}), 404
        
        # Create QR data - direct link to PDF certificate
        certificate_url = f"{request.host_url}certificate/{passport_id}"
        qr_image = generate_qr_code(certificate_url)
        
        return jsonify({
            'success': True,
            'qr_code': qr_image,
            'qr_url': f"/verify/{passport_id}",
            'certificate_url': f"/certificate/{passport_id}"
        })
            
    except Exception as e:
        app.logger.error(f"API QR generation error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/certificate/<token_id>')
def download_certificate(token_id):
    """Generate and download PDF certificate"""
    try:
        from services.pdf_certificate import generate_certificate_pdf
        from supabase_models.digital_passport import DigitalPassport
        from flask import Response
        
        # Get passport details
        passport = DigitalPassport.get_by_token_id(token_id)
        if not passport:
            return jsonify({'error': 'Passport not found'}), 404
        
        # Get farmer details
        farmer = get_supabase_farmer(passport.farmer_id)
        if not farmer:
            return jsonify({'error': 'Farmer not found'}), 404
        
        # Prepare data for PDF
        passport_data = {
            'nft_token_id': passport.nft_token_id,
            'crop_type': passport.crop_type,
            'season': passport.season,
            'created_at': passport.created_at
        }
        
        farmer_data = {
            'name': farmer.name,
            'place': farmer.place,
            'pincode': farmer.pincode,
            'phone': farmer.phone,
            'farming_experience_years': getattr(farmer, 'farming_experience_years', 0)
        }
        
        # QR data for verification
        verify_url = f"{request.host_url}verify/{token_id}"
        
        # Generate PDF
        pdf_data = generate_certificate_pdf(passport_data, farmer_data, verify_url)
        
        # Return PDF as download
        response = Response(pdf_data, mimetype='application/pdf')
        response.headers['Content-Disposition'] = f'attachment; filename="crop_certificate_{token_id}.pdf"'
        return response
        
    except Exception as e:
        app.logger.error(f"Certificate generation error: {str(e)}")
        return jsonify({'error': f'Failed to generate certificate: {str(e)}'}), 500

@app.route('/qr-label/<token_id>')
def generate_qr_label(token_id):
    """Generate printable QR label for crop packaging"""
    try:
        from services.qr_service import generate_qr_code
        from supabase_models.digital_passport import DigitalPassport
        
        # Get passport details
        passport = DigitalPassport.get_by_token_id(token_id)
        if not passport:
            return jsonify({'error': 'Passport not found'}), 404
        
        # Get farmer details
        farmer = get_supabase_farmer(passport.farmer_id)
        if not farmer:
            return jsonify({'error': 'Farmer not found'}), 404
        
        # Generate QR code for certificate
        certificate_url = f"{request.host_url}certificate/{token_id}"
        qr_image = generate_qr_code(certificate_url)
        
        # Create printable label HTML
        label_html = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Crop QR Label - {passport.crop_type}</title>
            <style>
                @media print {{
                    body {{ margin: 0; }}
                    .no-print {{ display: none; }}
                }}
                body {{ font-family: Arial, sans-serif; text-align: center; padding: 20px; }}
                .label {{ border: 2px solid #28a745; border-radius: 10px; padding: 20px; max-width: 300px; margin: 0 auto; }}
                .qr-code {{ margin: 20px 0; }}
                .crop-info {{ font-size: 14px; font-weight: bold; color: #28a745; }}
                .farmer-info {{ font-size: 12px; color: #666; margin: 10px 0; }}
                .instructions {{ font-size: 11px; color: #888; margin-top: 15px; }}
                .print-btn {{ margin: 20px; padding: 10px 20px; background: #28a745; color: white; border: none; border-radius: 5px; cursor: pointer; }}
            </style>
        </head>
        <body>
            <button class="print-btn no-print" onclick="window.print()">🖨️ Print Label</button>
            
            <div class="label">
                <div class="crop-info">
                    🌾 {passport.crop_type}<br>
                    {passport.season}
                </div>
                
                <div class="qr-code">
                    <img src="{qr_image}" alt="QR Code" style="width: 150px; height: 150px;">
                </div>
                
                <div class="farmer-info">
                    👨‍🌾 {farmer.name}<br>
                    📍 {farmer.place}, {farmer.pincode}
                </div>
                
                <div class="instructions">
                    📱 Scan QR code to download<br>
                    verified crop certificate
                </div>
                
                <div style="font-size: 10px; color: #aaa; margin-top: 10px;">
                    🌱 Krishi Sahayak Certified
                </div>
            </div>
            
            <div class="no-print" style="margin-top: 30px; font-size: 14px; color: #666;">
                <p>📋 Instructions for use:</p>
                <ul style="text-align: left; max-width: 400px; margin: 0 auto;">
                    <li>Print this label on adhesive paper</li>
                    <li>Cut around the border</li>
                    <li>Attach to your crop packaging</li>
                    <li>Consumers can scan to get certificate</li>
                </ul>
            </div>
        </body>
        </html>
        '''
        
        return f'''
<!DOCTYPE html>
<html>
<head>
    <title>QR Label - {passport.crop_type}</title>
    <style>
        @media print {{
            body {{ margin: 0; padding: 0; }}
            .no-print {{ display: none !important; }}
        }}
        body {{ font-family: Arial, sans-serif; padding: 20px; background: #f5f5f5; }}
        .container {{ max-width: 400px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; }}
        .label {{ border: 3px solid #28a745; border-radius: 15px; padding: 25px; text-align: center; }}
        .crop-info {{ font-size: 18px; font-weight: bold; color: #28a745; margin-bottom: 15px; }}
        .qr-code {{ margin: 20px 0; }}
        .farmer-info {{ font-size: 14px; color: #333; margin: 15px 0; }}
        .instructions {{ font-size: 12px; color: #666; margin-top: 15px; }}
        .print-btn {{ margin: 20px auto; padding: 12px 24px; background: #28a745; color: white; border: none; border-radius: 8px; cursor: pointer; font-size: 16px; display: block; }}
    </style>
</head>
<body>
    <div class="container">
        <button class="print-btn no-print" onclick="window.print()">🖨️ Print QR Label</button>
        
        <div class="label">
            <div class="crop-info">
                🌾 {passport.crop_type}<br>
                <span style="font-size: 14px; font-weight: normal;">{passport.season}</span>
            </div>
            
            <div class="qr-code">
                <img src="{qr_image}" alt="QR Code" style="width: 160px; height: 160px; border: 2px solid #eee; border-radius: 8px;">
            </div>
            
            <div class="farmer-info">
                <strong>👨🌾 {farmer.name}</strong><br>
                📍 {farmer.place}<br>
                PIN: {farmer.pincode}
            </div>
            
            <div class="instructions">
                📱 <strong>Scan QR code to download</strong><br>
                verified crop certificate
            </div>
            
            <div style="font-size: 11px; color: #999; margin-top: 15px; border-top: 1px solid #eee; padding-top: 10px;">
                🌱 <strong>Krishi Sahayak</strong> Certified<br>
                Blockchain Verified Quality
            </div>
        </div>
        
        <div class="no-print" style="background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 8px; padding: 20px; margin-top: 30px; text-align: left;">
            <h3 style="color: #28a745; margin-top: 0;">📋 How to use this QR label:</h3>
            <ul>
                <li><strong>Print:</strong> Use adhesive label paper for best results</li>
                <li><strong>Cut:</strong> Cut around the green border carefully</li>
                <li><strong>Attach:</strong> Stick on your crop packaging or bags</li>
                <li><strong>Consumer:</strong> They scan and get your certificate instantly</li>
            </ul>
            <p style="margin-top: 15px; font-size: 13px; color: #666;">
                <strong>Note:</strong> The QR code links directly to your verified crop certificate.
            </p>
        </div>
    </div>
</body>
</html>
        '''
        
    except Exception as e:
        app.logger.error(f"QR label generation error: {str(e)}")
        return f'<h1>Error</h1><p>Failed to generate QR label: {str(e)}</p>', 500

# Register passport blueprint
app.register_blueprint(passport_bp)

# Test QR generation endpoint
@app.route('/test-qr')
def test_qr():
    """Test QR code generation"""
    try:
        from services.qr_service import generate_qr_code
        
        test_data = {
            'test': 'QR Code Generation Test',
            'timestamp': datetime.now().isoformat(),
            'message': 'If you can see this, QR generation is working!'
        }
        
        qr_content = json.dumps(test_data)
        qr_image = generate_qr_code(qr_content)
        
        return f'''
        <html>
        <body>
            <h1>QR Code Test</h1>
            <img src="{qr_image}" alt="Test QR Code">
            <p>Test Data: {qr_content}</p>
            <br><a href="/test-qr-modal">Test QR Modal</a>
        </body>
        </html>
        '''
        
    except Exception as e:
        return f'QR Generation Error: {str(e)}'

@app.route('/test-qr-modal')
def test_qr_modal():
    """Serve QR modal test page"""
    try:
        with open('test_qr_modal.html', 'r') as f:
            return f.read()
    except:
        return 'Test file not found'

@app.route('/qr-simple')
def qr_simple():
    """Simple QR generation for testing"""
    try:
        from services.qr_service import generate_qr_code
        
        test_data = f"Test QR - {datetime.now().strftime('%H:%M:%S')}"
        qr_code = generate_qr_code(test_data)
        
        return jsonify({
            'success': True,
            'qr_code': qr_code,
            'data': test_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    print(f"🌱 Krishi Sahayak starting on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)