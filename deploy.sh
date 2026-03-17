#!/bin/bash

# Deployment script for Digital Ocean Droplet
# Usage: ./deploy.sh

set -e  # Exit on error

echo "🚀 Starting deployment to Digital Ocean Droplet..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration - UPDATE THESE VALUES
DROPLET_USER="root"  # Change if using different user
DROPLET_IP="170.64.177.253"  # Change to your droplet IP
APP_DIR="/var/www/sustainable-shine-backend"  # Change to your app directory on droplet
BRANCH="main"  # Git branch to deploy

# Check if configuration is updated
if [ "$DROPLET_IP" = "YOUR_DROPLET_IP" ]; then
    echo -e "${RED}❌ Error: Please update DROPLET_IP in deploy.sh${NC}"
    exit 1
fi

echo -e "${YELLOW}📋 Deployment Configuration:${NC}"
echo "   Server: ${DROPLET_USER}@${DROPLET_IP}"
echo "   App Directory: ${APP_DIR}"
echo "   Branch: ${BRANCH}"
echo ""

# Confirm deployment
read -p "Continue with deployment? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Deployment cancelled."
    exit 1
fi

echo -e "${GREEN}✅ Starting deployment...${NC}"

# Deploy via SSH
ssh ${DROPLET_USER}@${DROPLET_IP} << 'ENDSSH'
set -e

# Configuration (must match above)
APP_DIR="/var/www/sustainable-shine-backend"
BRANCH="main"

echo "📂 Navigating to app directory..."
cd $APP_DIR

echo "📥 Pulling latest changes from Git..."
git fetch origin
git checkout $BRANCH
git pull origin $BRANCH

echo "🐍 Activating virtual environment..."
source venv/bin/activate

echo "📦 Installing/updating dependencies..."
pip install -r requirements.txt --quiet

echo "🗄️  Running database migrations..."
python manage.py migrate --noinput

echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

echo "🔄 Restarting Gunicorn service..."
sudo systemctl restart gunicorn

echo "✅ Checking service status..."
sudo systemctl status gunicorn --no-pager -l

ENDSSH

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ Deployment completed successfully!${NC}"
    echo ""
    echo "🌐 Your site should now be updated at your domain."
    echo ""
else
    echo ""
    echo -e "${RED}❌ Deployment failed. Check the errors above.${NC}"
    exit 1
fi
