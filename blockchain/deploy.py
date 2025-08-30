"""
Deployment script for Krishi Sahayak smart contracts on MONAD Testnet
"""

import json
import os
from web3 import Web3
from eth_account import Account
from solcx import compile_source, install_solc
from dotenv import load_dotenv
from monad_config import MONAD_TESTNET_CONFIG, GAS_CONFIG

# Load environment variables
load_dotenv('../.env')

def compile_contract():
    """Compile the CropPassport smart contract"""
    
    # Install Solidity compiler
    try:
        install_solc('0.8.19')
    except Exception as e:
        print(f"Installing Solidity compiler: {e}")
        install_solc('0.8.19', show_progress=True)
    
    # Read contract source
    with open('../contracts/SimpleCropPassport.sol', 'r') as f:
        contract_source = f.read()
    
    # Compile contract
    compiled_sol = compile_source(contract_source)
    contract_interface = compiled_sol['<stdin>:SimpleCropPassport']
    
    return contract_interface

def deploy_contract():
    """Deploy CropPassport contract to MONAD Testnet"""
    
    # Connect to MONAD
    w3 = Web3(Web3.HTTPProvider(MONAD_TESTNET_CONFIG['rpc_url']))
    
    if not w3.is_connected():
        print("❌ Failed to connect to MONAD Testnet")
        return None
    
    print("✅ Connected to MONAD Testnet")
    
    # Load account
    private_key = os.getenv('MONAD_PRIVATE_KEY')
    if not private_key:
        print("❌ MONAD_PRIVATE_KEY not found in environment")
        return None
    
    account = Account.from_key(private_key)
    print(f"📝 Deploying from: {account.address}")
    
    # Check balance
    balance = w3.eth.get_balance(account.address)
    balance_eth = w3.from_wei(balance, 'ether')
    print(f"💰 Balance: {balance_eth} MON")
    
    if balance_eth < 0.01:
        print("❌ Insufficient balance for deployment")
        return None
    
    # Compile contract
    print("🔨 Compiling contract...")
    contract_interface = compile_contract()
    
    # Create contract instance
    contract = w3.eth.contract(
        abi=contract_interface['abi'],
        bytecode=contract_interface['bin']
    )
    
    # Build deployment transaction
    transaction = contract.constructor().build_transaction({
        'from': account.address,
        'gas': GAS_CONFIG['gas_limit'],
        'gasPrice': GAS_CONFIG['gas_price'],
        'nonce': w3.eth.get_transaction_count(account.address),
        'chainId': MONAD_TESTNET_CONFIG['chain_id']
    })
    
    print("📤 Deploying contract...")
    
    # Sign and send transaction
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    
    print(f"⏳ Transaction hash: {tx_hash.hex()}")
    print("⏳ Waiting for confirmation...")
    
    # Wait for deployment
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    
    if receipt.status == 1:
        contract_address = receipt.contractAddress
        print(f"✅ Contract deployed successfully!")
        print(f"📍 Contract address: {contract_address}")
        print(f"🔗 Explorer: {MONAD_TESTNET_CONFIG['explorer_url']}/address/{contract_address}")
        
        # Save contract data
        contract_data = {
            'address': contract_address,
            'abi': contract_interface['abi'],
            'bytecode': contract_interface['bin'],
            'deployment_tx': tx_hash.hex(),
            'deployment_block': receipt.blockNumber,
            'gas_used': receipt.gasUsed
        }
        
        with open('../contracts/CropPassport.json', 'w') as f:
            json.dump(contract_data, f, indent=2)
        
        # Update config
        from monad_config import CONTRACT_ADDRESSES
        CONTRACT_ADDRESSES['crop_passport'] = contract_address
        
        print("💾 Contract data saved to CropPassport.json")
        return contract_address
    else:
        print("❌ Deployment failed")
        return None

if __name__ == "__main__":
    print("🚀 Deploying Krishi Sahayak to MONAD Testnet")
    print("=" * 50)
    
    contract_address = deploy_contract()
    
    if contract_address:
        print("\n🎉 Deployment completed successfully!")
        print(f"Contract Address: {contract_address}")
        print("\nNext steps:")
        print("1. Update CONTRACT_ADDRESSES in monad_config.py")
        print("2. Add MONAD_PRIVATE_KEY to .env file")
        print("3. Add PINATA_API_KEY and PINATA_SECRET_KEY for IPFS")
        print("4. Test the contract with test_deployment.py")
    else:
        print("\n❌ Deployment failed!")
        print("Check your MONAD_PRIVATE_KEY and network connection")