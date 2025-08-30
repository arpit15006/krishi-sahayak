"""
Additional passport routes for MONAD blockchain integration
"""

from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from services.blockchain.passport_service import passport_service
from models import DigitalPassport

passport_bp = Blueprint('passport', __name__, url_prefix='/passport')

@passport_bp.route('/verify/<token_id>')
def verify_passport(token_id):
    """Public passport verification page"""
    
    result = passport_service.verify_passport(token_id)
    
    if result['success']:
        passport_data = result['data']
        return render_template('passport_verify.html', 
                             passport=passport_data, 
                             token_id=token_id,
                             verified=True)
    else:
        return render_template('passport_verify.html', 
                             error=result['error'],
                             token_id=token_id,
                             verified=False)

@passport_bp.route('/api/status')
def blockchain_status():
    """API endpoint for blockchain status"""
    
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    status = passport_service.get_blockchain_status()
    return jsonify(status)

@passport_bp.route('/api/verify/<token_id>')
def api_verify_passport(token_id):
    """API endpoint for passport verification"""
    
    result = passport_service.verify_passport(token_id)
    return jsonify(result)

@passport_bp.route('/api/user-passports')
def api_user_passports():
    """API endpoint to get user's passports"""
    
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    result = passport_service.get_user_passports(session['user_id'])
    
    if result['success']:
        passports_data = []
        for passport in result['passports']:
            passports_data.append({
                'id': passport.id,
                'crop_type': passport.crop_type,
                'season': passport.season,
                'token_id': passport.nft_token_id,
                'ipfs_hash': passport.ipfs_hash,
                'created_at': passport.created_at.isoformat()
            })
        
        return jsonify({
            'success': True,
            'passports': passports_data
        })
    else:
        return jsonify(result), 500

@passport_bp.route('/qr/<int:passport_id>')
def generate_qr(passport_id):
    """Generate QR code for passport"""
    
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    
    passport = DigitalPassport.query.filter_by(
        id=passport_id, 
        user_id=session['user_id']
    ).first()
    
    if not passport:
        return jsonify({'error': 'Passport not found'}), 404
    
    qr_data = passport_service.generate_qr_data(passport)
    
    return jsonify({
        'success': True,
        'qr_data': qr_data,
        'verify_url': f"/passport/verify/{passport.nft_token_id}"
    })