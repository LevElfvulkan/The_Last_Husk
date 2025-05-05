import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(self ,x , y):
        super().__init__()
        self.enemyIdle = [ pygame.image.load('C:/gameHollowKnight/The_Last_Husk/assets/sprites/enemyIdle/1.png') , pygame.image.load('C:/gameHollowKnight/The_Last_Husk/assets/sprites/enemyIdle/2.png') , pygame.image.load('C:/gameHollowKnight/The_Last_Husk/assets/sprites/enemyIdle/3.png') , pygame.image.load('C:/gameHollowKnight/The_Last_Husk/assets/sprites/enemyIdle/4.png') ]
        self.enemyWidth = 41
        self.enemyHeight = 32

        self.animation = 0
        self.image = pygame.Surface((self.enemyWidth , self.enemyHeight))
        self.image.fill((0, 0 ,0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.on_ground = False
        self.speed = 1
        self.gravity = 0.5
        self.y_speed = 0
        self.direction = 1
        self.health = 1000
        self.damage = 10

        self.activate = True
        self.knockback_delay  = 0
        self.knockback_direction = 1
        self.knockback_speed = 30
        self.knockback_damping = 0.6
        self.is_knockback = False


    def handle_collision(self, player):
        #с игроком
        if player.player_rect.colliderect(self.rect):
            if player.player_rect.right > self.rect.left and player.player_rect.left >= self.rect.right :
                player.player_rect.right = self.rect.left
            if player.player_rect.left > self.rect.right and player.player_rect.right <= self.rect.left:
                player.player_rect.left = self.rect.right


            if player.player_rect.bottom < self.rect.top:
                player.player_rect.bottom = self.rect.top
                player.is_on_ground = True
                player.y_speed = 0
            if player.player_rect.top > self.rect.bottom:
                player.player_rect.top = self.rect.bottom
                player.y_speed = 0
    def update(self, collision_rects , player):

        if self.knockback_delay > 0 :
            self.knockback_delay -=1
            if self.knockback_delay == 0:
                self.rect.x += self.knockback_speed
                self.knockback_speed *= self.knockback_damping


        # гравитация
        self.y_speed += self.gravity
        self.rect.y += self.y_speed

        # коллизий с землей
        self.on_ground = False
        for rect in collision_rects:
            if self.rect.colliderect(rect):
                if self.y_speed > 0:
                    self.rect.bottom = rect.top
                    self.on_ground = True
                    self.y_speed = 0
                elif self.y_speed < 0:
                    self.rect.top = rect.bottom
                    self.y_speed = 0
        self.handle_collision(player)

        if self.health <= 0:
            self.activate = False







    def draw(self , screen):
        if not self.activate:
            return
        if self.animation >= 16:
            self.animation =  0
        screen.blit(self.enemyIdle[self.animation // 4] ,  (self.rect.x , self.rect.y))
        self.animation += 1




