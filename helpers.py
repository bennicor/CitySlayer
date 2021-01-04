import pygame
import sys
import pickle
import os
from platforms import *
from enemies import *


# Инициализация групп
platform_sprites = pygame.sprite.Group()
platforms = []  # объекты, с которыми будет происходить взаимодействие

enemies_sprites = pygame.sprite.Group()
enemies = []


def load_image(name, width, height, color_keys=None):
    full_name = os.path.join(name)

    try:
        image = pygame.image.load(full_name)
        image = pygame.transform.scale(image, (width, height))
    except pygame.error as message:
        print('не удалось загрузить', name)
        raise SystemExit(message)
    return image

def load_level(filename):
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, ' '), level_map))

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
            elif col == "!":
                en = SlowWalkEnemy(x, y, enemies_sprites)
                enemies.append(en)
            elif col == "?":
                en = FastWalkEnemy(x, y, enemies_sprites)
                enemies.append(en)
            elif col == "1":
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

def render_text(text, font, color, surface, x, y, align="center"):
    text = font.render(text, 1, color)
    text_rect = text.get_rect()

    if align == "center":
        text_rect.center = (x, y)
    elif align == "left":
        text_rect = (x, y)
        
    surface.blit(text, text_rect)

def quit_game():
    pygame.quit()
    sys.exit()

def restart():
    pass

def save_game(hero, music, sounds, adult_content):
    saves = [hero.rect.x, hero.rect.y, music, sounds, adult_content]

    with open("saves.txt", "wb") as f:
        pickle.dump(saves, f)

def load_game():
    with open("saves.txt", "rb") as f:
        saves = pickle.load(f)

    return saves

pygame.mixer.init(buffer=2048)
def load_music(file):
    pygame.mixer.music.load(file)
    pygame.mixer.music.set_volume(0.05)

def start_music():
    pygame.mixer.music.play(loops=-1)

def unpause_music():
    pygame.mixer.music.unpause()

def pause_music():
    pygame.mixer.music.pause()

def load_sound(file):
    return pygame.mixer.Sound(file)

def play_sound(sound):
    pygame.mixer.stop()
    pygame.mixer.Sound.play(sound)

def get_length(sound):
    return pygame.mixer.Sound.get_length(sound)

def stop_sound():
    pygame.mixer.stop()
