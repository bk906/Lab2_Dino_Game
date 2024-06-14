from CharacterDisplay import CharacterDisplay
from ObstacleDisplay import ObstacleDisplay
from ScoreBoard import ScoreBoard
from HighScore import HighScore
from Buzzer import Buzzer
from Button import Button
import time

class GameController:
    def __init__(self, lcd_display, buttons, buzzer_pin):
        self.lcd_display = lcd_display
        self.character_display = CharacterDisplay(self.lcd_display.lcd)
        self.obstacle_display = ObstacleDisplay(self.lcd_display.lcd)
        self.score_board = ScoreBoard()
        self.buzzer = Buzzer(buzzer_pin)
        self.high_score = HighScore()
        self.is_running = False
        self.game_over = False
        self.restart_requested = False
        self.game_speed = 1.0  # Initial game speed factor

        # Initialize buttons and set handlers
        self.buttons = buttons
        for button in buttons:
            button.setHandler(self)

        self.create_custom_characters()
        self.show_welcome_message()

    def create_custom_characters(self):
        """Creates custom characters for the LCD."""
        self.character_display.create_custom_characters()
        self.obstacle_display.create_custom_characters()

    def show_welcome_message(self):
        """Displays the welcome message at the start of the game."""
        self.lcd_display.clear()
        self.lcd_display.lcd.move_to(0, 0)
        self.lcd_display.lcd.putstr("Welcome to")
        self.lcd_display.lcd.move_to(0, 1)
        self.lcd_display.lcd.putstr("Dino Game")
        time.sleep(3)
        self.lcd_display.clear()
        self.start_game()

    def start_game(self):
        """Starts the game loop."""
        self.is_running = True
        self.game_over = False
        self.restart_requested = False
        self.buzzer.happy_sound()
        self.score_board.reset()  # Reset score at the start of the game
        self.character_display.set_running_frames(self.character_display.slow_running_frames)  # Start with slow frames
        self.game_speed = 1.0  # Reset game speed
        while self.is_running:
            self.lcd_display.clear()
            self.character_display.update()
            self.obstacle_display.update()
            self.character_display.draw()
            self.obstacle_display.draw()
            self.check_collision()
            self.increment_score_for_crossed_obstacles()
            print(f"Current score: {self.score_board.get_score()}")
            time.sleep(0.1 / self.game_speed)  # Adjust the delay to control the game loop speed

            if self.score_board.get_score() > 10:  # Increase speed after a certain score
                self.game_speed = 1.5
                self.character_display.set_running_frames(self.character_display.running_frames)

            if self.game_over:
                self.display_final_score()
                break

        self.ask_play_again()

    def check_collision(self):
        """Checks for collisions between the character and obstacles."""
        character_x, character_y = self.character_display.get_position()
        for obs_x, obs_y, obs_type in self.obstacle_display.get_obstacles():
            if obs_x == character_x and obs_y == character_y:
                self.is_running = False
                self.game_over = True
                self.buzzer.sad_sound()
                self.lcd_display.blink_screen()  # Blink screen to indicate game over
                self.display_game_over()
                time.sleep(3)  # Display "Game Over" for 3 seconds
                self.high_score.update_high_score(self.score_board.get_score())
                return

    def increment_score_for_crossed_obstacles(self):
        """Increments the score for each obstacle that has been crossed."""
        self.score_board.set_score(self.obstacle_display.get_crossed_obstacles())

    def display_game_over(self):
        """Displays 'Game Over' on the LCD."""
        self.lcd_display.clear()
        self.lcd_display.lcd.move_to(0, 0)
        self.lcd_display.lcd.putstr("Game Over")

    def display_final_score(self):
        """Displays the final score when the game is over."""
        final_score = self.score_board.get_score()
        self.high_score.update_high_score(final_score)
        self.lcd_display.clear()
        self.lcd_display.lcd.move_to(0, 0)
        self.lcd_display.lcd.putstr("Game Over")
        time.sleep(2)
        self.lcd_display.clear()
        self.lcd_display.lcd.move_to(0, 0)
        self.lcd_display.lcd.putstr(f"Score: {final_score}")
        self.lcd_display.lcd.move_to(0, 1)
        self.lcd_display.lcd.putstr(f"High Score: {self.high_score.get_high_score()}")
        time.sleep(3)
        self.ask_play_again()

    def ask_play_again(self):
        """Asks the player if they want to play again."""
        self.lcd_display.clear()
        self.lcd_display.lcd.move_to(0, 0)
        self.lcd_display.lcd.putstr("Play Again?")
        self.restart_requested = False
        while not self.restart_requested:
            time.sleep(0.1)

        if self.restart_requested:
            self.restart_game()

    def jump(self):
        """Makes the character jump."""
        print("Jump button pressed")
        self.buzzer.enjoy_sound()
        self.character_display.jump()

    def stop_jump(self):
        """Stops the character's jump."""
        print("Jump button released")
        self.character_display.stop_jump()

    def stop(self):
        """Stops the game."""
        self.is_running = False
        self.buzzer.stop()

    def reset_game(self):
        """Resets the game to the initial state."""
        self.character_display.reset()
        self.obstacle_display.reset()
        self.score_board.reset()

    def restart_game(self):
        """Restarts the game from the beginning."""
        self.reset_game()
        self.lcd_display.clear()
        self.show_welcome_message()

    def buttonPressed(self, name):
        """Handles button press events."""
        if name == 'white':
            self.jump()
        elif name == 'red':
            self.restart_requested = True

    def buttonReleased(self, name):
        """Handles button release events."""
        if name == 'white':
            self.stop_jump()
