# Supabase models
from .farmer import Farmer
from .crop import Crop

# Legacy SQLAlchemy models (for backward compatibility)
try:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from models import User, ScanResult, DigitalPassport
except ImportError:
    pass