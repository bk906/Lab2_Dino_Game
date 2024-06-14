class CharacterDisplay:
    def __init__(self, lcd):
        self.lcd = lcd
        self.x = 0
        self.y = 1  # Bottom line of the display
        self.is_jumping = False
        self.slow_running_frames = [
            [
                0b00100,  # Head
                0b01110,  # Body
                0b00100,  # Body
                0b01110,  # Arms
                0b10101,  # Arms
                0b00100,  # Body
                0b01010,  # Legs
                0b10001   # Legs
            ],
            [
                0b00100,  # Head
                0b01110,  # Body
                0b00100,  # Body
                0b01110,  # Arms
                0b10101,  # Arms
                0b00100,  # Body
                0b10010,  # Legs
                0b01001   # Legs
            ]
        ]
        self.running_frames = self.slow_running_frames
        self.jumping_frame = [
            0b00100,  # Head
            0b01110,  # Body
            0b00100,  # Body
            0b01110,  # Arms
            0b10101,  # Arms
            0b01010,  # Legs
            0b01010,  # Legs
            0b00000   # Empty
        ]
        self.current_frame = 0
        self.frame_count = 0
        self.max_frame_count = 5  # Change frame every 5 updates
        self.create_custom_characters()

    def create_custom_characters(self):
        self.lcd.custom_char(0, bytearray(self.running_frames[self.current_frame]))

    def jump(self):
        """Initiates the jump."""
        self.is_jumping = True
        self.y = 0  # Move to the top line
        self.lcd.custom_char(0, bytearray(self.jumping_frame))

    def stop_jump(self):
        """Stops the jump and returns to the bottom line."""
        self.is_jumping = False
        self.y = 1  # Return to the bottom line
        self.lcd.custom_char(0, bytearray(self.running_frames[self.current_frame]))

    def update(self):
        """Updates the character's position and animation frame."""
        self.frame_count += 1
        if self.frame_count >= self.max_frame_count:
            self.frame_count = 0
            self.current_frame = (self.current_frame + 1) % len(self.running_frames)
            if not self.is_jumping:
                self.lcd.custom_char(0, bytearray(self.running_frames[self.current_frame]))

        self.draw()

    def draw(self):
        """Draws the character at the current position on the LCD."""
        self.lcd.move_to(self.x, self.y)
        self.lcd.putchar(chr(0))  # Custom character for the human

    def reset(self):
        """Resets the character's position and jump state."""
        self.x = 0
        self.y = 1  # Ensure the character is at the bottom of the display
        self.is_jumping = False
        self.frame_count = 0
        self.current_frame = 0
        self.lcd.custom_char(0, bytearray(self.running_frames[self.current_frame]))

    def get_position(self):
        """Returns the current position of the character."""
        return self.x, self.y

    def set_running_frames(self, frames):
        """Sets the running frames to control animation speed."""
        self.running_frames = frames
        self.create_custom_characters()
