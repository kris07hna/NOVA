#!/bin/bash

# PythonAnywhere Setup Script
# Run this script in a PythonAnywhere Bash console

echo "=== NOVA PythonAnywhere Setup ==="
echo ""

# Check if in correct directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py not found. Please run this script from the NOVA directory."
    exit 1
fi

echo "✓ Found NOVA project"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
if [ ! -d "$HOME/.virtualenvs/nova-env" ]; then
    mkvirtualenv --python=/usr/bin/python3.10 nova-env
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
workon nova-env

# Upgrade pip
echo ""
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo ""
echo "📦 Installing requirements..."
pip install -r requirements.txt

# Check if .env exists
echo ""
if [ -f ".env" ]; then
    echo "✓ .env file found"
else
    echo "⚠️  Warning: .env file not found"
    echo "   Please create .env file with your API keys"
    echo "   Or set environment variables in PythonAnywhere Web tab"
fi

echo ""
echo "=== Setup Complete! ==="
echo ""
echo "Next steps:"
echo "1. Go to PythonAnywhere Web tab"
echo "2. Add a new web app (Manual configuration, Python 3.10)"
echo "3. Set source code: $HOME/NOVA"
echo "4. Set virtualenv: $HOME/.virtualenvs/nova-env"
echo "5. Update WSGI file to point to wsgi.py"
echo "6. Add environment variables in Web tab"
echo "7. Reload web app"
echo ""
echo "Visit: https://yourusername.pythonanywhere.com"
