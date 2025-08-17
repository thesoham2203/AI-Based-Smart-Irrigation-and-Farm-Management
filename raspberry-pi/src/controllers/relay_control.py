import time
from typing import Optional

try:
    import RPi.GPIO as GPIO  # type: ignore
    HW_AVAILABLE = True
except Exception:  # pragma: no cover
    HW_AVAILABLE = False


class RelayController:
    def __init__(self, pin: int, active_low: bool = True):
        self.pin = pin
        self.active_low = active_low
        self._state = False
        if HW_AVAILABLE:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.pin, GPIO.OUT)
            self.off()

    def on(self):
        if HW_AVAILABLE:
            GPIO.output(self.pin, GPIO.LOW if self.active_low else GPIO.HIGH)
        self._state = True

    def off(self):
        if HW_AVAILABLE:
            GPIO.output(self.pin, GPIO.HIGH if self.active_low else GPIO.LOW)
        self._state = False

    def state(self) -> bool:
        return self._state

    def cleanup(self):  # pragma: no cover
        if HW_AVAILABLE:
            GPIO.cleanup(self.pin)
