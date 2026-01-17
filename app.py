from flask import Flask, request, jsonify, render_template_string
import json
from datetime import datetime

app = Flask(__name__)

# In-memory storage
submissions = []

# Mineral data
mineral_data = {
    'Gold': {'price': 60000, 'hardness': '2.5-3', 'use': 'Jewelry, electronics'},
    'Silver': {'price': 700, 'hardness': '2.5-3', 'use': 'Jewelry, coins, electronics'},
    'Copper': {'price': 9, 'hardness': '2.5-3', 'use': 'Wiring, plumbing'},
    'Iron': {'price': 0.5, 'hardness': '4-5', 'use': 'Construction, manufacturing'},
    'Diamond': {'price': 55000000, 'hardness': '10', 'use': 'Jewelry, cutting tools'},
    'Coal': {'price': 0.15, 'hardness': '1-2', 'use': 'Energy production'},
    'Limestone': {'price': 0.05, 'hardness': '3', 'use': 'Cement, agriculture'},
    'Quartz': {'price': 0.1, 'hardness': '7', 'use': 'Glass, electronics'}
}

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GeoScan Minerals - Mining Survey Platform</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 { text-align: center; color: white; margin-bottom: 30px; font-size: 2.5em; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
        .card { background: white; border-radius: 15px; padding: 25px; margin-bottom: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; color: #333; }
        input, select, textarea { width: 100%; padding: 12px; border: 2px solid #ddd; border-radius: 8px; font-size: 14px; transition: border 0.3s; }
        input:focus, select:focus, textarea:focus { outline: none; border-color: #667eea; }
        button { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 12px 30px; border: none; border-radius: 8px; cursor: pointer; font-size: 16px; font-weight: bold; transition: transform 0.2s; }
        button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.3); }
        .leaderboard-item { display: flex; justify-content: space-between; padding: 12px; margin-bottom: 8px; background: #f8f9fa; border-radius: 8px; cursor: pointer; transition: background 0.2s; }
        .leaderboard-item:hover { background: #e9ecef; }
        #map { height: 400px; border-radius: 10px; margin-top: 15px; }
        .success-msg { background: #28a745; color: white; padding: 15px; border-radius: 8px; margin-bottom: 20px; display: none; text-align: center; }
        .price-tag { background: #ffc107; padding: 4px 10px; border-radius: 5px; font-weight: bold; color: #333; }
        .info-box { background: #e7f3ff; padding: 12px; margin-bottom: 10px; border-radius: 8px; border-left: 4px solid #667eea; }
        .mineral-info { background: #f0f8ff; padding: 15px; border-radius: 8px; margin-top: 10px; }
        #mapCard { display: none; position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 90%; max-width: 800px; background: white; border-radius: 15px; padding: 20px; box-shadow: 0 20px 60px rgba(0,0,0,0.4); z-index: 1000; }
        .overlay { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 999; }
        .close-btn { float: right; font-size: 28px; font-weight: bold; cursor: pointer; color: #999; }
        .close-btn:hover { color: #333; }
    </style>
</head>
<body>
    <div class="container">
        <h1>⛏️ GeoScan Minerals Platform</h1>
        
        <div class="success-msg" id="successMsg">✓ Submission successful!</div>
        
        <div class="card">
            <h2>📝 Submit Mineral Discovery</h2>
            <form id="submitForm">
                <div class="form-group">
                    <label>Mineral Name:</label>
                    <select id="mineralName" required>
                        <option value="">Select Mineral</option>
                        <option>Gold</option>
                        <option>Silver</option>
                        <option>Copper</option>
                        <option>Iron</option>
                        <option>Diamond</option>
                        <option>Coal</option>
                        <option>Limestone</option>
                        <option>Quartz</option>
                    </select>
                </div>
                <div id="mineralInfo"></div>
                <div class="form-group">
                    <label>Location (lat, lon):</label>
                    <input type="text" id="location" placeholder="e.g., 27.4728, 89.6394" required>
                    <button type="button" onclick="showMapModal()" style="margin-top: 10px;">📍 View on Map</button>
                </div>
                <div class="form-group">
                    <label>Properties:</label>
                    <textarea id="properties" rows="3" placeholder="Describe mineral properties..." required></textarea>
                </div>
                <div class="form-group">
                    <label>Image URL:</label>
                    <input type="url" id="imageUrl" placeholder="https://example.com/image.jpg">
                </div>
                <button type="submit">Submit Discovery</button>
            </form>
        </div>
        
        <div class="card">
            <h2>🏆 Leaderboard</h2>
            <div id="leaderboard"></div>
        </div>
        
        <div class="card">
            <h2>💰 Current Mineral Prices</h2>
            <div id="prices"></div>
        </div>
    </div>
    
    <div class="overlay" id="overlay" onclick="closeMapModal()"></div>
    <div class="card" id="mapCard">
        <span class="close-btn" onclick="closeMapModal()">×</span>
        <h3>Location Map</h3>
        <div id="map"></div>
    </div>
    
    <script>
        const mineralData = {
            'Gold': {price: 60000, hardness: '2.5-3', use: 'Jewelry, electronics'},
            'Silver': {price: 700, hardness: '2.5-3', use: 'Jewelry, coins, electronics'},
            'Copper': {price: 9, hardness: '2.5-3', use: 'Wiring, plumbing'},
            'Iron': {price: 0.5, hardness: '4-5', use: 'Construction, manufacturing'},
            'Diamond': {price: 55000000, hardness: '10', use: 'Jewelry, cutting tools'},
            'Coal': {price: 0.15, hardness: '1-2', use: 'Energy production'},
            'Limestone': {price: 0.05, hardness: '3', use: 'Cement, agriculture'},
            'Quartz': {price: 0.1, hardness: '7', use: 'Glass, electronics'}
        };
        
        let map;
        
        function showMapModal() {
            const location = document.getElementById('location').value;
            if (!location) { alert('Enter location!'); return; }
            const [lat, lon] = location.split(',').map(x => parseFloat(x.trim()));
            if (isNaN(lat) || isNaN(lon)) { alert('Invalid format: lat, lon'); return; }
            document.getElementById('mapCard').style.display = 'block';
            document.getElementById('overlay').style.display = 'block';
            setTimeout(() => {
                if (map) map.remove();
                map = L.map('map').setView([lat, lon], 10);
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {attribution: 'OSM'}).addTo(map);
                L.marker([lat, lon]).addTo(map).bindPopup('Sample Location');
            }, 100);
        }
        
        function closeMapModal() { 
            document.getElementById('mapCard').style.display = 'none'; 
            document.getElementById('overlay').style.display = 'none';
        }
        
        document.getElementById('submitForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const data = {
                mineralName: document.getElementById('mineralName').value,
                location: document.getElementById('location').value,
                properties: document.getElementById('properties').value,
                imageUrl: document.getElementById('imageUrl').value,
                timestamp: new Date().toISOString()
            };
            try {
                const res = await fetch('/api/submit', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(data)});
                if (res.ok) {
                    document.getElementById('successMsg').style.display = 'block';
                    document.getElementById('submitForm').reset();
                    setTimeout(() => { document.getElementById('successMsg').style.display = 'none'; }, 3000);
                    loadLeaderboard();
                }
            } catch (err) { console.error(err); }
        });
        
        function loadLeaderboard() {
            fetch('/api/leaderboard').then(r => r.json()).then(data => {
                const lb = document.getElementById('leaderboard');
                if (!data || data.length === 0) {
                    lb.innerHTML = '<p style="text-align: center; color: #999;">No submissions yet.</p>';
                } else {
                    lb.innerHTML = data.map((item, i) => `<div class="leaderboard-item" onclick="loadLocationMap('${item.location}')"><span>#${i+1} ${item.mineralName}</span><span>${item.points} pts</span></div>`).join('');
                }
            });
        }
        
        function loadLocationMap(location) {
            document.getElementById('location').value = location;
            showMapModal();
        }
        
        function showPrices() {
            const prices = document.getElementById('prices');
            prices.innerHTML = Object.entries(mineralData).map(([name, data]) => `<div class="info-box"><strong>${name}:</strong> <span class="price-tag">$${data.price}/kg</span> (Hardness: ${data.hardness})</div>`).join('');
        }
        
        window.addEventListener('load', () => {
            loadLeaderboard();
            showPrices();
            document.getElementById('mineralName').addEventListener('change', (e) => {
                const mineral = e.target.value;
                const info = document.getElementById('mineralInfo');
                if (mineral && mineralData[mineral]) {
                    const data = mineralData[mineral];
                    info.innerHTML = `<div class="mineral-info"><h4>${mineral}</h4><p><strong>Uses:</strong> ${data.use}</p><p><strong>Hardness:</strong> ${data.hardness}</p><p><strong>Market Price:</strong> <span class="price-tag">$${data.price}/kg</span></p></div>`;
                } else {
                    info.innerHTML = '';
                }
            });
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/submit', methods=['POST'])
def submit():
    data = request.json
    data['points'] = len(submissions) * 10 + 50
    submissions.append(data)
    return jsonify({'success': True, 'points': data['points']})

@app.route('/api/leaderboard', methods=['GET'])
def leaderboard():
    return jsonify(sorted(submissions, key=lambda x: x.get('points', 0), reverse=True))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
