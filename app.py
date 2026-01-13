from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3, uuid
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    user_id = str(uuid.uuid4())[:8]
    return jsonify({'status': 'success', 'user_id': user_id}), 201

@app.route('/api/submit-sample', methods=['POST'])
def submit_sample():
    data = request.json
    return jsonify({'status': 'success', 'points': 5}), 201

@app.route('/api/leaderboard', methods=['GET'])
def leaderboard():
    return jsonify([])

@app.route('/')
def index():
    return 'GeoScan Minerals - Backend Running!'

if __name__ == '__main__':
    app.run(debug=False, port=5000)
