import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self , x , y ):
        super().__init__()
        self.x_speed = 3
        self.y_speed = 0
        self.gravity = 1
        self.jump_speed = -20
        self.is_on_ground = False
        self.playerWidth = 32
        self.playerHeight = 60
        self.image = pygame.Surface((self.playerWidth , self.playerHeight))
        self.image.fill((0, 0 ,0))
        self.player_rect = self.image.get_rect()
        self.player_rect.x = x
        self.player_rect.y = y
        self.playerIdle = [pygame.image.load('C:/gameHollowKnight/The_Last_Husk/assets/sprites/idlePlayer/idle-with-weapon-1.png')  , pygame.image.load('C:/gameHollowKnight/The_Last_Husk/assets/sprites/idlePlayer/idle-with-weapon-2.png'),pygame.image.load('C:/gameHollowKnight/The_Last_Husk/assets/sprites/idlePlayer/idle-with-weapon-3.png'), pygame.image.load('C:/gameHollowKnight/The_Last_Husk/assets/sprites/idlePlayer/idle-with-weapon-4.png'),pygame.image.load('C:/gameHollowKnight/The_Last_Husk/assets/sprites/idlePlayer/idle-with-weapon-5.png'),pygame.image.load('C:/gameHollowKnight/The_Last_Husk/assets/sprites/idlePlayer/idle-with-weapon-6.png') ]
        self.playerRunRight = [pygame.image.load('C:/gameHollowKnight/The_Last_Husk/assets/sprites/runPLayer/run-1.png') , pygame.image.load('C:/gameHollowKnight/The_Last_Husk/assets/sprites/runPLayer/run-2.png'),pygame.image.load('C:/gameHollowKnight/The_Last_Husk/assets/sprites/runPLayer/run-3.png') , pygame.image.load('C:/gameHollowKnight/The_Last_Husk/assets/sprites/runPLayer/run-4.png') , pygame.image.load('C:/gameHollowKnight/The_Last_Husk/assets/sprites/runPLayer/run-5.png') , pygame.image.load('C:/gameHollowKnight/The_Last_Husk/assets/sprites/runPLayer/run-6.png')]
        self.playerRunLeft = [pygame.transform.flip(f, True , False) for f in self.playerRunRight]
        self.animation_run = 0
        self.rightRun = False
        self.leftRun = False
        self.rightAttack  = [pygame.image.load('C:/gameHollowKnight/The_Last_Husk/assets/sprites/attack/attack-C1.png') ,  pygame.image.load('C:/gameHollowKnight/The_Last_Husk/assets/sprites/attack/attack-C2.png') ,  pygame.image.load('C:/gameHollowKnight/The_Last_Husk/assets/sprites/attack/attack-C3.png') , pygame.image.load('C:/gameHollowKnight/The_Last_Husk/assets/sprites/attack/attack-C4.png') , pygame.image.load('C:/gameHollowKnight/The_Last_Husk/assets/sprites/attack/attack-C5.png') , pygame.image.load('C:/gameHollowKnight/The_Last_Husk/assets/sprites/attack/attack-C6.png') ]
        self.leftAttack = [pygame.transform.flip(f , True , False) for f in self.rightAttack]
        self.is_attacking = False
        self.attack_index = 0

        self.attackRect = pygame.Rect(0 , 0, 0,0)
        self.attack_block_rects = []
        self.animation = 0
        self.attack_animation = 0


    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player_rect.x -= self.x_speed
            self.rightRun = False
            self.leftRun = True
        elif keys[pygame.K_RIGHT]:
            self.player_rect.x +=self.x_speed
            self.rightRun = True
            self.leftRun = False
        else :
            self.rightRun = False
            self.leftRun = False
        if keys[pygame.K_UP]:
            if (self.is_on_ground):
                self.y_speed += self.jump_speed
                self.is_on_ground = False


    def attack(self):
        if not self.is_attacking  :
            self.is_attacking = True

            if self.playerRunRight:
                self.attackRect = pygame.Rect(self.player_rect.right , self.player_rect.y , 50 , self.player_rect.height)
            else :
                self.attackRect = pygame.Rect(self.player_rect.left , self.player_rect.y, 50, self.player_rect.height)


    def update_attack(self):
        if self.is_attacking :
            self.attack_animation +=1
            if self.attack_animation >= 48:
                self.is_attacking = False
                self.attack_animation =  0




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


    def update(self, collisions):
        self.withPlatforms(collisions)
        self.update_attack()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_z]:
            self.attack()




    def draw(self , screen):

        if self.is_attacking :

            self.attack_index = min(self.attack_animation // (48 // len(self.rightAttack )),
                                   len(self.leftAttack) - 1)
            if self.rightRun:
                screen.blit(self.rightAttack[self.attack_index] , (self.player_rect.x  , self.player_rect.y))
            if self.leftRun:
                screen.blit(self.leftAttack[self.attack_index], (self.player_rect.x , self.player_rect.y))
            if self.rightRun == False and self.leftRun == False:
                screen.blit(self.rightAttack[self.attack_index], (self.player_rect.x, self.player_rect.y))

        else:
            if self.animation >= 24:
                self.animation = 0
            if (self.leftRun) and (self.rightRun == False):
                screen.blit(self.playerRunLeft[self.animation // 12] , (self.player_rect.x ,self.player_rect.y))
                self.animation += 1
            elif (self.rightRun) and (self.leftRun == False):

                screen.blit(self.playerRunRight[self.animation // 12], (self.player_rect.x ,self.player_rect.y))
                self.animation +=1
            else:
                screen.blit(self.playerIdle[self.animation // 6] , (self.player_rect.x ,self.player_rect.y))
                self.animation += 1





