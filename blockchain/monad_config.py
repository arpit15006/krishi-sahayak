
# MONAD Testnet Configuration for Krishi Sahayak

MONAD_TESTNET_CONFIG = {
    'network_name': 'MONAD Testnet',
    'chain_id': 10143,
    'rpc_url': 'https://testnet-rpc.monad.xyz',
    'explorer_url': 'https://testnet-explorer.monad.xyz',
    'currency_symbol': 'MON',
    'currency_decimals': 18,
    'block_time': 1,
}

CONTRACT_ADDRESSES = {
    'crop_passport': '0xF011419a5086dD4C3A112EFafD1115d752d5a900',
    'weather_insurance': None,
}

IPFS_CONFIG = {
    'gateway': 'https://gateway.pinata.cloud/ipfs/',
    'api_endpoint': 'https://api.pinata.cloud',
    'upload_endpoint': 'https://api.pinata.cloud/pinning/pinFileToIPFS'
}

GAS_CONFIG = {
    'gas_limit': 500000,
    'gas_price': 50000000000,
    'max_fee_per_gas': 100000000000,
    'max_priority_fee_per_gas': 50000000000,
}
