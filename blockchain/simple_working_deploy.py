"""
Deploy minimal working contract
"""

import json
import os
from web3 import Web3
from eth_account import Account
from dotenv import load_dotenv

load_dotenv('../.env')

def deploy_minimal():
    w3 = Web3(Web3.HTTPProvider("https://testnet-rpc.monad.xyz"))
    
    private_key = os.getenv('MONAD_PRIVATE_KEY').strip('"')
    account = Account.from_key(private_key)
    
    # Minimal working contract bytecode
    bytecode = "0x608060405234801561001057600080fd5b50336000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555061041c806100606000396000f3fe608060405234801561001057600080fd5b50600436106100415760003560e01c80638da5cb5b14610046578063a0712d6814610064578063c87b56dd14610080575b600080fd5b61004e6100b0565b60405161005b91906102c1565b60405180910390f35b61007e600480360381019061007991906102dc565b6100d4565b005b61009a60048036038101906100959190610309565b610178565b6040516100a79190610336565b60405180910390f35b60008054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b60016000815480929190600101919050555060405180608001604052808381526020018281526020013373ffffffffffffffffffffffffffffffffffffffff168152602001428152506002600060015481526020019081526020016000206000820151816000015560208201518160010155604082015181600201906101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555060608201518160030155905050505050565b606060405180608001604052806002600084815260200190815260200160002060000154815260200160026000848152602001908152602001600020600101548152602001600260008481526020019081526020016000206002015f9054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001600260008481526020019081526020016000206003015481525090506040518060800160405280826000015181526020018260200151815260200182604001518152602001826060015181525092505050919050565b600073ffffffffffffffffffffffffffffffffffffffff82169050919050565b600061026c82610241565b9050919050565b61027c81610261565b82525050565b60006020820190506102976000830184610273565b92915050565b6000819050919050565b6102b08161029d565b82525050565b60006020820190506102cb60008301846102a7565b92915050565b6102da8161029d565b81146102e557600080fd5b50565b6000813590506102f7816102d1565b92915050565b600060208284031215610313576103126102dc565b5b6000610321848285016102e8565b91505092915050565b600081519050919050565b600082825260208201905092915050565b6000601f19601f8301169050919050565b600061036282610330565b61036c818561033b565b935061037c81856020860161034c565b6103858161034c565b840191505092915050565b600060208201905081810360008301526103aa8184610357565b90509291505056fea2646970667358221220abcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdef64736f6c63430008130033"
    
    transaction = {
        'from': account.address,
        'data': bytecode,
        'gas': 500000,
        'gasPrice': 50000000000,
        'nonce': w3.eth.get_transaction_count(account.address),
        'chainId': 10143
    }
    
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    
    print(f"TX: {tx_hash.hex()}")
    
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    
    if receipt.status == 1:
        print(f"✅ Deployed: {receipt.contractAddress}")
        
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
    'crop_passport': '{receipt.contractAddress}',
    'weather_insurance': None,
}}

IPFS_CONFIG = {{
    'gateway': 'https://gateway.pinata.cloud/ipfs/',
    'api_endpoint': 'https://api.pinata.cloud',
    'upload_endpoint': 'https://api.pinata.cloud/pinning/pinFileToIPFS'
}}

GAS_CONFIG = {{
    'gas_limit': 500000,
    'gas_price': 50000000000,
    'max_fee_per_gas': 100000000000,
    'max_priority_fee_per_gas': 50000000000,
}}
"""
        
        with open('../blockchain/monad_config.py', 'w') as f:
            f.write(config_content)
        
        return receipt.contractAddress
    else:
        print("❌ Failed")
        return None

if __name__ == "__main__":
    deploy_minimal()