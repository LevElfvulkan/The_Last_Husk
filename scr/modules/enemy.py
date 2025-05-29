import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(self ,x , y):
        super().__init__()
        self.enemyIdle = [ pygame.image.load('C:/gameHollowKnight/The_Last_Husk/assets/sprites/enemyIdle/Golem1.png') , pygame.image.load('C:/gameHollowKnight/The_Last_Husk/assets/sprites/enemyIdle/Golem2.png') , pygame.image.load('C:/gameHollowKnight/The_Last_Husk/assets/sprites/enemyIdle/Golem3.png') , pygame.image.load('C:/gameHollowKnight/The_Last_Husk/assets/sprites/enemyIdle/Golem4.png') , pygame.image.load('C:/gameHollowKnight/The_Last_Husk/assets/sprites/enemyIdle/Golem5.png') ,pygame.image.load('C:/gameHollowKnight/The_Last_Husk/assets/sprites/enemyIdle/Golem6.png') , pygame.image.load('C:/gameHollowKnight/The_Last_Husk/assets/sprites/enemyIdle/Golem7.png') , pygame.image.load('C:/gameHollowKnight/The_Last_Husk/assets/sprites/enemyIdle/Golem8.png') ]
        self.enemyRun = [pygame.image.load('C:/gameHollowKnight/The_Last_Husk/assets/sprites/enemyRun/Golem1walk.png') , pygame.image.load('C:/gameHollowKnight/The_Last_Husk/assets/sprites/enemyRun/Golem2walk.png') , pygame.image.load('C:/gameHollowKnight/The_Last_Husk/assets/sprites/enemyRun/Golem3walk.png') , pygame.image.load('C:/gameHollowKnight/The_Last_Husk/assets/sprites/enemyRun/Golem4walk.png') , pygame.image.load('C:/gameHollowKnight/The_Last_Husk/assets/sprites/enemyRun/Golem5walk.png') , pygame.image.load('C:/gameHollowKnight/The_Last_Husk/assets/sprites/enemyRun/Golem6walk.png') , pygame.image.load('C:/gameHollowKnight/The_Last_Husk/assets/sprites/enemyRun/Golem7walk.png') , pygame.image.load('C:/gameHollowKnight/The_Last_Husk/assets/sprites/enemyRun/Golem8walk.png') , pygame.image.load('C:/gameHollowKnight/The_Last_Husk/assets/sprites/enemyRun/Golem9walk.png') , pygame.image.load('C:/gameHollowKnight/The_Last_Husk/assets/sprites/enemyRun/Golem10walk.png')]
        self.enemyDeath = [pygame.image.load(f'C:/gameHollowKnight/The_Last_Husk/assets/sprites/deathEnemy/Golem_{i}_die.png') for i in range(1, 13)]
        self.enemyWidth = 39
        self.enemyHeight = 38

        self.animation = 0
        self.image = pygame.Surface((self.enemyWidth , self.enemyHeight))
        self.image.fill((0, 0 ,0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.on_ground = False
        self.speed = 0.7
        self.gravity = 0.5
        self.y_speed = 0
        self.direction = 1
        self.health =10
        self.max_health = 10
        self.damage = 10

        self.activate = True
        self.knockback_delay  = 0
        self.knockback_direction = 1
        self.knockback_speed = 30
        self.knockback_damping = 0.6
        self.is_knockback = False
        self.attack_cooldown = 0

        self.is_dying = False
        self.death_animation_frame = 0
        self.death_animation_speed = 0.3
        self.death_delay = 12

        self.original_x = x
        self.patrol_range = 250




    def handle_collision(self, player):

        if ((self.activate and self.attack_cooldown <= 0) and (player.player_rect.colliderect(self.rect))):
            player.take_damage(self.damage)
            self.attack_cooldown = 60
            if player.face_right == False :
                player.player_rect.left = player.player_rect.left + 50
            else:
                player.player_rect.right = player.player_rect.right - 50

        # с игроком
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        if player.player_rect.colliderect(self.rect):
            if player.player_rect.right > self.rect.left and player.player_rect.left >= self.rect.right :
                player.player_rect.right = self.rect.left

            if player.player_rect.left > self.rect.right and player.player_rect.right <= self.rect.left:
                player.player_rect.left = self.rect.right-20



            if player.player_rect.bottom < self.rect.top:
                player.player_rect.bottom = self.rect.top
                player.is_on_ground = True
                player.y_speed = 0
            if player.player_rect.top > self.rect.bottom:
                player.player_rect.top = self.rect.bottom
                player.y_speed = 0
    def update(self, collision_rects , player):
        if self.is_dying:
            if self.death_delay > 0:
                self.death_delay -=1
                return
            self.death_animation_frame += self.death_animation_speed
            if self.death_animation_frame >= len(self.enemyDeath):
                self.activate = False

            return
        if self.health <=0 and not self.is_dying:

            self.death_animation()
            return

        if self.rect.x > self.original_x + self.patrol_range / 2:
            self.direction = -1  # Разворачиваемся если вышли за правую границу
        elif self.rect.x < self.original_x - self.patrol_range / 2:
            self.direction = 1  # Разворачиваемся если вышли за левую границу

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

        if self.activate and not self.is_knockback:
            self.rect.x += self.speed * self.direction
            for rect in collision_rects:
                if self.rect.colliderect(rect):
                    if self.direction > 0:
                        self.rect.right = rect.left
                    else:
                        self.rect.left = rect.right
                    self.direction *= -1
                    break


    def death_animation(self):
        self.is_dying = True
        self.death_animation_frame = 0
        self.speed = 0
        self.death_delay = 12



    def draw(self, screen):
        if not self.activate and not self.is_dying:
            return

        if self.is_dying:

            if self.death_delay > 0:
                if abs(self.speed * self.direction) > 0.1:
                    current_frame = self.enemyRun[-1]  # Последний кадр бега
                else:
                    current_frame = self.enemyIdle[-1]  # Последний кадр idle

                if self.direction < 0:
                    current_frame = pygame.transform.flip(current_frame, True, False)
                screen.blit(current_frame, (self.rect.x, self.rect.y))
                return

                # Отрисовка анимации смерти
            frame_index = min(int(self.death_animation_frame), len(self.enemyDeath) - 1)
            current_frame = self.enemyDeath[frame_index]
            if self.direction < 0:
                current_frame = pygame.transform.flip(current_frame, True, False)
            screen.blit(current_frame, (self.rect.x, self.rect.y - 5))
            return

        if self.animation >= 40:
            self.animation = 0


        if abs(self.speed * self.direction) > 0.1:
            current_frame = self.enemyRun[self.animation // 2 % len(self.enemyRun)]
        else:
            current_frame = self.enemyIdle[self.animation // 4 % len(self.enemyIdle)]

        # Отражаем изображение, если движется влево
        if self.direction < 0:
            current_frame = pygame.transform.flip(current_frame, True, False)

        screen.blit(current_frame, (self.rect.x, self.rect.y))
        self.animation += 1


