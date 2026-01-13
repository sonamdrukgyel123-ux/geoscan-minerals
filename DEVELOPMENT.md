# GeoScan Minerals - Local Development & Testing Guide

This guide provides step-by-step instructions for setting up GeoScan Minerals for local development and testing on your computer.

## Prerequisites

- **Python**: 3.8 or higher
- **pip**: Python package manager (comes with Python)
- **Git**: Version control system
- **Virtual Environment**: venv (built-in with Python 3.3+)
- **Code Editor**: VS Code, PyCharm, or your preferred editor
- **Operating System**: Windows, macOS, or Linux

## Quick Start (5 minutes)

### Windows Users:

```bash
# 1. Clone the repository
git clone https://github.com/sonamdrukgyel123-ux/geoscan-minerals.git
cd geoscan-minerals

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
copy .env.example .env
# Edit .env with your local settings

# 5. Run the application
python app.py
```

Then open browser: `http://localhost:5000`

### macOS/Linux Users:

```bash
# 1. Clone the repository
git clone https://github.com/sonamdrukgyel123-ux/geoscan-minerals.git
cd geoscan-minerals

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
cp .env.example .env
# Edit .env with your local settings

# 5. Run the application
python app.py
```

Then open browser: `http://localhost:5000`

## Detailed Setup Instructions

### Step 1: Clone the Repository

```bash
git clone https://github.com/sonamdrukgyel123-ux/geoscan-minerals.git
cd geoscan-minerals
```

### Step 2: Create Virtual Environment

A virtual environment isolates project dependencies:

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` prefix in your terminal.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Flask 2.3.3
- Flask-CORS 4.0.0
- Gunicorn 21.2.0
- And other required packages

### Step 4: Configure Environment Variables

```bash
# Copy template
cp .env.example .env  # macOS/Linux
# OR
copy .env.example .env  # Windows
```

**Edit `.env` file** with these settings for local development:

```ini
# Flask
FLASK_ENV=development
FLASK_APP=app.py
FLASK_DEBUG=True
SECRET_KEY=dev-secret-key-12345

# Database (local SQLite)
DATABASE_URL=sqlite:///geoscan_local.db

# Disable external APIs for testing
MINERAL_API_PROVIDER=mock
GOOGLE_MAPS_API_KEY=test-key

# Email (optional for development)
MAIL_SERVER=localhost
MAIL_PORT=1025

# Rewards System
BASE_REWARD_POINTS=100
REWARD_CURRENCY=TEST_GEMS
```

### Step 5: Initialize Database

```bash
python
```

In Python shell:
```python
from app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
    print("Database initialized!")
exit()
```

### Step 6: Run the Application

```bash
python app.py
```

You should see:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

Open browser: **http://localhost:5000**

## Development Workflow

### Directory Structure

```
geoscan-minerals/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── requirements.txt      # Dependencies
├── .env.example         # Environment template
├── .env                 # Local environment (not committed)
├── .gitignore          # Git ignore rules
├── venv/               # Virtual environment (not committed)
├── geoscan_local.db    # SQLite database (local)
└── README.md           # Project documentation
```

### Making Changes

1. **Create a branch** for your feature:
```bash
git checkout -b feature/your-feature-name
```

2. **Make your changes** in the code

3. **Test your changes** locally (see Testing section)

4. **Commit your changes**:
```bash
git add .
git commit -m "Add description of changes"
```

5. **Push to GitHub**:
```bash
git push origin feature/your-feature-name
```

6. **Create a Pull Request** on GitHub

## Testing

### Run the Application in Debug Mode

When `FLASK_DEBUG=True` in `.env`:
- Auto-reloads on code changes
- Interactive debugger on errors
- Shows detailed error pages

### Test API Endpoints

**Using curl:**
```bash
# Test if server is running
curl http://localhost:5000/

# Test API endpoint
curl http://localhost:5000/api/minerals
```

**Using Python requests:**
```python
import requests

response = requests.get('http://localhost:5000/api/minerals')
print(response.json())
```

### Test Database

```bash
# Check if database exists
ls -la geoscan_local.db  # macOS/Linux
dir geoscan_local.db    # Windows
```

### View Logs

Logs appear in terminal where Flask is running. Set log level in `.env`:
```ini
LOG_LEVEL=DEBUG  # More verbose
LOG_LEVEL=INFO   # Less verbose
```

## Troubleshooting

### Python not found
```bash
# Check Python version
python --version
python3 --version

# May need to use python3 on some systems
python3 -m venv venv
```

### Port 5000 already in use
```bash
# Find process using port 5000
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows

# Kill the process
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows

# Or change port in code:
# Change app.run(port=5000) to app.run(port=5001)
```

### Virtual environment not activating
```bash
# Try full path
./venv/Scripts/activate  # Windows PowerShell
source ./venv/bin/activate  # macOS/Linux
```

### Dependency installation fails
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Clear pip cache
pip cache purge

# Try installing again
pip install -r requirements.txt
```

### Database errors
```bash
# Remove old database and recreate
rm geoscan_local.db  # macOS/Linux
del geoscan_local.db  # Windows

# Reinitialize
python app.py  # Will create new database
```

## Development Tips

### Use IDE Features
- **VS Code**: Install Python extension
- **PyCharm**: Community edition is free
- Enable code completion and debugging

### Format Code
```bash
# Install formatter
pip install black

# Format code
black .
```

### Check Code Quality
```bash
# Install linter
pip install pylint

# Check code
pylint app.py
```

### Git Best Practices
```bash
# See what changed
git status

# See differences
git diff

# See commit history
git log --oneline
```

## Deactivating Virtual Environment

```bash
deactivate
```

Your terminal will return to normal state.

## Next Steps

After setting up locally:

1. Read `README.md` for API documentation
2. Explore the codebase in `app.py`
3. Review `config.py` for configuration options
4. Test the API endpoints
5. Make your first contribution!

## Getting Help

If you encounter issues:

1. **Check GitHub Issues**: https://github.com/sonamdrukgyel123-ux/geoscan-minerals/issues
2. **Read the documentation** in README.md
3. **Review error messages** carefully
4. **Search online** for the error message
5. **Ask in Issues** if problem persists

## Happy Coding! 🎉

Your local environment is now ready for development and testing!
