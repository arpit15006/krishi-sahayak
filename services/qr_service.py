"""
QR Code generation service
"""

import qrcode
import base64
from io import BytesIO

def generate_qr_code(data, size=10):
    """Generate QR code as base64 image"""
    try:
        # Limit data size for QR code readability
        data_str = str(data)
        if len(data_str) > 1000:
            # Truncate large data to essential info only
            import json
            try:
                data_obj = json.loads(data_str)
                essential_data = {
                    'passport_id': data_obj.get('passport_id', 'Unknown'),
                    'farmer': data_obj.get('farmer', {}).get('name', 'Unknown'),
                    'crop': data_obj.get('crop', {}).get('type', 'Unknown'),
                    'verified': True,
                    'verify_url': data_obj.get('verification', {}).get('verify_url', '')
                }
                data_str = json.dumps(essential_data)
            except:
                data_str = data_str[:500]  # Fallback truncation
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=size,
            border=4,
        )
        qr.add_data(data_str)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"
        
    except Exception as e:
        print(f"QR Code generation error: {e}")
        # Return a simple fallback QR code
        try:
            fallback_qr = qrcode.QRCode(version=1, box_size=10, border=4)
            fallback_qr.add_data("QR Error - Contact Support")
            fallback_qr.make(fit=True)
            fallback_img = fallback_qr.make_image(fill_color="red", back_color="white")
            
            buffer = BytesIO()
            fallback_img.save(buffer, format='PNG')
            buffer.seek(0)
            fallback_str = base64.b64encode(buffer.getvalue()).decode()
            
            return f"data:image/png;base64,{fallback_str}"
        except:
            # Ultimate fallback - return a minimal data URL
            return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="