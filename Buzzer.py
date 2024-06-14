from machine import Pin, PWM
import time

class Buzzer:
    def __init__(self, pin):
        self.buzzer = PWM(Pin(pin))
        self.buzzer.duty_u16(0)  # Ensure the buzzer is off initially

    def play_tone(self, frequency, duration):
        """Plays a tone at a specific frequency for a given duration."""
        self.buzzer.freq(frequency)
        self.buzzer.duty_u16(1000)  # Set duty cycle to make the sound audible
        time.sleep(duration)
        self.buzzer.duty_u16(0)  # Turn off the buzzer after the duration

    def happy_sound(self):
        """Plays a happy sound."""
        self.play_tone(1000, 0.5)
        time.sleep(0.1)
        self.play_tone(1200, 0.5)
        time.sleep(0.1)
        self.play_tone(1400, 0.5)

    def sad_sound(self):
        """Plays a sad sound."""
        self.play_tone(200, 0.5)
        time.sleep(0.1)
        self.play_tone(150, 0.5)
        time.sleep(0.1)
        self.play_tone(100, 0.5)

    def enjoy_sound(self):
        """Plays an enjoyment sound."""
        self.play_tone(1500, 0.2)
        time.sleep(0.1)
        self.play_tone(1700, 0.2)
        time.sleep(0.1)
        self.play_tone(2000, 0.2)

    def stop(self):
        """Stops any sound from the buzzer."""
        self.buzzer.duty_u16(0)
