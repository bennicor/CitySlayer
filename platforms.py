import pygame
from random import randrange
import os
import configparser
from helpers import load_image


config = configparser.ConfigParser()
config.read("settings.ini")

width = config.getint('PLATFORM', 'height')
height = config.getint('PLATFORM', 'height')


floor = [load_image('data/sprite_down/sprite_down_1.png', width, height),
         load_image('data/sprite_down/sprite_down_2.png', width, height),
         load_image('data/sprite_down/sprite_down_3.png', width, height),
         load_image('data/sprite_down/sprite_down_4.png', width, height)]


# Пол
class FloorPlatform(pygame.sprite.Sprite):
    def __init__(self, x, y, group):
        super().__init__(group)
        self.width = width
        self.height = height
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
