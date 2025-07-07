@echo off
REM Deployment script for Music API on Windows
REM Usage: deploy.bat

REM Load configuration from config.env file
if exist "config.env" (
    for /f "usebackq tokens=1,2 delims==" %%a in ("config.env") do (
        if /i "%%a"=="DEPLOYMENT_STATUS" set CONFIG_STATUS=%%b
    )
) else (
    set CONFIG_STATUS=DEACTIVATED
)

REM Configuration Check - Deployment Deactivated
if "%CONFIG_STATUS%"=="DEACTIVATED" (
    echo ⚠️  DEPLOYMENT DEACTIVATED
    echo 🔒 This deployment has been disabled via configuration
    echo 💡 To enable deployment, edit config.env and change DEPLOYMENT_STATUS to ACTIVATED
    echo 📁 Config file: config.env
    echo.
    pause
    exit /b 1
)

echo 📦 Deploying Music API locally...

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
echo � Your API is now available at: http://localhost:8000
echo � Your frontend can be accessed through the API at: http://localhost:8000
echo 📋 To check logs: docker-compose logs -f
echo � API Documentation: http://localhost:8000/docs
