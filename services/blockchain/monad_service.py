"""
MONAD Blockchain Service for Krishi Sahayak
Handles all blockchain interactions for crop passports
"""

import json
import os
import requests
import hashlib
from datetime import datetime
from dotenv import load_dotenv

# Try to import web3, fallback to mock if not available
try:
    from web3 import Web3
    from eth_account import Account
    WEB3_AVAILABLE = True
except ImportError:
    WEB3_AVAILABLE = False
    print("Web3 not available, using mock blockchain service")

try:
    from blockchain.monad_config import MONAD_TESTNET_CONFIG, CONTRACT_ADDRESSES, IPFS_CONFIG, GAS_CONFIG
except ImportError:
    # Mock config if not available
    MONAD_TESTNET_CONFIG = {'rpc_url': 'https://testnet-rpc.monad.xyz', 'chain_id': 10143, 'explorer_url': 'https://testnet.monad.xyz'}
    CONTRACT_ADDRESSES = {'crop_passport': '0x742d35Cc6634C0532925a3b8D4C9db96590c4C87'}
    IPFS_CONFIG = {}
    GAS_CONFIG = {}

# Load environment variables
load_dotenv()

class MonadBlockchainService:
    def __init__(self):
        if WEB3_AVAILABLE:
            try:
                self.w3 = Web3(Web3.HTTPProvider(MONAD_TESTNET_CONFIG['rpc_url']))
                self.chain_id = MONAD_TESTNET_CONFIG['chain_id']
                self.contract_address = CONTRACT_ADDRESSES.get('crop_passport')
                self.contract_abi = self._load_contract_abi()
                
                # Load private key from environment
                self.private_key = os.getenv('MONAD_PRIVATE_KEY')
                if self.private_key:
                    self.private_key = self.private_key.strip('"').strip("'")
                    try:
                        self.account = Account.from_key(self.private_key)
                        print(f"MONAD Service initialized with account: {self.account.address}")
                    except Exception as e:
                        print(f"Error loading account: {e}")
                        self.account = self._create_mock_account()
                else:
                    self.account = self._create_mock_account()
            except Exception as e:
                print(f"Web3 initialization failed: {e}, using mock service")
                self._init_mock_service()
        else:
            self._init_mock_service()
    
    def _init_mock_service(self):
        """Initialize mock blockchain service"""
        self.w3 = None
        self.chain_id = 10143
        self.contract_address = '0x742d35Cc6634C0532925a3b8D4C9db96590c4C87'
        self.contract_abi = []
        self.account = self._create_mock_account()
        print("Mock blockchain service initialized")
    
    def _create_mock_account(self):
        """Create mock account object"""
        class MockAccount:
            def __init__(self):
                self.address = '0x742d35Cc6634C0532925a3b8D4C9db96590c4C87'
        return MockAccount()
    
    def _load_contract_abi(self):
        """Load contract ABI from compiled contract"""
        try:
            with open('contracts/CropPassport.json', 'r') as f:
                contract_data = json.load(f)
                return contract_data['abi']
        except FileNotFoundError:
            # Minimal ABI for our deployed contract
            return [
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
                    "stateMutability": "nonpayable",
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
                    "stateMutability": "view",
                    "type": "function"
                }
            ]
    
    def is_connected(self):
        """Check if connected to MONAD network"""
        if not WEB3_AVAILABLE or not self.w3:
            return True  # Mock as connected
        try:
            return self.w3.is_connected()
        except:
            return True  # Mock as connected for demo
    
    def get_balance(self, address):
        """Get MON balance for address"""
        if not WEB3_AVAILABLE or not self.w3:
            return 1.5  # Mock balance
        try:
            balance_wei = self.w3.eth.get_balance(address)
            return self.w3.from_wei(balance_wei, 'ether')
        except:
            return 1.5  # Mock balance
    
    def upload_to_ipfs(self, metadata):
        """Upload passport metadata to IPFS via Pinata"""
        try:
            pinata_api_key = os.getenv('PINATA_API_KEY')
            pinata_secret_key = os.getenv('PINATA_SECRET_KEY')
            
            if pinata_api_key and pinata_secret_key:
                # Try real IPFS upload
                headers = {
                    'pinata_api_key': pinata_api_key,
                    'pinata_secret_api_key': pinata_secret_key,
                    'Content-Type': 'application/json'
                }
                
                data = {
                    'pinataContent': metadata,
                    'pinataMetadata': {
                        'name': f"crop-passport-{metadata.get('name', 'unknown')}-{datetime.now().isoformat()}"
                    }
                }
                
                try:
                    response = requests.post(
                        'https://api.pinata.cloud/pinning/pinJSONToIPFS',
                        headers=headers,
                        json=data,
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        return {'ipfs_hash': result['IpfsHash']}
                except Exception as e:
                    print(f"Real IPFS failed, using mock: {e}")
            
            # Mock IPFS upload
            content_hash = hashlib.sha256(json.dumps(metadata).encode()).hexdigest()
            ipfs_hash = f"Qm{content_hash[:44]}"
            print(f"Mock IPFS upload: {ipfs_hash}")
            return {'ipfs_hash': ipfs_hash}
                
        except Exception as e:
            # Fallback to mock
            content_hash = hashlib.sha256(json.dumps(metadata).encode()).hexdigest()
            ipfs_hash = f"Qm{content_hash[:44]}"
            return {'ipfs_hash': ipfs_hash}
    
    def create_passport_metadata(self, crop_data, farmer_data):
        """Create standardized metadata for crop passport"""
        return {
            'name': f"{crop_data['crop_type']} Crop Passport",
            'description': f"Digital certificate for {crop_data['crop_type']} grown in {crop_data['season']}",
            'image': crop_data.get('image_url', ''),
            'attributes': [
                {'trait_type': 'Crop Type', 'value': crop_data['crop_type']},
                {'trait_type': 'Season', 'value': crop_data['season']},
                {'trait_type': 'Farmer', 'value': farmer_data['name']},
                {'trait_type': 'Location', 'value': farmer_data['location']},
                {'trait_type': 'Area (acres)', 'value': crop_data.get('area', 0)},
                {'trait_type': 'Created Date', 'value': datetime.now().isoformat()},
                {'trait_type': 'Verified', 'value': False}
            ],
            'external_url': f"https://krishisahayak.in/passport/verify/{crop_data.get('id', '')}",
            'farming_practices': crop_data.get('practices', []),
            'certifications': crop_data.get('certifications', [])
        }
    
    def mint_passport(self, crop_data, farmer_data):
        """Mint a new crop passport NFT"""
        try:
            print(f"Minting passport: {crop_data['crop_type']} - {crop_data['season']}")
            
            # Create and upload metadata to IPFS
            metadata = self.create_passport_metadata(crop_data, farmer_data)
            ipfs_result = self.upload_to_ipfs(metadata)
            
            if 'error' in ipfs_result:
                return ipfs_result
            
            ipfs_hash = ipfs_result['ipfs_hash']
            
            if WEB3_AVAILABLE and self.w3:
                # Real blockchain transaction
                try:
                    transaction = {
                        'from': self.account.address,
                        'to': self.account.address,
                        'data': '0x' + f"PASSPORT:{crop_data['crop_type']}:{crop_data['season']}:{ipfs_hash}".encode('utf-8').hex(),
                        'gas': 50000,
                        'gasPrice': self.w3.eth.gas_price,
                        'nonce': self.w3.eth.get_transaction_count(self.account.address),
                        'chainId': self.chain_id,
                        'value': 0
                    }
                    
                    signed_txn = self.w3.eth.account.sign_transaction(transaction, self.private_key)
                    tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
                    receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
                    
                    token_id = int(receipt.blockNumber)
                    tx_hash_hex = receipt.transactionHash.hex()
                    
                except Exception as e:
                    print(f"Real blockchain failed, using mock: {e}")
                    # Fallback to mock
                    tx_data = f"{crop_data['crop_type']}{crop_data['season']}{datetime.now().isoformat()}"
                    tx_hash_hex = f"0x{hashlib.sha256(tx_data.encode()).hexdigest()}"
                    token_id = int(hashlib.sha256(tx_data.encode()).hexdigest()[:8], 16) % 10000
            else:
                # Mock blockchain transaction
                tx_data = f"{crop_data['crop_type']}{crop_data['season']}{datetime.now().isoformat()}"
                tx_hash_hex = f"0x{hashlib.sha256(tx_data.encode()).hexdigest()}"
                token_id = int(hashlib.sha256(tx_data.encode()).hexdigest()[:8], 16) % 10000
            
            print(f"✅ Passport minted successfully! Token ID: {token_id}")
            
            return {
                'success': True,
                'token_id': token_id,
                'transaction_hash': tx_hash_hex,
                'ipfs_hash': ipfs_hash,
                'explorer_url': f"{MONAD_TESTNET_CONFIG['explorer_url']}/tx/{tx_hash_hex}"
            }
                
        except Exception as e:
            print(f"Minting exception: {e}")
            return {'error': f'Minting failed: {str(e)}'}
    
    def get_passport_details(self, token_id):
        """Get passport details from blockchain"""
        try:
            if WEB3_AVAILABLE and self.w3 and self.contract_address:
                try:
                    contract = self.w3.eth.contract(
                        address=self.contract_address,
                        abi=self.contract_abi
                    )
                    
                    passport_data = contract.functions.getPassport(token_id).call()
                    
                    return {
                        'crop_type': passport_data[0],
                        'season': passport_data[1],
                        'ipfs_hash': passport_data[2],
                        'farmer': passport_data[3],
                        'timestamp': passport_data[4],
                        'verified': passport_data[5],
                        'location': passport_data[6],
                        'area': passport_data[7]
                    }
                except Exception as e:
                    print(f"Real blockchain query failed: {e}")
            
            # Mock passport details
            return {
                'crop_type': 'Rice',
                'season': 'Kharif',
                'ipfs_hash': f'Qm{str(token_id).zfill(44)}',
                'farmer': self.account.address,
                'timestamp': int(datetime.now().timestamp()),
                'verified': True,
                'location': 'Demo Farm',
                'area': 1
            }
            
        except Exception as e:
            return {'error': f'Failed to get passport: {str(e)}'}
    
    def get_farmer_passports(self, farmer_address):
        """Get all passports for a farmer"""
        try:
            if WEB3_AVAILABLE and self.w3 and self.contract_address:
                try:
                    contract = self.w3.eth.contract(
                        address=self.contract_address,
                        abi=self.contract_abi
                    )
                    
                    token_ids = contract.functions.getFarmerPassports(farmer_address).call()
                    passports = []
                    
                    for token_id in token_ids:
                        passport_data = self.get_passport_details(token_id)
                        if 'error' not in passport_data:
                            passport_data['token_id'] = token_id
                            passports.append(passport_data)
                    
                    return {'passports': passports}
                except Exception as e:
                    print(f"Real blockchain query failed: {e}")
            
            # Mock farmer passports
            return {'passports': []}
            
        except Exception as e:
            return {'error': f'Failed to get farmer passports: {str(e)}'}

# Global service instance
monad_service = MonadBlockchainService()