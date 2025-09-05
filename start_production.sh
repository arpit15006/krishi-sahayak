#!/bin/bash

# Production startup script for Krishi Sahayak
echo "🌱 Starting Krishi Sahayak Production Server..."

# Set memory limits and optimization
export PYTHONUNBUFFERED=1
export MALLOC_ARENA_MAX=2
export PYTHONDONTWRITEBYTECODE=1
export PYTHONHASHSEED=random

# Garbage collection optimization
export PYTHONGC=1

# Start with optimized Gunicorn
echo "📊 Memory optimization enabled"
echo "⚡ Starting with reduced worker timeout"
gunicorn --config gunicorn.conf.py complete_app:app