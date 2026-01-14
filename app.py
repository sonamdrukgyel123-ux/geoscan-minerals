from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import sqlite3, uuid
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# HTML Template with embedded CSS and JS
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GeoScan Minerals - Mineral Identification Platform</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .container {
            width: 100%;
            max-width: 1200px;
        }
        header {
            text-align: center;
            color: white;
            margin-bottom: 40px;
        }
        header h1 {
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        .main-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: 40px;
        }
        .card {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            transition: transform 0.3s, box-shadow 0.3s;
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 50px rgba(0,0,0,0.3);
        }
        .card h2 {
            color: #667eea;
            margin-bottom: 20px;
            font-size: 1.8em;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            color: #333;
            font-weight: 500;
        }
        input, textarea, select {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 1em;
            font-family: inherit;
            transition: border-color 0.3s;
        }
        input:focus, textarea:focus, select:focus {
            outline: none;
            border-color: #667eea;
        }
        textarea {
            resize: vertical;
            min-height: 100px;
        }
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 8px;
            font-size: 1em;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            font-weight: 600;
            width: 100%;
        }
        .btn:hover {
            transform: scale(1.02);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        }
        .btn:active {
            transform: scale(0.98);
        }
        .success-message {
            background: #4caf50;
            color: white;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            display: none;
            animation: slideDown 0.3s ease;
        }
        @keyframes slideDown {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        .leaderboard-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px;
            border-bottom: 1px solid #f0f0f0;
            animation: fadeIn 0.5s ease;
        }
        .leaderboard-item:last-child {
            border-bottom: none;
        }
        .rank {
            font-size: 1.2em;
            font-weight: bold;
            color: #667eea;
            min-width: 40px;
        }
        .user-info {
            flex: 1;
            margin: 0 15px;
        }
        .user-name {
            font-weight: 600;
            color: #333;
        }
        .user-minerals {
            font-size: 0.9em;
            color: #999;
            margin-top: 5px;
        }
        .points {
            font-size: 1.3em;
            font-weight: bold;
            color: #764ba2;
        }
        @keyframes fadeIn {
            from {
                opacity: 0;
            }
            to {
                opacity: 1;
            }
        }
        .empty-state {
            text-align: center;
            color: #999;
            padding: 40px 20px;
        }
        .empty-state svg {
            width: 80px;
            height: 80px;
            margin-bottom: 20px;
            opacity: 0.5;
        }
        @media (max-width: 768px) {
            .main-grid {
                grid-template-columns: 1fr;
            }
            header h1 {
                font-size: 2em;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>💎 GeoScan Minerals</h1>
            <p>Identify minerals and earn rewards through contributions</p>
        </header>
        
        <div class="main-grid">
            <!-- Submission Form -->
            <div class="card">
                <h2>Submit Mineral Sample</h2>
                <div class="success-message" id="successMsg">Sample submitted successfully! You earned 5 points.</div>
                <form id="submitForm">
                    <div class="form-group">
                        <label for="mineralName">Mineral Name</label>
                        <input type="text" id="mineralName" name="mineralName" placeholder="e.g., Quartz, Feldspar" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="location">Location Found</label>
                        <input type="text" id="location" name="location" placeholder="Latitude, Longitude or location name" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="properties">Mineral Properties</label>
                        <textarea id="properties" name="properties" placeholder="Color, luster, crystal structure, hardness, etc." required></textarea>
                    </div>
                    
                    <div class="form-group">
                        <label for="images">Image Description</label>
                        <input type="text" id="images" name="images" placeholder="Describe the sample photos or upload link" required>
                    </div>
                    
                    <button type="submit" class="btn">Submit Sample</button>
                </form>
            </div>
            
            <!-- Leaderboard -->
            <div class="card">
                <h2>🏆 Leaderboard</h2>
                <div id="leaderboardContainer">
                    <div class="empty-state">
                        <p>No submissions yet. Be the first to contribute!</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        // Handle form submission
        document.getElementById('submitForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = {
                mineralName: document.getElementById('mineralName').value,
                location: document.getElementById('location').value,
                properties: document.getElementById('properties').value,
                images: document.getElementById('images').value,
                timestamp: new Date().toISOString()
            };
            
            try {
                const response = await fetch('/api/submit-sample', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formData)
                });
                
                if (response.ok) {
                    // Show success message
                    const successMsg = document.getElementById('successMsg');
                    successMsg.style.display = 'block';
                    
                    // Reset form
                    document.getElementById('submitForm').reset();
                    
                    // Hide message after 3 seconds
                    setTimeout(() => {
                        successMsg.style.display = 'none';
                    }, 3000);
                    
                    // Refresh leaderboard
                    loadLeaderboard();
                } else {
                    alert('Error submitting sample');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Error submitting sample: ' + error.message);
            }
        });
        
        // Load leaderboard
        async function loadLeaderboard() {
            try {
                const response = await fetch('/api/leaderboard');
                const data = await response.json();
                
                const container = document.getElementById('leaderboardContainer');
                
                if (!data || data.length === 0) {
                    container.innerHTML = '<div class="empty-state"><p>No submissions yet. Be the first to contribute!</p></div>';
                } else {
                    container.innerHTML = data.map((item, index) => `
                        <div class="leaderboard-item">
                            <span class="rank">\#${index + 1}</span>
                            <div class="user-info">
                                <div class="user-name">${item.mineralName || 'Unknown'}</div>
                                <div class="user-minerals">${item.location || 'Location unknown'}</div>
                            </div>
                            <div class="points">${item.points || 5}pts</div>
                        </div>
                    `).join('');
                }
            } catch (error) {
                console.error('Error loading leaderboard:', error);
            }
        }
        
        // Load leaderboard on page load
        window.addEventListener('load', loadLeaderboard);
    </script>
</body>
</html>
'''

# In-memory storage for submissions
submissions = []
user_points = {}

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.json
        user_id = str(uuid.uuid4())[:8]
        user_points[user_id] = 0
        return jsonify({'status': 'success', 'user_id': user_id}), 201
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/submit-sample', methods=['POST'])
def submit_sample():
    try:
        data = request.json
        submission = {
            'id': str(uuid.uuid4())[:8],
            'mineralName': data.get('mineralName', 'Unknown'),
            'location': data.get('location', ''),
            'properties': data.get('properties', ''),
            'images': data.get('images', ''),
            'timestamp': data.get('timestamp', datetime.now().isoformat()),
            'points': 5
        }
        submissions.append(submission)
        return jsonify({'status': 'success', 'points': 5, 'submission_id': submission['id']}), 201
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/leaderboard', methods=['GET'])
def leaderboard():
    try:
        # Return submissions sorted by timestamp (newest first)
        return jsonify(sorted(submissions, key=lambda x: x.get('timestamp', ''), reverse=True))
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/submissions', methods=['GET'])
def get_submissions():
    try:
        return jsonify(submissions)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
