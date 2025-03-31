
import pygame
from scr.config.settings import *
from scr.modules.player import Player
from scr.modules.world import Platform

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Квест-игра")


player= Player(200 , 0)
clock = pygame.time.Clock()



platforms = pygame.sprite.Group()
platforms.add(Platform(0, SCREEN_HEIGHT-100 , SCREEN_WIDTH , 20 , (255,100,50)))
platforms.add(Platform(SCREEN_WIDTH-20 ,  0 , 20 , SCREEN_HEIGHT-100 , color=(255,100,50) ))
platforms.add(Platform( 0,  0 , 20 , SCREEN_HEIGHT-100 , color=(255,100,50) ))
platforms.add(Platform(400 , SCREEN_HEIGHT- 200  , 200 , 20 ,color=(255,100,50)))

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.withPlatforms(platforms)
    screen.fill((255 , 255 ,255))

    player.draw(screen)
    platforms.draw(screen)
    pygame.display.flip()

pygаme.quit()














