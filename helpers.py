import pygame
import sys
import pickle
import os


def load_image(name, width, height, color_keys=None):
    full_name = os.path.join(name)

    try:
        image = pygame.image.load(full_name)
        image = pygame.transform.scale(image, (width, height))
    except pygame.error as message:
        print('не удалось загрузить', name)
        raise SystemExit(message)
    return image

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

def save_game(hero, music, sounds, adult_content):
    saves = [hero.rect.x, hero.rect.y, music, sounds, adult_content]

    with open("saves.txt", "wb") as f:
        pickle.dump(saves, f)

def load_game():
    with open("saves.txt", "rb") as f:
        saves = pickle.load(f)

    return saves

pygame.mixer.init()
def load_music(file):
    pygame.mixer.music.load(file)
    pygame.mixer.music.set_volume(0.2)

def start_music():
    pygame.mixer.music.play(loops=-1)

def unpause_music():
    pygame.mixer.music.unpause()

def pause_music():
    pygame.mixer.music.pause()
