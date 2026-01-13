# GeoScan Minerals 🪨

A professional web-based mineral identification and documentation platform that combines mobile scanning technology with a community-driven rewards system.

## Overview

GeoScan Minerals is a comprehensive web application designed to help users identify minerals and natural resources through photo submission and scanning. Users can contribute mineral samples, identify geological resources, and earn incentives through the platform's rewards system.

## Features

### Core Functionality
- **Mineral Identification**: Advanced image recognition to identify minerals from photos
- **Photo Upload**: Easy-to-use image upload interface for mineral scanning
- **Mineral Database**: Comprehensive library of minerals with identification characteristics
- **User Rewards System**: Earn points and incentives for contributions
- **Location Tracking**: Geo-tag mineral findings for exploration mapping
- **Community Contributions**: Share discoveries with the exploration sector

### Technical Features
- Responsive web design for mobile and desktop
- Secure user authentication system
- Image processing and AI-powered mineral identification
- RESTful API backend
- Database management for mineral records
- User dashboard and profile management

## Technology Stack

### Backend
- **Framework**: Flask (Python)
- **Database**: SQLite / PostgreSQL
- **Image Processing**: Python OpenCV, PIL
- **API**: Flask-RESTful
- **Authentication**: Flask-Login, JWT

### Frontend
- **HTML5/CSS3**: Responsive design
- **JavaScript**: Interactive features and AJAX
- **Bootstrap**: UI framework

### Additional Tools
- **Image Recognition**: Cloud Vision API / Custom ML Model
- **Map Integration**: Google Maps API
- **Cloud Storage**: AWS S3 for image storage
- **Email Service**: SMTP for notifications

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git

### Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/sonamdrukgyel123-ux/geoscan-minerals.git
cd geoscan-minerals
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Initialize the database**
```bash
python
>>> from app import create_app, db
>>> app = create_app()
>>> with app.app_context():
>>>     db.create_all()
```

6. **Run the development server**
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Usage

1. **Register**: Create a new account on the platform
2. **Upload Image**: Take or upload a photo of a mineral
3. **Get Identification**: The system analyzes and identifies the mineral
4. **View Details**: See mineral properties and characteristics
5. **Earn Rewards**: Accumulate points for valid submissions
6. **Redeem Rewards**: Exchange points for incentives

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout

### Minerals
- `GET /api/minerals` - Get all minerals
- `GET /api/minerals/<id>` - Get mineral details
- `POST /api/minerals` - Add new mineral record

### Submissions
- `POST /api/submissions` - Submit mineral photo
- `GET /api/submissions/<id>` - Get submission details
- `GET /api/my-submissions` - Get user submissions

### Rewards
- `GET /api/rewards` - Get reward info
- `GET /api/points` - Check user points

## Project Structure

```
geoscan-minerals/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── templates/           # HTML templates
│   ├── base.html       # Base template
│   ├── index.html      # Home page
│   ├── upload.html     # Upload page
│   └── dashboard.html  # User dashboard
├── static/              # Static files
│   ├── css/            # Stylesheets
│   ├── js/             # JavaScript files
│   └── images/         # Images and icons
└── uploads/            # User uploaded images
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, email support@geoscanminerals.com or open an issue on GitHub.

## Roadmap

- [ ] Mobile app (iOS/Android)
- [ ] Advanced ML model for identification
- [ ] Integration with mining companies
- [ ] Real-time mineral price tracking
- [ ] Advanced geospatial analysis
- [ ] Blockchain integration for verification

## Acknowledgments

- Created for the mining engineering sector in Bhutan
- Special thanks to Aditya University for educational support
- Open-source community for tools and libraries
