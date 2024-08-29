import pygame

class Ship:
    """A class to manage ship"""

    def __init__(self, ai_game):
        """Initialise the ship and set its starting position"""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship image and get its rect
        self.image = pygame.transform.scale(
            pygame.image.load('images/player.png'), (60,45))
        self.rect = self.image.get_rect()

    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)

class ShooterShip(Ship):
    """A class to manage shooter ship"""
    def __init__(self, ai_game):
        super().__init__(ai_game)

        #Movement flag; start with a ship that's not moving
        self.moving_right = False
        self.moving_left = False

        # Start each new ship at the bottom center of the screen half ship length up.
        self.rect.midbottom = self.screen_rect.midbottom
        self.rect.y -= self.rect.height/2

        # Store a float for sips exact horizontal position
        self.x = float(self.rect.x)

    def update(self):
        """Update the ship's position based on the movement flag."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # update rect obhect from self.x
        self.rect.x = self.x

    def center_ship(self):
        """Center the ship on the screen"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.rect.y -= self.rect.height/2
        self.x = float(self.rect.x)



 
