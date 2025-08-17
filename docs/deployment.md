# Irrigation System - Production Deployment Guide

## Overview
This guide covers the complete deployment of the Precision Irrigation IoT system across all components.

## Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Raspberry Pi  │    │   Backend API   │    │   Web Frontend  │
│   (Edge Agent)  │◄──►│   (Django)      │◄──►│   (React)       │
│                 │    │                 │    │                 │
│ • Sensors       │    │ • REST API      │    │ • Dashboard     │
│ • Relay Control │    │ • Database      │    │ • Controls      │
│ • Data Collection│    │ • Weather API   │    │ • Charts        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Prerequisites

### Hardware Requirements
- **Raspberry Pi 4B** (4GB+ RAM recommended)
- **MicroSD Card** (32GB+ Class 10)
- **DHT22** Temperature/Humidity sensor
- **MCP3008** ADC chip
- **Soil Moisture Sensor** (analog)
- **5V Relay Module**
- **Water Pump** (12V DC recommended)
- **Jumper Wires** and breadboard
- **Power Supply** (5V 3A for Pi, 12V for pump)

### Software Requirements
- **Raspberry Pi OS** (Bullseye or newer)
- **Python 3.9+**
- **Node.js 16+** (for frontend)
- **Docker** (optional, for containerized deployment)

## Deployment Options

### Option 1: All-in-One Raspberry Pi (Recommended for Small Scale)
```bash
# Single device deployment
┌─────────────────────────────┐
│      Raspberry Pi 4B       │
│                             │
│  ┌─────────┐ ┌───────────┐  │
│  │ Backend │ │ Frontend  │  │
│  │ Django  │ │ React     │  │
│  │ :8000   │ │ :3000     │  │
│  └─────────┘ └───────────┘  │
│                             │
│  ┌─────────────────────────┐│
│  │    Edge Agent           ││
│  │    Sensor Control       ││
│  └─────────────────────────┘│
└─────────────────────────────┘
```

### Option 2: Distributed Deployment (Recommended for Production)
```bash
# Multi-device deployment
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Raspberry Pi  │    │   Cloud Server  │    │   Web Server    │
│                 │    │                 │    │                 │
│  Edge Agent     │    │  Backend API    │    │  Frontend       │
│  Sensors        │    │  Database       │    │  Static Files   │
│  Relay Control  │    │  Weather API    │    │  Load Balancer  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Step-by-Step Deployment

### 1. Raspberry Pi Edge Agent Setup

#### Hardware Connections
```
DHT22 Sensor:
- VCC → 3.3V (Pin 1)
- GND → Ground (Pin 6)
- DATA → GPIO 4 (Pin 7)

MCP3008 ADC:
- VCC → 3.3V (Pin 1)
- GND → Ground (Pin 6)
- CLK → GPIO 11 (Pin 23)
- DOUT → GPIO 9 (Pin 21)
- DIN → GPIO 10 (Pin 19)
- CS → GPIO 8 (Pin 24)

Soil Moisture Sensor:
- VCC → 3.3V
- GND → Ground
- A0 → MCP3008 CH0

Relay Module:
- VCC → 5V (Pin 2)
- GND → Ground (Pin 6)
- IN → GPIO 18 (Pin 12)
```

#### Software Installation
```bash
# 1. Download installation script
curl -sSL https://raw.githubusercontent.com/your-repo/irrigation-system/main/scripts/install_pi.sh -o install_pi.sh

# 2. Make executable and run
chmod +x install_pi.sh
sudo ./install_pi.sh

# 3. Configure the system
sudo nano /opt/irrigation/config/config.yaml

# 4. Start the service
sudo systemctl start irrigation
sudo systemctl status irrigation

# 5. Check logs
sudo journalctl -u irrigation -f
```

#### Configuration File (`/opt/irrigation/config/config.yaml`)
```yaml
# Irrigation System Configuration
api:
  base_url: "http://your-backend-server:8000"
  timeout: 30
  retry_attempts: 3

sensors:
  dht22:
    pin: 4
    read_interval: 60  # seconds
  
  soil_moisture:
    mcp3008_channel: 0
    dry_threshold: 30
    wet_threshold: 70
    calibration_offset: 0

irrigation:
  pump_pin: 18
  max_duration: 1800  # 30 minutes max
  min_interval: 300   # 5 minutes between cycles
  auto_mode: true

logging:
  level: "INFO"
  file: "/opt/irrigation/logs/irrigation.log"
  max_size: "10MB"
  backup_count: 5
```

### 2. Backend API Deployment

#### Option A: Cloud Server (DigitalOcean, AWS, etc.)
```bash
# 1. Create server (Ubuntu 20.04+)
# 2. Connect via SSH
ssh root@your-server-ip

# 3. Download and run deployment script
curl -sSL https://raw.githubusercontent.com/your-repo/irrigation-system/main/scripts/deploy_backend.sh -o deploy_backend.sh
chmod +x deploy_backend.sh
sudo ./deploy_backend.sh

# 4. Configure environment variables
sudo nano /opt/irrigation-backend/.env
```

#### Environment Configuration (`.env`)
```bash
# Django Settings
DEBUG=False
SECRET_KEY=your-super-secret-key-here
ALLOWED_HOSTS=your-domain.com,your-server-ip

# Database
DATABASE_URL=postgresql://irrigation:password@localhost/irrigation

# Weather API
OPENWEATHER_API_KEY=your-openweather-api-key

# Security
CORS_ALLOWED_ORIGINS=http://your-frontend-domain.com,https://your-frontend-domain.com

# Email (for notifications)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

#### Option B: Docker Deployment
```bash
# 1. Clone repository
git clone https://github.com/your-repo/irrigation-system.git
cd irrigation-system

# 2. Create environment file
cp .env.example .env
nano .env

# 3. Start services
docker-compose up -d

# 4. Run migrations
docker-compose exec backend python manage.py migrate

# 5. Create superuser
docker-compose exec backend python manage.py createsuperuser
```

### 3. Frontend Deployment

#### Option A: Static Hosting (Netlify, Vercel)
```bash
# 1. Build the frontend
cd frontend/web-dashboard
npm install
npm run build

# 2. Deploy dist/ folder to your hosting service
# 3. Set environment variable: REACT_APP_API_URL=https://your-backend-domain.com
```

#### Option B: Self-hosted
```bash
# 1. Run deployment script
cd frontend/web-dashboard
chmod +x ../../scripts/deploy_frontend.sh
sudo ../../scripts/deploy_frontend.sh
```

### 4. SSL Certificate Setup
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

## Testing the Deployment

### 1. Hardware Test
```bash
# On Raspberry Pi
cd /opt/irrigation
sudo -u irrigation venv/bin/python src/main.py --test

# Expected output:
# ✅ DHT22 sensor: OK
# ✅ Soil moisture sensor: OK  
# ✅ Relay control: OK
# ✅ API connection: OK
```

### 2. API Test
```bash
# Check backend health
curl http://your-backend-domain/api/health/

# Test sensor data endpoint
curl http://your-backend-domain/api/readings/latest/

# Test manual irrigation
curl -X POST http://your-backend-domain/api/control/ \
  -H "Content-Type: application/json" \
  -d '{"command": "start_irrigation", "duration": 30}'
```

### 3. Frontend Test
```bash
# Open in browser
http://your-frontend-domain

# Check console for errors
# Verify real-time data updates
# Test manual controls
```

## Monitoring and Maintenance

### Log Locations
```bash
# Raspberry Pi Edge Agent
sudo journalctl -u irrigation -f
tail -f /opt/irrigation/logs/irrigation.log

# Backend API
sudo journalctl -u irrigation-backend -f
tail -f /var/log/nginx/access.log

# System monitoring
htop
df -h
free -h
```

### Health Checks
```bash
# Create monitoring script
cat > /usr/local/bin/irrigation-health.sh << 'EOF'
#!/bin/bash
# Health check script

echo "=== Irrigation System Health Check ==="
echo "Time: $(date)"
echo ""

# Check services
echo "Service Status:"
systemctl is-active irrigation || echo "❌ Edge Agent DOWN"
systemctl is-active irrigation-backend || echo "❌ Backend DOWN"
systemctl is-active nginx || echo "❌ Nginx DOWN"
echo ""

# Check disk space
echo "Disk Usage:"
df -h | grep -E "(/$|/opt)"
echo ""

# Check memory
echo "Memory Usage:"
free -h
echo ""

# Check API
echo "API Health:"
curl -s http://localhost:8000/api/health/ || echo "❌ API unreachable"
echo ""

# Check sensors (on Pi)
if [ -f /opt/irrigation/src/main.py ]; then
    echo "Sensor Status:"
    cd /opt/irrigation
    sudo -u irrigation timeout 10 venv/bin/python src/main.py --test
fi
EOF

chmod +x /usr/local/bin/irrigation-health.sh

# Add to cron for daily checks
echo "0 8 * * * /usr/local/bin/irrigation-health.sh | mail -s 'Irrigation Health Report' admin@yourdomain.com" | crontab -
```

### Backup Strategy
```bash
# Database backup
sudo -u irrigation pg_dump irrigation > /backups/irrigation-$(date +%Y%m%d).sql

# Configuration backup
tar -czf /backups/irrigation-config-$(date +%Y%m%d).tar.gz /opt/irrigation/config/

# Automated backup script
cat > /usr/local/bin/irrigation-backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/backups/irrigation"
mkdir -p $BACKUP_DIR

# Database
sudo -u irrigation pg_dump irrigation | gzip > $BACKUP_DIR/db-$(date +%Y%m%d-%H%M).sql.gz

# Configuration
tar -czf $BACKUP_DIR/config-$(date +%Y%m%d-%H%M).tar.gz /opt/irrigation/config/

# Cleanup old backups (keep 30 days)
find $BACKUP_DIR -name "*.gz" -mtime +30 -delete
EOF

chmod +x /usr/local/bin/irrigation-backup.sh

# Add to cron (daily at 2 AM)
echo "0 2 * * * /usr/local/bin/irrigation-backup.sh" | crontab -
```

## Troubleshooting

### Common Issues

#### 1. Sensor Reading Errors
```bash
# Check hardware connections
# Verify I2C/SPI interfaces
ls /dev/i2c* /dev/spi*

# Test sensors individually
cd /opt/irrigation
sudo -u irrigation venv/bin/python -c "
import adafruit_dht
import board
dht = adafruit_dht.DHT22(board.D4)
print(f'Temp: {dht.temperature}°C, Humidity: {dht.humidity}%')
"
```

#### 2. API Connection Issues
```bash
# Check network connectivity
ping your-backend-domain

# Check firewall
sudo ufw status

# Check service logs
sudo journalctl -u irrigation -n 50
```

#### 3. Permission Issues
```bash
# Fix file permissions
sudo chown -R irrigation:irrigation /opt/irrigation
sudo usermod -a -G gpio,i2c,spi irrigation
```

#### 4. Database Issues
```bash
# Check database connection
sudo -u irrigation psql irrigation -c "SELECT COUNT(*) FROM sensors_sensorreading;"

# Reset database (CAUTION: Deletes all data)
sudo -u irrigation python manage.py flush
sudo -u irrigation python manage.py migrate
```

## Security Considerations

### 1. Network Security
- Use VPN for remote access
- Configure firewall rules
- Regular security updates
- Strong passwords and SSH keys

### 2. Application Security
- Keep Django SECRET_KEY secure
- Use HTTPS in production
- Validate all API inputs
- Regular dependency updates

### 3. Physical Security
- Secure device placement
- Environmental protection
- Backup power supply
- Access control

## Performance Optimization

### 1. Database Optimization
```sql
-- Add indexes for common queries
CREATE INDEX idx_sensorreading_timestamp ON sensors_sensorreading(timestamp);
CREATE INDEX idx_irrigationevent_started ON sensors_irrigationevent(started_at);
```

### 2. API Optimization
- Enable database connection pooling
- Use Redis for caching
- Optimize query patterns
- Enable gzip compression

### 3. Frontend Optimization
- Enable browser caching
- Minimize bundle size
- Use CDN for static assets
- Optimize images

## Scaling Considerations

### Multiple Field Support
```yaml
# Multi-field configuration
fields:
  field_1:
    name: "North Field"
    sensors:
      dht22_pin: 4
      soil_moisture_channel: 0
    irrigation:
      pump_pin: 18
  
  field_2:
    name: "South Field"  
    sensors:
      dht22_pin: 17
      soil_moisture_channel: 1
    irrigation:
      pump_pin: 19
```

### Load Balancing
```nginx
# Nginx load balancer configuration
upstream backend {
    server 192.168.1.10:8000;
    server 192.168.1.11:8000;
    server 192.168.1.12:8000;
}

server {
    location /api/ {
        proxy_pass http://backend;
    }
}
```

This deployment guide provides a comprehensive overview for setting up the irrigation system from development to production. Adjust configurations based on your specific hardware setup and deployment environment.
