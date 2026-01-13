#!/usr/bin/env python3
"""
Local Testing Script for GeoScan Minerals

Run this script to verify your local setup is working correctly.
Usage: python test_local.py
"""

import os
import sys
import requests
import json
from pathlib import Path

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*50}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*50}{Colors.END}")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")

def test_python_version():
    """Check Python version"""
    print_header("Testing Python Version")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print_success(f"Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print_error(f"Python {version.major}.{version.minor} - Need Python 3.8+")
        return False

def test_required_files():
    """Check if required files exist"""
    print_header("Testing Required Files")
    required_files = [
        'app.py',
        'config.py',
        'requirements.txt',
        '.env',
        'README.md'
    ]
    
    all_exist = True
    for file in required_files:
        if Path(file).exists():
            print_success(f"{file} exists")
        else:
            print_error(f"{file} missing")
            all_exist = False
    
    return all_exist

def test_dependencies():
    """Check if required packages are installed"""
    print_header("Testing Dependencies")
    required_packages = {
        'flask': 'Flask',
        'flask_cors': 'Flask-CORS',
        'requests': 'requests'
    }
    
    all_installed = True
    for module, name in required_packages.items():
        try:
            __import__(module)
            print_success(f"{name} installed")
        except ImportError:
            print_error(f"{name} NOT installed")
            all_installed = False
    
    return all_installed

def test_env_file():
    """Check .env file configuration"""
    print_header("Testing .env Configuration")
    if not Path('.env').exists():
        print_error(".env file not found. Run: cp .env.example .env")
        return False
    
    try:
        with open('.env', 'r') as f:
            env_content = f.read()
            if 'FLASK_ENV=development' in env_content:
                print_success("FLASK_ENV set to development")
            else:
                print_warning("FLASK_ENV not set to development")
            
            if 'SECRET_KEY' in env_content:
                print_success("SECRET_KEY configured")
            else:
                print_error("SECRET_KEY not set")
                return False
            
            if 'DATABASE_URL' in env_content:
                print_success("DATABASE_URL configured")
            else:
                print_error("DATABASE_URL not set")
                return False
        
        return True
    except Exception as e:
        print_error(f"Error reading .env: {e}")
        return False

def test_server_connection():
    """Test if server is running and accessible"""
    print_header("Testing Server Connection")
    print_warning("Make sure the Flask server is running (python app.py)")
    
    try:
        response = requests.get('http://localhost:5000/', timeout=5)
        if response.status_code == 200:
            print_success("Server is accessible at http://localhost:5000")
            return True
        else:
            print_error(f"Server returned status code {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to server. Is it running? (python app.py)")
        return False
    except Exception as e:
        print_error(f"Connection error: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints"""
    print_header("Testing API Endpoints")
    
    endpoints = {
        '/api/health': 'Health Check',
        '/api/minerals': 'Minerals List'
    }
    
    all_working = True
    for endpoint, description in endpoints.items():
        try:
            response = requests.get(f'http://localhost:5000{endpoint}', timeout=5)
            if response.status_code == 200:
                print_success(f"{description} ({endpoint}) - OK")
            else:
                print_warning(f"{description} ({endpoint}) - Status {response.status_code}")
        except Exception as e:
            print_error(f"{description} ({endpoint}) - Error: {e}")
            all_working = False
    
    return all_working

def print_summary(tests):
    """Print test summary"""
    print_header("Test Summary")
    passed = sum(1 for t in tests.values() if t)
    total = len(tests)
    percentage = (passed / total) * 100
    
    print(f"\nPassed: {passed}/{total} tests ({percentage:.0f}%)\n")
    
    for test_name, result in tests.items():
        status = f"{Colors.GREEN}PASS{Colors.END}" if result else f"{Colors.RED}FAIL{Colors.END}"
        print(f"{test_name}: {status}")
    
    return passed == total

def main():
    """Run all tests"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}GeoScan Minerals - Local Development Test Suite{Colors.END}")
    print(f"{Colors.BLUE}Testing your local environment setup...{Colors.END}\n")
    
    tests = {
        'Python Version': test_python_version(),
        'Required Files': test_required_files(),
        'Dependencies': test_dependencies(),
        '.env Configuration': test_env_file(),
        'Server Connection': test_server_connection(),
    }
    
    # Only test API endpoints if server is running
    if tests.get('Server Connection', False):
        tests['API Endpoints'] = test_api_endpoints()
    else:
        print_warning("\nSkipping API endpoint tests (server not running)")
    
    # Print summary
    all_pass = print_summary(tests)
    
    if all_pass:
        print(f"\n{Colors.GREEN}{Colors.BOLD}All tests passed! Your environment is ready.{Colors.END}\n")
        return 0
    else:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}Some tests failed. Check the errors above.{Colors.END}\n")
        return 1

if __name__ == '__main__':
    exit(main())
