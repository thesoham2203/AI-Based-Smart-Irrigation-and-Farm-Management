#!/bin/bash

# Irrigation System Installation Script for Raspberry Pi
# This script sets up the complete IoT irrigation system

set -e

echo "🌱 Starting Irrigation System Installation..."

# Configuration
INSTALL_DIR="/opt/irrigation"
SERVICE_USER="irrigation"
PYTHON_VERSION="3.11"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

# Check if running on Raspberry Pi
check_platform() {
    log "Checking platform compatibility..."
    
    if ! grep -q "Raspberry Pi" /proc/cpuinfo 2>/dev/null; then
        warn "This script is designed for Raspberry Pi. Proceeding anyway..."
    fi
    
    if [[ $EUID -ne 0 ]]; then
        error "This script must be run as root (use sudo)"
    fi
}

# Update system packages
update_system() {
    log "Updating system packages..."
    apt-get update
    apt-get upgrade -y
    
    log "Installing system dependencies..."
    apt-get install -y \
        python3 python3-pip python3-venv \
        git curl wget \
        build-essential \
        libffi-dev libssl-dev \
        i2c-tools \
        nginx \
        sqlite3
}

# Setup hardware interfaces
setup_hardware() {
    log "Configuring hardware interfaces..."
    
    # Enable I2C and SPI
    raspi-config nonint do_i2c 0
    raspi-config nonint do_spi 0
    
    # Add user to gpio group
    usermod -a -G gpio,i2c,spi $SERVICE_USER 2>/dev/null || true
    
    log "Hardware interfaces configured. Reboot may be required."
}

# Create service user
create_user() {
    log "Creating service user..."
    
    if ! id "$SERVICE_USER" &>/dev/null; then
        useradd --system --create-home --shell /bin/bash $SERVICE_USER
        usermod -a -G gpio,i2c,spi $SERVICE_USER
        log "Created user: $SERVICE_USER"
    else
        log "User $SERVICE_USER already exists"
    fi
}

# Install Python dependencies
install_python_deps() {
    log "Installing Python dependencies..."
    
    # Create virtual environment
    sudo -u $SERVICE_USER python3 -m venv $INSTALL_DIR/venv
    
    # Install packages
    sudo -u $SERVICE_USER $INSTALL_DIR/venv/bin/pip install --upgrade pip
    sudo -u $SERVICE_USER $INSTALL_DIR/venv/bin/pip install -r $INSTALL_DIR/requirements.txt
}

# Setup application files
setup_application() {
    log "Setting up application files..."
    
    # Create directory structure
    mkdir -p $INSTALL_DIR/{config,logs,data}
    
    # Copy application files
    cp -r raspberry-pi/* $INSTALL_DIR/
    
    # Set permissions
    chown -R $SERVICE_USER:$SERVICE_USER $INSTALL_DIR
    chmod +x $INSTALL_DIR/src/main.py
    
    # Copy config template
    if [ ! -f $INSTALL_DIR/config/config.yaml ]; then
        cp $INSTALL_DIR/config/config.example.yaml $INSTALL_DIR/config/config.yaml
        log "Created config file. Please edit: $INSTALL_DIR/config/config.yaml"
    fi
}

# Create systemd service
create_service() {
    log "Creating systemd service..."
    
    cat > /etc/systemd/system/irrigation.service << EOF
[Unit]
Description=Precision Irrigation System
After=network.target
Wants=network.target

[Service]
Type=simple
User=$SERVICE_USER
Group=$SERVICE_USER
WorkingDirectory=$INSTALL_DIR
Environment=PATH=$INSTALL_DIR/venv/bin
ExecStart=$INSTALL_DIR/venv/bin/python src/main.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

# Security settings
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=$INSTALL_DIR

[Install]
WantedBy=multi-user.target
EOF

    systemctl daemon-reload
    systemctl enable irrigation.service
    log "Systemd service created and enabled"
}

# Setup log rotation
setup_logging() {
    log "Setting up log rotation..."
    
    cat > /etc/logrotate.d/irrigation << EOF
$INSTALL_DIR/logs/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    copytruncate
    su $SERVICE_USER $SERVICE_USER
}
EOF
}

# Setup firewall
setup_firewall() {
    log "Configuring firewall..."
    
    if command -v ufw &> /dev/null; then
        ufw allow ssh
        ufw allow 80/tcp
        ufw allow 443/tcp
        ufw --force enable
    else
        warn "UFW not installed, skipping firewall configuration"
    fi
}

# Validate installation
validate_installation() {
    log "Validating installation..."
    
    # Check service status
    if sudo -u $SERVICE_USER $INSTALL_DIR/venv/bin/python -c "import RPi.GPIO, spidev, adafruit_dht"; then
        log "Python dependencies OK"
    else
        warn "Some Python dependencies may be missing"
    fi
    
    # Check hardware access
    if [ -c /dev/spidev0.0 ]; then
        log "SPI interface available"
    else
        warn "SPI interface not available"
    fi
    
    if [ -c /dev/i2c-1 ]; then
        log "I2C interface available"
    else
        warn "I2C interface not available"
    fi
}

# Main installation process
main() {
    log "=== Irrigation System Installation ==="
    
    check_platform
    update_system
    create_user
    setup_hardware
    setup_application
    install_python_deps
    create_service
    setup_logging
    setup_firewall
    validate_installation
    
    log "=== Installation Complete ==="
    echo ""
    log "Next steps:"
    log "1. Edit configuration: sudo nano $INSTALL_DIR/config/config.yaml"
    log "2. Start service: sudo systemctl start irrigation"
    log "3. Check status: sudo systemctl status irrigation"
    log "4. View logs: sudo journalctl -u irrigation -f"
    echo ""
    log "System installed to: $INSTALL_DIR"
    log "Service user: $SERVICE_USER"
    echo ""
    warn "IMPORTANT: A reboot may be required for hardware interfaces to work properly"
}

# Run installation
main "$@"
