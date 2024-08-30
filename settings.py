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
        self.bullets_allowed = 10

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

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize the settings that can change throught the game"""
        self.ship_speed = 5
        self.bullet_speed = 5
        self.alien_speed = 1.0

        # fleet_direction of 1 represents right and -1 represents left
        self.fleet_direction = 1

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.alien_speed