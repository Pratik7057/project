#!/bin/bash
# Activation script to enable deployment
# Usage: ./activate.sh

echo "🔓 Activating deployment configuration..."
echo ""

# Check if config.env exists
if [ ! -f "config.env" ]; then
    echo "❌ config.env file not found!"
    echo "💡 Please run the project first to generate config.env"
    read -p "Press Enter to exit..."
    exit 1
fi

# Update config.env
sed -i 's/DEPLOYMENT_STATUS=DEACTIVATED/DEPLOYMENT_STATUS=ACTIVATED/g' config.env

# Update deploy.sh
sed -i 's/CONFIG_STATUS="DEACTIVATED"/CONFIG_STATUS="ACTIVATED"/g' deploy.sh

# Update docker-compose.yml
sed -i 's/API_STATUS=DEACTIVATED/API_STATUS=ACTIVATED/g' docker-compose.yml

echo "✅ Deployment has been ACTIVATED!"
echo "🚀 You can now run ./deploy.sh to start the services"
echo ""
read -p "Press Enter to continue..."
