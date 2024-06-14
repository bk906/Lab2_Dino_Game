from LCDDisplay import LCDDisplay
from GameController import GameController
from Button import Button

# Initialize buttons
buttons = [
    Button(pin=10, name='white'),  # Jump
    Button(pin=11, name='red'),    # Restart
]

# Initialize LCD Display
lcd_display = LCDDisplay(sda_pin=0, scl_pin=1)

# Initialize Game Controller with the LCD display and buttons
game_controller = GameController(lcd_display, buttons, buzzer_pin=16)

# Start the game
game_controller.show_welcome_message()
