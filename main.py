import pygame
import os
from scr.config.settings import *
from scr.modules.player import Player
from scr.modules.world import Platform , Level
from scr.modules.camera import Camera

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Квест-игра")


player= Player(300 , 300)
clock = pygame.time.Clock()

camera = Camera(800 , 600)

level = Level("test_map.tmx")
if level is None:
    raise ValueError("Не удалось загрузить файл level.tmx")
collision = level.load_collisions()

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    camera.updatePlayer(player)
    player.withPlatforms(level.load_collisions())






    #Отрисовка всех спрайтов
    screen.fill((255 , 255 ,255))

    level.draw_level(screen)
    player.draw(screen)
    pygame.display.flip()

pygаme.quit()














