class Settings:
    """A class to store all settings of alien invasion"""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen Settings
        self.screen_width = 900
        self.screen_height = 900
        self.bg_color = (230, 230, 230)

        # Bullet Settings
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = (255,0,0)
        self.bullets_allowed = 4

        #Alien settings
        self.fleet_drop_speed = 10
        
        #Ship Settings
        self.ship_limit = 2

        #Remaining ship
        self.remaining_ship_height = 30
        self.remaining_ship_width = 40
        self.remaining_ship_size = (self.remaining_ship_width, self.remaining_ship_height)

        # How quickly the game should speed up
        self.speedup_scale = 1.1
        # How quickly the alien point values increase
        self.score_scale = 1.5

    def initialize_dynamic_settings(self, game_mode):
        """Initialize the settings that can change throught the game"""
        match game_mode:
            case "Easy":
                self.ship_speed = 4.0
                self.bullet_speed = 4.0
                self.alien_speed = 1.0
            case "Medium":
                self.ship_speed = 5.0
                self.bullet_speed = 4.0
                self.alien_speed = 1.1
            case "Hard":
                self.ship_speed = 6.0
                self.bullet_speed = 4.0
                self.alien_speed = 1.15

        # Scoring settings
        self.alien_points = 50
        # fleet_direction of 1 represents right and -1 represents left
        self.fleet_direction = 1

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.alien_speed
        
        self.alien_points = int(self.alien_points * self.score_scale)