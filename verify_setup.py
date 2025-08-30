#!/usr/bin/env python3
"""
Krishi Sahayak - Setup Verification Script
Run this to verify everything is working correctly
"""

import os
import sys
import importlib.util

def check_python_version():
    """Check if Python version is 3.11+"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 11:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} (Good)")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} (Need 3.11+)")
        return False

def check_dependencies():
    """Check if all required packages are installed"""
    required_packages = [
        'flask', 'flask_sqlalchemy', 'PIL', 'requests', 
        'werkzeug', 'sqlalchemy', 'gunicorn'
    ]
    
    missing = []
    for package in required_packages:
        try:
            if package == 'PIL':
                import PIL
            else:
                importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} (missing)")
            missing.append(package)
    
    return len(missing) == 0, missing

def check_files():
    """Check if all required files exist"""
    required_files = [
        'app.py', 'main.py', 'routes.py', 'models.py',
        'services/ai_service.py', 'services/weather_service.py', 'services/market_service.py',
        'templates/base.html', 'templates/dashboard.html', 'templates/scanner.html',
        'static/css/styles.css', 'static/js/app.js', 'static/manifest.json'
    ]
    
    missing = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} (missing)")
            missing.append(file_path)
    
    return len(missing) == 0, missing

def check_directories():
    """Check if required directories exist"""
    required_dirs = ['uploads', 'static', 'templates', 'services', 'instance']
    
    for directory in required_dirs:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            print(f"✅ Created directory: {directory}")
        else:
            print(f"✅ {directory}/")
    
    return True

def check_app_import():
    """Check if the Flask app can be imported"""
    try:
        from app import app
        print("✅ Flask app imports successfully")
        return True
    except Exception as e:
        print(f"❌ Flask app import failed: {str(e)}")
        return False

def check_database():
    """Check if database can be created"""
    try:
        from app import app, db
        with app.app_context():
            db.create_all()
        print("✅ Database creation successful")
        return True
    except Exception as e:
        print(f"❌ Database creation failed: {str(e)}")
        return False

def check_api_keys():
    """Check API key configuration"""
    groq_key = os.getenv('GROQ_API_KEY')
    weather_key = os.getenv('ACCUWEATHER_API_KEY', 'dM1leSojtDVmCX2hn97fMdqVVxh5r5OI')
    
    if groq_key:
        print("✅ Groq API key configured")
    else:
        print("❌ Groq API key missing")
    
    if weather_key:
        print("✅ AccuWeather API key configured")
    else:
        print("❌ AccuWeather API key missing")
    
    return bool(groq_key and weather_key)

def main():
    """Run all verification checks"""
    print("🔍 Krishi Sahayak - Setup Verification")
    print("="*50)
    
    checks = []
    
    print("\n📋 Checking Python Version...")
    checks.append(check_python_version())
    
    print("\n📦 Checking Dependencies...")
    deps_ok, missing_deps = check_dependencies()
    checks.append(deps_ok)
    if missing_deps:
        print(f"\n💡 Install missing packages: pip install {' '.join(missing_deps)}")
    
    print("\n📁 Checking Files...")
    files_ok, missing_files = check_files()
    checks.append(files_ok)
    if missing_files:
        print(f"\n❌ Missing files: {', '.join(missing_files)}")
    
    print("\n📂 Checking Directories...")
    checks.append(check_directories())
    
    print("\n🔧 Checking App Import...")
    checks.append(check_app_import())
    
    print("\n🗄️ Checking Database...")
    checks.append(check_database())
    
    print("\n🔑 Checking API Keys...")
    checks.append(check_api_keys())
    
    print("\n" + "="*50)
    passed = sum(checks)
    total = len(checks)
    
    if passed == total:
        print(f"🎉 All checks passed! ({passed}/{total})")
        print("\n🚀 Ready to start Krishi Sahayak!")
        print("   Run: python3 run.py")
        return 0
    else:
        print(f"⚠️ {total - passed} checks failed ({passed}/{total})")
        print("\n🔧 Please fix the issues above before starting the app")
        return 1

if __name__ == "__main__":
    sys.exit(main())