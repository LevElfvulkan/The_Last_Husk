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
        self.face_right = True
        self.playerRunRight = [pygame.image.load('C:/gameHollowKnight/The_Last_Husk/assets/sprites/runPLayer/run-1.png') , pygame.image.load('C:/gameHollowKnight/The_Last_Husk/assets/sprites/runPLayer/run-2.png'),pygame.image.load('C:/gameHollowKnight/The_Last_Husk/assets/sprites/runPLayer/run-3.png') , pygame.image.load('C:/gameHollowKnight/The_Last_Husk/assets/sprites/runPLayer/run-4.png') , pygame.image.load('C:/gameHollowKnight/The_Last_Husk/assets/sprites/runPLayer/run-5.png') , pygame.image.load('C:/gameHollowKnight/The_Last_Husk/assets/sprites/runPLayer/run-6.png')]
        self.playerRunLeft = [pygame.transform.flip(f, True , False) for f in self.playerRunRight]
        self.animation_run = 0
        self.rightRun = False
        self.leftRun = False
        self.rightAttack  = [pygame.image.load('C:/gameHollowKnight/The_Last_Husk/assets/sprites/attack/attack-C1.png') ,  pygame.image.load('C:/gameHollowKnight/The_Last_Husk/assets/sprites/attack/attack-C2.png') ,  pygame.image.load('C:/gameHollowKnight/The_Last_Husk/assets/sprites/attack/attack-C3.png') , pygame.image.load('C:/gameHollowKnight/The_Last_Husk/assets/sprites/attack/attack-C4.png') , pygame.image.load('C:/gameHollowKnight/The_Last_Husk/assets/sprites/attack/attack-C5.png') , pygame.image.load('C:/gameHollowKnight/The_Last_Husk/assets/sprites/attack/attack-C6.png') ]
        self.leftAttack = [pygame.transform.flip(f , True , False) for f in self.rightAttack]
        self.is_attacking = False
        self.attack_index = 0
        self.direction = None
        self.attackRect = pygame.Rect(0 , 0, 0,0)
        self.attack_block_rects = []
        self.animation = 0
        self.attack_animation = 0
        self.health  = 100
        self.damage = 20
        self.invincible = False
        self.invincible_timer = 0
        self.invincible_duration = 60
        self.has_hit_damage = False


    def move(self):
        keys = pygame.key.get_pressed()
        if not self.is_attacking:
            if keys[pygame.K_LEFT]:
                self.player_rect.x -= self.x_speed
                self.rightRun = False
                self.leftRun = True
                self.face_right = False
            elif keys[pygame.K_RIGHT]:
                self.player_rect.x +=self.x_speed
                self.rightRun = True
                self.leftRun = False
                self.face_right = True
            else :
                self.rightRun = False
                self.leftRun = False
            if keys[pygame.K_UP]:
                if (self.is_on_ground):
                    self.y_speed += self.jump_speed
                    self.is_on_ground = False




    def attack_rect(self):
        attack_width = 67
        if self.rightRun or (not self.leftRun and not self.rightRun):
            self.attackRect = pygame.Rect(
                self.player_rect.right,
                self.player_rect.y,
                attack_width,
                self.player_rect.height
            )
        else:
            self.attackRect = pygame.Rect(
                self.player_rect.left - attack_width,
                self.player_rect.y,
                attack_width,
                self.player_rect.height
            )
    def can_attack(self, collisions):
        self.attack_rect()
        for block in collisions:
            if self.attackRect.colliderect(block):
                return False
        return True

    def attack(self,collisions):
        if not self.is_attacking and self.can_attack(collisions):
            self.is_attacking = True
            self.attack_animation = 0
            self.attack_rect()
    def update_attack(self):
        if self.is_attacking :
            self.attack_rect()
            self.attack_animation +=1
            if self.attack_animation >= 48:
                self.is_attacking = False
                self.attack_animation =0
                self.has_hit_damage = False




    def lateralPLatf(self , collision):
        for rect in collision:
            if   self.player_rect.colliderect(rect):
                if self.player_rect.left < rect.right and self.player_rect.left >= rect.left:
                    self.player_rect.left = rect.right
                elif self.player_rect.right > rect.left and self.player_rect.right <= rect.right:
                    self.player_rect.right = rect.left


    def withPlatforms(self , collision , enemy):

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

        if enemy.activate and self.player_rect.colliderect(enemy.rect):

            if self.player_rect.left < enemy.rect.right and self.player_rect.left >= enemy.rect.left:
                self.player_rect.left = enemy.rect.right
            elif self.player_rect.right > enemy.rect.left and self.player_rect.right <= enemy.rect.right:
                self.player_rect.right = enemy.rect.left

        self.move()
        self.lateralPLatf(collision)

    def attack_collision(self, collision):
        if not self.is_attacking:
            return

        for block in collision:
            if self.attackRect.colliderect(block):

                if self.rightRun:
                    new_width = block.left - self.attackRect.left
                    if new_width > 0:
                        self.attackRect.width = new_width

                else:
                    new_width = self.attackRect.right - block.right
                    if new_width > 0:
                        self.attackRect.width = new_width
                        self.attackRect.x = block.right
                break




    def attack_enemy(self ,  enemy):
        if self.is_attacking and self.attackRect.colliderect(enemy.rect) and enemy.activate and not self.has_hit_damage :
            self.has_hit_damage = True
            enemy.health -= self.damage
            enemy.knockback_delay = 40

            if self.rightRun or  (not self.leftRun and not self.rightRun):
                enemy.knockback_direction = 1
                enemy.knockback_speed = 25 * enemy.knockback_direction
            else:
                enemy.knockback_direction = -1
                enemy.knockback_speed = 25 * enemy.knockback_direction




    def update(self, collisions , enemy):
        self.withPlatforms(collisions , enemy)
        self.update_attack()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_z]:
            self.attack(collisions)
        if self.is_attacking:
            self.attack_rect()
            self.attack_collision(collisions)
            self.attack_enemy(enemy)




    def draw(self , screen):
        if self.is_attacking :
            self.attack_index = min(self.attack_animation // (48 // len(self.rightAttack )),
                                   len(self.leftAttack) - 1)
            if self.face_right:
                screen.blit(self.rightAttack[self.attack_index] , (self.player_rect.x  , self.player_rect.y))
            if not self.face_right:
                if self.attack_index in [4,5] :
                    offset_x = 30
                    screen.blit(self.leftAttack[self.attack_index], (self.player_rect.x - offset_x, self.player_rect.y))
                else:
                    screen.blit(self.leftAttack[self.attack_index], (self.player_rect.x  , self.player_rect.y))



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
                if self.face_right:
                    screen.blit(self.playerIdle[self.animation // 6] , (self.player_rect.x ,self.player_rect.y))
                    self.animation += 1
                else:
                    flipped_idle = [pygame.transform.flip(img, True, False) for img in self.playerIdle]
                    screen.blit(flipped_idle[self.animation // 6], (self.player_rect.x, self.player_rect.y))
                    self.animation += 1






