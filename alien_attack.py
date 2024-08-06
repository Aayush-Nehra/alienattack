import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from ship import Ship,ShooterShip
from bullet import Bullet
from alien import Alien
from button import Button


class AlienAttack:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources"""
        pygame.init()

        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((
            self.settings.screen_width,
            self.settings.screen_height
        ))

        # For fulscreen mode
        # self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        #Create an instance to store game stats
        self.stats = GameStats(self)

        self.ship = ShooterShip(self)
        self.bullets = pygame.sprite.Group()
        
        #Working with Alien
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        #Start the game in an inactive state
        self.game_active = False

        #Make the play button
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            #Events
            self._check_events()
            if self.game_active:
                #Update positons
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            #Render
            self._update_screen()
            self.clock.tick(60)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            # Move the ship to right
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p:
            self._start_game()

    def _start_game(self):
        if self.game_active == False:
            self.stats.reset_stats()
            self.game_active = True

            # get rid of remaining bullets:
            self.bullets.empty()
            self.aliens.empty()

            # Creat new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()
            pygame.mouse.set_visible(False)

    def _check_play_button(self, mouse_pos):
        """Start new game when player clicks play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked:
            self._start_game()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_events(self):
        """Responds to key presses and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in a row"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any alien has reached an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change fleet's direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed  
        self.settings.fleet_direction *= -1

    def _create_fleet(self):
        """Create a fleet of aliens"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        
        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 5 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            
            current_x = alien_width
            current_y += 2 * alien_height

    def _update_aliens(self):
        """Update the positions of all aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        #Look for aliens reaching bottom of the screen
        self._check_aliens_bottom()

    def _update_screen(self):
        """Updates images on the screen, and flip to the new screen"""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
             bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        self.draw_ships_remaining()

        #Draw the play button if game is inactive
        if not self.game_active:
            self.play_button.draw_button()
        pygame.display.flip()

    def _fire_bullet(self):
        """Create a new bullet and add it to bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    
    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        self.bullets.update()
        for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)
        self._check_bullet_alien_collisons()
        
    def _check_bullet_alien_collisons(self):
        """Destroy bullet and alien on collision"""
        collisons = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True) 
        if not self.aliens:
            #Destory existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()

    def _ship_hit(self):
        """Respond to ship being hit by a alien"""
        print("Ship Hit!")
        if self.stats.ships_left > 0:
            # Decrement ships left
            self.stats.ships_left -= 1

            # Get rid of any bullets or aliens
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center ship
            self._create_fleet()
            self.ship.center_ship()

            #Pause
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break

    def draw_ships_remaining(self):
        ship = Ship(self)
        ship.image = pygame.transform.scale(ship.image, self.settings.remaining_ship_size)
        ship.rect.y = self.settings.screen_height - self.settings.remaining_ship_height
        ship.rect.x = 0
        for i in range(0,self.stats.ships_left):
            ship.blitme()
            ship.rect.x += self.settings.remaining_ship_width


if __name__ == '__main__':
    #Make a game instance, and run the game
    ai = AlienAttack()
    ai.run_game()
            