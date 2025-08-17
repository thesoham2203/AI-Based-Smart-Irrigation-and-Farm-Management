from __future__ import annotations
import time
from typing import Optional

try:
    import spidev
    HW_AVAILABLE = True
except ImportError:
    HW_AVAILABLE = False

# Simulation fallback
import random


class SoilMoistureSensor:
    """Soil moisture sensor using MCP3008 ADC."""
    
    def __init__(self, spi_bus: int = 0, spi_device: int = 0, channel: int = 0):
        self.channel = channel
        self.spi = None
        
        if HW_AVAILABLE:
            try:
                self.spi = spidev.SpiDev()
                self.spi.open(spi_bus, spi_device)
                self.spi.max_speed_hz = 1000000
            except Exception:
                self.spi = None

    def _read_adc(self) -> int:
        """Read raw ADC value from MCP3008."""
        if not self.spi:
            return 0
        
        # MCP3008 command for single-ended read
        command = [1, (8 + self.channel) << 4, 0]
        response = self.spi.xfer2(command)
        
        # Extract 10-bit value
        value = ((response[1] & 3) << 8) + response[2]
        return value

    def read_moisture_percentage(self, simulate: bool = False) -> float:
        """
        Read soil moisture as percentage (0-100).
        Higher percentage = more moisture.
        """
        if simulate or not HW_AVAILABLE or not self.spi:
            # Simulation: realistic varying moisture
            base = random.uniform(25, 65)
            noise = random.uniform(-3, 3)
            return max(0.0, min(100.0, base + noise))
        
        # Real sensor reading
        raw_value = self._read_adc()
        
        # Calibration: convert 10-bit ADC (0-1023) to moisture %
        # These values need calibration for your specific sensor
        dry_value = 1023    # ADC reading in completely dry soil
        wet_value = 300     # ADC reading in saturated soil
        
        # Convert to percentage (inverted because lower ADC = more moisture)
        moisture_percent = ((dry_value - raw_value) / (dry_value - wet_value)) * 100
        return max(0.0, min(100.0, moisture_percent))

    def cleanup(self):
        """Clean up SPI connection."""
        if self.spi:
            self.spi.close()


# Legacy function for backward compatibility
def read_soil_moisture(adc_channel: int = 0, simulate: bool = False) -> float:
    """Legacy function - creates temporary sensor instance."""
    sensor = SoilMoistureSensor(channel=adc_channel)
    try:
        return sensor.read_moisture_percentage(simulate)
    finally:
        sensor.cleanup()
