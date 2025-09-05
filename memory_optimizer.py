import gc
import psutil
import os
from functools import wraps

def memory_monitor(func):
    """Decorator to monitor and optimize memory usage"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Force garbage collection before heavy operations
        gc.collect()
        
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            # Clean up after operation
            gc.collect()
    return wrapper

def check_memory_usage():
    """Check current memory usage"""
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    memory_percent = process.memory_percent()
    
    if memory_percent > 80:  # If using more than 80% memory
        gc.collect()  # Force garbage collection
        
    return {
        'memory_mb': memory_info.rss / 1024 / 1024,
        'memory_percent': memory_percent
    }