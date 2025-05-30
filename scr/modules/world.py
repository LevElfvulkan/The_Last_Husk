import pygame
import pytmx
from ..modules.enemy import Enemy
class Platform(pygame.sprite.Sprite):
    def __init__(self  , x , y  , width , height  , color = (0,255,0)):
        super().__init__()
        self.image = pygame.Surface((width , height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y= y

level_enemies = {
    'level1': [(500, 300), (800, 400)],
    'level2': [(600, 200), (700, 500), (900, 300)],
    'level3': [(400, 100), (500, 400), (700, 200), (900, 500)]
}


class Level(pygame.sprite.Sprite):
    def __init__(self , filename):
        self.tmx_data = pytmx.load_pygame(filename)
        self.background = None
        self.exit_rect = None
        self.enemy_positions = []
        try :
            self.background = pygame.image.load("assets/bg/Bg_level.jpg").convert()
            self.background = pygame.transform.scale(self.background,(960 , 800))
        except:
            self.background = pygame.Surface((960, 800))
            self.background.fill((0, 0, 0))
            print(f"Фон для уровня  не найден, используется черный фон")

        self.load_exit()

    def load_exit(self):
        # Ищем слой с именем "exit" в Tiled
        if "exit" in self.tmx_data.layernames:
            layer = self.tmx_data.get_layer_by_name("exit")
            for obj in layer:
                self.exit_rect = pygame.Rect(
                    obj.x, obj.y,
                    obj.width, obj.height
                )
                break
    def load_collisions(self):
        collision_rects = []
        if "map" in self.tmx_data.layernames:
            layer = self.tmx_data.get_layer_by_name("map")
            for x, y, tile in layer.tiles():
                if tile:
                    collision_rects.append(pygame.Rect(
                        x * self.tmx_data.tilewidth,
                        y * self.tmx_data.tileheight,
                        self.tmx_data.tilewidth,
                        self.tmx_data.tileheight
                    ))
        return collision_rects


    def load_enemies(self):
        return [Enemy(x, y) for x, y in self.enemy_positions]
    def draw_level(self, surface):
        if self.background:
            surface.blit(self.background, (0 ,0))
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, 'tiles'):
                for x, y, image in layer.tiles():
                    if image:
                        surface.blit(
                            image,
                            (x * self.tmx_data.tilewidth,
                             y * self.tmx_data.tileheight)
                        )
