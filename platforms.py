import pygame
from random import randint
import os

# загрузка изображения
def load_image(name, color_keys=None):
    print(name)
    full_name = os.path.join(name)
    try:
        image = pygame.image.load(full_name)
    except pygame.error as message:
        print('не удалось загрузить', name)
        raise SystemExit(message)
    return image


WIDTH, HEIGHT = 32, 32
floor = [load_image('sprite_down/sprite_duwn_1.png'),
         load_image('sprite_down/sprite_duwn_2.png'),
         load_image('sprite_down/sprite_duwn_3.png'),
         load_image('sprite_down/sprite_duwn_4.png')]

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, group):
        super().__init__(group)
        self.width = WIDTH
        self.height = HEIGHT
        self.color = "#FF6262"
        self.can_wall_jump = False

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(pygame.Color(self.color))
        self.rect = pygame.Rect(x, y, self.width, self.height)

# пол
class Fllower_Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, group):
        super().__init__(group)
        self.width = WIDTH
        self.height = HEIGHT

        self.image = floor[randint(0, 3)]
        self.rect = pygame.Rect(x, y, self.width, self.height)


class WallPlatform(pygame.sprite.Sprite):
    def __init__(self, x, y, group):
        super().__init__(group)
        self.width = WIDTH
        self.height = HEIGHT
        self.color = "#EF4213"
        self.can_wall_jump = True

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(pygame.Color(self.color))
        self.rect = pygame.Rect(x, y, self.width, self.height)
