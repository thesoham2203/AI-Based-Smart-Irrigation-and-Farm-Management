#!/bin/bash

# Build and deploy frontend to production

set -e

# Configuration
BUILD_DIR="./frontend/web-dashboard"
DEPLOY_DIR="/var/www/irrigation"
NGINX_CONFIG="/etc/nginx/sites-available/irrigation-frontend"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() { echo -e "${GREEN}[INFO]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    error "Node.js is not installed. Please install Node.js first."
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    error "npm is not installed. Please install npm first."
fi

log "Building frontend application..."

# Navigate to frontend directory
cd $BUILD_DIR

# Install dependencies
log "Installing dependencies..."
npm ci

# Build production bundle
log "Building production bundle..."
npm run build

# Check if build was successful
if [ ! -d "dist" ]; then
    error "Build failed - dist directory not found"
fi

log "Build completed successfully"

# Deploy to server (if running on server)
if [[ $EUID -eq 0 ]] || groups $USER | grep -q sudo; then
    log "Deploying to production server..."
    
    # Create deploy directory
    mkdir -p $DEPLOY_DIR
    
    # Copy built files
    cp -r dist/* $DEPLOY_DIR/
    
    # Set proper permissions
    chown -R www-data:www-data $DEPLOY_DIR
    chmod -R 755 $DEPLOY_DIR
    
    # Create nginx configuration if it doesn't exist
    if [ ! -f "$NGINX_CONFIG" ]; then
        log "Creating Nginx configuration..."
        cat > $NGINX_CONFIG << EOF
server {
    listen 3000;
    server_name _;
    root $DEPLOY_DIR;
    index index.html;
    
    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_types text/css text/javascript application/javascript application/json;
    
    # Main app
    location / {
        try_files \$uri \$uri/ /index.html;
    }
    
    # Static assets with long cache
    location /static/ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # API proxy (if backend is on same server)
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
}
EOF
        
        # Enable site
        ln -sf $NGINX_CONFIG /etc/nginx/sites-enabled/irrigation-frontend
        
        # Test nginx configuration
        nginx -t
        
        # Reload nginx
        systemctl reload nginx
        
        log "Nginx configuration created and reloaded"
    fi
    
    log "Frontend deployed successfully to $DEPLOY_DIR"
    log "Frontend URL: http://$(hostname -I | awk '{print $1}'):3000"
    
else
    log "Build completed. To deploy:"
    log "1. Copy dist/* to your web server"
    log "2. Configure your web server to serve the files"
    log "3. Set up proxy for /api/ to your backend server"
fi

# Create deployment info
cat > dist/deployment-info.json << EOF
{
    "buildTime": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
    "version": "$(git rev-parse --short HEAD 2>/dev/null || echo 'unknown')",
    "nodeVersion": "$(node --version)",
    "npmVersion": "$(npm --version)"
}
EOF

log "=== Frontend Deployment Complete ==="
echo ""
log "Build artifacts are in: $(pwd)/dist/"
log "Deployment info: $(pwd)/dist/deployment-info.json"

# Show build size
if command -v du &> /dev/null; then
    echo ""
    log "Build size:"
    du -sh dist/
    echo ""
    log "Largest files:"
    find dist/ -type f -exec du -h {} + | sort -rh | head -10
fi
