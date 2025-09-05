# Gunicorn configuration for production
bind = "0.0.0.0:8000"
workers = 1  # Single worker for memory efficiency
worker_class = "sync"
worker_connections = 500
timeout = 60  # Reduced timeout - dashboard now loads faster
keepalive = 2
max_requests = 500  # Restart workers more frequently
max_requests_jitter = 50
preload_app = True
worker_tmp_dir = "/dev/shm"  # Use RAM for temp files
worker_memory_limit = 400  # MB limit per worker