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
        self.main_options = ["Начать игру", "Настройки", "Выход"]
        self.level_options = ["Легкий уровень", "Средний уровень", "Сложный уровень", "Назад"]
        self.settings_options = ["Назад"]
        self.current_options = self.main_options
        self.state = "main"  # может быть "main", "level_select", "settings"
        try:
            self.background = pygame.image.load('assets/bg/menu_bg.png').convert()
            self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background.fill((0, 0, 30))
            print("Не удалось загрузить фоновое изображение, используется цветной фон")

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))

        if self.state != "settings":
            title = self.font.render("The Last Husk", True, (255, 255, 255))
            title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
            self.screen.blit(title, title_rect)

        if self.state == "settings":
            self.draw_settings()
        else:
            for i, option in enumerate(self.current_options):
                color = (255, 215, 0) if i == self.selected else (255, 255, 255)
                text = self.small_font.render(option, True, color)
                y_pos = SCREEN_HEIGHT // 2 + i * 60 if self.state == "main" else SCREEN_HEIGHT // 2 + i * 50
                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
                self.screen.blit(text, text_rect)

        hint_text = "Используйте стрелки и Enter для выбора"
        if self.state == "level_select":
            hint_text = "Выберите уровень или нажмите Назад"
        elif self.state == "settings":
            hint_text = "Нажмите Enter чтобы вернуться"

        hint = self.small_font.render(hint_text, True, (200, 200, 200))
        hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(hint, hint_rect)

    def draw_settings(self):
        title = self.font.render("Управление", True, (255, 255, 255))
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        self.screen.blit(title, title_rect)

        controls = [
            "Движение: Стрелки влево/вправо",
            "Прыжок: Стрелка вверх",
            "Атака: Z",
            "Выход: ESC"
        ]

        for i, control in enumerate(controls):
            text = self.small_font.render(control, True, (255, 255, 255))
            y_pos = SCREEN_HEIGHT // 2 + i * 40
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
            self.screen.blit(text, text_rect)

        # Кнопка назад
        color = (255, 215, 0) if self.selected == 0 else (255, 255, 255)
        back_text = self.small_font.render("Назад", True, color)
        back_rect = back_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150))
        self.screen.blit(back_text, back_rect)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % len(self.current_options)
                elif event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % len(self.current_options)
                elif event.key == pygame.K_RETURN:
                    if self.state == "main":
                        if self.selected == 0:
                            self.state = "level_select"
                            self.current_options = self.level_options
                            self.selected = 0
                            return None
                        elif self.selected == 1:
                            self.state = "settings"
                            self.current_options = self.settings_options
                            self.selected = 0
                            return None
                        elif self.selected == 2:
                            return "exit"
                    elif self.state == "level_select":
                        if self.selected == 0:
                            return "level_1"
                        elif self.selected == 1:
                            return "level_2"
                        elif self.selected == 2:
                            return "level_3"
                        elif self.selected == 3:
                            self.state = "main"
                            self.current_options = self.main_options
                            self.selected = 0
                            return None
                    elif self.state == "settings":
                        if self.selected == 0:
                            self.state = "main"
                            self.current_options = self.main_options
                            self.selected = 0
                            return None
                elif event.key == pygame.K_ESCAPE:
                    if self.state == "level_select" or self.state == "settings":
                        self.state = "main"
                        self.current_options = self.main_options
                        self.selected = 0
                        return None
        return None
def load_level(index):
    global level, current_level_index

    if 0 <= index < len(levels):
        try:
            level = Level(levels[index])
            player.player_rect.x = 300
            player.player_rect.y = 100
            current_level_index = index
            return True

        except Exception as e:
            print(f"Error loading level {levels[index]}: {e}")
            return False
    return False



def draw_all():
    level.draw_level(screen)
    player.draw(screen)
    enemy.draw(screen)

    font = pygame.font.SysFont(None, 36)
    level_text = font.render(f"Уровень: {current_level_index + 1}", True, (255, 255, 255))
    screen.blit(level_text, (10, 10))

    # Отображение состояния игрока
    if player.is_attacking:
        attack_text = font.render("Атака!", True, (255, 0, 0))
        screen.blit(attack_text, (10, 50))


def game_loop():
    global running, current_level_index

    clock = pygame.time.Clock()
    level_complete = False
    complete_timer = 0

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"


        if not level_complete:
            player.update(level.load_collisions(), enemy)
            enemy.update(level.load_collisions(), player)


        screen.fill((255, 255, 255))
        level.draw_level(screen)
        player.draw(screen)
        enemy.draw(screen)

        font = pygame.font.SysFont(None, 36)
        level_text = font.render(f"Уровень: {current_level_index + 1}", True, (255, 255, 255))
        screen.blit(level_text, (820, 10))


        pygame.display.flip()

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

    levels = ['level1.tmx', "level2.tmx", "level3.tmx"]
    current_level_index = 0
    level = Level(levels[current_level_index])
    player = Player(300, 100)
    enemy = Enemy(500, 300)
    running = True

    menu = Menu(screen)
    app_state = "menu"

    while True:
        if app_state == "menu":
            menu.draw()
            pygame.display.flip()

            result = menu.handle_events()
            if result == "level_1":
                current_level_index = 0
                app_state = "game"
                load_level(current_level_index)
            elif result == "level_2":
                current_level_index = 1
                app_state = "game"
                load_level(current_level_index)
            elif result == "level_3":
                current_level_index = 2
                app_state = "game"
                load_level(current_level_index)
            elif result == "exit":
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