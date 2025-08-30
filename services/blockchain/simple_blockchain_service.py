"""
Simple blockchain service for hackathon demo
Provides all blockchain functionality without external dependencies
"""

import json
import uuid
from datetime import datetime
import hashlib

class SimpleBlockchainService:
    def __init__(self):
        self.connected = True
        self.account_address = "0x742d35Cc6634C0532925a3b8D4C9db96590c4C87"
        self.balance = 1.5
        
    def is_connected(self):
        return True
    
    def get_balance(self, address):
        return self.balance
    
    def upload_to_ipfs(self, metadata):
        """Simulate IPFS upload"""
        content_hash = hashlib.sha256(json.dumps(metadata).encode()).hexdigest()
        ipfs_hash = f"Qm{content_hash[:44]}"
        return {'ipfs_hash': ipfs_hash}
    
    def mint_passport(self, crop_data, farmer_data):
        """Simulate blockchain passport minting"""
        try:
            # Create metadata
            metadata = {
                'name': f"{crop_data['crop_type']} Crop Passport",
                'description': f"Digital certificate for {crop_data['crop_type']} grown in {crop_data['season']}",
                'attributes': [
                    {'trait_type': 'Crop Type', 'value': crop_data['crop_type']},
                    {'trait_type': 'Season', 'value': crop_data['season']},
                    {'trait_type': 'Farmer', 'value': farmer_data['name']},
                    {'trait_type': 'Location', 'value': farmer_data['location']},
                    {'trait_type': 'Created Date', 'value': datetime.now().isoformat()}
                ]
            }
            
            # Upload to IPFS
            ipfs_result = self.upload_to_ipfs(metadata)
            ipfs_hash = ipfs_result['ipfs_hash']
            
            # Generate transaction hash
            tx_data = f"{crop_data['crop_type']}{crop_data['season']}{datetime.now().isoformat()}"
            tx_hash = f"0x{hashlib.sha256(tx_data.encode()).hexdigest()}"
            
            # Generate token ID
            token_id = int(hashlib.sha256(tx_data.encode()).hexdigest()[:8], 16) % 10000
            
            return {
                'success': True,
                'token_id': token_id,
                'transaction_hash': tx_hash,
                'ipfs_hash': ipfs_hash,
                'explorer_url': f"https://testnet.monad.xyz/tx/{tx_hash}"
            }
            
        except Exception as e:
            return {'error': f'Minting failed: {str(e)}'}

# Global service instance
simple_blockchain_service = SimpleBlockchainService()