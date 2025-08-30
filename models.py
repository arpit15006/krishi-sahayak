from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    village_city = db.Column(db.String(100), nullable=False)
    pin_code = db.Column(db.String(6), nullable=False)
    main_crops = db.Column(db.Text, nullable=False)  # JSON string of crop list
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
