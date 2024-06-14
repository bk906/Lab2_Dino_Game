import random

class ObstacleDisplay:
    def __init__(self, lcd):
        self.lcd = lcd
        self.obstacles = []
        self.obstacle_gap = 5  # Minimum gap between obstacles
        self.tree_frame = [
            0b00000,
            0b00100,
            0b01110,
            0b11111,
            0b11111,
            0b00100,
            0b00100,
            0b00000
        ]
        self.bird_frames = [
            [
                0b00100,  # Wings up
                0b10101,  # Wings up
                0b11111,  # Body
                0b01110,  # Body
                0b00100,  # Tail
                0b00000,  # Empty
                0b00000,  # Empty
                0b00000   # Empty
            ],
            [
                0b00000,  # Empty
                0b00100,  # Wings down
                0b11111,  # Body
                0b10101,  # Body
                0b01110,  # Tail
                0b00100,  # Tail
                0b00000,  # Empty
                0b00000   # Empty
            ]
        ]
        self.current_frame = 0
        self.frame_count = 0
        self.max_frame_count = 5  # Change frame every 5 updates
        self.crossed_obstacles = 0
        self.speed = 0.5  # Initial speed
        self.speed_increment = 0.01  # Speed increment

    def create_custom_characters(self):
        self.lcd.custom_char(1, bytearray(self.tree_frame))
        self.lcd.custom_char(2, bytearray(self.bird_frames[self.current_frame]))

    def update(self):
        """Updates the positions of the obstacles and adds new ones if necessary."""
        new_obstacles = []
        for (x, y, obs_type) in self.obstacles:
            if x > 0:
                new_obstacles.append((x - 1, y, obs_type))
            else:
                self.crossed_obstacles += 1  # Increment score when an obstacle is crossed
        self.obstacles = new_obstacles
        if self.can_add_new_obstacle():
            self.add_random_obstacle()
        
        self.frame_count += 1
        if self.frame_count >= self.max_frame_count:
            self.frame_count = 0
            self.current_frame = (self.current_frame + 1) % len(self.bird_frames)
            self.create_custom_characters()

        self.draw()
        self.speed += self.speed_increment  # Increase speed

    def can_add_new_obstacle(self):
        """Checks if a new obstacle can be added based on the minimum gap."""
        if not self.obstacles:
            return True
        last_obstacle_x = self.obstacles[-1][0]
        return last_obstacle_x < (16 - self.obstacle_gap)

    def add_random_obstacle(self):
        """Adds a new random obstacle to the display."""
        obs_type = random.choice([1, 2])  # Tree or Bird
        y = 1 if obs_type == 1 else random.choice([0, 1])  # Tree on bottom, bird on top
        self.obstacles.append((15, y, obs_type))

    def draw(self):
        """Draws the obstacles on the LCD."""
        for (x, y, obs_type) in self.obstacles:
            self.lcd.move_to(x, y)
            self.lcd.putchar(chr(obs_type))

    def reset(self):
        """Resets the obstacles to the initial state."""
        self.obstacles = []
        self.crossed_obstacles = 0
        self.speed = 0.5  # Reset speed

    def get_obstacles(self):
        """Returns the list of current obstacles."""
        return self.obstacles

    def get_crossed_obstacles(self):
        """Returns the number of crossed obstacles."""
        return self.crossed_obstacles