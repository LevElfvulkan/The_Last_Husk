import pygame
import pytmx

class Platform(pygame.sprite.Sprite):
    def __init__(self  , x , y  , width , height  , color = (0,255,0)):
        super().__init__()
        self.image = pygame.Surface((width , height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y= y


class Level(pygame.sprite.Sprite):
    def __init__(self , filename):
        self.tmx_data = pytmx.load_pygame(filename)

    def draw_level(self , screen):
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, 'tiles'):
                for x, y, image in layer.tiles():
                    if image:
                        screen.blit(image, (x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight))

    def load_collisions(self):
        collision_rects = []

        # Вариант 1: Загрузка из Tile Layer
        if "map" in self.tmx_data.layernames:
            layer = self.tmx_data.get_layer_by_name("map")
            for x, y, tile in layer.tiles():
                if tile:  # Если тайл существует
                    collision_rects.append(pygame.Rect(
                        x * self.tmx_data.tilewidth,
                        y * self.tmx_data.tileheight,
                        self.tmx_data.tilewidth,
                        self.tmx_data.tileheight
                    ))
        return collision_rects


