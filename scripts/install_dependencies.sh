#!/bin/bash
# Install all dependencies with options

echo "📦 Advanced Job Engine - Dependency Installer"
echo "=============================================="
echo ""

# Base installation
echo "Installing base dependencies..."
pip install python-dateutil PyPDF2 python-docx requests

# Optional: Data processing
read -p "Install data processing libraries (pandas, openpyxl)? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    pip install pandas openpyxl
    echo "✓ Data processing libraries installed"
fi

# Optional: Development tools
read -p "Install development tools (pytest, black, flake8)? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    pip install pytest pytest-cov black flake8 mypy
    echo "✓ Development tools installed"
fi

# Optional: Documentation
read -p "Install documentation tools (sphinx)? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    pip install sphinx sphinx-rtd-theme
    echo "✓ Documentation tools installed"
fi

echo ""
echo "=============================================="
echo "✅ Dependencies installed!"
echo "=============================================="
