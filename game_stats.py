class GameStats:
    """Track status of alien invasion"""
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()

    def reset_stats(self):
        """Initialize stats that can change during game"""
        self.ships_left = self.settings.ship_limit
        self.score = 0