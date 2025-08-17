import time
import atexit
from typing import Optional

try:
    import RPi.GPIO as GPIO
    HW_AVAILABLE = True
except ImportError:
    HW_AVAILABLE = False


class RelayController:
    """Controls irrigation pump via relay module."""
    
    def __init__(self, pin: int, active_low: bool = True):
        self.pin = pin
        self.active_low = active_low
        self._state = False
        self._initialized = False
        
        if HW_AVAILABLE:
            try:
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(self.pin, GPIO.OUT)
                self.off()  # Start with relay off
                self._initialized = True
                # Register cleanup on exit
                atexit.register(self.cleanup)
            except Exception as e:
                print(f"GPIO initialization failed: {e}")

    def on(self) -> bool:
        """Turn on the relay (start irrigation)."""
        if HW_AVAILABLE and self._initialized:
            try:
                GPIO.output(self.pin, GPIO.LOW if self.active_low else GPIO.HIGH)
                self._state = True
                return True
            except Exception as e:
                print(f"Failed to turn relay on: {e}")
                return False
        else:
            # Simulation mode
            self._state = True
            print("SIMULATION: Relay turned ON (irrigation started)")
            return True

    def off(self) -> bool:
        """Turn off the relay (stop irrigation)."""
        if HW_AVAILABLE and self._initialized:
            try:
                GPIO.output(self.pin, GPIO.HIGH if self.active_low else GPIO.LOW)
                self._state = False
                return True
            except Exception as e:
                print(f"Failed to turn relay off: {e}")
                return False
        else:
            # Simulation mode
            self._state = False
            print("SIMULATION: Relay turned OFF (irrigation stopped)")
            return True

    def state(self) -> bool:
        """Get current relay state."""
        return self._state

    def toggle(self) -> bool:
        """Toggle relay state."""
        if self._state:
            return self.off()
        else:
            return self.on()

    def pulse(self, duration: float) -> bool:
        """Turn on relay for specified duration (seconds)."""
        if self.on():
            time.sleep(duration)
            return self.off()
        return False

    def cleanup(self):
        """Clean up GPIO resources."""
        if HW_AVAILABLE and self._initialized:
            try:
                self.off()  # Ensure relay is off
                GPIO.cleanup(self.pin)
                self._initialized = False
            except Exception as e:
                print(f"GPIO cleanup failed: {e}")
