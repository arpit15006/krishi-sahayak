import qrcode
import json
import os
from datetime import datetime
from io import BytesIO
import base64

class SupplyChainService:
    def __init__(self):
        self.base_url = "https://krishisahayak.in/track"  # Replace with actual domain
    
    def create_product_qr(self, farmer_data, crop_data, passport_id):
        """Create QR code for product tracking"""
        
        # Create tracking data
        tracking_data = {
            "passport_id": passport_id,
            "farmer": {
                "name": farmer_data.get('full_name', 'Unknown Farmer'),
                "village": farmer_data.get('village_city', 'Unknown Village'),
                "pin_code": farmer_data.get('pin_code', '000000'),
                "phone": farmer_data.get('phone_number', '')[:6] + "****"  # Masked for privacy
            },
            "crop": {
                "type": crop_data.get('crop_type', 'Unknown Crop'),
                "season": crop_data.get('season', 'Unknown Season'),
                "harvest_date": crop_data.get('harvest_date', datetime.now().strftime('%Y-%m-%d')),
                "organic": crop_data.get('is_organic', False),
                "certification": crop_data.get('certification_type', 'Standard')
            },
            "created_at": datetime.now().isoformat(),
            "track_url": f"{self.base_url}/{passport_id}"
        }
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        
        # Add tracking URL to QR code
        qr.add_data(tracking_data['track_url'])
        qr.make(fit=True)
        
        # Create QR code image
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64 for storage
        buffer = BytesIO()
        qr_img.save(buffer, format='PNG')
        qr_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        return {
            'success': True,
            'qr_code': qr_base64,
            'tracking_data': tracking_data,
            'qr_url': tracking_data['track_url'],
            'message': 'QR code generated successfully for supply chain tracking'
        }
    
    def get_tracking_info(self, passport_id):
        """Get tracking information for consumers"""
        
        # In a real implementation, this would fetch from database
        # For now, return sample data
        return {
            'success': True,
            'farmer': {
                'name': 'राम कुमार (Ram Kumar)',
                'village': 'हरियाणा गांव, पंजाब (Haryana Village, Punjab)',
                'pin_code': '144001',
                'experience': '15 years farming experience',
                'crops_grown': ['Rice', 'Wheat', 'Sugarcane'],
                'farming_method': 'Organic & Traditional'
            },
            'crop': {
                'type': 'Basmati Rice',
                'variety': 'Pusa Basmati 1121',
                'harvest_date': '2024-08-15',
                'organic_certified': True,
                'pesticide_free': True,
                'water_source': 'Tube well + Rainwater',
                'soil_type': 'Alluvial'
            },
            'journey': [
                {
                    'stage': 'Farm',
                    'date': '2024-08-15',
                    'location': 'Haryana Village, Punjab',
                    'description': 'Harvested by farmer Ram Kumar'
                },
                {
                    'stage': 'Processing',
                    'date': '2024-08-17',
                    'location': 'Local Rice Mill',
                    'description': 'Cleaned and processed'
                },
                {
                    'stage': 'Quality Check',
                    'date': '2024-08-18',
                    'location': 'Quality Control Center',
                    'description': 'Organic certification verified'
                },
                {
                    'stage': 'Packaging',
                    'date': '2024-08-20',
                    'location': 'Packaging Unit',
                    'description': 'Sealed with QR code'
                }
            ],
            'certifications': [
                'Organic India Certified',
                'Pesticide Free',
                'Traditional Farming Methods'
            ],
            'blockchain_verified': True,
            'passport_id': passport_id
        }

# Initialize service
supply_chain_service = SupplyChainService()