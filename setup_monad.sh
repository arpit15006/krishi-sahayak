#!/bin/bash

echo "🚀 Setting up MONAD Blockchain Integration for Krishi Sahayak"
echo "============================================================"

# Install blockchain dependencies
echo "📦 Installing blockchain dependencies..."
pip install web3==6.11.3 eth-account==0.9.0 py-solc-x==1.12.0

# Create necessary directories
mkdir -p contracts/compiled

# Check environment variables
echo "🔧 Checking environment configuration..."

if [ -z "$MONAD_PRIVATE_KEY" ]; then
    echo "⚠️  MONAD_PRIVATE_KEY not set"
    echo "   Add to .env: MONAD_PRIVATE_KEY=your-private-key"
fi

if [ -z "$PINATA_API_KEY" ]; then
    echo "⚠️  PINATA_API_KEY not set"
    echo "   Add to .env: PINATA_API_KEY=your-pinata-key"
fi

if [ -z "$PINATA_SECRET_KEY" ]; then
    echo "⚠️  PINATA_SECRET_KEY not set"
    echo "   Add to .env: PINATA_SECRET_KEY=your-pinata-secret"
fi

# Test blockchain connection
echo "🔗 Testing MONAD connection..."
python3 -c "
try:
    from services.blockchain.monad_service import monad_service
    if monad_service.is_connected():
        print('✅ MONAD connection successful')
    else:
        print('❌ MONAD connection failed')
except Exception as e:
    print(f'⚠️  Connection test failed: {e}')
"

echo ""
echo "🎯 Next steps:"
echo "1. Add your API keys to .env file"
echo "2. Get testnet MON from faucet"
echo "3. Run: cd blockchain && python deploy.py"
echo "4. Test with: python blockchain/test_deployment.py"
echo ""
echo "✅ Setup complete!"