import pygame
import sys
import pickle


def render_text(text, font, color, surface, x, y):
    text = font.render(text, 1, color)
    text_rect = text.get_rect()
    text_rect.center = (x, y)
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