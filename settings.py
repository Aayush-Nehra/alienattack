class Settings:
    """A class to store all settings of alien invasion"""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen Settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Bullet Settings
        self.bullet_speed = 2
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255,0,0)
        self.bullets_allowed = 10

        #Alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 50

        # fleet_direction of 1 represents right and -1 represents left
        self.fleet_direction = 1
        
        #Ship Settings
        self.ship_speed = 1.5
        self.ship_limit = 3

        #Remaining ship
        self.remaining_ship_height = 30
        self.remaining_ship_width = 40
        self.remaining_ship_size = (self.remaining_ship_width, self.remaining_ship_height)
