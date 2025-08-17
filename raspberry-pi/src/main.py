import argparse
import json
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
import requests
import yaml

from logger import configure_logger
from sensors.soil_moisture import read_soil_moisture
from sensors.dht22 import read_dht22
from controllers.relay_control import RelayController

logger = configure_logger()


def load_config(path: str | Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def decide_irrigation(moisture: float, cfg: Dict[str, Any], dry_streak: int) -> bool:
    threshold = cfg.get("moisture_threshold", 35)
    consecutive_needed = cfg.get("offline_mode", {}).get("consecutive_dry_readings", 3)
    return moisture < threshold and dry_streak >= consecutive_needed


def post_reading(cfg: Dict[str, Any], payload: Dict[str, Any]) -> dict | None:
    base = cfg.get("backend_base_url")
    if not base:
        return None
    try:
        r = requests.post(f"{base}/api/readings/", json=payload, timeout=5)
        if r.status_code == 201:
            return r.json()
        logger.warning("Backend response %s", r.status_code)
    except Exception as e:  # pragma: no cover
        logger.warning("Post failed: %s", e)
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/config.example.yaml")
    parser.add_argument("--simulate", action="store_true")
    args = parser.parse_args()

    cfg = load_config(args.config)
    relay = RelayController(cfg.get("relay_gpio_pin", 18))
    dry_streak = 0
    try:
        while True:
            moisture = read_soil_moisture(cfg.get("sensor", {}).get("soil_moisture_adc_channel", 0), simulate=args.simulate)
            temp_c, humidity = read_dht22(cfg.get("sensor", {}).get("dht22_pin", 4), simulate=args.simulate)
            timestamp = datetime.utcnow().isoformat()
            payload = {
                "field_id": cfg.get("field_id"),
                "crop_stage": cfg.get("crop_stage"),
                "moisture": moisture,
                "temperature_c": temp_c,
                "humidity": humidity,
                "timestamp": timestamp,
            }
            backend_decision = post_reading(cfg, payload) or {}
            decision = backend_decision.get("action")
            if decision == "IRRIGATE":
                logger.info("Backend instructed irrigation.")
                relay.on()
            elif decision == "SKIP":
                relay.off()
            else:
                # Offline / rule based fallback
                if moisture < cfg.get("moisture_threshold", 35):
                    dry_streak += 1
                else:
                    dry_streak = 0
                if decide_irrigation(moisture, cfg, dry_streak):
                    logger.info("Offline rule triggered irrigation (moisture=%.2f).", moisture)
                    relay.on()
                else:
                    relay.off()
            logger.info("Reading: %s | Relay=%s", json.dumps(payload), relay.state())
            time.sleep(cfg.get("sampling_interval_seconds", 60))
    except KeyboardInterrupt:  # pragma: no cover
        logger.info("Stopping edge agent")
    finally:
        relay.off()
        relay.cleanup()


if __name__ == "__main__":
    main()
