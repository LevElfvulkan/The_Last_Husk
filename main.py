import pygame
import os
from scr.config.settings import *
from scr.modules.player import Player
from scr.modules.world import Platform , Level
from scr.modules.camera import Camera
from scr.modules.enemy import Enemy
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Квест-игра")


enemy = Enemy(500 ,300)


player= Player(300 , 300)
clock = pygame.time.Clock()

camera = Camera(800 , 600)

level = Level("test_map.tmx")
if level is None:
    raise ValueError("Не удалось загрузить файл level.tmx")
collision = level.load_collisions()




def draw_all():
    level.draw_level(screen)
    player.draw(screen)
    enemy.draw(screen)








running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.update(level.load_collisions() , enemy)
    enemy.update(level.load_collisions() , player)




    #Отрисовка всех спрайтов
    screen.fill((255 , 255 ,255))
    draw_all()
    pygame.display.flip()

pygаme.quit()














