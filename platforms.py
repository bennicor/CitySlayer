import pygame
from pygame.math import Vector2
from random import randrange
import os
import configparser
from helpers import load_image


config = configparser.ConfigParser()
config.read("settings.ini")

width = config.getint('PLATFORM', 'height')
height = config.getint('PLATFORM', 'height')
gravity = config.getfloat('PLATFORM', 'gravity')

floor = [load_image('data/sprite_down/sprite_down_1_dop.png', width, height),
         load_image('data/sprite_down/sprite_down_2_dop.png', width, height),
         load_image('data/sprite_down/sprite_down_3_dop.png', width, height),
         load_image('data/sprite_down/sprite_down_4_dop.png', width, height)]
wall = load_image('data/sprite_wall/sprite_wall_dop2.png', width, height)
Falling_wall = [load_image('data/Falling_Wall/sprite_Falling_wall.png', width, height),
                load_image('data/Falling_Wall/sprite_Falling_wall2.png', width, height),
                load_image('data/Falling_Wall/sprite_Falling_wall3.png', width, height)]


# Пол
class FloorPlatform(pygame.sprite.Sprite):
    def __init__(self, x, y, group):
        super().__init__(group)
        self.width = width
        self.height = height
        self.can_wall_jump = False
        self.vel_y = self.vel_x = 0

        self.image = floor[randrange(3)]
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def update(self):
        pass

# Стена
class WallPlatform(FloorPlatform):
    def __init__(self, x, y, group):
        super().__init__(x, y, group)
        self.width = width
        self.height = height
        self.can_wall_jump = True

        self.image = wall
        self.rect = pygame.Rect(x, y, self.width, self.height)

# Двигающаяся платформа
class MovingPlatform(FloorPlatform):
    def __init__(self, x, y, group, dir):
        super().__init__(x, y, group)
        self.color = pygame.Color("red")

        self.counter = 0
        self.vel_x = 2 if dir == ">" else -2

        self.image = load_image('data/MovingPlatform/spriteMovingPlatform.png', self.width, self.height)
        self.rect = pygame.Rect(x, y, self.width, self.height)

    # Перемещение платформы на заданном промежутке
    def update(self):
        if abs(self.counter) >= 200:
            self.vel_x = -self.vel_x

        self.rect = self.rect.move(self.vel_x, 0)
        self.counter += self.vel_x

# Падающая платформа
class FallingPlatform(FloorPlatform):
    def __init__(self, x, y, group):
        super().__init__(x, y, group)

        self.gravity = gravity
        self.falling = False

        self.image = Falling_wall[randrange(3)]
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def update(self):
        if self.falling:
            if self.vel_y <= 12.5:
                self.vel_y += self.gravity

            self.rect = self.rect.move(0, self.vel_y)

# Смертельная платформа
class DeadlyPlatform(FloorPlatform):
    def __init__(self, x, y, group):
        super().__init__(x, y, group)

        self.image = load_image('data/dead_sprite/sprite_DeadlyPlatform.png', self.width, self.height)
        self.rect = pygame.Rect(x, y, self.width, self.height)
