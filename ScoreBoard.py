class ScoreBoard:
    def __init__(self):
        self.score = 0

    def increment(self):
        self.score += 1

    def set_score(self, score):
        self.score = score

    def reset(self):
        self.score = 0

    def get_score(self):
        return self.score

    def draw(self, lcd):
        lcd.move_to(0, 0)
        lcd.putstr(f"Score: {self.score:<5}")  # Ensure the score string fits the display width
