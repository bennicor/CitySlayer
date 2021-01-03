import pygame
import os
import configparser
import json
from platforms import FloorPlatform, WallPlatform, MovingPlatform
from hero import Hero
from playerStates import IdleState
from helpers import *
from gui_elements.checkbox import Checkbox
from gui_elements.buttons import Button


pygame.init()

# Импорт настроек
config = configparser.ConfigParser()
config.read("settings.ini")

width = config.getint('MAIN', 'width')
height = config.getint('MAIN', 'height')

size = width, height
screen = pygame.display.set_mode(size)

# Загружаем сохраненные данные, если они имеются
if os.path.exists("saves.txt"):
    start_x, start_y, music, sounds, adult_content = load_game()
    saves = True
else:
    saves = False
    start_x, start_y = json.loads(config.get("MAIN", "start_pos"))
    music = config.getboolean("MAIN", "music")
    sounds = config.getboolean("MAIN", "sounds")
    adult_content = config.getboolean("MAIN", "adult_content")

title_font = pygame.font.Font("data/fonts/pixel_font.ttf", 120)
pause_font = pygame.font.Font("data/fonts/pixel_font.ttf", 80)
font = pygame.font.Font("data/fonts/pixel_font.ttf", 50)

bg = load_image("data/images/bg.jpg", width, height)

# Загружаем музыку
load_music("data/sounds/main_theme.mp3")

if music:
    start_music()
else:
    start_music()
    pause_music()


def menu_setup(background, title):
    screen.fill(pygame.Color("black"))
    screen.blit(background, (0, 0))
    background = screen.copy()

    render_text(title, pause_font, pygame.Color(
        "#c2c1bf"), screen, width // 2, height * 0.2)
    pygame.display.flip()

    return background

# Прорисовка главного меню
def main_menu():
    pygame.mouse.set_visible(True)
    click = False

    # Инициализация кнопок меню
    button_start = Button(screen, 500, 300, 280, 65, "Start Game", font)
    button_options = Button(screen, 500, 430, 280, 65, "Options", font)
    button_exit = Button(screen, 500, 560, 280, 65, "Exit", font)

    while True:
        # Ставим картинку на задний фон
        screen.fill(pygame.Color("black"))
        screen.blit(bg, (0, 0))

        # Координаты курсора
        x, y = pygame.mouse.get_pos()

        # Отрисовка кнопок
        button_start.update((x, y))
        button_options.update((x, y))
        button_exit.update((x, y))

        # Отрисовка текста
        render_text("Game Title", title_font, pygame.Color(
            "#c2c1bf"), screen, width // 2, height // 4)

        # Проверяем нажатие на кнопки
        if button_start.collide((x, y)) and click:
            game()

        if button_options.collide((x, y)) and click:
            options()

        if button_exit.collide((x, y)) and click:
            # При выходе из игры сохраняемся
            save_game(hero, music, sounds, adult_content)
            quit_game()

        click = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.flip()

# Проработка меню паузы
def pause_menu():
    global saves

    # Затенение фона
    background = pygame.Surface((width, height), pygame.SRCALPHA, 32)
    background.fill((96, 0, 159, 50))
    background = menu_setup(background, "Pause")

    button_continue = Button(screen, 500, 300, 280, 65, "Continue", font)
    button_options = Button(screen, 500, 430, 280, 65, "Options", font)
    button_exit = Button(screen, 500, 560, 280, 65, "Main Menu", font)

    pygame.mouse.set_visible(True)

    hero.state = IdleState()  # Останавлиаем персонажа

    pause = True
    click = False

    while pause:
        x, y = pygame.mouse.get_pos()

        button_continue.update((x, y))
        button_options.update((x, y))
        button_exit.update((x, y))

        # Проверяем нажатие на кнопки
        if button_continue.collide((x, y)) and click:
            pause = False

        if button_options.collide((x, y)) and click:
            options()
            menu_setup(background, "Pause")

        if button_exit.collide((x, y)) and click:
            # Сохраняемся при выходе из игры
            saves = True
            save_game(hero, music, sounds, adult_content)
            main_menu()

        click = False
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.flip()

# Прорисовка меню настроек
def options():
    global music, sounds, adult_content

    # Затемнение фона
    background = pygame.Surface((width, height), pygame.SRCALPHA, 32)
    background.fill((96, 0, 159, 50))
    background = menu_setup(background, "Options")

    checkbox_music = Checkbox(screen, width * 0.6, height * 0.4, checked=music)
    checkbox_sounds = Checkbox(
        screen, width * 0.6, height * 0.6, checked=sounds)
    checkbox_adult = Checkbox(
        screen, width * 0.6, height * 0.8, checked=adult_content)

    button_back = Button(screen, 20, 20, 75, 50, "<-", font)

    running = True
    click = False

    while running:
        x, y = pygame.mouse.get_pos()

        # Отрисовка обьектов
        checkbox_music.update()
        checkbox_sounds.update()
        checkbox_adult.update()
        button_back.update((x, y))

        # Отрисовка текста
        render_text("Music", font, pygame.Color("#c2c1bf"),
                    screen, width // 3, height * 0.425)
        render_text("Sounds", font, pygame.Color("#c2c1bf"),
                    screen, width // 3, height * 0.625)
        render_text("Adult Content", font, pygame.Color(
            "#c2c1bf"), screen, width // 3, height * 0.825)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

            checkbox_music.onCheckbox(event)
            checkbox_sounds.onCheckbox(event)
            checkbox_adult.onCheckbox(event)

        if button_back.collide((x, y)) and click:
            running = False

        if not music:
            pause_music()
        else:
            unpause_music()

        # Отключаем музыку
        if not checkbox_music.checked:
            music = False
        else:
            music = True

        # Отключаем звуки
        if not checkbox_sounds.checked:
            sounds = False
        else:
            sounds = True

        if not checkbox_adult.checked:
            adult_content = False
        else:
            adult_content = True

        pygame.display.flip()

# Прорисовка окна с обучением
def training():
    background = pygame.Surface((width, height), pygame.SRCALPHA, 32)
    background.fill((96, 0, 159, 50))
    background = menu_setup(background, "Training")

    button_start = Button(screen, 500, height * 0.8, 280, 65, "Start", font)

    running = True
    click = False

    # Отрисовка текста обучения
    text_coords = height * 0.3
    training_text = ["Movement: LEFT and RIGHT",
                     "Jump: Space",
                     "Dash: Left Shift",
                     "Extra Abilities:",
                     "  Double Jump: Space(when in air)",
                     "  Wall Jump: Space(when on wall)"
                     ]

    for line in training_text:
        render_text(line, font, pygame.Color("#c2c1bf"), screen, width * 0.15, text_coords, align="left")
        text_coords += 50

    while running:
        x, y = pygame.mouse.get_pos()

        # Отрисовка обьектов
        button_start.update((x, y))

        click = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        if button_start.collide((x, y)) and click:
            running = False

        pygame.display.flip()


# Прорисовка карты уровня
level = [
    "###########################",
    "#                  #      #",
    "#                  #      #",
    "#           #      #      #",
    "#                  #      #",
    "#                  #      #",
    "#       <<<<<      #      #",
    "#                  #      #",
    "#                  #      #",
    "#                  #      #",
    "#        >>>       #      #",
    "#                  #      #",
    "#                         #",
    "#                         #",
    "___________________________"]


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

            x += pf.width
        y += pf.height
        x = 0


platform_sprites = pygame.sprite.Group()
platforms = []  # объекты, с которыми будет происходить взаимодействие

hero_sprites = pygame.sprite.Group()
hero = Hero((start_x, start_y), hero_sprites)
render(level)


def game():
    global saves
    clock = pygame.time.Clock()
    fps = 60
    dt = 0
    running = True

    # Вызываем экран с обучением
    if not saves:
        training()

    pygame.mouse.set_visible(False)

    while running:
        screen.fill(pygame.Color("black"))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_menu()

            hero.handle_event(event)

        platform_sprites.update()
        platform_sprites.draw(screen)

        hero_sprites.update(dt, platforms)
        hero_sprites.draw(screen)

        dt = clock.tick(fps) / 1000
        pygame.display.flip()


if __name__ == "__main__":
    main_menu()
