# Supabase-compatible models (no SQLAlchemy needed)
from datetime import datetime

class User:
    """User model for Supabase integration"""
    def __init__(self, data=None):
        if data:
            self.id = data.get('id')
            self.phone_number = data.get('phone_number')
            self.full_name = data.get('full_name')
            self.village_city = data.get('village_city')
            self.pin_code = data.get('pin_code')
            self.main_crops = data.get('main_crops', '[]')
            self.created_at = data.get('created_at')
            self.is_verified = data.get('is_verified', False)

class ScanResult:
    """Scan result model for Supabase integration"""
    def __init__(self, data=None):
        if data:
            self.id = data.get('id')
            self.user_id = data.get('user_id')
            self.image_filename = data.get('image_filename')
            self.diagnosis = data.get('diagnosis')
            self.treatment_advice = data.get('treatment_advice')
            self.weather_warning = data.get('weather_warning')
            self.created_at = data.get('created_at')

class DigitalPassport:
    """Digital passport model for Supabase integration"""
    def __init__(self, data=None):
        if data:
            self.id = data.get('id')
            self.user_id = data.get('user_id')
            self.crop_type = data.get('crop_type')
            self.season = data.get('season')
            self.nft_token_id = data.get('nft_token_id')
            self.ipfs_hash = data.get('ipfs_hash')
            self.created_at = data.get('created_at')
