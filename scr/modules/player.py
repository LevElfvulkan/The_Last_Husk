import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self , x , y ):
        super().__init__()
        self.x = x
        self.y = y
        self.x_speed = 2
        self.y_speed = 0
        self.gravity = 1
        self.jump_speed = -20
        self.is_on_ground = False
        self.playerWidth = 40
        self.playerHeight = 40
        self.player_rect = pygame.Rect( self.x , self.y , self.playerWidth , self.playerHeight )


    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player_rect.x -= self.x_speed
        if keys[pygame.K_RIGHT]:
            self.player_rect.x +=self.x_speed
        if keys[pygame.K_UP]:
            if (self.is_on_ground):
                self.y_speed += self.jump_speed
                self.is_on_ground = False

    def lateralPLatf(self , platforms):
        for platform in platforms:
            if   self.player_rect.colliderect(platform.rect):
                if self.player_rect.left < platform.rect.right and self.player_rect.left >= platform.rect.left:
                    self.player_rect.left = platform.rect.right
                elif self.player_rect.right > platform.rect.left and self.player_rect.right <= platform.rect.right:
                    self.player_rect.right = platform.rect.left


    def withPlatforms(self , platforms):

        self.y_speed += self.gravity
        self.player_rect.y += self.y_speed


        self.is_on_ground = False
        for platform in platforms:
            if self.player_rect.colliderect(platform.rect):
                if self.y_speed > 0 and self.player_rect.bottom > platform.rect.top:
                    self.player_rect.bottom  = platform.rect.top
                    self.is_on_ground = True
                    self.y_speed = 0
                elif self.y_speed < 0 and self.player_rect.top < platform.rect.bottom:
                    self.player_rect.top = platform.rect.bottom
                    self.y_speed = 0
            elif self.y_speed > 0 and self.player_rect.y > 800 :
                self.player_rect.x = 200
                self.player_rect.y = 100

        self.move()
        self.lateralPLatf(platforms)




    def draw(self , screen):
        pygame.draw.rect(screen ,  (100 , 100 , 100) , self.player_rect)




