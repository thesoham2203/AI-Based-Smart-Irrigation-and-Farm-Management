from __future__ import annotations
import time
import random
from typing import Tuple, Optional

try:
    import adafruit_dht
    import board
    HW_AVAILABLE = True
except ImportError:
    HW_AVAILABLE = False


class DHT22Sensor:
    """Temperature and humidity sensor DHT22/AM2302."""
    
    def __init__(self, pin: int = 4):
        self.pin = pin
        self.sensor = None
        
        if HW_AVAILABLE:
            try:
                # Map pin number to board pin
                pin_map = {
                    4: board.D4,
                    18: board.D18,
                    22: board.D22,
                    27: board.D27
                }
                board_pin = pin_map.get(pin, board.D4)
                self.sensor = adafruit_dht.DHT22(board_pin)
            except Exception:
                self.sensor = None

    def read_temperature_humidity(self, simulate: bool = False, retries: int = 3) -> Tuple[float, float]:
        """
        Read temperature and humidity from DHT22.
        Returns (temperature_c, humidity_percent).
        """
        if simulate or not HW_AVAILABLE or not self.sensor:
            # Realistic simulation with some correlation
            temp = random.uniform(18, 35)
            # Humidity inversely correlated with temperature somewhat
            humidity_base = 85 - (temp - 18) * 1.5
            humidity = max(30, min(90, humidity_base + random.uniform(-10, 10)))
            return round(temp, 1), round(humidity, 1)
        
        # Real sensor reading with retries
        for attempt in range(retries):
            try:
                temperature = self.sensor.temperature
                humidity = self.sensor.humidity
                
                if temperature is not None and humidity is not None:
                    # Validate reasonable ranges
                    if -40 <= temperature <= 80 and 0 <= humidity <= 100:
                        return round(temperature, 1), round(humidity, 1)
                
            except RuntimeError as e:
                # DHT sensors often need multiple attempts
                if attempt < retries - 1:
                    time.sleep(0.5)
                    continue
                else:
                    # Fall back to simulation on repeated failures
                    break
        
        # Fallback to simulation if sensor fails
        return self.read_temperature_humidity(simulate=True)

    def cleanup(self):
        """Clean up sensor resources."""
        if self.sensor:
            self.sensor.exit()


# Legacy function for backward compatibility
def read_dht22(pin: int = 4, simulate: bool = False) -> Tuple[float, float]:
    """Legacy function - creates temporary sensor instance."""
    sensor = DHT22Sensor(pin)
    try:
        return sensor.read_temperature_humidity(simulate)
    finally:
        sensor.cleanup()
