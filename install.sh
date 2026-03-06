#!/bin/bash

echo "================================================"
echo "  शिक्षा (Shiksha) - STEM Glossary Installer"
echo "  Installing for Nepal school deployment..."
echo "================================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python3 first."
    exit 1
fi

echo "✅ Python3 found: $(python3 --version)"

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip install flask --quiet

echo "✅ Flask installed"

# Seed the database
echo ""
echo "🌱 Setting up database with 507 STEM terms..."
python shabdakosh/seed_data.py

# Get local IP
IP=$(hostname -I | awk '{print $1}')

echo ""
echo "================================================"
echo "  ✅ Shiksha is ready!"
echo "================================================"
echo ""
echo "  To start the app, run:"
echo "  source venv/bin/activate"
echo "  python shabdakosh/app.py"
echo ""
echo "  Then open in browser:"
echo "  → This computer:  http://localhost:5000"
echo "  → Other devices:  http://$IP:5000"
echo ""
echo "  Teacher Dashboard: http://localhost:5000/dashboard"
echo "  Password: shiksha2024"
echo "================================================"