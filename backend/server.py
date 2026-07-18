#!/usr/bin/env python3
"""
Dino Game Backend Server
Handles score storage in JSON format and serves the frontend.
"""

import json
import os
import logging
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# Setup
app = Flask(__name__)
CORS(app)

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')
SCORES_FILE = os.path.join(DATA_DIR, 'scores.json')
LOG_FILE = os.path.join(LOGS_DIR, 'server.log')

# Create directories if they don't exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

# Setup logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def load_scores():
    """Load scores from JSON file"""
    try:
        if os.path.exists(SCORES_FILE):
            with open(SCORES_FILE, 'r') as f:
                return json.load(f)
        return []
    except Exception as e:
        logging.error(f"Error loading scores: {e}")
        return []

def save_scores(scores):
    """Save scores to JSON file"""
    try:
        with open(SCORES_FILE, 'w') as f:
            json.dump(scores, f, indent=2)
        return True
    except Exception as e:
        logging.error(f"Error saving scores: {e}")
        return False

@app.route('/')
def serve_frontend():
    """Serve the frontend"""
    return send_from_directory(FRONTEND_DIR, 'game.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files"""
    return send_from_directory(FRONTEND_DIR, path)

@app.route('/api/scores', methods=['GET'])
def get_scores():
    """Get all scores"""
    try:
        scores = load_scores()
        # Sort by score descending and return top 10
        scores.sort(key=lambda x: x['score'], reverse=True)
        scores = scores[:10]
        logging.info("Scores retrieved successfully")
        return jsonify({'success': True, 'scores': scores})
    except Exception as e:
        logging.error(f"Error getting scores: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/scores', methods=['POST'])
def add_score():
    """Add a new score"""
    try:
        data = request.json
        player_name = data.get('player_name', 'Anonymous')
        score = data.get('score', 0)
        
        if score <= 0:
            return jsonify({'success': False, 'message': 'Invalid score'}), 400
        
        scores = load_scores()
        scores.append({
            'player_name': player_name,
            'score': score,
            'date': datetime.now().isoformat()
        })
        
        if save_scores(scores):
            logging.info(f"Score saved: {player_name} - {score}")
            return jsonify({'success': True, 'message': 'Score saved successfully'})
        else:
            return jsonify({'success': False, 'message': 'Failed to save score'}), 500
            
    except Exception as e:
        logging.error(f"Error adding score: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    logging.info("Starting Dino Game Server...")
    print("=" * 50)
    print("Dino Game Server")
    print("=" * 50)
    print(f"Data directory: {DATA_DIR}")
    print(f"Logs directory: {LOGS_DIR}")
    print(f"Frontend directory: {FRONTEND_DIR}")
    print(f"Scores file: {SCORES_FILE}")
    print("=" * 50)
    print("Server starting on http://localhost:5000")
    print("Press Ctrl+C to stop")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5000, debug=False)
