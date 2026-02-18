// Mineral database
const mineralData = {
    'Gold': {price: 60000, hardness: '2.5-3', use: 'Jewelry, electronics'},
    'Silver': {price: 700, hardness: '2.5-3', use: 'Jewelry, coins'},
    'Copper': {price: 9, hardness: '2.5-3', use: 'Wiring, plumbing'},
    'Iron': {price: 0.5, hardness: '4-5', use: 'Construction'},
    'Diamond': {price: 55000000, hardness: '10', use: 'Jewelry, cutting tools'},
    'Coal': {price: 0.15, hardness: '1-2', use: 'Energy production'},
    'Limestone': {price: 0.05, hardness: '3', use: 'Cement, agriculture'},
    'Quartz': {price: 0.1, hardness: '7', use: 'Glass, electronics'}
};

let map = null;

function showMapModal() {
    const location = document.getElementById('location').value;
    if (!location) {
        alert('Please enter a location!');
        return;
    }
    const [lat, lon] = location.split(',').map(x => parseFloat(x.trim()));
    if (isNaN(lat) || isNaN(lon)) {
        alert('Invalid format');
        return;
    }
    document.getElementById('mapCard').style.display = 'block';
    document.getElementById('overlay').style.display = 'block';
    setTimeout(() => {
        if (map) map.remove();
        map = L.map('map').setView([lat, lon], 10);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
        L.marker([lat, lon]).addTo(map).bindPopup('Location').openPopup();
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
        imageUrl: document.getElementById('imageUrl').value || 'No image',
        timestamp: new Date().toISOString()
    };
    try {
        const res = await fetch('/api/submit', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        if (res.ok) {
            document.getElementById('successMsg').style.display = 'block';
            document.getElementById('submitForm').reset();
            setTimeout(() => {
                document.getElementById('successMsg').style.display = 'none';
            }, 3000);
            loadLeaderboard();
        }
    } catch (err) {
        console.error(err);
    }
});

function loadLeaderboard() {
    fetch('/api/leaderboard').then(r => r.json()).then(data => {
        const lb = document.getElementById('leaderboard');
        if (!data || data.length === 0) {
            lb.innerHTML = '<p style="text-align:center;color:#999;">No submissions yet</p>';
        } else {
            lb.innerHTML = data.map((item, i) => 
                `<div class="leaderboard-item"><span>#${i+1} ${item.mineralName}</span><span>${item.points} pts</span></div>`
            ).join('');
        }
    });
}

function showPrices() {
    const prices = document.getElementById('prices');
    prices.innerHTML = Object.entries(mineralData).map(([name, data]) => 
        `<div class="info-box"><strong>${name}:</strong> <span class="price-tag">$${data.price}/kg</span></div>`
    ).join('');
}

document.getElementById('mineralName').addEventListener('change', (e) => {
    const mineral = e.target.value;
    const info = document.getElementById('mineralInfo');
    if (mineral && mineralData[mineral]) {
        const data = mineralData[mineral];
        info.innerHTML = `<div class="mineral-info"><h4>${mineral}</h4><p><strong>Price:</strong> $${data.price}/kg</p><p><strong>Hardness:</strong> ${data.hardness}</p></div>`;
    } else {
        info.innerHTML = '';
    }
});

window.addEventListener('load', () => {
    loadLeaderboard();
    showPrices();
});
