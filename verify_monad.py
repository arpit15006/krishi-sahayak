"""
Verify MONAD blockchain data directly
"""

from web3 import Web3

def verify_monad_data():
    w3 = Web3(Web3.HTTPProvider('https://testnet-rpc.monad.xyz'))
    
    print("🔍 MONAD Blockchain Verification")
    print("=" * 50)
    
    # Check recent transactions from our account
    account = "0x97F14D6031B64F9e82153A69458b5b9Af8248EE6"
    
    try:
        # Get latest block
        latest_block = w3.eth.get_block('latest')
        print(f"Latest block: {latest_block.number}")
        
        # Check our specific transaction
        tx_hash = "41a0e232b51b178222fcccec0684dd5e5e0050010a3157d89f40f744ccb4b6dc"
        
        tx = w3.eth.get_transaction(tx_hash)
        receipt = w3.eth.get_transaction_receipt(tx_hash)
        
        print(f"\n📋 Transaction Details:")
        print(f"Hash: {tx_hash}")
        print(f"Block: {tx.blockNumber}")
        print(f"From: {tx['from']}")
        print(f"To: {tx.to}")
        print(f"Status: {'✅ Success' if receipt.status == 1 else '❌ Failed'}")
        print(f"Gas Used: {receipt.gasUsed:,}")
        
        # Decode the data
        if tx.input and tx.input != '0x':
            try:
                decoded_data = bytes.fromhex(tx.input.hex()[2:]).decode('utf-8')
                print(f"\n📦 Stored Data:")
                print(f"Raw: {decoded_data}")
                
                if decoded_data.startswith('PASSPORT:'):
                    parts = decoded_data.split(':')
                    if len(parts) >= 4:
                        print(f"Crop: {parts[1]}")
                        print(f"Season: {parts[2]}")
                        print(f"IPFS: {parts[3]}")
                        print(f"Certificate: https://gateway.pinata.cloud/ipfs/{parts[3]}")
                        
            except Exception as e:
                print(f"Data decode error: {e}")
        
        print(f"\n🔗 Explorer Links:")
        print(f"Transaction: https://testnet-explorer.monad.xyz/tx/{tx_hash}")
        print(f"Account: https://testnet-explorer.monad.xyz/address/{account}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    verify_monad_data()