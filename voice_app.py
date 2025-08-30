#!/usr/bin/env python3
import os
from flask import Flask, request, jsonify, session, render_template, redirect, url_for
from dotenv import load_dotenv
import json

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "krishi-sahayak-secret-key")

# Simple in-memory user for demo
demo_user = {
    'id': 1,
    'phone_number': '9999999999',
    'full_name': 'Demo Farmer',
    'village_city': 'Demo Village',
    'pin_code': '110001',
    'main_crops': ['Rice', 'Wheat', 'Sugarcane']
}

@app.route('/')
def index():
    session['user_id'] = demo_user['id']
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', user=demo_user, weather={}, market_data={})

@app.route('/api/voice-query', methods=['POST'])
def voice_query():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        language = data.get('language', 'hi-IN')
        
        if not query:
            return jsonify({'success': False, 'error': 'No query provided'})
        
        # Process voice query with AI
        from services.ai_service import process_voice_query
        response = process_voice_query(query, language, demo_user['main_crops'], demo_user['pin_code'])
        
        return jsonify({
            'success': True,
            'response': response,
            'language': language
        })
        
    except Exception as e:
        app.logger.error(f"Voice query error: {str(e)}")
        return jsonify({
            'success': False, 
            'error': 'माफ करें, कुछ तकनीकी समस्या है।' if language == 'hi-IN' else 'Sorry, there was a technical issue.'
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)