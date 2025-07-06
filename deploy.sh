#!/bin/bash
# Deployment script for Radha Music API on a VPS
# Usage: ./deploy.sh

echo "📦 Deploying Music API to VPS (www.Radhaapi.me)..."

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
echo "🔗 Your frontend is now available at: https://www.Radhaapi.me"
echo "🔌 Your API is now available at: https://api.radhaapi.me"
echo "🔒 To set up SSL: Run \"docker exec -it $CONTAINER_ID certbot --nginx -d www.Radhaapi.me -d api.radhaapi.me\""
echo "📋 To check logs: docker-compose logs -f"
