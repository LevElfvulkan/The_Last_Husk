import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self , x , y ):
        super().__init__()
        self.x_speed = 2
        self.y_speed = 0
        self.gravity = 1
        self.jump_speed = -20
        self.is_on_ground = False
        self.playerWidth = 40
        self.playerHeight = 40
        self.image = pygame.Surface((self.playerWidth , self.playerHeight))
        self.image.fill((0, 255 ,55))
        self.player_rect = self.image.get_rect()
        self.player_rect.x = x
        self.player_rect.y = y
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

    def lateralPLatf(self , collision):
        for rect in collision:
            if   self.player_rect.colliderect(rect):
                if self.player_rect.left < rect.right and self.player_rect.left >= rect.left:
                    self.player_rect.left = rect.right
                elif self.player_rect.right > rect.left and self.player_rect.right <= rect.right:
                    self.player_rect.right = rect.left


    def withPlatforms(self , collision):

        self.y_speed += self.gravity
        self.player_rect.y += self.y_speed


        self.is_on_ground = False
        for rect in collision:
            if self.player_rect.colliderect(rect):
                if self.y_speed > 0 and self.player_rect.bottom > rect.top:
                    self.player_rect.bottom  = rect.top
                    self.is_on_ground = True
                    self.y_speed = 0
                elif self.y_speed < 0 and self.player_rect.top < rect.bottom:
                    self.player_rect.top =rect.bottom
                    self.y_speed = 0
            elif self.y_speed > 0 and self.player_rect.y > 800 :
                self.player_rect.x = 200
                self.player_rect.y = 100

        self.move()
        self.lateralPLatf(collision)




    def draw(self , screen):
        pygame.draw.rect(screen ,  (100 , 100 , 100) , self.player_rect)




