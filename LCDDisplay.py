from machine import Pin, I2C
from pico_i2c_lcd import I2cLcd
import time

class LCDDisplay:
    def __init__(self, sda_pin, scl_pin):
        i2c = I2C(0, sda=Pin(sda_pin), scl=Pin(scl_pin), freq=400000)
        self.lcd = I2cLcd(i2c, 0x27, 2, 16)
        self.lcd.backlight_on()  # Ensure the backlight is on for brightness

    def clear(self):
        """Clears the LCD display."""
        self.lcd.clear()

    def blink_screen(self, times=3):
        """Blinks the screen a given number of times."""
        for _ in range(times):
            self.lcd.backlight_off()
            time.sleep(0.2)
            self.lcd.backlight_on()
            time.sleep(0.2)
