import pygame

def render_text(text, font, color, surface, x, y):
    text = font.render(text, 1, color)
    text_rect = text.get_rect()
    text_rect.center = (x, y)
    surface.blit(text, text_rect)

def draw_button(screen, color1, color2, button, border):
    pygame.draw.rect(screen, pygame.Color(color1), button)
    pygame.draw.rect(screen, pygame.Color(color2), button, border)

def draw_checkbox():
    pass