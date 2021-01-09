import pygame
import os
import configparser
import json
import time
from hero import Hero
from camera import Camera
from playerStates import IdleState
from helpers import *
from platforms import *
from enemies import *
from gui_elements.checkbox import Checkbox
from gui_elements.buttons import Button


pygame.init()

# Импорт настроек
config = configparser.ConfigParser()
config.read("settings.ini")

width, height = json.loads(config.get("MAIN", "res"))
fps = config.getint("MAIN", "fps")
start_x, start_y = json.loads(config.get("MAIN", "start_pos"))
death = config.getint("PLAYER", "death")
death_sound = load_sound("data/sounds/death.wav")
death_sound.set_volume(0.3)

size = width, height
screen = pygame.display.set_mode(size)

# Загружаем сохраненные данные, если они имеются
if os.path.exists("saves.txt"):
    music, sounds, adult_content = load_game()
    saves = True
else:
    music = config.getboolean("MAIN", "music")
    sounds = config.getboolean("MAIN", "sounds")
    adult_content = config.getboolean("MAIN", "adult_content")
    saves = False

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

    render_text(title, pause_font, pygame.Color("#c2c1bf"), screen, width // 2, height * 0.2)
    pygame.display.flip()

    return background

# Прорисовка главного меню
def main_menu():
    pygame.mouse.set_visible(True)
    click = False

    # Инициализация кнопок меню
    if not saves:
        button_start = Button(screen, 500, 300, 280, 65, "Start Game", font)
    else:
        button_start = Button(screen, 500, 300, 280, 65, "Continue", font)
    button_options = Button(screen, 500, 430, 280, 65, "Options", font)
    button_exit = Button(screen, 500, 560, 280, 65, "Exit", font)

    while True:
        # Ставим картинку на задний фон
        screen.fill(pygame.Color("black"))
        screen.blit(bg, (0, 0))

        # Отрисовка текста
        render_text("City Slayer", title_font, pygame.Color("#c2c1bf"), screen, width // 2, height // 4)

        # Координаты курсора
        x, y = pygame.mouse.get_pos()

        # Отрисовка кнопок
        button_start.update((x, y))
        button_options.update((x, y))
        button_exit.update((x, y))

        # Проверяем нажатие на кнопки
        if button_start.collide((x, y)) and click:
            game()

        if button_options.collide((x, y)) and click:
            options()

        if button_exit.collide((x, y)) and click:
            # При выходе из игры сохраняемся
            save_game(music, sounds, adult_content)
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

    stop_sound()
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
            save_game(music, sounds, adult_content)
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

    # Отрисовка текста
    render_text("Music", font, pygame.Color("#c2c1bf"), screen, width // 3, height * 0.425)
    render_text("Sounds", font, pygame.Color("#c2c1bf"), screen, width // 3, height * 0.625)
    render_text("Adult Content", font, pygame.Color("#c2c1bf"), screen, width // 3, height * 0.825)

    checkbox_music = Checkbox(screen, width * 0.6, height * 0.4, checked=music)
    checkbox_sounds = Checkbox(screen, width * 0.6, height * 0.6, checked=sounds)
    checkbox_adult = Checkbox(screen, width * 0.6, height * 0.8, checked=adult_content)

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

        # Отключаем музыку
        if not music:
            pause_music()
        else:
            unpause_music()

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
def tutorial():
    background = pygame.Surface((width, height), pygame.SRCALPHA, 32)
    background.fill((96, 0, 159, 50))
    background = menu_setup(background, "Tutorial")

    button_start = Button(screen, 500, height * 0.8, 280, 65, "Start", font)

    running = True
    click = False

    # Отрисовка текста обучения
    text_coords = height * 0.3
    tutorial_text = ["Movement: LEFT and RIGHT",
                     "Jump: Space",
                     "Dash: Left Shift",
                     "Extra Abilities:",
                     "  Double Jump: Space(when in air)",
                     "  Wall Jump: Space(when on wall)"
                     ]

    for line in tutorial_text:
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

def end_screen():
    pygame.mouse.set_visible(True)
    background = pygame.Surface((width, height), pygame.SRCALPHA, 32)
    background.fill((96, 0, 159, 50))
    background = menu_setup(background, "The End")

    button_end = Button(screen, 500, height * 0.8, 280, 65, "Exit", font)

    running = True
    click = False

    # Отрисовка текста
    text_coords = height * 0.35
    tutorial_text = ["Game Created By",
                     "",
                     "Vlad Boldyrev",
                     "Vladimir Sviridkin",
                    ]

    for line in tutorial_text:
        render_text(line, font, pygame.Color("#c2c1bf"), screen, width * 0.5, text_coords)
        text_coords += 50

    while running:
        x, y = pygame.mouse.get_pos()

        # Отрисовка обьектов
        button_end.update((x, y))

        click = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        if button_end.collide((x, y)) and click:
            if saves:
                os.remove("saves.txt")
            quit_game()

        pygame.display.flip()

def death_screen():
    pygame.mouse.set_visible(False)
    background = pygame.Surface((width, height), pygame.SRCALPHA, 32)
    background.fill((96, 0, 159, 50))
    background = menu_setup(background, "")

    render_text("Loading", font, pygame.Color("#c2c1bf"), screen, width * 0.8, height * 0.8, align="left")
    running = True

    while running:
        pygame.display.flip()
        time.sleep(2)
        running = False

def respawn():
    hero.rect.x = start_x
    hero.rect.y = start_y

def restart():
    global saves

    pause_music()
    if sounds:
        play_sound(death_sound)

    time.sleep(death)
    death_screen()
    saves = True
    hero.state = IdleState()
    hero.dead = False
    respawn()

    if music:
        unpause_music()

    game()

def render(level, platforms, platform_sprites, enemies, enemies_sprites):
    x = y = 0
    for row in level:
        for col in row:
            if col == "_":
                pf = FloorPlatform(x, y, platform_sprites)
                platforms.append(pf)
            elif col == "-" or col == "|":
                pf = WallPlatform(x, y, platform_sprites)
                platforms.append(pf)
            elif col == ">":
                pf = MovingPlatform(x, y, platform_sprites, ">")
                platforms.append(pf)
            elif col == "<":
                pf = MovingPlatform(x, y, platform_sprites, "<")
                platforms.append(pf)
            elif col == "S":
                en = SlowWalkEnemy(x, y, enemies_sprites)
                enemies.append(en)
            elif col == "F":
                en = FastWalkEnemy(x, y, enemies_sprites)
                enemies.append(en)
            elif col == "J":
                en = JumpEnemy(x, y, enemies_sprites)
                enemies.append(en)
            elif col == "=":
                pf = FallingPlatform(x, y, platform_sprites)
                platforms.append(pf)
            elif col == "^":
                pf = DeadlyPlatform(x, y, platform_sprites)
                platforms.append(pf)
    
            x += pf.width
        y += pf.height
        x = 0

hero_sprites = pygame.sprite.Group()
hero = Hero((start_x, start_y), hero_sprites)

def game():
    global saves, sounds

    camera = Camera()
    clock = pygame.time.Clock()
    dt = 0
    running = True

    # Инициализация групп
    platform_sprites = pygame.sprite.Group()
    platforms = []  # объекты, с которыми будет происходить взаимодействие

    enemies_sprites = pygame.sprite.Group()
    enemies = []

    # Перемещение героя
    respawn()

    # Выводим на экран все обьекты на уровня
    render(load_level("level.txt"), platforms, platform_sprites, enemies, enemies_sprites)

    # Вызываем экран с обучением
    if not saves:
        tutorial()

    while running:
        pygame.mouse.set_visible(False)
        # Отключаем звуки
        if not sounds:
            hero.sounds = False
        else:
            hero.sounds = True

        screen.blit(load_image('data/fonts/city.png', 1280, 720), (0, 0))
        # screen.fill(pygame.Color("#C990BD"))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_menu()

            hero.handle_event(event)

        camera.update(hero)
        camera.apply(hero)

        for sprite in platform_sprites:
            camera.apply(sprite)

        # for sprite in enemies_sprites:
        #     camera.apply(sprite)

        platform_sprites.update()
        platform_sprites.draw(screen)

        enemies_sprites.update(dt, platforms, hero_sprites, hero)
        enemies_sprites.draw(screen)

        hero_sprites.update(dt, platforms, camera)
        hero_sprites.draw(screen)

        if hero.dead:
            restart()

        if hero.end:
            end_screen()

        dt = clock.tick(fps) / 1000
        pygame.display.flip()

if __name__ == "__main__":
    main_menu()
