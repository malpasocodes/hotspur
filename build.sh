#!/bin/bash
# Render build script for Hotspur Shakespeare Search

set -e  # Exit on any error

echo "🎭 Building Hotspur Shakespeare Search..."

# Install Python dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p hotspur_search/data
mkdir -p hotspur_search/index

# Check if Shakespeare data exists, if not download/extract it
if [ ! -f "data/processed/shakespeare_only.txt" ]; then
    echo "📚 Shakespeare data not found, need to set up data..."
    echo "⚠️  WARNING: Shakespeare data missing - deployment may fail"
    echo "   Please ensure data/processed/shakespeare_only.txt is available"
    exit 1
fi

# Parse Shakespeare texts and create search index
echo "🔍 Setting up search system..."
echo "🔧 Using fixed parser for proper work detection..."
python fix_parser.py

# Verify the build
echo "✅ Verifying build..."
python verify_setup.py

echo "🎉 Build complete! Hotspur is ready to serve."