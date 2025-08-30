"""
Simplified passport service for testing without database dependencies
"""

import json
import uuid
from datetime import datetime
from services.blockchain.monad_service import monad_service

# In-memory storage for testing
passport_storage = []

class SimplePassportService:
    
    @staticmethod
    def create_digital_passport(user_id, crop_type, season, user_data=None):
        """Create a new digital passport with blockchain integration"""
        
        try:
            # Prepare crop data
            crop_data = {
                'id': str(uuid.uuid4()),
                'crop_type': crop_type,
                'season': season,
                'area': 1.0,
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
                    'id': str(uuid.uuid4()),
                    'farmer_id': user_id,
                    'crop_type': crop_type,
                    'season': season,
                    'nft_token_id': str(blockchain_result['token_id']),
                    'ipfs_hash': blockchain_result['ipfs_hash'],
                    'created_at': datetime.now().isoformat(),
                    'verified': False
                }
                
                # Store in memory for testing
                passport_storage.append(passport_data)
                
                return {
                    'success': True,
                    'passport': passport_data,
                    'blockchain_data': blockchain_result,
                    'message': 'Digital passport created and minted on MONAD blockchain!'
                }
            else:
                # Fallback to mock implementation
                print(f"Blockchain minting failed: {blockchain_result.get('error')}")
                
                passport_data = {
                    'id': str(uuid.uuid4()),
                    'farmer_id': user_id,
                    'crop_type': crop_type,
                    'season': season,
                    'nft_token_id': f"MOCK-{user_id[:8]}-{crop_type[:3].upper()}-{season[:4].upper()}",
                    'ipfs_hash': f"Qm{hash(str(user_id) + crop_type + season) % 10**44:044d}",
                    'created_at': datetime.now().isoformat(),
                    'verified': False
                }
                
                # Store in memory for testing
                passport_storage.append(passport_data)
                
                return {
                    'success': True,
                    'passport': passport_data,
                    'blockchain_data': None,
                    'message': 'Digital passport created (blockchain unavailable - using mock data)',
                    'warning': blockchain_result.get('error')
                }
                
        except Exception as e:
            print(f"Error creating passport: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to create passport: {str(e)}'
            }
    
    @staticmethod
    def get_user_passports(user_id):
        """Get all passports for a user"""
        try:
            user_passports = [p for p in passport_storage if p['farmer_id'] == user_id]
            return {
                'success': True,
                'passports': user_passports
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to get passports: {str(e)}'
            }
    
    @staticmethod
    def get_blockchain_status():
        """Get current blockchain connection status"""
        try:
            is_connected = monad_service.is_connected()
            
            status = {
                'connected': is_connected,
                'network': 'MONAD Testnet',
                'chain_id': 10143
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

# Global service instance
simple_passport_service = SimplePassportService()