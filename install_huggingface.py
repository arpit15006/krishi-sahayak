#!/usr/bin/env python3
"""Install Hugging Face dependencies for local AI vision"""

import subprocess
import sys

def install_dependencies():
    """Install required packages for Hugging Face vision"""
    packages = [
        'transformers',
        'torch',
        'torchvision', 
        'pillow'
    ]
    
    print("🤖 Installing Hugging Face AI Vision dependencies...")
    print("This will enable local plant disease analysis without API limits!")
    print()
    
    for package in packages:
        print(f"📦 Installing {package}...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✅ {package} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {package}: {e}")
            return False
        print()
    
    print("🎉 All dependencies installed!")
    print("🌱 Krishi Sahayak now has local AI vision analysis!")
    print()
    print("🧪 Testing installation...")
    
    try:
        import transformers
        import torch
        import torchvision
        from PIL import Image
        print("✅ All imports successful!")
        print("🚀 Ready for local plant disease analysis!")
        return True
    except ImportError as e:
        print(f"❌ Import test failed: {e}")
        return False

if __name__ == "__main__":
    success = install_dependencies()
    if success:
        print("\n🎯 Next steps:")
        print("1. Restart your application")
        print("2. Upload plant images for analysis")
        print("3. Get instant AI diagnosis without API limits!")
    else:
        print("\n⚠️ Installation failed. Please check your Python environment.")
    
    sys.exit(0 if success else 1)