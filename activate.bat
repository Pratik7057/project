@echo off
REM Activation script to enable deployment
REM Usage: activate.bat

echo 🔓 Activating deployment configuration...
echo.

REM Check if config.env exists
if not exist "config.env" (
    echo ❌ config.env file not found!
    echo 💡 Please run the project first to generate config.env
    pause
    exit /b 1
)

REM Update config.env
powershell -Command "(Get-Content config.env) -replace 'DEPLOYMENT_STATUS=DEACTIVATED', 'DEPLOYMENT_STATUS=ACTIVATED' | Set-Content config.env"

REM Update deploy.bat
powershell -Command "(Get-Content deploy.bat) -replace 'CONFIG_STATUS=DEACTIVATED', 'CONFIG_STATUS=ACTIVATED' | Set-Content deploy.bat"

REM Update docker-compose.yml
powershell -Command "(Get-Content docker-compose.yml) -replace 'API_STATUS=DEACTIVATED', 'API_STATUS=ACTIVATED' | Set-Content docker-compose.yml"

echo ✅ Deployment has been ACTIVATED!
echo 🚀 You can now run deploy.bat to start the services
echo.
pause
