import pygame
import sys
from platforms import FloorPlatform, WallPlatform, MovingPlatform, FallingPlatform, DeadlyPlatform
from hero import Hero
from camera import Camera
from playerStates import IdleState
from gui_helper import *
from checkbox import Checkbox


pygame.init()
size = WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode(size)


title_font = pygame.font.Font("pixel_font.ttf", 120)
pause_font = pygame.font.Font("pixel_font.ttf", 80)
font = pygame.font.Font("pixel_font.ttf", 50)

bg = pygame.image.load("images/bg.jpg")
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

def menu_setup(background, title):
    screen.fill(pygame.Color("black"))
    screen.blit(background, (0, 0))
    background = screen.copy()
    render_text(title, pause_font, pygame.Color("#c2c1bf"), screen, WIDTH // 2, HEIGHT * 0.2)
    pygame.display.flip()
    return background

# Прорисовка главного меню
def main_menu():
    pygame.mouse.set_visible(True)
    click = False
    
    while True:
        screen.fill(pygame.Color("black"))
        screen.blit(bg, (0, 0))

        pygame.mouse.set_visible(True)

        # Отрисовка кнопок
        button_start = pygame.Rect(500, 300, 280, 65)
        button_options = pygame.Rect(500, 430, 280, 65)
        button_exit = pygame.Rect(500, 560, 280, 65)

        draw_button(screen, "#0a2a59", "#082145", button_start, 10)
        draw_button(screen, "#0a2a59", "#082145", button_options, 10)
        draw_button(screen, "#0a2a59", "#082145", button_exit, 10)

        # Отрисовка текста
        render_text("Game Title", title_font, pygame.Color("#c2c1bf"), screen, WIDTH // 2, HEIGHT // 4)
        render_text("Start Game", font, pygame.Color("#c2c1bf"), screen, WIDTH // 2, 330)
        render_text("Options", font, pygame.Color("#c2c1bf"), screen, WIDTH // 2, 460)
        render_text("Exit", font, pygame.Color("#c2c1bf"), screen, WIDTH // 2, 590)

        # Координаты курсора
        x, y = pygame.mouse.get_pos()

        # Проверяем нажатие на кнопки
        if button_start.collidepoint((x, y)):
            if click:
                game()

        if button_options.collidepoint((x, y)):
            if click:
                options()

        if button_exit.collidepoint((x, y)):
            if click:
                pygame.quit()
                sys.exit()

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.flip()

# Проработка меню паузы
def pause_menu():
    # Затемнение фона
    background = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA, 32)
    background.fill((96, 0, 159, 50))
    background = menu_setup(background, "Pause")

    pygame.mouse.set_visible(True)

    hero.state = IdleState() # Останавлиаем персонажа 

    pause = True
    click = False
    
    while pause:        
        button_continue = pygame.Rect(500, 300, 280, 65)
        button_options = pygame.Rect(500, 430, 280, 65)
        button_exit = pygame.Rect(500, 560, 280, 65)

        draw_button(screen, "#0a2a59", "#082145", button_continue, 10)
        draw_button(screen, "#0a2a59", "#082145", button_options, 10)
        draw_button(screen, "#0a2a59", "#082145", button_exit, 10)

        render_text("Continue", font, pygame.Color("#c2c1bf"), screen, WIDTH // 2, 330)
        render_text("Options", font, pygame.Color("#c2c1bf"), screen, WIDTH // 2, 460)
        render_text("Main Menu", font, pygame.Color("#c2c1bf"), screen, WIDTH // 2, 590)

        x, y = pygame.mouse.get_pos()

        # Проверяем нажатие на кнопки
        if button_continue.collidepoint((x, y)):
            if click:
                game()

        if button_options.collidepoint((x, y)):
            if click:
                options()
                menu_setup(background, "Pause")

        if button_exit.collidepoint((x, y)):
            if click:
                main_menu()

        click = False
        for event in pygame.event.get():                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause = False
                    pygame.mouse.set_visible(False)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.flip()

# Прорисовка меню настроек
def options():
    # Затемнение фона
    background = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA, 32)
    background.fill((96, 0, 159, 50))
    background = menu_setup(background, "Options")

    checkbox_music = Checkbox(screen, WIDTH * 0.6, HEIGHT * 0.4, checked=False)
    checkbox_adult = Checkbox(screen, WIDTH * 0.6, HEIGHT * 0.6)

    running = True

    while running:
        render_text("Music", font, pygame.Color("#c2c1bf"), screen, WIDTH // 3, HEIGHT * 0.425)
        render_text("Adult Content", font, pygame.Color("#c2c1bf"), screen, WIDTH // 3, HEIGHT * 0.625)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    
            checkbox_music.onCheckbox(event)
            checkbox_adult.onCheckbox(event)

        checkbox_music.update()
        checkbox_adult.update()

        # Отключаем музыку
        if checkbox_music.checked:
            pass

        pygame.display.flip()


def load_level(filename):
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, ' '), level_map))


# Выводим на экран все платформы на уровне
def render(level):
    x = y = 0
    for row in level:
        for col in row:
            if col == "_":
                pf = FloorPlatform(x, y, platform_sprites)
                platforms.append(pf)
            elif col == "#":
                pf = WallPlatform(x, y, platform_sprites)
                platforms.append(pf)
            elif col == ">":
                pf = MovingPlatform(x, y, platform_sprites, ">")
                platforms.append(pf)
            elif col == "<":
                pf = MovingPlatform(x, y, platform_sprites, "<")
                platforms.append(pf)
            elif col == "=":
                pf = FallingPlatform(x, y, platform_sprites)
                platforms.append(pf)
            elif col == "^":
                pf = DeadlyPlatform(x, y, platform_sprites)
                platforms.append(pf)
            x += pf.width
        y += pf.height
        x = 0

platform_sprites = pygame.sprite.Group()
platforms = [] # объекты, с которыми будет происходить взаимодействие

hero_sprites = pygame.sprite.Group()
hero = Hero((500, 100), hero_sprites)
render(load_level('level'))

falling = False

def game():
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()
    fps = 60
    dt = 0
    camera = Camera()
    running = True
    while running:
        screen.fill(pygame.Color("black"))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_menu()
                
            hero.handle_event(event)

#############################---------v---------##################################################################

        camera.update(hero)
        camera.apply(hero)
        for sprite in platform_sprites:
            camera.apply(sprite)

#############################---------^---------##################################################################

        platform_sprites.update()
        platform_sprites.draw(screen)

        hero_sprites.update(dt, platforms)
        hero_sprites.draw(screen)

        dt = clock.tick(fps) / 1000
        pygame.display.flip()


if __name__ == "__main__":
    main_menu()
