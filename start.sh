#!/bin/bash

# ============================================================================
# MINISTRIA E SHËNDETËSISË DHE MBROJTJES SOCIALE
# Platforma Kombëtare AI e Imazherisë Mjekësore
# Startup Script
# ============================================================================

set -e

echo "=========================================="
echo "🇦🇱 MOH Albania Medical Imaging Platform"
echo "=========================================="
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop."
    exit 1
fi

echo "✓ Docker is running"
echo ""

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose not found. Please install Docker Compose."
    exit 1
fi

echo "✓ docker-compose is available"
echo ""

# Stop any existing containers
echo "🛑 Stopping existing containers..."
docker-compose down 2>/dev/null || true
echo ""

# Build and start services
echo "🏗️  Building and starting services..."
echo "This may take 5-10 minutes on first run..."
echo ""

docker-compose up -d --build

echo ""
echo "⏳ Waiting for services to be healthy..."
echo ""

# Wait for services
sleep 10

# Check service status
echo "📊 Service Status:"
echo ""
docker-compose ps
echo ""

echo "=========================================="
echo "✅ Platform Started Successfully!"
echo "=========================================="
echo ""
echo "Access Points:"
echo "  🏠 Dashboard:     http://localhost/"
echo "  👁️  OHIF Viewer:   http://localhost/viewer"
echo "  🗄️  Orthanc PACS:  http://localhost:8042"
echo "  🤖 MONAI Label:   http://localhost:8000/info/"
echo ""
echo "Direct Access (for testing):"
echo "  Orthanc:  http://localhost:8042"
echo "  MONAI:    http://localhost:8000"
echo ""
echo "To view logs:"
echo "  docker-compose logs -f"
echo ""
echo "To stop:"
echo "  docker-compose down"
echo ""
echo "=========================================="
