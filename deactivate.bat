@echo off
REM Deactivation script to disable deployment
REM Usage: deactivate.bat

echo 🔒 Deactivating deployment configuration...
echo.

REM Update config.env
if exist "config.env" (
    powershell -Command "(Get-Content config.env) -replace 'DEPLOYMENT_STATUS=ACTIVATED', 'DEPLOYMENT_STATUS=DEACTIVATED' | Set-Content config.env"
)

REM Update deploy.bat
powershell -Command "(Get-Content deploy.bat) -replace 'CONFIG_STATUS=ACTIVATED', 'CONFIG_STATUS=DEACTIVATED' | Set-Content deploy.bat"

REM Update docker-compose.yml
powershell -Command "(Get-Content docker-compose.yml) -replace 'API_STATUS=ACTIVATED', 'API_STATUS=DEACTIVATED' | Set-Content docker-compose.yml"

echo ✅ Deployment has been DEACTIVATED!
echo 🛡️ All services are now disabled for security
echo 💡 Run activate.bat to enable deployment again
echo.
pause
