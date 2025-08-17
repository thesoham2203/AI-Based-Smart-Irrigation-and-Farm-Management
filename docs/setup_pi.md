# Raspberry Pi Setup

1. Flash latest Raspberry Pi OS (Lite recommended).
2. Enable SSH & I2C / SPI interfaces if needed (`raspi-config`).
3. Clone repository & install dependencies:
```
sudo apt update
sudo apt install -y python3-venv git
git clone <repo-url>
cd raspberry-pi
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
4. Copy config:
```
cp config/config.example.yaml config/config.yaml
```
5. Edit thresholds as needed.
6. Run in foreground for test:
```
python src/main.py
```
7. (Optional) Create systemd service.
