import pygame
from pygame.sprite import Sprite
from random import randint

class Alien(Sprite):
    """A class to represent single alien in the fleet"""

    def __init__(self, ai_game) -> None:
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        #Alien Image
        self.alien_type = "alien" + str(randint(1,5))
        self.image = pygame.transform.scale(
            pygame.image.load("images/"+self.alien_type + ".png").convert_alpha(), (50,50)
            )
        self.rect = self.image.get_rect()

        #Initial Postion of alien
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #Store the alien's exact horizontal position
        self.x = float(self.rect.x)

    def check_edges(self):
        """return true if alien is at edge of screen"""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)

    def update(self):
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x


        