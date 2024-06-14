import ujson as json

class HighScore:
    def __init__(self, filename="high_score.json"):
        self.filename = filename
        self.high_score = self.load_high_score()

    def load_high_score(self):
        """Loads the high score from a file."""
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
                return data.get('high_score', 0)
        except (OSError, ValueError):
            return 0

    def save_high_score(self):
        """Saves the high score to a file."""
        try:
            with open(self.filename, 'w') as file:
                json.dump({'high_score': self.high_score}, file)
        except OSError:
            pass

    def update_high_score(self, score):
        """Updates the high score if the current score is higher and saves it."""
        if score > self.high_score:
            self.high_score = score
            self.save_high_score()

    def reset(self):
        """Resets the high score (if desired)."""
        self.high_score = 0
        self.save_high_score()

    def get_high_score(self):
        """Returns the current high score."""
        return self.high_score
