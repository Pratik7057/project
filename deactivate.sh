#!/bin/bash
# Deactivation script to disable deployment
# Usage: ./deactivate.sh

echo "🔒 Deactivating deployment configuration..."
echo ""

# Update config.env
if [ -f "config.env" ]; then
    sed -i 's/DEPLOYMENT_STATUS=ACTIVATED/DEPLOYMENT_STATUS=DEACTIVATED/g' config.env
fi

# Update deploy.sh
sed -i 's/CONFIG_STATUS="ACTIVATED"/CONFIG_STATUS="DEACTIVATED"/g' deploy.sh

# Update docker-compose.yml
sed -i 's/API_STATUS=ACTIVATED/API_STATUS=DEACTIVATED/g' docker-compose.yml

echo "✅ Deployment has been DEACTIVATED!"
echo "🛡️ All services are now disabled for security"
echo "💡 Run ./activate.sh to enable deployment again"
echo ""
read -p "Press Enter to continue..."
