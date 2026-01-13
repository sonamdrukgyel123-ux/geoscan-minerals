#!/bin/bash

# GeoScan Minerals - Local Development Setup Script
# For macOS and Linux users
# Usage: bash LOCAL_SETUP.sh

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'  # No Color

# Helper functions
print_header() {
    echo -e "\n${BLUE}=== $1 ===${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Start setup
echo -e "${BLUE}"
echo "  ╔═══════════════════════════════════════════════════════════╗"
echo "  ║   GeoScan Minerals - Local Development Setup              ║"
echo "  ║   Starting automated setup for your environment...       ║"
echo "  ╚═══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check Python
print_header "Checking Python Installation"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    print_success "Python 3 found: $PYTHON_VERSION"
else
    print_error "Python 3 not found. Please install Python 3.8 or higher."
    echo "  Download from: https://www.python.org/downloads/"
    exit 1
fi

# Check Git
print_header "Checking Git Installation"
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version)
    print_success "$GIT_VERSION"
else
    print_error "Git not found. Please install Git first."
    exit 1
fi

# Create virtual environment
print_header "Setting up Virtual Environment"
if [ -d "venv" ]; then
    print_info "Virtual environment already exists"
else
    python3 -m venv venv
    print_success "Virtual environment created"
fi

# Activate virtual environment
print_header "Activating Virtual Environment"
source venv/bin/activate
print_success "Virtual environment activated"

# Upgrade pip
print_header "Updating pip"
python -m pip install --upgrade pip > /dev/null 2>&1
print_success "pip upgraded"

# Install dependencies
print_header "Installing Dependencies"
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    print_success "Dependencies installed"
else
    print_error "requirements.txt not found"
    exit 1
fi

# Setup environment file
print_header "Setting up Environment Configuration"
if [ -f ".env" ]; then
    print_info ".env file already exists"
else
    if [ -f ".env.example" ]; then
        cp .env.example .env
        print_success ".env file created from template"
        echo ""
        print_info "Please edit .env file with your configuration"
        echo "  nano .env  # or use your preferred editor"
    else
        print_error ".env.example not found"
        exit 1
    fi
fi

# Initialize database
print_header "Initializing Database"
if [ -f "app.py" ]; then
    echo -e "\n${YELLOW}Initializing database...${NC}"
    python3 << 'EOF'
from app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
    print("\nDatabase initialized successfully!")
EOF
    print_success "Database ready"
else
    print_error "app.py not found"
    exit 1
fi

# Summary
print_header "Setup Complete!"
echo -e "${GREEN}Your local development environment is ready!${NC}"
echo ""
echo "Next steps:"
echo "  1. Edit .env file with your configuration (if needed)"
echo "  2. Run the Flask app: python app.py"
echo "  3. Open http://localhost:5000 in your browser"
echo "  4. In another terminal, run tests: python test_local.py"
echo ""
echo "The virtual environment is already activated."
echo "To deactivate later, run: deactivate"
echo ""
print_info "For detailed setup instructions, see DEVELOPMENT.md"
echo -e "\n${GREEN}Happy coding! 🎉${NC}\n"
