import pygame.font

class Button:
    """A class to build buttons for the game"""
    def __init__(self, aa_game, msg, position) -> None:
        #initialize the button attributes
        self.screen = aa_game.screen
        self.screen_rect = self.screen.get_rect()

        self.width, self.height = 200, 50
        self.button_color = (0, 135, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        #Build button rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = position

        #The button message needs to be prepared only once
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn message into rendered image and center text on button"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Draw blank button and then draw message"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)