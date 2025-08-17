# 🌱 AI-Based Smart Irrigation and Farm Management System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/Django-4.2+-green.svg)](https://djangoproject.com/)
[![React](https://img.shields.io/badge/React-18.2+-blue.svg)](https://reactjs.org/)
[![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-4B-red.svg)](https://www.raspberrypi.org/)

> A complete precision irrigation IoT system using artificial intelligence for automated, intelligent watering based on real-time sensor data, weather forecasts, and machine learning algorithms.

## 📋 Table of Contents

- [🎯 Features](#-features)
- [🏗️ System Architecture](#️-system-architecture)
- [� Hardware Setup](#-hardware-setup)
- [📊 Project Overview](#-project-overview)
- [🚀 Quick Start](#-quick-start)
- [📱 Web Dashboard](#-web-dashboard)
- [🔧 Configuration](#-configuration)
- [🐳 Docker Deployment](#-docker-deployment)
- [📊 API Documentation](#-api-documentation)
- [🔒 Security](#-security)
- [📈 Performance & Monitoring](#-performance--monitoring)
- [🧪 Testing](#-testing)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

## 🎯 Features

### 🤖 AI-Powered Intelligence
- **Machine Learning Decisions** - Advanced algorithms analyze sensor patterns
- **Weather Integration** - OpenWeatherMap API for predictive irrigation
- **Adaptive Learning** - System learns from irrigation outcomes
- **Predictive Analytics** - Forecast irrigation needs based on historical data

### 🔧 IoT Hardware Integration
- **DHT22 Sensor** - High-precision temperature and humidity monitoring
- **Soil Moisture Detection** - Analog sensors with MCP3008 ADC conversion
- **Automated Pump Control** - Relay-based irrigation system with safety features
- **Edge Computing** - Local decision making on Raspberry Pi

### � Real-Time Monitoring
- **Live Dashboard** - React-based web interface with real-time updates
- **Historical Analytics** - Chart.js visualizations of sensor trends
- **System Health Monitoring** - Component status and connectivity tracking
- **Mobile Responsive** - Access from any device, anywhere

### ⚡ Automation & Control
- **Smart Irrigation Scheduling** - Multi-factor decision algorithms
- **Manual Override** - Complete manual control when needed
- **Safety Systems** - Maximum duration limits and emergency stops
- **Event Logging** - Comprehensive audit trail of all activities

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           🌱 SMART IRRIGATION ECOSYSTEM                         │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌───────────────────┐    ┌───────────────────┐    ┌───────────────────────┐    │
│  │   🔧 HARDWARE     │    │  🧠 AI PROCESSING │    │  🖥️ USER INTERFACE    │    │
│  │   LAYER           │    │  LAYER            │    │  LAYER                │    │
│  │                   │    │                   │    │                       │    │
│  │ • DHT22 Sensors   │◄──►│ • Django REST API │◄──►│ • React Dashboard     │    │
│  │ • Soil Moisture   │    │ • ML Algorithms   │    │ • Real-time Charts    │    │
│  │ • MCP3008 ADC     │    │ • Weather AI      │    │ • Mobile Controls     │    │
│  │ • Relay Control   │    │ • Decision Engine │    │ • Status Monitoring   │    │
│  │ • Water Pumps     │    │ • SQLite Database │    │ • Alert System       │    │
│  └───────────────────┘    └───────────────────┘    └───────────────────────┘    │
│           │                         │                         │                 │
│           │                         │                         │                 │
│           ▼                         ▼                         ▼                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐│
│  │                          ⚡ AUTOMATION ENGINE                                ││
│  │                                                                             ││
│  │    🚿 Smart Irrigation  •  📱 Remote Control  •  📊 Analytics  •  🔔 Alerts ││
│  └─────────────────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Data Flow Architecture
```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   🌡️ Sensors    │────▶│  🤖 AI Engine   │────▶│  💧 Irrigation   │
│                 │     │                 │     │                 │
│ • Temperature   │     │ • Data Analysis │     │ • Pump Control  │
│ • Humidity      │     │ • ML Predictions│     │ • Valve Control │
│ • Soil Moisture │     │ • Weather Data  │     │ • Safety Checks │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                        │                        │
         ▼                        ▼                        ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  📊 Database    │     │  🌐 Web API     │     │  📱 Dashboard   │
│                 │     │                 │     │                 │
│ • Historical    │     │ • RESTful API   │     │ • Real-time     │
│ • Analytics     │     │ • Authentication│     │ • Controls      │
│ • Predictions   │     │ • Rate Limiting │     │ • Visualizations│
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

## � Hardware Setup

### Required Components

| Component | Model | Purpose | Quantity |
|-----------|-------|---------|----------|
| **Microcontroller** | Raspberry Pi 4B (4GB+) | Main processing unit | 1 |
| **Temperature/Humidity** | DHT22 (AM2302) | Environmental monitoring | 1 |
| **Soil Moisture Sensor** | Capacitive/Resistive | Soil moisture detection | 1-4 |
| **ADC Converter** | MCP3008 | Analog to digital conversion | 1 |
| **Relay Module** | 5V Single/Multi Channel | Pump control | 1 |
| **Water Pump** | 12V DC Submersible | Water delivery | 1 |
| **Power Supply** | 5V 3A + 12V 2A | System power | 2 |
| **MicroSD Card** | 32GB Class 10 | OS and data storage | 1 |
| **Jumper Wires** | Male-Female, Male-Male | Connections | 20+ |

### 📋 Pin Configuration Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    🔌 RASPBERRY PI 4B GPIO PINOUT               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│     3.3V  ●1  ●2   5V      ┌─────────────────────────────────┐   │
│    GPIO2  ●3  ●4   5V      │       🌡️ DHT22 SENSOR          │   │
│    GPIO3  ●5  ●6   GND     │                                 │   │
│ 🌡️ GPIO4  ●7  ●8   GPIO14  │  VCC ────────────── Pin 1 (3.3V) │   │
│      GND  ●9  ●10  GPIO15  │  GND ────────────── Pin 6 (GND)  │   │
│    GPIO17 ●11 ●12  GPIO18 🚿│  DATA ───────────── Pin 7 (GPIO4)│   │
│    GPIO27 ●13 ●14  GND     └─────────────────────────────────┘   │
│    GPIO22 ●15 ●16  GPIO23                                        │
│      3.3V ●17 ●18  GPIO24                                        │
│ 📊 GPIO10 ●19 ●20  GND     ┌─────────────────────────────────┐   │
│ 📊 GPIO9  ●21 ●22  GPIO25  │       📊 MCP3008 ADC           │   │
│ 📊 GPIO11 ●23 ●24  GPIO8 📊│                                 │   │
│      GND  ●25 ●26  GPIO7   │  VCC ────────────── Pin 1 (3.3V) │   │
│    GPIO0  ●27 ●28  GPIO1   │  GND ────────────── Pin 6 (GND)  │   │
│    GPIO5  ●29 ●30  GND     │  CLK ────────────── Pin 23(GPIO11)│   │
│    GPIO6  ●31 ●32  GPIO12  │  DOUT ───────────── Pin 21(GPIO9) │   │
│    GPIO13 ●33 ●34  GND     │  DIN ────────────── Pin 19(GPIO10)│   │
│    GPIO19 ●35 ●36  GPIO16  │  CS ─────────────── Pin 24(GPIO8) │   │
│    GPIO26 ●37 ●38  GPIO20  └─────────────────────────────────┘   │
│      GND  ●39 ●40  GPIO21                                        │
│                                                                 │
│         🚿 = Relay Control (GPIO18, Pin 12)                     │
│         🌡️ = DHT22 Sensor (GPIO4, Pin 7)                       │
│         📊 = MCP3008 ADC (SPI Interface)                        │
└─────────────────────────────────────────────────────────────────┘
```

### 🔗 Detailed Wiring Connections

#### DHT22 Temperature/Humidity Sensor
```
DHT22          Raspberry Pi
┌─────┐        ┌──────────┐
│ VCC │────────│ Pin 1    │ 3.3V
│ GND │────────│ Pin 6    │ Ground
│DATA │────────│ Pin 7    │ GPIO4
└─────┘        └──────────┘
```

#### MCP3008 ADC (SPI Interface)
```
MCP3008        Raspberry Pi
┌─────┐        ┌──────────┐
│ VCC │────────│ Pin 1    │ 3.3V
│ GND │────────│ Pin 6    │ Ground
│ CLK │────────│ Pin 23   │ GPIO11 (SCLK)
│DOUT │────────│ Pin 21   │ GPIO9 (MISO)
│ DIN │────────│ Pin 19   │ GPIO10 (MOSI)
│ CS  │────────│ Pin 24   │ GPIO8 (CE0)
└─────┘        └──────────┘
```

#### Soil Moisture Sensor → MCP3008
```
Soil Sensor    MCP3008
┌─────┐        ┌──────────┐
│ VCC │────────│ VCC      │ 3.3V
│ GND │────────│ GND      │ Ground
│ A0  │────────│ CH0      │ Analog Input
└─────┘        └──────────┘
```

#### Relay Module (Pump Control)
```
Relay Module   Raspberry Pi
┌─────┐        ┌──────────┐
│ VCC │────────│ Pin 2    │ 5V
│ GND │────────│ Pin 6    │ Ground
│ IN  │────────│ Pin 12   │ GPIO18
└─────┘        └──────────┘

Water Pump     Relay Module
┌─────┐        ┌──────────┐
│ +12V│────────│ NO       │ Normally Open
│ GND │────────│ COM      │ Common
└─────┘        └──────────┘
```

### ⚠️ Safety Precautions

1. **Power Isolation**: Keep 5V/12V power circuits separate from 3.3V logic
2. **Grounding**: Ensure common ground for all components
3. **Current Limits**: Use appropriate fuses for pump circuits
4. **Water Protection**: Use waterproof enclosures for outdoor sensors
5. **Backup Power**: Consider UPS for critical operations

## 📊 Project Status

✅ **Complete IoT System** - All 46 project files implemented
- ✅ **Hardware Layer** - Real sensor implementations (DHT22, MCP3008, soil moisture)
- ✅ **Processing Layer** - Django API with weather integration and automated decisions
- ✅ **Interface Layer** - React dashboard with Chart.js visualization
- ✅ **Action Layer** - Relay control with safety features and event logging
- ✅ **Deployment Ready** - Docker configs, installation scripts, production settings

## Components

| Layer | Folder | Purpose |
|-------|--------|---------|
| Edge / Hardware | `raspberry-pi` | Reads sensors, controls relay/pump, pushes readings to backend, can decide locally when offline. |
| Backend API | `backend` | Django + DRF API storing readings, computing irrigation recommendations, exposing control endpoints. |
| Frontend | `frontend/web-dashboard` | React dashboard for real‑time monitoring & manual control. |
| Integrations | `integrations` | Weather + (optional) cloud sync adapters. |
| Docs | `docs` | Architecture, roadmap, setup guides. |

## Quick Start (Development)

### Backend
```
cd backend
python -m venv .venv
./.venv/Scripts/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

### Raspberry Pi (Sim Mode)
```
cd raspberry-pi
python -m venv .venv
./.venv/Scripts/Activate.ps1
pip install -r requirements.txt
python src/main.py --simulate
```

### Frontend
```
cd frontend/web-dashboard
npm install
npm start
```

## Environment Variables (Backend)
Copy `.env.example` to `.env` and adjust.

| Key | Description | Default |
|-----|-------------|---------|
| `SECRET_KEY` | Django secret | dev-temp-key |
| `ALLOWED_HOSTS` | Comma list | * |
| `CORS_ALLOWED_ORIGINS` | Frontend origins | http://localhost:3000 |

## Data Flow (High Level)
1. Edge collects sensor + weather data.
2. Edge posts to `/api/readings/`.
3. Backend persists, runs rule engine / ML placeholder.
4. Decision results returned ("IRRIGATE" or "SKIP").
5. Edge toggles relay if instructed (or local override when offline).
6. Frontend polls/WebSocket for updates.

## Next Steps
See `docs/roadmap.md`.
