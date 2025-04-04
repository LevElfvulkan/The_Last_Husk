import pygame
from ..config.settings import *



class Camera():
    def __init__(self , level_width, level_height ):
        self.level_width = level_width
        self.level_height = level_width
        self.set = pygame.math.Vector2(0 , 0)

    def updatePlayer(self , player):
        camera_x = SCREEN_WIDTH // 2 - player.player_rect.centerx
        camera_y = SCREEN_HEIGHT // 2 - player.player_rect.centery
        # camera_x = max(-(self.level_width - SCREEN_WIDTH), min(0, camera_x))
        # camera_y = max(-(self.level_height - SCREEN_HEIGHT), min(0, camera_y))
        self.set = pygame.math.Vector2( camera_x ,camera_y )


