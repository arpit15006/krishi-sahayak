"""
Enhanced Passport Service with MONAD Blockchain Integration
"""

import json
import uuid
from datetime import datetime
from supabase_models.digital_passport import DigitalPassport
from services.blockchain.monad_service import monad_service

class PassportService:
    
    @staticmethod
    def create_digital_passport(user_id, crop_type, season, user_data=None):
        """Create a new digital passport with blockchain integration"""
        
        try:
            # Prepare crop data
            crop_data = {
                'id': str(uuid.uuid4()),
                'crop_type': crop_type,
                'season': season,
                'area': 1.0,  # Default area, can be made configurable
                'practices': ['Organic farming', 'Sustainable irrigation'],
                'certifications': ['Quality Assured']
            }
            
            # Prepare farmer data
            farmer_data = {
                'name': user_data.get('full_name', 'Farmer') if user_data else 'Demo Farmer',
                'location': user_data.get('village_city', 'Unknown') if user_data else 'Demo Village'
            }
            
            # Try blockchain minting first
            blockchain_result = monad_service.mint_passport(crop_data, farmer_data)
            
            if blockchain_result.get('success'):
                # Blockchain minting successful
                passport_data = {
                    'farmer_id': user_id,
                    'crop_type': crop_type,
                    'season': season,
                    'nft_token_id': str(blockchain_result['token_id']),
                    'ipfs_hash': blockchain_result['ipfs_hash'],
                    'transaction_hash': blockchain_result['transaction_hash'],
                    'verified': False
                }
                
                passport = DigitalPassport.create(passport_data)
                print(f"Passport saved to database: {passport.id if passport else 'Failed'}")
                
                return {
                    'success': True,
                    'passport': passport,
                    'blockchain_data': blockchain_result,
                    'message': 'Digital passport created and minted on MONAD blockchain!'
                }
            else:
                # Blockchain failed - return error instead of mock
                print(f"Blockchain minting failed: {blockchain_result.get('error')}")
                return {
                    'success': False,
                    'error': f"Blockchain minting failed: {blockchain_result.get('error')}"
                }
                
        except Exception as e:
            print(f"Error creating passport: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'error': f'Failed to create passport: {str(e)}'
            }
    
    @staticmethod
    def get_user_passports(user_id):
        """Get all passports for a user"""
        try:
            passports = DigitalPassport.get_by_farmer_id(user_id)
            return {
                'success': True,
                'passports': passports
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to get passports: {str(e)}'
            }
    
    @staticmethod
    def verify_passport(token_id):
        """Verify a passport on the blockchain"""
        try:
            # Check if it's a mock token
            if token_id.startswith('MOCK-'):
                return {
                    'success': True,
                    'verified': True,
                    'data': {
                        'crop_type': 'Mock Crop',
                        'season': 'Mock Season',
                        'farmer': 'Mock Farmer',
                        'verified': True,
                        'mock': True
                    }
                }
            
            # Try blockchain verification
            blockchain_result = monad_service.get_passport_details(int(token_id))
            
            if 'error' not in blockchain_result:
                return {
                    'success': True,
                    'verified': True,
                    'data': blockchain_result
                }
            else:
                return {
                    'success': False,
                    'error': blockchain_result['error']
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Verification failed: {str(e)}'
            }
    
    @staticmethod
    def get_blockchain_status():
        """Get current blockchain connection status"""
        try:
            is_connected = monad_service.is_connected()
            
            status = {
                'connected': is_connected,
                'network': 'MONAD Testnet',
                'chain_id': 41454
            }
            
            if monad_service.account:
                balance = monad_service.get_balance(monad_service.account.address)
                status.update({
                    'account': monad_service.account.address,
                    'balance': f"{balance:.4f} MON"
                })
            
            return status
            
        except Exception as e:
            return {
                'connected': False,
                'error': str(e)
            }
    
    @staticmethod
    def generate_qr_data(passport):
        """Generate QR code data for passport verification"""
        base_url = 'http://localhost:8000'
        
        qr_data = {
            'url': f"{base_url}/passport/verify/{passport.nft_token_id}",
            'token_id': passport.nft_token_id,
            'crop_type': passport.crop_type,
            'season': passport.season,
            'created': passport.created_at.isoformat()
        }
        
        return json.dumps(qr_data)

# Global service instance
passport_service = PassportService()