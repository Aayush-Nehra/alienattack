from pathlib import Path

class GameStats:
    """Track status of alien invasion"""
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.high_score = self.read_high_score()
        self.reset_stats()

    def reset_stats(self):
        """Initialize stats that can change during game"""
        self.ships_left = self.settings.ship_limit
        self.score = 0

    def read_high_score(self):
        path = Path('highscore.txt')
        try:
            with open(path, 'r') as file:
                content = file.read().rstrip()
                if content:
                    highscore = int(content)
                    return highscore
                else:
                    raise ValueError("The file does not contain valid data")
        except FileNotFoundError:
            print(f"File not found. Creating file with default value: {self.settings.default_high_score}")
            with open(path, 'w') as file:
                file.write(str(self.settings.default_high_score))
            return self.settings.default_high_score
        except ValueError as e:
            print(f"Error: the file does not contain a valid integer. {e}")
            return self.settings.default_high_score
    
    def save_high_score(self):
        path = Path('highscore.txt')
        path.write_text(str(self.high_score))