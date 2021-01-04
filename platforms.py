import pygame
from pygame.math import Vector2
from random import randrange
import os

WIDTH = HEIGHT = 48

# загрузка изображения
def load_image(name, color_keys=None):
    full_name = os.path.join(name)

    try:
        image = pygame.image.load(full_name)
        image = pygame.transform.scale(image, (WIDTH, HEIGHT))
    except pygame.error as message:
        print('не удалось загрузить', name)
        raise SystemExit(message)
    return image

floor = [load_image('sprite_down/sprite_down_1.png'),
         load_image('sprite_down/sprite_down_2.png'),
         load_image('sprite_down/sprite_down_3.png'),
         load_image('sprite_down/sprite_down_4.png')]


# Пол
class FloorPlatform(pygame.sprite.Sprite):
    def __init__(self, x, y, group):
        super().__init__(group)
        self.width = WIDTH
        self.height = HEIGHT
        self.can_wall_jump = False

        self.image = floor[randrange(3)]
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def update(self):
        pass


# Стена
class WallPlatform(FloorPlatform):
    def __init__(self, x, y, group):
        super().__init__(x, y, group)
        self.color = pygame.Color("yellow")
        self.can_wall_jump = True

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = pygame.Rect(x, y, self.width, self.height)


# Двигающаяся платформа
class MovingPlatform(FloorPlatform):
    def __init__(self, x, y, group, dir):
        super().__init__(x, y, group)
        self.color = pygame.Color("red")

        self.counter = 0
        self.x = 2 if dir == ">" else -2

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = pygame.Rect(x, y, self.width, self.height)

    # Перемещение платформы на заданном промежутке
    def update(self):
        if abs(self.counter) >= 200:
            self.x = -self.x

        self.rect = self.rect.move(self.x, 0)
        self.counter += self.x


class FallingPlatform(FloorPlatform):
    def __init__(self, x, y, group):
        super().__init__(x, y, group)

        self.vel = Vector2(0, 0)
        self.gravity = 1.5
        self.falling = False

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(pygame.Color("red"))
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def update(self):
        if self.falling:
            if self.vel.y <= 12.5:
                self.vel.y += self.gravity

            self.rect = self.rect.move(self.vel.x, self.vel.y)

class DeadlyPlatform(FloorPlatform):
    def __init__(self, x, y, group):
        super().__init__(x, y, group)

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(pygame.Color('#838B8B'))
        self.rect = pygame.Rect(x, y, self.width, self.height)

class ShimmeringPlatform(FloorPlatform):
    def __init__(self, x, y, group):
        super().__init__(x, y, group)



