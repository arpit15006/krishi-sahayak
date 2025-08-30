"""
Mock deployment for testing MONAD integration
"""

import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('../.env')

def create_mock_deployment():
    """Create mock contract deployment for testing"""
    
    # Mock contract address (for testing)
    mock_contract_address = "0x1234567890123456789012345678901234567890"
    
    # Create mock contract ABI
    mock_abi = [
        {
            "inputs": [
                {"name": "cropType", "type": "string"},
                {"name": "season", "type": "string"},
                {"name": "ipfsHash", "type": "string"},
                {"name": "location", "type": "string"},
                {"name": "area", "type": "uint256"}
            ],
            "name": "mintPassport",
            "outputs": [{"name": "", "type": "uint256"}],
            "type": "function"
        },
        {
            "inputs": [{"name": "tokenId", "type": "uint256"}],
            "name": "getPassport",
            "outputs": [
                {"name": "cropType", "type": "string"},
                {"name": "season", "type": "string"},
                {"name": "ipfsHash", "type": "string"},
                {"name": "farmer", "type": "address"},
                {"name": "timestamp", "type": "uint256"},
                {"name": "verified", "type": "bool"},
                {"name": "location", "type": "string"},
                {"name": "area", "type": "uint256"}
            ],
            "type": "function"
        }
    ]
    
    # Save mock contract data
    contract_data = {
        'address': mock_contract_address,
        'abi': mock_abi,
        'network': 'MONAD Testnet (Mock)',
        'chain_id': 10143,
        'deployed': True,
        'mock': True
    }
    
    with open('../contracts/CropPassport.json', 'w') as f:
        json.dump(contract_data, f, indent=2)
    
    print("🎭 Mock deployment created!")
    print(f"📍 Mock Contract: {mock_contract_address}")
    print("✅ System ready for testing with fallback mode")
    
    return mock_contract_address

if __name__ == "__main__":
    print("🎭 Creating Mock MONAD Deployment")
    print("=" * 40)
    
    contract_address = create_mock_deployment()
    
    print(f"\n✅ Mock deployment ready!")
    print(f"Contract: {contract_address}")
    print("\n📝 The system will:")
    print("1. Try real blockchain operations first")
    print("2. Fall back to mock data if blockchain unavailable")
    print("3. Work seamlessly for testing")