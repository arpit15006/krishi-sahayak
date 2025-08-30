import os
import logging
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.DEBUG)

def create_app():
    # Create the app
    app = Flask(__name__)
    app.secret_key = os.environ.get("SESSION_SECRET", "krishi-sahayak-secret-key")
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    
    # File upload configuration
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    
    # Import and register routes
    import routes
    app.register_blueprint(routes.bp)
    
    # Register new Supabase routes
    try:
        from routes_package.farmer_routes import farmer_bp
        app.register_blueprint(farmer_bp)
    except ImportError:
        pass
    
    return app

# Create app instance
app = create_app()
