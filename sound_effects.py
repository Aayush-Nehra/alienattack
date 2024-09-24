import pygame

pygame.mixer.init()

#Game sound effect
bullet_sound = pygame.mixer.Sound("sounds/short_laser_gun.wav")
alien_hit_sound = pygame.mixer.Sound("sounds/laser.wav")
start_game_sound = pygame.mixer.Sound("sounds/xeon6.ogg")
start_game_sound.set_volume(0.2)
select_sound = pygame.mixer.Sound("sounds/select.ogg")

#Channels for simultaneous play
channel0 = pygame.mixer.Channel(0)
channel1 = pygame.mixer.Channel(1)