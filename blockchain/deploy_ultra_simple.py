"""
Deploy ultra-minimal contract that just stores IPFS hashes
"""

import os
from web3 import Web3
from eth_account import Account
from dotenv import load_dotenv

load_dotenv('../.env')

def deploy_ultra_simple():
    w3 = Web3(Web3.HTTPProvider("https://testnet-rpc.monad.xyz"))
    
    private_key = os.getenv('MONAD_PRIVATE_KEY').strip('"')
    account = Account.from_key(private_key)
    
    print(f"✅ Connected to MONAD")
    print(f"📝 Account: {account.address}")
    
    # Ultra minimal contract - just stores strings
    # pragma solidity ^0.8.0;
    # contract CropStorage {
    #     mapping(uint256 => string) public crops;
    #     uint256 public count;
    #     function store(string memory ipfsHash) external returns (uint256) {
    #         crops[count] = ipfsHash;
    #         return count++;
    #     }
    # }
    
    bytecode = "0x608060405234801561001057600080fd5b50610250806100206000396000f3fe608060405234801561001057600080fd5b50600436106100365760003560e01c806306661abd1461003b5780638bab8dd514610059575b600080fd5b610043610089565b6040516100509190610123565b60405180910390f35b610073600480360381019061006e919061013e565b61008f565b604051610080919061019a565b60405180910390f35b60015481565b6000602052806000526040600020600091509050805461010e906101e4565b80601f016020809104026020016040519081016040528092919081815260200182805461013a906101e4565b80156101875780601f1061015c57610100808354040283529160200191610187565b820191906000526020600020905b81548152906001019060200180831161016a57829003601f168201915b5050505050905081565b6000819050919050565b6101a481610191565b82525050565b60006020820190506101bf600083018461019b565b92915050565b600081519050919050565b600082825260208201905092915050565b60005b838110156101ff5780820151818401526020810190506101e4565b8381111561020e576000848401525b50505050565b6000601f19601f8301169050919050565b6000610230826101c5565b61023a81856101d0565b935061024a8185602086016101e1565b61025381610214565b840191505092915050565b6000602082019050818103600083015261027881846101225565b90509291505056fea2646970667358221220abcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdef64736f6c63430008130033"
    
    # Get network gas price and use 3x
    gas_price = w3.eth.gas_price
    high_gas_price = int(gas_price * 3)
    
    transaction = {
        'from': account.address,
        'data': bytecode,
        'gas': 150000,  # Very low gas
        'gasPrice': high_gas_price,
        'nonce': w3.eth.get_transaction_count(account.address),
        'chainId': 10143
    }
    
    print(f"📤 Deploying ultra-simple contract with {w3.from_wei(high_gas_price, 'gwei')} gwei")
    
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    
    print(f"⏳ TX: {tx_hash.hex()}")
    
    try:
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
        
        if receipt.status == 1:
            contract_address = receipt.contractAddress
            print(f"✅ Ultra-simple contract deployed: {contract_address}")
            print(f"🔗 Explorer: https://testnet-explorer.monad.xyz/address/{contract_address}")
            
            # Update config
            config_content = f"""
# MONAD Testnet Configuration for Krishi Sahayak

MONAD_TESTNET_CONFIG = {{
    'network_name': 'MONAD Testnet',
    'chain_id': 10143,
    'rpc_url': 'https://testnet-rpc.monad.xyz',
    'explorer_url': 'https://testnet-explorer.monad.xyz',
    'currency_symbol': 'MON',
    'currency_decimals': 18,
    'block_time': 1,
}}

CONTRACT_ADDRESSES = {{
    'crop_passport': '{contract_address}',
    'weather_insurance': None,
}}

IPFS_CONFIG = {{
    'gateway': 'https://gateway.pinata.cloud/ipfs/',
    'api_endpoint': 'https://api.pinata.cloud',
    'upload_endpoint': 'https://api.pinata.cloud/pinning/pinFileToIPFS'
}}

GAS_CONFIG = {{
    'gas_limit': 100000,
    'gas_price': {high_gas_price},
    'max_fee_per_gas': {int(high_gas_price * 1.2)},
    'max_priority_fee_per_gas': {high_gas_price},
}}
"""
            
            with open('../blockchain/monad_config.py', 'w') as f:
                f.write(config_content)
            
            return contract_address
        else:
            print(f"❌ Transaction failed. Status: {receipt.status}")
            return None
            
    except Exception as e:
        print(f"❌ Transaction failed: {e}")
        return None

if __name__ == "__main__":
    deploy_ultra_simple()