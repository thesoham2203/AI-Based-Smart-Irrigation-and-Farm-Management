#!/bin/bash

# Deployment script for Irrigation System Backend
# Deploys Django API to production server

set -e

# Configuration
DEPLOY_USER="irrigation"
DEPLOY_DIR="/opt/irrigation-backend"
REPO_URL="https://github.com/your-username/irrigation-system.git"
BRANCH="main"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() { echo -e "${GREEN}[INFO]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

# Check if running as root
if [[ $EUID -ne 0 ]]; then
    error "This script must be run as root (use sudo)"
fi

# Update system
log "Updating system packages..."
apt-get update
apt-get upgrade -y

# Install dependencies
log "Installing system dependencies..."
apt-get install -y \
    python3 python3-pip python3-venv \
    nginx postgresql postgresql-contrib \
    git curl wget \
    build-essential \
    libpq-dev \
    redis-server \
    supervisor \
    certbot python3-certbot-nginx

# Create deploy user
if ! id "$DEPLOY_USER" &>/dev/null; then
    useradd --system --create-home --shell /bin/bash $DEPLOY_USER
    log "Created user: $DEPLOY_USER"
fi

# Setup application directory
log "Setting up application directory..."
mkdir -p $DEPLOY_DIR
cd $DEPLOY_DIR

# Clone or update repository
if [ -d ".git" ]; then
    log "Updating existing repository..."
    sudo -u $DEPLOY_USER git fetch origin
    sudo -u $DEPLOY_USER git reset --hard origin/$BRANCH
else
    log "Cloning repository..."
    sudo -u $DEPLOY_USER git clone -b $BRANCH $REPO_URL .
fi

# Setup virtual environment
log "Setting up Python virtual environment..."
sudo -u $DEPLOY_USER python3 -m venv venv
sudo -u $DEPLOY_USER venv/bin/pip install --upgrade pip

# Install Python dependencies
log "Installing Python dependencies..."
sudo -u $DEPLOY_USER venv/bin/pip install -r backend/requirements.txt
sudo -u $DEPLOY_USER venv/bin/pip install gunicorn psycopg2-binary

# Setup database
log "Setting up PostgreSQL database..."
sudo -u postgres createdb irrigation 2>/dev/null || true
sudo -u postgres createuser $DEPLOY_USER 2>/dev/null || true
sudo -u postgres psql -c "ALTER USER $DEPLOY_USER CREATEDB;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE irrigation TO $DEPLOY_USER;"

# Django setup
log "Running Django migrations..."
cd $DEPLOY_DIR/backend
sudo -u $DEPLOY_USER ../venv/bin/python manage.py collectstatic --noinput
sudo -u $DEPLOY_USER ../venv/bin/python manage.py migrate

# Create superuser
log "Creating Django superuser..."
sudo -u $DEPLOY_USER ../venv/bin/python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@irrigation.local', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
EOF

# Setup Gunicorn service
log "Setting up Gunicorn service..."
cat > /etc/systemd/system/irrigation-backend.service << EOF
[Unit]
Description=Irrigation System Backend
After=network.target

[Service]
User=$DEPLOY_USER
Group=$DEPLOY_USER
WorkingDirectory=$DEPLOY_DIR/backend
Environment="PATH=$DEPLOY_DIR/venv/bin"
ExecStart=$DEPLOY_DIR/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 irrigation_api.wsgi:application
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Setup Nginx
log "Setting up Nginx configuration..."
cat > /etc/nginx/sites-available/irrigation << EOF
server {
    listen 80;
    server_name _;
    
    client_max_body_size 10M;
    
    location /static/ {
        alias $DEPLOY_DIR/backend/staticfiles/;
        expires 30d;
    }
    
    location /media/ {
        alias $DEPLOY_DIR/backend/media/;
        expires 30d;
    }
    
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
    
    location /admin/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
    
    location / {
        root $DEPLOY_DIR/frontend/dist;
        try_files \$uri \$uri/ /index.html;
    }
}
EOF

# Enable nginx site
ln -sf /etc/nginx/sites-available/irrigation /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Set file permissions
chown -R $DEPLOY_USER:$DEPLOY_USER $DEPLOY_DIR
chmod +x $DEPLOY_DIR/backend/manage.py

# Enable and start services
systemctl daemon-reload
systemctl enable irrigation-backend nginx
systemctl start irrigation-backend nginx

# Setup SSL (optional)
read -p "Setup SSL certificate? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    log "Setting up SSL certificate..."
    certbot --nginx -d your-domain.com --non-interactive --agree-tos --email admin@your-domain.com
fi

# Setup firewall
log "Configuring firewall..."
ufw allow 'Nginx Full'
ufw allow ssh
ufw --force enable

log "=== Deployment Complete ==="
echo ""
log "Backend URL: http://$(hostname -I | awk '{print $1}')/api/"
log "Admin URL: http://$(hostname -I | awk '{print $1}')/admin/"
log "Admin credentials: admin / admin123"
echo ""
log "Service status:"
systemctl status irrigation-backend --no-pager -l
systemctl status nginx --no-pager -l
echo ""
log "View logs:"
log "  Backend: sudo journalctl -u irrigation-backend -f"
log "  Nginx: sudo tail -f /var/log/nginx/access.log"
