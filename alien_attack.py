import math
import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from ship import Ship,ShooterShip
from bullet import Bullet
from alien import Alien
from button import Button
from game_constants import EASY, MEDIUM, HARD, PLAY
from scoreboard import Scoreboard
from text_renderer import TextRenderer
import sound_effects as se

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

        #Create an instance to store game stats,
        #   and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = ShooterShip(self)
        self.bullets = pygame.sprite.Group()

        #Working with Alien
        self.aliens = pygame.sprite.Group()

        #Start the game in an inactive state
        self.game_active = False

        # Make the play button
        self.is_play_button_clicked = False
        self.play_button = Button(self, PLAY, self.screen.get_rect().center)

        # Make difficulty buttons
        self._create_difficulty_buttons()
        self.select_difficulty_text = TextRenderer(self, "SELECT DIFFICULTY")
        
        # Get backgroud for game
        self.game_background = pygame.image.load("images/bg_space.png").convert_alpha()

    def _create_difficulty_buttons(self):
        """Create easy, medium, and difficult buttons to control game difficulty"""
        # Creating coordinates for buttons
        cen_x, cen_y = self.screen.get_rect().center
        easy_x_pos = (0 + cen_x)/2
        hard_x_pos = (cen_x + self.settings.screen_width)/2

        self.easy_button = Button(self, EASY, (easy_x_pos, cen_y))
        self.medium_button = Button(self, MEDIUM, (cen_x, cen_y))
        self.hard_button = Button(self, HARD, (hard_x_pos, cen_y))

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
            self.stats.save_high_score()
            sys.exit()
        elif event.key == pygame.K_SPACE and self.game_active:
            self._fire_bullet()
        elif event.key == pygame.K_RETURN:
            self.is_play_button_clicked = True
    
    def _start_game(self, game_mode):
        if self.game_active == False:
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.game_active = True
            # get rid of remaining bullets:
            self.bullets.empty()
            self.aliens.empty()
            self.settings.initialize_dynamic_settings(game_mode)
            # Creat new fleet and center the ship
            self._create_fleet(self.stats.level)
            self.ship.center_ship()
            pygame.mouse.set_visible(False)

    def _check_click_events(self, mouse_pos):
        """Start new game when player clicks play"""
        game_difficulty = ""
        if self.play_button.rect.collidepoint(mouse_pos) and self.is_play_button_clicked == False:
            #Draw difficulty levels if play is clicked
            self.is_play_button_clicked = True
        elif self.easy_button.rect.collidepoint(mouse_pos):
            game_difficulty = EASY
        elif self.medium_button.rect.collidepoint(mouse_pos):
            game_difficulty = MEDIUM
        elif self.hard_button.rect.collidepoint(mouse_pos):
            game_difficulty = HARD
        
        if game_difficulty!="":
            self._start_game(game_difficulty)

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_events(self):
        """Responds to key presses and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stats.save_high_score()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_click_events(mouse_pos)

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

    def _create_fleet(self, game_level=1):
        """Create a fleet of aliens for game level"""
        game_level %= 6
        match game_level:
            case 1:
                self.create_level_1_fleet()
            case 2:
                self.create_level_2_fleet()
            case 3:
                self.create_level_3_fleet()
            case 4:
                self.create_level_4_fleet()
            case 5:
                self.create_level_5_fleet()
            case _:
                self.create_level_1_fleet()

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
        self.screen.blit(self.game_background, (0,0))
        for bullet in self.bullets.sprites():
             bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        self.draw_ships_remaining()

        #Draw the score information
        self.sb.show_score()

        #Draw the play button if game is inactive
        if not self.game_active:
            #Reset settings if game is over
            if not self.is_play_button_clicked:
                self.play_button.draw_button()
            else:
                self.select_difficulty_text.render_text()            
                self.medium_button.draw_button()
                self.easy_button.draw_button()
                self.hard_button.draw_button()

        pygame.display.flip()

    def _fire_bullet(self):
        """Create a new bullet and add it to bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            se.bullet_sound.play()

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
        
        if collisons:
            for aliens in collisons.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_highscore()
            se.alien_hit_sound.play()

        if not self.aliens:
            #Destory existing bullets and create new fleet
            self.bullets.empty()
            self.level_up()

    def level_up(self):
        self.stats.level += 1
        self.sb.prep_level()
        self._create_fleet(self.stats.level)
        self.settings.increase_speed()

    def _ship_hit(self):
        """Respond to ship being hit by a alien"""
        if self.stats.ships_left > 0:
            # Decrement ships left
            self.stats.ships_left -= 1

            # Get rid of any bullets or aliens
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center ship
            self._create_fleet(self.stats.level)
            self.ship.center_ship()

            #Pause
            sleep(0.5)
        else:
            self.stats.save_high_score()
            self.game_active = False
            self.is_play_button_clicked = False
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

    def create_level_1_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = 2*alien_width, alien_height
        while current_y < (self.settings.screen_height - 7 * alien_height):
            while current_x < (self.settings.screen_width - 3 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            current_x = 2 * alien_width
            current_y += 2 * alien_height

    def create_level_2_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        current_x, current_y = 2 * alien_width, alien_height
        max_aliens_per_row = int(math.floor(self.settings.screen_width - 4 * alien_width)/(2 * alien_width))
        alien_rows = 8
        for i in range(1,alien_rows):
            for j in range(max_aliens_per_row, i-1, -1):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            current_x = (2 + i) * alien_width
            current_y += 2 * alien_height

    def create_level_3_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        current_x, current_y = alien_width, alien_height
        alien_rows = 8
        for i in range(0, alien_rows):
            for j in range(0, alien_rows-i-1):
                current_x += alien_width

            for j in range(0,(2*i+1)):
                self._create_alien(current_x, current_y)
                current_x += alien_width

            current_x = alien_width
            current_y += 1.5*alien_height

    def create_level_4_fleet(self):
        #Copied from level 2
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        current_x, current_y = 2 * alien_width, alien_height
        alien_rows = 7
        for i in range(1,alien_rows):
            for j in range(alien_rows-1, i-1, -1):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            current_x = (2 + i) * alien_width
            current_y += alien_height

        current_x = current_x-alien_width
        for i in range(1, alien_rows):
            for j in range(0,i):
                self._create_alien(current_x, current_y)
                current_x += 2*alien_width
            current_x = (alien_rows-i) * alien_width
            current_y += alien_height

    def create_level_5_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        current_y = alien_height
        alien_rows = 8
        smaller_fleet_rows = 3

        #group 1
        for i in range(1, alien_rows):
            current_x = (alien_rows-i) * alien_width
            for j in range(0,i):
                self._create_alien(current_x, current_y)
                current_x += 2*alien_width
            current_y += alien_height

        # group 2
        x2 = current_x - 2 * alien_width
        y2 = alien_height

        for i in range(0,smaller_fleet_rows):
            for j in range(smaller_fleet_rows, i, -1):
                self._create_alien(x2,y2)
                x2 -= alien_width
            x2 = current_x - 2 * alien_width
            y2 += alien_height

        # group 3
        current_x = 2 * alien_width
        alien_rows = alien_rows-1
        for i in range(1,alien_rows-1): # remove -1 for symmetric patters
            for j in range(alien_rows-1, i-1, -1):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            current_x = (2 + i) * alien_width
            current_y += alien_height

        # group 4
        current_x = alien_width
        current_y = alien_height

        for i in range(0,smaller_fleet_rows):
            for j in range(smaller_fleet_rows, i, -1):
                self._create_alien(current_x,current_y)
                current_x += alien_width
            current_x = alien_width
            current_y += alien_height

if __name__ == '__main__':
    #Make a game instance, and run the game
    ai = AlienAttack()
    ai.run_game()
