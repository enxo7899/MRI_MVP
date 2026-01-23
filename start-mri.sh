#!/bin/bash

# ============================================================================
# MINISTRIA E SHËNDETËSISË DHE MBROJTJES SOCIALE
# MRI Analysis Platform - Startup Script
# ============================================================================

set -e

echo "=========================================="
echo "🇦🇱 MRI Analysis Platform"
echo "Ministria e Shëndetësisë"
echo "=========================================="
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop."
    exit 1
fi

echo "✓ Docker is running"
echo ""

# Stop any existing containers
echo "🛑 Stopping existing containers..."
docker-compose -f docker-compose-simple.yml down 2>/dev/null || true
echo ""

# Build and start
echo "🏗️  Building and starting MRI Analysis App..."
echo "This may take 2-3 minutes on first run..."
echo ""

docker-compose -f docker-compose-simple.yml up -d --build

echo ""
echo "⏳ Waiting for service to be ready..."
sleep 5
echo ""

# Check status
echo "📊 Service Status:"
docker-compose -f docker-compose-simple.yml ps
echo ""

echo "=========================================="
echo "✅ MRI Analysis Platform Started!"
echo "=========================================="
echo ""
echo "🌐 Open in your browser:"
echo "   http://localhost:5001"
echo ""
echo "📋 How to use:"
echo "   1. Open http://localhost:5001"
echo "   2. Upload an MRI scan (.nii, .nii.gz, .dcm, or image)"
echo "   3. Click 'Analizoni Skanimin'"
echo "   4. View Albanian report with detected organs"
echo ""
echo "To view logs:"
echo "   docker-compose -f docker-compose-simple.yml logs -f"
echo ""
echo "To stop:"
echo "   docker-compose -f docker-compose-simple.yml down"
echo ""
echo "=========================================="
