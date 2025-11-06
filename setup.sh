#!/bin/bash

# Lucida Flow - Quick Start Script

echo "🎵 Lucida Flow Setup"
echo "===================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

echo ""

# Activate virtual environment and install dependencies
echo "📥 Installing dependencies..."
source venv/bin/activate
pip install -q -r requirements.txt

echo "✓ Dependencies installed"
echo ""

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    cp .env.python.example .env
    echo "✓ Created .env file (you can customize it)"
else
    echo "✓ .env file exists"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "To use the CLI:"
echo "  source venv/bin/activate"
echo "  python cli.py services"
echo "  python cli.py search \"your query\""
echo ""
echo "To start the API:"
echo "  source venv/bin/activate"
echo "  python api_server.py"
echo ""
echo "For more information, see README.md and DOCUMENTATION.md"
