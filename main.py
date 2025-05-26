import pygame
import sys
from scr.config.settings import *
from scr.modules.player import Player
from scr.modules.world import Level
from scr.modules.enemy import Enemy


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('Times New Roman', 80)
        self.small_font = pygame.font.SysFont('Arial', 30)
        self.selected = 0
        self.options = ["Начать игру", "Настройки", "Выход"]

        try:
            self.background = pygame.image.load('assets/bg/menu_bg.png').convert()
            self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:

            self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background.fill((0, 0, 30))
            print("Не удалось загрузить фоновое изображение, используется цветной фон")

    def draw(self):

        self.screen.blit(self.background, (0, 0))
        #для читаемости
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))

        # заголовок
        title = self.font.render("The Last Husk", True, (255, 255, 255))
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        self.screen.blit(title, title_rect)

        #  меню
        for i, option in enumerate(self.options):
            color = (255, 215, 0) if i == self.selected else (255, 255, 255)
            text = self.small_font.render(option, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 60))
            self.screen.blit(text, text_rect)


        hint = self.small_font.render("Используйте стрелки и Enter для выбора", True, (200, 200, 200))
        hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(hint, hint_rect)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % len(self.options)
                elif event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    return self.selected
        return None


def load_level(index):
    global level, collision
    if 0 <= index < len(levels):
        level = Level(levels[index])
        if level is None:
            raise ValueError(f"Не удалось загрузить файл {levels[index]}")
        collision = level.load_collisions()
        player.player_rect.x = 300
        player.player_rect.y = 300
        return True
    return False


def draw_all():
    level.draw_level(screen)
    player.draw(screen)
    enemy.draw(screen)
    font = pygame.font.SysFont(None, 36)
    level_text = font.render(f"Уровень: {current_level_index + 1}", True, (255, 255, 255))
    screen.blit(level_text, (10, 10))


def game_loop():
    global running, current_level_index

    clock = pygame.time.Clock()
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"  # Возвращаемся в меню
                elif event.key == pygame.K_n:
                    current_level_index = (current_level_index + 1) % len(levels)
                    load_level(current_level_index)

        player.update(level.load_collisions(), enemy)
        enemy.update(level.load_collisions(), player)

        screen.fill((255, 255, 255))
        draw_all()
        pygame.display.flip()

        # Проверка смерти игрока
        if player.is_dead and player.death_finished:
            return "game_over"

    return "exit"


def game_over_screen():
    font = pygame.font.SysFont('Arial', 50)
    small_font = pygame.font.SysFont('Arial', 30)

    while True:
        screen.fill((0, 0, 0))

        title = font.render("Игра Окончена", True, (255, 0, 0))
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        screen.blit(title, title_rect)

        score = small_font.render(f"Достигнут уровень: {current_level_index + 1}", True, (255, 255, 255))
        score_rect = score.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(score, score_rect)

        hint = small_font.render("Нажмите Enter чтобы вернуться в меню", True, (200, 200, 200))
        hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
        screen.blit(hint, hint_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return "menu"


def main():
    global screen, levels, current_level_index, level, player, enemy, running

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("The Last Husk")

    # Инициализация игровых объектов
    levels = ['level1.tmx', "level2.tmx", "level3.tmx"]
    current_level_index = 0
    level = Level(levels[current_level_index])
    player = Player(300, 300)
    enemy = Enemy(500, 300)
    running = True

    # Создаем меню
    menu = Menu(screen)

    # Основной цикл приложения
    app_state = "menu"  # menu/game/game_over/exit

    while True:
        if app_state == "menu":
            # Отрисовка и обработка меню
            menu.draw()
            pygame.display.flip()

            result = menu.handle_events()
            if result == 0:  # Начать игру
                app_state = "game"
                load_level(current_level_index)
                player = Player(300, 300)  # Сброс игрока
            elif result == 1:  # Настройки (заглушка)
                pass  # Можно добавить экран настроек
            elif result == 2:  # Выход
                app_state = "exit"

        elif app_state == "game":
            result = game_loop()
            app_state = result

        elif app_state == "game_over":
            result = game_over_screen()
            app_state = result

        elif app_state == "exit":
            pygame.quit()
            sys.exit()


if __name__ == "__main__":
    main()