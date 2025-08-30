#!/usr/bin/env python3
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "krishi-sahayak-secret-key")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///krishi_sahayak.db")
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

db = SQLAlchemy(app)

# Define models directly here
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    village_city = db.Column(db.String(100), nullable=False)
    pin_code = db.Column(db.String(6), nullable=False)
    main_crops = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_verified = db.Column(db.Boolean, default=False)

class ScanResult(db.Model):
    __tablename__ = 'scan_results'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    image_filename = db.Column(db.String(255), nullable=False)
    diagnosis = db.Column(db.Text, nullable=False)
    treatment_advice = db.Column(db.Text, nullable=False)
    weather_warning = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class DigitalPassport(db.Model):
    __tablename__ = 'digital_passports'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    crop_type = db.Column(db.String(100), nullable=False)
    season = db.Column(db.String(50), nullable=False)
    nft_token_id = db.Column(db.String(100))
    ipfs_hash = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Import routes after models are defined
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from routes import bp as main_bp
app.register_blueprint(main_bp)

# Register Supabase routes
try:
    from routes.farmer_routes import farmer_bp
    app.register_blueprint(farmer_bp)
except ImportError:
    pass

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=3000, debug=True)