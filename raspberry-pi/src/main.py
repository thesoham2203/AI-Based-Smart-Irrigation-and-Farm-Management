#!/usr/bin/env python3
"""
IoT Edge Agent for Precision Irrigation System
Collects sensor data, makes irrigation decisions, communicates with backend API.
"""

import argparse
import json
import os
import time
import signal
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional
import requests
import yaml

from logger import configure_logger
from sensors.soil_moisture import SoilMoistureSensor
from sensors.dht22 import DHT22Sensor
from controllers.relay_control import RelayController

logger = configure_logger()


class IrrigationAgent:
    """Main IoT agent for irrigation control."""
    
    def __init__(self, config_path: str):
        self.config = self.load_config(config_path)
        self.running = True
        
        # Initialize hardware
        self.soil_sensor = SoilMoistureSensor(
            channel=self.config.get("sensor", {}).get("soil_moisture_adc_channel", 0)
        )
        self.dht_sensor = DHT22Sensor(
            pin=self.config.get("sensor", {}).get("dht22_pin", 4)
        )
        self.relay = RelayController(
            pin=self.config.get("relay_gpio_pin", 18)
        )
        
        # State tracking
        self.dry_streak = 0
        self.last_irrigation = None
        self.irrigation_count_today = 0
        self.last_backend_contact = datetime.now()
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def load_config(self, path: str) -> Dict[str, Any]:
        """Load YAML configuration file."""
        try:
            with open(path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.error(f"Config file not found: {path}")
            sys.exit(1)
        except yaml.YAMLError as e:
            logger.error(f"Invalid YAML config: {e}")
            sys.exit(1)

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully."""
        logger.info(f"Received signal {signum}, shutting down...")
        self.running = False

    def read_sensors(self, simulate: bool = False) -> Dict[str, float]:
        """Read all sensor values."""
        moisture = self.soil_sensor.read_moisture_percentage(simulate)
        temp_c, humidity = self.dht_sensor.read_temperature_humidity(simulate)
        
        return {
            "moisture": moisture,
            "temperature_c": temp_c,
            "humidity": humidity,
            "timestamp": datetime.now().isoformat()
        }

    def should_irrigate_offline(self, moisture: float) -> bool:
        """Local irrigation decision when backend unavailable."""
        threshold = self.config.get("moisture_threshold", 35)
        consecutive_needed = self.config.get("offline_mode", {}).get("consecutive_dry_readings", 2)
        
        if moisture < threshold:
            self.dry_streak += 1
        else:
            self.dry_streak = 0
        
        # Safety checks
        if self.irrigation_count_today >= self.config.get("safety", {}).get("max_irrigation_per_day", 4):
            logger.warning("Daily irrigation limit reached")
            return False
        
        if self.last_irrigation:
            min_interval = self.config.get("safety", {}).get("min_time_between_cycles", 3600)
            if (datetime.now() - self.last_irrigation).seconds < min_interval:
                logger.info("Too soon since last irrigation")
                return False
        
        return self.dry_streak >= consecutive_needed

    def post_to_backend(self, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Send sensor data to backend API."""
        base_url = self.config.get("backend_base_url")
        if not base_url:
            return None
        
        try:
            timeout = self.config.get("api_timeout_seconds", 10)
            response = requests.post(
                f"{base_url}/api/readings/",
                json=payload,
                timeout=timeout,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 201:
                self.last_backend_contact = datetime.now()
                return response.json()
            else:
                logger.warning(f"Backend error: {response.status_code}")
                
        except requests.RequestException as e:
            logger.warning(f"Backend communication failed: {e}")
        
        return None

    def execute_irrigation(self, duration: int, reason: str):
        """Execute irrigation cycle."""
        logger.info(f"Starting irrigation: {reason} (duration: {duration}s)")
        
        if self.relay.on():
            self.last_irrigation = datetime.now()
            self.irrigation_count_today += 1
            
            # Wait for irrigation duration
            time.sleep(duration)
            
            if self.relay.off():
                logger.info("Irrigation completed successfully")
            else:
                logger.error("Failed to stop irrigation - manual intervention needed!")
        else:
            logger.error("Failed to start irrigation")

    def reset_daily_counters(self):
        """Reset daily counters at midnight."""
        now = datetime.now()
        if self.last_irrigation and now.date() > self.last_irrigation.date():
            self.irrigation_count_today = 0
            logger.info("Daily irrigation counter reset")

    def run_cycle(self, simulate: bool = False):
        """Execute one sensor reading and decision cycle."""
        try:
            # Reset daily counters if needed
            self.reset_daily_counters()
            
            # Read sensors
            sensor_data = self.read_sensors(simulate)
            
            # Prepare payload for backend
            payload = {
                "field_id": self.config.get("field_id"),
                "crop_stage": self.config.get("crop_stage"),
                "location": self.config.get("location"),
                **sensor_data
            }
            
            # Try to get decision from backend
            backend_response = self.post_to_backend(payload)
            irrigation_decision = None
            
            if backend_response:
                irrigation_decision = backend_response.get("action")
                logger.info(f"Backend decision: {irrigation_decision}")
            else:
                # Offline decision making
                offline_hours = (datetime.now() - self.last_backend_contact).total_seconds() / 3600
                max_offline = self.config.get("offline_mode", {}).get("max_offline_hours", 12)
                
                if offline_hours > max_offline:
                    logger.warning(f"Backend offline for {offline_hours:.1f}h - conservative mode")
                    # Be more conservative when offline for long time
                    if self.should_irrigate_offline(sensor_data["moisture"] - 5):  # Lower threshold
                        irrigation_decision = "IRRIGATE"
                else:
                    if self.should_irrigate_offline(sensor_data["moisture"]):
                        irrigation_decision = "IRRIGATE"
            
            # Execute irrigation if needed
            if irrigation_decision == "IRRIGATE":
                duration = self.config.get("min_irrigation_run_seconds", 120)
                self.execute_irrigation(duration, "Automated decision")
                self.dry_streak = 0  # Reset dry streak after irrigation
            
            # Log current status
            logger.info(
                f"Sensors: {sensor_data['moisture']:.1f}% moisture, "
                f"{sensor_data['temperature_c']:.1f}°C, {sensor_data['humidity']:.1f}% RH | "
                f"Relay: {'ON' if self.relay.state() else 'OFF'} | "
                f"Dry streak: {self.dry_streak}"
            )
            
        except Exception as e:
            logger.error(f"Cycle error: {e}")

    def run(self, simulate: bool = False):
        """Main agent loop."""
        interval = self.config.get("sampling_interval_seconds", 300)
        logger.info(f"Starting irrigation agent (interval: {interval}s, simulate: {simulate})")
        
        try:
            while self.running:
                start_time = time.time()
                
                self.run_cycle(simulate)
                
                # Sleep for remaining interval time
                elapsed = time.time() - start_time
                sleep_time = max(0, interval - elapsed)
                if sleep_time > 0:
                    time.sleep(sleep_time)
                    
        except KeyboardInterrupt:
            logger.info("Interrupted by user")
        finally:
            self.cleanup()

    def cleanup(self):
        """Clean up resources."""
        logger.info("Cleaning up resources...")
        self.relay.off()
        self.relay.cleanup()
        self.soil_sensor.cleanup()
        self.dht_sensor.cleanup()


def main():
    parser = argparse.ArgumentParser(description="IoT Irrigation Edge Agent")
    parser.add_argument(
        "--config", 
        default="config/config.yaml",
        help="Configuration file path"
    )
    parser.add_argument(
        "--simulate", 
        action="store_true",
        help="Run in simulation mode (no real hardware)"
    )
    args = parser.parse_args()
    
    # Use example config if main config doesn't exist
    if not os.path.exists(args.config) and os.path.exists("config/config.example.yaml"):
        logger.warning(f"Config file {args.config} not found, using example config")
        args.config = "config/config.example.yaml"
    
    agent = IrrigationAgent(args.config)
    agent.run(simulate=args.simulate)


if __name__ == "__main__":
    main()
