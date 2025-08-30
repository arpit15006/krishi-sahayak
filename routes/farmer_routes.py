from flask import Blueprint, request, jsonify
from auth.clerk_auth import require_auth
from supabase_models.farmer import Farmer
from supabase_models.crop import Crop

farmer_bp = Blueprint('farmer', __name__)

@farmer_bp.route('/api/farmer/profile', methods=['POST'])
@require_auth
def create_farmer_profile():
    data = request.get_json()
    clerk_user_id = request.current_user.get('sub')
    
    farmer_data = {
        'clerk_user_id': clerk_user_id,
        'name': data.get('name'),
        'phone': data.get('phone'),
        'email': data.get('email'),
        'place': data.get('place'),
        'district': data.get('district'),
        'state': data.get('state'),
        'pincode': data.get('pincode'),
        'farm_size_acres': data.get('farm_size_acres'),
        'farming_experience_years': data.get('farming_experience_years'),
        'preferred_language': data.get('preferred_language', 'en')
    }
    
    farmer = Farmer.create(farmer_data)
    return jsonify({'success': True, 'farmer_id': farmer.id})

@farmer_bp.route('/api/farmer/profile', methods=['GET'])
@require_auth
def get_farmer_profile():
    clerk_user_id = request.current_user.get('sub')
    farmer = Farmer.get_by_clerk_id(clerk_user_id)
    
    if not farmer:
        return jsonify({'error': 'Profile not found'}), 404
        
    return jsonify({
        'id': farmer.id,
        'name': farmer.name,
        'phone': farmer.phone,
        'email': farmer.email,
        'place': farmer.place,
        'district': farmer.district,
        'state': farmer.state,
        'pincode': farmer.pincode,
        'farm_size_acres': farmer.farm_size_acres,
        'farming_experience_years': farmer.farming_experience_years,
        'preferred_language': farmer.preferred_language
    })

@farmer_bp.route('/api/farmer/crops', methods=['POST'])
@require_auth
def add_crop():
    data = request.get_json()
    clerk_user_id = request.current_user.get('sub')
    farmer = Farmer.get_by_clerk_id(clerk_user_id)
    
    if not farmer:
        return jsonify({'error': 'Farmer profile not found'}), 404
    
    crop_data = {
        'farmer_id': farmer.id,
        'crop_name': data.get('crop_name'),
        'variety': data.get('variety'),
        'area_acres': data.get('area_acres'),
        'planting_date': data.get('planting_date'),
        'expected_harvest_date': data.get('expected_harvest_date'),
        'season': data.get('season'),
        'irrigation_type': data.get('irrigation_type'),
        'farming_method': data.get('farming_method')
    }
    
    crop = Crop.create(crop_data)
    return jsonify({'success': True, 'crop_id': crop.id})

@farmer_bp.route('/api/farmer/crops', methods=['GET'])
@require_auth
def get_crops():
    clerk_user_id = request.current_user.get('sub')
    farmer = Farmer.get_by_clerk_id(clerk_user_id)
    
    if not farmer:
        return jsonify({'error': 'Farmer profile not found'}), 404
    
    crops = farmer.get_crops()
    return jsonify({'crops': crops})