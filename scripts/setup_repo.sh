#!/bin/bash
# Setup script for Advanced Job Engine

echo "🚀 Setting up Advanced Job Engine..."
echo "=================================="

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Upgrade pip
echo ""
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Install development dependencies
read -p "Install development dependencies? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    pip install -r requirements-dev.txt
    echo "✓ Development dependencies installed"
fi

# Create data directories
echo ""
echo "📁 Creating data directories..."
mkdir -p data
mkdir -p job_search_data
mkdir -p exports
touch data/.gitkeep
touch job_search_data/.gitkeep

# Copy environment template
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✓ Created .env file (customize as needed)"
fi

# Test installation
echo ""
echo "🧪 Testing installation..."
python3 -c "from src.python_advanced_job_engine import AdvancedJobEngine; print('✅ Installation successful!')" || {
    echo "❌ Installation test failed"
    exit 1
}

echo ""
echo "=================================="
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Place your CV in: data/my_cv.pdf"
echo "2. Place job description in: data/target_job.pdf"
echo "3. Run: python src/python_advanced_job_engine.py"
echo ""
echo "Or follow the Quick Start guide: docs/getting-started.md"
echo "=================================="
