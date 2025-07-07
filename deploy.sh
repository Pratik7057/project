#!/bin/bash
# Deployment script for Music API locally
# Usage: ./deploy.sh

# Configuration Check - Deployment Deactivated
CONFIG_STATUS="DEACTIVATED"
if [ "$CONFIG_STATUS" = "DEACTIVATED" ]; then
    echo "⚠️  DEPLOYMENT DEACTIVATED"
    echo "🔒 This deployment has been disabled via configuration"
    echo "💡 To enable deployment, change CONFIG_STATUS to ACTIVATED in this file"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

echo "📦 Deploying Music API locally..."

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose is not installed. Installing..."
    sudo apt update
    sudo apt install -y docker-compose
fi

# Check if docker is running
if ! docker info &> /dev/null; then
    echo "❌ Docker is not running. Starting docker..."
    sudo systemctl start docker
fi

# Build and start the services
echo "🔨 Building and starting services..."
docker-compose up -d --build

# Get container ID
CONTAINER_ID=$(docker-compose ps -q music-api)

# Show status
echo "✅ Deployment completed!"
echo "� Your API is now available at: http://localhost:8000"
echo "� Your frontend can be accessed through the API at: http://localhost:8000"
echo "📋 To check logs: docker-compose logs -f"
echo "📖 API Documentation: http://localhost:8000/docs"
