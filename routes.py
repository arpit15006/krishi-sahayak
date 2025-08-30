import os
import json
from flask import render_template, request, redirect, url_for, session, flash, jsonify, current_app
from werkzeug.utils import secure_filename
from PIL import Image
from services.weather_service import get_weather_data, get_weather_by_coordinates, get_weather_by_current_location
from services.ai_service import analyze_plant_image
from services.market_service import get_market_prices
from datetime import datetime

def create_fallback_insights(crops):
    """Create fallback market insights when API fails"""
    fallback_insights = []
    for crop in crops[:3]:  # Limit to 3 crops
        fallback_insights.append({
            'crop': crop,
            'current_price': 2500 if crop == 'Rice' else 2000 if crop == 'Wheat' else 3000,
            'predicted_price': 2600 if crop == 'Rice' else 2100 if crop == 'Wheat' else 3200,
            'trend': 'UP',
            'percentage_change': 4.0,
            'action': 'HOLD',
            'reason': 'Seasonal demand expected to increase',
            'advice': f'{crop} की कीमत बढ़ने की संभावना है। 2-3 सप्ताह इंतजार करें।',
            'confidence': 'Medium',
            'timeframe': '2-3 weeks'
        })
    return fallback_insights

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

from flask import Blueprint

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    from simple_run import User, db, ScanResult, DigitalPassport
    # Temporary bypass: Create demo user and auto-login for testing
    demo_user = User.query.filter_by(phone_number="9999999999").first()
    if not demo_user:
        # Create demo user
        demo_user = User(
            phone_number="9999999999",
            full_name="Demo Farmer",
            village_city="Demo Village",
            pin_code="110001",
            main_crops=json.dumps(['Rice', 'Wheat', 'Sugarcane']),
            is_verified=True
        )
        db.session.add(demo_user)
        db.session.commit()
    
    # Auto-login demo user
    session['user_id'] = demo_user.id
    session['phone_number'] = demo_user.phone_number
    
    if 'user_id' in session:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    from simple_run import User, db
    
    if request.method == 'POST':
        phone_number = request.form.get('phone_number')
        
        if not phone_number:
            flash('Phone number is required', 'error')
            return render_template('login.html')
        
        # In a real app, you would send OTP here
        # For MVP, we'll simulate OTP verification
        user = User.query.filter_by(phone_number=phone_number).first()
        
        if user:
            session['user_id'] = user.id
            session['phone_number'] = phone_number
            flash('Login successful!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            # New user, redirect to profile setup
            session['phone_number'] = phone_number
            flash('Please complete your profile setup', 'info')
            return redirect(url_for('main.profile'))
    
    return render_template('login.html')

@bp.route('/profile', methods=['GET', 'POST'])
def profile():
    from simple_run import User, db
    
    if 'phone_number' not in session:
        return redirect(url_for('main.login'))
    
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        village_city = request.form.get('village_city')
        pin_code = request.form.get('pin_code')
        main_crops = request.form.getlist('main_crops')
        
        if not all([full_name, village_city, pin_code, main_crops]):
            flash('All fields are required', 'error')
            return render_template('profile.html')
        
        # Create new user
        user = User(
            phone_number=session['phone_number'],
            full_name=full_name,
            village_city=village_city,
            pin_code=pin_code,
            main_crops=json.dumps(main_crops),
            is_verified=True
        )
        
        db.session.add(user)
        db.session.commit()
        
        session['user_id'] = user.id
        flash('Profile created successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    
    crops_list = [
        'Rice', 'Wheat', 'Sugarcane', 'Cotton', 'Jute', 'Maize', 'Barley', 
        'Bajra', 'Jowar', 'Ragi', 'Potato', 'Onion', 'Tomato', 'Brinjal',
        'Cabbage', 'Cauliflower', 'Okra', 'Chili', 'Turmeric', 'Ginger',
        'Garlic', 'Coriander', 'Cumin', 'Mustard', 'Groundnut', 'Sesame',
        'Sunflower', 'Soybean', 'Black gram', 'Green gram', 'Chickpea',
        'Pigeon pea', 'Banana', 'Mango', 'Papaya', 'Guava', 'Coconut'
    ]
    
    return render_template('profile.html', crops_list=crops_list)

@bp.route('/dashboard')
def dashboard():
    from simple_run import User
    
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    
    user = User.query.get(session['user_id'])
    if not user:
        return redirect(url_for('main.login'))
    
    # Get weather data - try current location first, then user's PIN code
    weather_data = get_weather_by_current_location()
    if weather_data.get('error'):
        weather_data = get_weather_data(user.pin_code)
    
    # Get market prices for user's crops
    user_crops = json.loads(user.main_crops)
    # Add more popular crops to show comprehensive market data
    all_crops = user_crops + ['Cotton', 'Maize', 'Onion', 'Potato', 'Tomato', 'Soybean', 'Groundnut', 'Turmeric', 'Chili', 'Garlic']
    # Remove duplicates while preserving order
    unique_crops = list(dict.fromkeys(all_crops))
    market_data = get_market_prices(unique_crops[:13])  # Show up to 13 crops
    
    return render_template('dashboard.html', 
                         user=user, 
                         weather=weather_data, 
                         market_data=market_data)

@bp.route('/scanner', methods=['GET', 'POST'])
def scanner():
    from simple_run import User, ScanResult, db
    
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    
    if request.method == 'POST':
        if 'plant_image' not in request.files:
            flash('No image selected', 'error')
            return render_template('scanner.html')
        
        file = request.files['plant_image']
        if file.filename == '':
            flash('No image selected', 'error')
            return render_template('scanner.html')
        
        if file and allowed_file(file.filename):
            # Create uploads directory if it doesn't exist
            os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
            
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Process the image
            try:
                # Resize image if needed
                with Image.open(filepath) as img:
                    # Convert to RGB if needed
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    # Resize if too large
                    max_size = (1024, 1024)
                    img.thumbnail(max_size, Image.LANCZOS)
                    img.save(filepath, 'JPEG', quality=85)
                
                # Get AI analysis
                user = User.query.get(session['user_id'])
                weather_data = get_weather_data(user.pin_code)
                
                analysis_result = analyze_plant_image(filepath, weather_data)
                
                # Save scan result
                scan_result = ScanResult(
                    user_id=session['user_id'],
                    image_filename=filename,
                    diagnosis=analysis_result['diagnosis'],
                    treatment_advice=analysis_result['treatment'],
                    weather_warning=analysis_result.get('weather_warning')
                )
                
                db.session.add(scan_result)
                db.session.commit()
                
                return redirect(url_for('main.results', scan_id=scan_result.id))
                
            except Exception as e:
                current_app.logger.error(f"Error processing image: {str(e)}")
                flash('Error processing image. Please try again.', 'error')
        else:
            flash('Invalid file type. Please upload a valid image.', 'error')
    
    return render_template('scanner.html')

@bp.route('/results/<int:scan_id>')
def results(scan_id):
    from simple_run import ScanResult
    
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    
    scan_result = ScanResult.query.filter_by(id=scan_id, user_id=session['user_id']).first()
    if not scan_result:
        flash('Scan result not found', 'error')
        return redirect(url_for('main.scanner'))
    
    return render_template('results.html', result=scan_result)

@bp.route('/market')
def market():
    from simple_run import User
    
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    
    user = User.query.get(session['user_id'])
    user_crops = json.loads(user.main_crops)
    
    # Get comprehensive market data with more crops
    all_crops = user_crops + ['Cotton', 'Maize', 'Onion', 'Potato', 'Tomato', 'Soybean', 'Groundnut', 'Turmeric', 'Chili', 'Garlic', 'Mustard', 'Sesame', 'Sunflower']
    unique_crops = list(dict.fromkeys(all_crops))
    market_data = get_market_prices(unique_crops[:13])
    
    # Get AI market insights for market page - load by default
    market_insights = []
    try:
        from services.market_guru import get_market_insights
        # Always load insights with fallback crops if user crops are empty
        crops_to_analyze = user_crops if user_crops else ['Rice', 'Wheat', 'Cotton', 'Onion']
        market_insights = get_market_insights(crops_to_analyze)
        current_app.logger.info(f"Loaded {len(market_insights)} market insights for crops: {crops_to_analyze}")
    except Exception as e:
        current_app.logger.error(f"Market insights error: {str(e)}")
        # Create fallback insights if API fails
        market_insights = create_fallback_insights(user_crops if user_crops else ['Rice', 'Wheat', 'Cotton'])
    
    return render_template('market.html', market_data=market_data, user_crops=user_crops, market_insights=market_insights)

@bp.route('/passport', methods=['GET', 'POST'])
def passport():
    from simple_run import User, DigitalPassport
    
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    
    if request.method == 'POST':
        from services.blockchain.passport_service import passport_service
        from services.supply_chain import supply_chain_service
        
        crop_type = request.form.get('crop_type')
        season = request.form.get('season')
        create_qr = request.form.get('create_qr') == 'on'
        
        if not all([crop_type, season]):
            flash('All fields are required', 'error')
            return render_template('passport.html')
        
        # Get user data for blockchain
        user = User.query.get(session['user_id'])
        user_data = {
            'full_name': user.full_name,
            'village_city': user.village_city,
            'pin_code': user.pin_code,
            'phone_number': user.phone_number
        }
        
        # Create digital passport with MONAD blockchain integration
        result = passport_service.create_digital_passport(
            user_id=session['user_id'],
            crop_type=crop_type,
            season=season,
            user_data=user_data
        )
        
        if result['success']:
            # Generate QR code for supply chain tracking if requested
            if create_qr:
                crop_data = {
                    'crop_type': crop_type,
                    'season': season,
                    'harvest_date': datetime.now().strftime('%Y-%m-%d'),
                    'is_organic': True,  # Default to organic
                    'certification_type': 'Blockchain Verified'
                }
                
                qr_result = supply_chain_service.create_product_qr(
                    user_data, crop_data, result.get('passport_id', 'demo')
                )
                
                if qr_result['success']:
                    flash(f"{result['message']} QR code generated for supply chain tracking!", 'success')
                    session['latest_qr'] = qr_result
                else:
                    flash(result['message'], 'success')
            else:
                flash(result['message'], 'success')
                
            if result.get('warning'):
                flash(f"Warning: {result['warning']}", 'warning')
        else:
            flash(result['error'], 'error')
    
    user = User.query.get(session['user_id'])
    user_crops = json.loads(user.main_crops)
    passports = DigitalPassport.query.filter_by(user_id=session['user_id']).all()
    
    # Get blockchain status for display
    from services.blockchain.passport_service import passport_service
    blockchain_status = passport_service.get_blockchain_status()
    
    # Get latest QR code if available
    latest_qr = session.pop('latest_qr', None)
    
    return render_template('passport.html', 
                         user_crops=user_crops, 
                         passports=passports,
                         blockchain_status=blockchain_status,
                         latest_qr=latest_qr)

@bp.route('/weather')
def weather():
    from simple_run import User
    
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    
    user = User.query.get(session['user_id'])
    
    # Check if coordinates are provided
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    pin_code = request.args.get('pin')
    
    if lat and lon:
        # Use coordinates to get weather
        weather_data = get_weather_by_coordinates(float(lat), float(lon))
    elif pin_code:
        # Use specific PIN code
        weather_data = get_weather_data(pin_code)
    else:
        # Use current location first, then user's profile PIN code
        weather_data = get_weather_by_current_location()
        if weather_data.get('error'):
            weather_data = get_weather_data(user.pin_code)
    
    return render_template('weather.html', weather=weather_data, user=user)

@bp.route('/yield', methods=['GET', 'POST'])
def yield_prediction():
    from simple_run import User
    
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    
    user = User.query.get(session['user_id'])
    user_crops = json.loads(user.main_crops)
    prediction = None
    
    if request.method == 'POST':
        crop_type = request.form.get('crop_type')
        area_acres = float(request.form.get('area_acres', 0))
        
        if crop_type and area_acres > 0:
            # Get weather data for prediction
            weather_data = get_weather_data(user.pin_code)
            location_data = {'pin_code': user.pin_code, 'village': user.village_city}
            
            # Get yield prediction
            from services.yield_service import predict_crop_yield
            prediction = predict_crop_yield(crop_type, area_acres, location_data, weather_data)
        else:
            flash('Please fill all required fields', 'error')
    
    return render_template('yield.html', user_crops=user_crops, prediction=prediction)

@bp.route('/api/market-insights')
def api_market_insights():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    try:
        from simple_run import User
        from services.market_guru import get_market_insights
        import json
        
        user = User.query.get(session['user_id'])
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404
        
        user_crops = json.loads(user.main_crops) if user.main_crops else ['Rice', 'Wheat', 'Cotton', 'Onion']
        
        # Get real market insights
        insights = get_market_insights(user_crops)
        
        return jsonify({
            'success': True,
            'insights': insights
        })
        
    except Exception as e:
        current_app.logger.error(f"Market insights error: {str(e)}")
        return jsonify({'success': False, 'error': 'Failed to fetch market insights'}), 500

@bp.route('/track/<passport_id>')
def track_product(passport_id):
    """Public route for consumers to track products via QR code"""
    from services.supply_chain import supply_chain_service
    
    # Get tracking information
    tracking_data = supply_chain_service.get_tracking_info(passport_id)
    
    if tracking_data['success']:
        return render_template('track.html', tracking_data=tracking_data)
    else:
        return render_template('track.html', tracking_data=None)

@bp.route('/api/generate-qr', methods=['POST'])
def generate_qr():
    """Generate QR code for existing passport"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    try:
        from simple_run import User
        from services.supply_chain import supply_chain_service
        
        data = request.get_json()
        passport_id = data.get('passport_id')
        crop_type = data.get('crop_type')
        
        if not passport_id:
            return jsonify({'success': False, 'error': 'Passport ID required'})
        
        user = User.query.get(session['user_id'])
        user_data = {
            'full_name': user.full_name,
            'village_city': user.village_city,
            'pin_code': user.pin_code,
            'phone_number': user.phone_number
        }
        
        crop_data = {
            'crop_type': crop_type or 'Unknown',
            'season': 'Current Season',
            'harvest_date': datetime.now().strftime('%Y-%m-%d'),
            'is_organic': True,
            'certification_type': 'Blockchain Verified'
        }
        
        result = supply_chain_service.create_product_qr(user_data, crop_data, passport_id)
        return jsonify(result)
        
    except Exception as e:
        current_app.logger.error(f"QR generation error: {str(e)}")
        return jsonify({'success': False, 'error': 'Failed to generate QR code'}), 500

@bp.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'info')
    return redirect(url_for('main.index'))

@bp.errorhandler(404)
def not_found(error):
    return render_template('base.html'), 404

@bp.route('/api/chat', methods=['POST'])
def chat():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    try:
        from simple_run import User
        
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'})
            
        question = data.get('question', '').strip()
        scan_result = data.get('scan_result', {})
        
        if not question:
            return jsonify({'success': False, 'error': 'No question provided'})
        
        # Get user context
        user = User.query.get(session['user_id'])
        if not user:
            return jsonify({'success': False, 'error': 'User not found'})
            
        user_crops = json.loads(user.main_crops) if user.main_crops else []
        
        # Get weather data for enhanced context
        weather_data = None
        try:
            weather_data = get_weather_data(user.pin_code)
        except:
            pass
        
        # Get market data for enhanced context
        market_data = None
        try:
            market_data = get_market_prices(user_crops[:3])  # Limit to 3 crops
        except:
            pass
        
        # Process question with enhanced context
        from services.ai_service import process_contextual_query
        response = process_contextual_query(
            query=question, 
            language='hi-IN', 
            user_crops=user_crops, 
            pin_code=user.pin_code, 
            scan_result=scan_result,
            weather_data=weather_data,
            market_data=market_data
        )
        
        return jsonify({
            'success': True,
            'response': response
        })
        
    except Exception as e:
        current_app.logger.error(f"Chat error: {str(e)}")
        import traceback
        current_app.logger.error(f"Chat traceback: {traceback.format_exc()}")
        return jsonify({
            'success': False, 
            'error': 'माफ करें, कुछ तकनीकी समस्या है। कृपया दोबारा कोशिश करें।'
        }), 500

@bp.route('/api/voice-query', methods=['POST'])
def voice_query():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    try:
        from simple_run import User
        
        data = request.get_json()
        query = data.get('query', '').strip()
        language = data.get('language', 'hi-IN')
        scan_result = data.get('scan_result', {})
        
        if not query:
            return jsonify({'success': False, 'error': 'No query provided'})
        
        # Get user context
        user = User.query.get(session['user_id'])
        user_crops = json.loads(user.main_crops) if user.main_crops else []
        
        # Get weather data for enhanced context
        weather_data = None
        try:
            weather_data = get_weather_data(user.pin_code)
        except:
            pass
        
        # Get market data for enhanced context
        market_data = None
        try:
            market_data = get_market_prices(user_crops[:3])  # Limit to 3 crops
        except:
            pass
        
        # Process voice query with enhanced context
        from services.ai_service import process_contextual_query
        response = process_contextual_query(
            query=query, 
            language=language, 
            user_crops=user_crops, 
            pin_code=user.pin_code, 
            scan_result=scan_result,
            weather_data=weather_data,
            market_data=market_data
        )
        
        return jsonify({
            'success': True,
            'response': response,
            'language': language
        })
        
    except Exception as e:
        current_app.logger.error(f"Voice query error: {str(e)}")
        return jsonify({
            'success': False, 
            'error': 'माफ करें, कुछ तकनीकी समस्या है।' if language == 'hi-IN' else 'Sorry, there was a technical issue.'
        }), 500

@bp.errorhandler(404)
def not_found(error):
    return render_template('base.html'), 404

@bp.errorhandler(500)
def internal_error(error):
    return render_template('base.html'), 500
