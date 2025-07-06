@echo off
REM Deployment script for Radha Music API on Windows
REM Usage: deploy.bat

echo 📦 Deploying Music API to VPS (radhaapi.me)...

REM Check if Docker is installed and running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not running or not installed. Please start Docker Desktop.
    exit /b 1
)

REM Build and start the services
echo 🔨 Building and starting services...
docker-compose up -d --build

REM Show status
echo ✅ Deployment completed!
echo 🔗 Your frontend is now available at: https://radhaapi.me
echo 🔌 Your API is now available at: https://api.radhaapi.me
echo 📋 To check logs: docker-compose logs -f
echo 🔒 To set up SSL: Run "docker exec -it [container_id] certbot --nginx -d radhaapi.me -d www.radhaapi.me -d api.radhaapi.me"
