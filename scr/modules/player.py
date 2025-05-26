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
        self.max_health = 100
        self.health  = self.max_health
        self.damage = 20
        self.invincible = False
        self.invincible_timer = 0
        self.invincible_duration = 60
        self.has_hit_damage = False
        self.hit_cooldown = 0
        self.death_animation = 0
        self.is_dead = False
        self.death_finished = False
        self.death_timer = 0
        self.death_duration = 60
        self.playerDeath = [pygame.image.load('C:/gameHollowKnight/The_Last_Husk/assets/sprites/death/dead-1.png'),
                           pygame.image.load('C:/gameHollowKnight/The_Last_Husk/assets/sprites/death/dead-2.png'),
                           pygame.image.load('C:/gameHollowKnight/The_Last_Husk/assets/sprites/death/dead-4.png'),
                           pygame.image.load('C:/gameHollowKnight/The_Last_Husk/assets/sprites/death/dead-5.png'),
                           pygame.image.load('C:/gameHollowKnight/The_Last_Husk/assets/sprites/death/dead-6.png')]


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
        if self.face_right :
            self.attackRect = pygame.Rect(
                self.player_rect.right,
                self.player_rect.y,
                attack_width,
                self.player_rect.height
            )
        else:
            self.attackRect = pygame.Rect(
                self.player_rect.left - attack_width+30,
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
            self.attack_animation +=2
            if self.attack_animation >= 48:
                self.is_attacking = False
                self.attack_animation =0
                self.has_hit_damage = False

    def take_damage(self, amount):
        if not self.invincible and self.hit_cooldown <= 0:
            self.health -= amount
            if self.health < 0:
                self.health = 0
                self.is_dead = True
                self.death_animation = 0
            self.invincible = True
            self.invincible_timer = self.invincible_duration
            self.hit_cooldown = 30

    def draw_health_bar(self, screen):
        #полоска здоровья
        health_bar_width = 200
        health_bar_height = 20
        outline_rect = pygame.Rect(10, 10, health_bar_width, health_bar_height)
        pygame.draw.rect(screen, (255, 0, 0), outline_rect)

        # сколько здоровья на данный момент
        health_ratio = self.health / self.max_health
        fill_width = health_ratio * health_bar_width
        fill_rect = pygame.Rect(10, 10, fill_width, health_bar_height)
        pygame.draw.rect(screen, (0, 255, 0), fill_rect)

        pygame.draw.rect(screen, (255, 255, 0), outline_rect, 2) # контур

        # сама полоска здоровья
        font = pygame.font.SysFont(None, 24)
        health_text = font.render(f"{self.health}/{self.max_health}", True, (255, 255, 255))
        screen.blit(health_text, (outline_rect.right + 10, outline_rect.y))

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
            enemy.knockback_delay = 10

            if self.face_right :
                enemy.knockback_direction = 1
                enemy.knockback_speed = 25 * enemy.knockback_direction
            else:
                enemy.knockback_direction = -1
                enemy.knockback_speed = 25 * enemy.knockback_direction


    def death(self):
        if self.is_dead and not self.death_finished:
            self.death_timer += 1
            # Обновляем анимацию каждые 12 кадров (5 кадров анимации)
            if self.death_timer % 12 == 0 and self.death_animation < len(self.playerDeath) - 1:
                self.death_animation += 1

            if self.death_timer >= self.death_duration:
                self.death_finished = True

    def update(self, collisions , enemy):
        if self.is_dead:
            self.death()
        if self.hit_cooldown > 0:
            self.hit_cooldown -=1
        if self.invincible:
            self.invincible_timer -=1
            if self.invincible_timer <= 0:
                self.invincible =False
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
        if self.is_dead:
            screen.blit(self.playerDeath[self.death_animation], (self.player_rect.x , self.player_rect.y))
            return
        if self.is_attacking :
            self.attack_index = min(self.attack_animation // (36// len(self.rightAttack )),
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
        self.draw_health_bar(screen)






