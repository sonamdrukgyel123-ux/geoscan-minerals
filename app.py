from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import json, uuid
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

MINERAL_DATA = {
    'Quartz': {'use': 'Glass, Electronics, Jewelry', 'price': 2.5, 'hardness': 7},
    'Feldspar': {'use': 'Ceramics, Glass, Fillers', 'price': 1.8, 'hardness': 6},
    'Mica': {'use': 'Insulation, Cosmetics, Paint', 'price': 4.2, 'hardness': 2.5},
    'Calcite': {'use': 'Cement, Fertilizer, Construction', 'price': 1.2, 'hardness': 3},
    'Hematite': {'use': 'Iron ore, Pigments, Jewelry', 'price': 3.5, 'hardness': 5.5},
    'Magnetite': {'use': 'Iron ore, Electronics', 'price': 2.8, 'hardness': 6}
}

submissions = []
user_rewards = {}

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GeoScan Minerals</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }
    .container { max-width: 1400px; margin: 0 auto; }
    header { text-align: center; color: white; margin-bottom: 40px; }
    header h1 { font-size: 2.5em; margin-bottom: 10px; }
    .main-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; margin-bottom: 40px; }
    .card { background: white; border-radius: 10px; padding: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
    .card h2 { color: #667eea; margin-bottom: 20px; font-size: 1.5em; }
    .form-group { margin-bottom: 15px; }
    label { display: block; margin-bottom: 5px; font-weight: 600; color: #333; }
    input, textarea, select { width: 100%; padding: 10px; border: 2px solid #e0e0e0; border-radius: 5px; font-size: 1em; }
    input:focus, textarea:focus, select:focus { outline: none; border-color: #667eea; }
    .btn { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; font-weight: 600; width: 100%; margin-top: 10px; }
    .btn:hover { transform: scale(1.02); }
    .map-btn { background: #4caf50; width: auto; padding: 8px 15px; margin-top: 5px; }
    .info-box { background: #f9f9f9; padding: 12px; border-radius: 5px; margin-bottom: 12px; border-left: 4px solid #667eea; }
    .leaderboard-item { padding: 12px; border-bottom: 1px solid #f0f0f0; display: flex; justify-content: space-between; align-items: center; cursor: pointer; transition: background 0.3s; }
    .leaderboard-item:hover { background: #f5f5f5; }
    .mineral-info { background: #f0f7ff; padding: 12px; border-radius: 5px; margin: 10px 0; }
    .price-tag { background: #4caf50; color: white; padding: 4px 8px; border-radius: 3px; font-weight: 600; font-size: 0.9em; }
    .success-msg { background: #4caf50; color: white; padding: 12px; border-radius: 5px; margin-bottom: 15px; display: none; }
    #map { height: 400px; border-radius: 10px; margin-bottom: 10px; }
    @media (max-width: 1200px) { .main-grid { grid-template-columns: 1fr 1fr; } }
    @media (max-width: 768px) { .main-grid { grid-template-columns: 1fr; } }
    </style>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
</head>
<body>
    <div class="container">
        <header>
            <h1>GeoScan Minerals</h1>
            <p>Identify minerals, share discoveries, earn rewards - with location mapping!</p>
        </header>
        
        <div class="main-grid">
            <div class="card">
                <h2>Submit Mineral Sample</h2>
                <div class="success-msg" id="successMsg">Sample submitted! You earned 10 points!</div>
                <form id="submitForm">
                    <div class="form-group">
                        <label for="mineralName">Mineral Name</label>
                        <select id="mineralName" name="mineralName" required>
                            <option value="">Select a mineral...</option>
                            <option value="Quartz">Quartz</option>
                            <option value="Feldspar">Feldspar</option>
                            <option value="Mica">Mica</option>
                            <option value="Calcite">Calcite</option>
                            <option value="Hematite">Hematite</option>
                            <option value="Magnetite">Magnetite</option>
                            <option value="Other">Other</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="location">Location (Lat, Lon)</label>
                        <input type="text" id="location" name="location" placeholder="e.g., 27.1751, 78.0421" required>
                        <button type="button" class="btn map-btn" onclick="showMapModal()">View on Map</button>
                    </div>
                    <div class="form-group">
                        <label for="properties">Properties</label>
                        <textarea id="properties" placeholder="Color, hardness, texture..." required></textarea>
                    </div>
                    <div class="form-group">
                        <label for="imageUrl">Image URL</label>
                        <input type="text" id="imageUrl" placeholder="https://..." required>
                    </div>
                    <button type="submit" class="btn">Submit & Earn Points</button>
                </form>
                <h3 style="margin-top: 20px; color: #667eea;">Mineral Information</h3>
                <div id="mineralInfo"></div>
            </div>
            
            <div class="card" id="mapCard" style="display: none;">
                <h2>Location Map</h2>
                <div id="map"></div>
                <button onclick="closeMapModal()" class="btn">Close</button>
            </div>
            
            <div class="card">
                <h2>Top Contributors</h2>
                <div id="leaderboard" style="max-height: 400px; overflow-y: auto;">
                    <p style="text-align: center; color: #999;">No submissions yet.</p>
                </div>
                <h3 style="margin-top: 20px; color: #667eea;">Market Prices (per kg)</h3>
                <div id="prices"></div>
            </div>
        </div>
    </div>
    <script>
    let map = null;
    const mineralData = {
        'Quartz': {'use': 'Glass, Electronics, Jewelry', 'price': 2.5, 'hardness': 7},
        'Feldspar': {'use': 'Ceramics, Glass, Fillers', 'price': 1.8, 'hardness': 6},
        'Mica': {'use': 'Insulation, Cosmetics, Paint', 'price': 4.2, 'hardness': 2.5},
        'Calcite': {'use': 'Cement, Fertilizer, Construction', 'price': 1.2, 'hardness': 3},
        'Hematite': {'use': 'Iron ore, Pigments, Jewelry', 'price': 3.5, 'hardness': 5.5},
        'Magnetite': {'use': 'Iron ore, Electronics', 'price': 2.8, 'hardness': 6}
    };
    
    function showMapModal() {
        const location = document.getElementById('location').value;
        if (!location) { alert('Enter location!'); return; }
        const [lat, lon] = location.split(',').map(x => parseFloat(x.trim()));
        if (isNaN(lat) || isNaN(lon)) { alert('Invalid format: lat, lon'); return; }
        document.getElementById('mapCard').style.display = 'block';
        window.scrollTo(0, 0);
        setTimeout(() => {
            if (map) map.remove();
            map = L.map('map').setView([lat, lon], 10);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {attribution: 'OSM'}).addTo(map);
            L.marker([lat, lon]).addTo(map).bindPopup('Sample Location');
        }, 100);
    }
    
    function closeMapModal() { document.getElementById('mapCard').style.display = 'none'; }
    
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
def submit_sample():
    try:
        data = request.json
        submission = {
            'id': str(uuid.uuid4())[:8],
            'mineralName': data.get('mineralName'),
            'location': data.get('location'),
            'properties': data.get('properties'),
            'imageUrl': data.get('imageUrl'),
            'timestamp': datetime.now().isoformat(),
            'points': 10
        }
        submissions.append(submission)
        return jsonify({'status': 'success', 'points': 10}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/leaderboard')
def leaderboard():
    return jsonify(sorted(submissions, key=lambda x: x['timestamp'], reverse=True))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
