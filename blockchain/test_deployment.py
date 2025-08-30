"""
Test MONAD blockchain deployment and integration
"""

import os
from web3 import Web3
from services.blockchain.monad_service import monad_service
from services.blockchain.passport_service import passport_service

def test_connection():
    """Test MONAD network connection"""
    print("🔗 Testing MONAD connection...")
    
    if monad_service.is_connected():
        print("✅ Connected to MONAD Testnet")
        
        if monad_service.account:
            balance = monad_service.get_balance(monad_service.account.address)
            print(f"💰 Account: {monad_service.account.address}")
            print(f"💰 Balance: {balance:.4f} MON")
            
            if balance < 0.01:
                print("⚠️  Low balance - get testnet MON from faucet")
        else:
            print("⚠️  No private key configured")
    else:
        print("❌ Failed to connect to MONAD")

def test_passport_creation():
    """Test passport creation flow"""
    print("\n📜 Testing passport creation...")
    
    crop_data = {
        'crop_type': 'Rice',
        'season': 'Kharif 2024',
        'area': 2.5
    }
    
    farmer_data = {
        'name': 'Test Farmer',
        'location': 'Test Village'
    }
    
    result = passport_service.create_digital_passport(
        user_id=1,
        crop_type=crop_data['crop_type'],
        season=crop_data['season'],
        user_data=farmer_data
    )
    
    if result['success']:
        print("✅ Passport created successfully")
        if result.get('blockchain_data'):
            print(f"🔗 Token ID: {result['blockchain_data']['token_id']}")
            print(f"📎 IPFS: {result['blockchain_data']['ipfs_hash']}")
        else:
            print("⚠️  Created as mock (blockchain unavailable)")
    else:
        print(f"❌ Failed: {result['error']}")

if __name__ == "__main__":
    print("🧪 MONAD Integration Test")
    print("=" * 40)
    
    test_connection()
    test_passport_creation()
    
    print("\n✅ Test completed")