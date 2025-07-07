@echo off
REM Configuration Management Script
REM Usage: config.bat [action] [option]

if "%1"=="" goto show_help
if "%1"=="help" goto show_help
if "%1"=="status" goto show_status
if "%1"=="activate" goto activate
if "%1"=="deactivate" goto deactivate
if "%1"=="activate-deploy" goto activate_deploy
if "%1"=="deactivate-deploy" goto deactivate_deploy
if "%1"=="activate-api" goto activate_api
if "%1"=="deactivate-api" goto deactivate_api
goto show_help

:show_help
echo 🔧 Configuration Management Tool
echo.
echo Usage: config.bat [action]
echo.
echo Actions:
echo   status           - Show current configuration status
echo   activate         - Activate both deployment and API
echo   deactivate       - Deactivate both deployment and API
echo   activate-deploy  - Activate deployment only
echo   deactivate-deploy- Deactivate deployment only
echo   activate-api     - Activate API only
echo   deactivate-api   - Deactivate API only
echo   help             - Show this help
echo.
goto end

:show_status
echo 📊 Current Configuration Status:
echo.
if exist "config.env" (
    for /f "usebackq tokens=1,2 delims==" %%a in ("config.env") do (
        if /i "%%a"=="DEPLOYMENT_STATUS" echo 🚀 Deployment: %%b
        if /i "%%a"=="API_STATUS" echo 🔌 API: %%b
    )
) else (
    echo ❌ config.env file not found
)
echo.
goto end

:activate
echo 🟢 Activating both deployment and API...
powershell -Command "(Get-Content config.env) -replace 'DEPLOYMENT_STATUS=DEACTIVATED', 'DEPLOYMENT_STATUS=ACTIVATED' | Set-Content config.env"
powershell -Command "(Get-Content config.env) -replace 'API_STATUS=DEACTIVATED', 'API_STATUS=ACTIVATED' | Set-Content config.env"
echo ✅ Both deployment and API activated
goto end

:deactivate
echo 🔴 Deactivating both deployment and API...
powershell -Command "(Get-Content config.env) -replace 'DEPLOYMENT_STATUS=ACTIVATED', 'DEPLOYMENT_STATUS=DEACTIVATED' | Set-Content config.env"
powershell -Command "(Get-Content config.env) -replace 'API_STATUS=ACTIVATED', 'API_STATUS=DEACTIVATED' | Set-Content config.env"
echo ✅ Both deployment and API deactivated
goto end

:activate_deploy
echo 🟢 Activating deployment...
powershell -Command "(Get-Content config.env) -replace 'DEPLOYMENT_STATUS=DEACTIVATED', 'DEPLOYMENT_STATUS=ACTIVATED' | Set-Content config.env"
echo ✅ Deployment activated
goto end

:deactivate_deploy
echo 🔴 Deactivating deployment...
powershell -Command "(Get-Content config.env) -replace 'DEPLOYMENT_STATUS=ACTIVATED', 'DEPLOYMENT_STATUS=DEACTIVATED' | Set-Content config.env"
echo ✅ Deployment deactivated
goto end

:activate_api
echo 🟢 Activating API...
powershell -Command "(Get-Content config.env) -replace 'API_STATUS=DEACTIVATED', 'API_STATUS=ACTIVATED' | Set-Content config.env"
echo ✅ API activated
goto end

:deactivate_api
echo 🔴 Deactivating API...
powershell -Command "(Get-Content config.env) -replace 'API_STATUS=ACTIVATED', 'API_STATUS=DEACTIVATED' | Set-Content config.env"
echo ✅ API deactivated
goto end

:end
