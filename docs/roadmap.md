# Roadmap

## Phase 0 – Scaffold (DONE)
- Repo structure, basic Django API, React dashboard, edge agent simulation.

## Phase 1 – Core Functionality
- Configure real sensor drivers (ADC, DHT22) on Raspberry Pi.
- Persist irrigation events from edge (start/stop hooks).
- Add authentication (token) for edge posting.
- Basic charts (last 24h moisture, temperature, humidity) with mini graph library.

## Phase 2 – Weather & Forecast Integration
- Add weather adapter (OpenWeatherMap) to backend.
- Store forecast + actual weather.
- Adjust decision rule using forecasted rainfall probability & ET.

## Phase 3 – Configuration & Multi-Field Support
- CRUD API for fields, crops, thresholds.
- UI management page.
- Edge pulls dynamic config periodically.

## Phase 4 – Advanced Automation
- ET-based irrigation scheduling.
- Optional ML predictive model.
- Anomaly detection (sensor drift, stuck values).

## Phase 5 – Cloud & Remote Access
- Optional Postgres + timeseries DB (TimescaleDB).
- MQTT integration for multi-edge scaling.
- User auth, roles, audit logs.

## Phase 6 – UX Enhancements
- Progressive Web App offline caching.
- Role-based dashboards (farmer, agronomist).
- Alerting (SMS/email) for extremes.

## Phase 7 – Voice Assistant
- Expose secure webhook endpoints.
- Alexa / Google Assistant intents (status, start/stop irrigation, moisture report).
