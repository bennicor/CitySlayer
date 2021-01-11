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
fall_timer = config.getfloat("PLATFORM", "fall_timer")

floor = [load_image('data/sprite_down/sprite_down_1_dop.png', width, height),
         load_image('data/sprite_down/sprite_down_2_dop.png', width, height),
         load_image('data/sprite_down/sprite_down_3_dop.png', width, height),
         load_image('data/sprite_down/sprite_down_4_dop.png', width, height)]

wall = load_image('data/sprite_wall/sprite_wall_dop2.png', width, height)
moving_platform = load_image('data/MovingPlatform/spriteMovingPlatform.png', width, height)
death_platform = load_image('data/dead_sprite/sprite_DeadlyPlatform.png', width, height)

falling_platform = [load_image('data/falling_platform/sprite_falling_platform.png', width, height),
                load_image('data/falling_platform/sprite_falling_platform2.png', width, height),
                load_image('data/falling_platform/sprite_falling_platform3.png', width, height)]


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, group):
        super().__init__(group)
        self.group = group
        self.width = width
        self.height = height
        self.can_wall_jump = False
        self.vel_y = self.vel_x = 0

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(pygame.Color("#1E1124"))
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def update(self, dt):
        pass


# Пол
class FloorPlatform(Platform):
    def __init__(self, x, y, group):
        super().__init__(x, y, group)
        self.width = width
        self.height = height
        self.can_wall_jump = False
        self.vel_y = self.vel_x = 0

        self.image = floor[randrange(3)]
        self.rect = pygame.Rect(x, y, self.width, self.height)


class EndPlatform(FloorPlatform):
    def __init__(self, x, y, group):
        super().__init__(x, y, group)

# Стена
class WallPlatform(Platform):
    def __init__(self, x, y, group):
        super().__init__(x, y, group)
        self.width = width
        self.height = height
        self.can_wall_jump = True

        self.image = wall
        self.rect = pygame.Rect(x, y, self.width, self.height)

# Двигающаяся платформа
class MovingPlatform(Platform):
    def __init__(self, x, y, group, dir):
        super().__init__(x, y, group)
        self.color = pygame.Color("red")

        self.counter = 0
        self.vel_x = 2 if dir == ">" else -2

        self.image = moving_platform
        self.rect = pygame.Rect(x, y, self.width, self.height)

    # Перемещение платформы на заданном промежутке
    def update(self, dt):
        if abs(self.counter) >= 200:
            self.vel_x = -self.vel_x

        self.rect = self.rect.move(self.vel_x, 0)
        self.counter += self.vel_x

# Падающая платформа
class FallingPlatform(Platform):
    def __init__(self, x, y, group):
        super().__init__(x, y, group)
        self.gravity = gravity
        self.falling = False
        self.fall_timer = fall_timer

        self.image = falling_platform[randrange(3)]
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def remove(self):
        self.group.remove(self)

    def update(self, dt):
        if self.falling:
            self.fall_timer -= dt

            if self.fall_timer <= 0:
                if self.vel_y <= 12.5:
                    self.vel_y += self.gravity

                self.rect = self.rect.move(0, self.vel_y)

        if self.rect.y >= 2500:
            self.remove()

# Смертельная платформа
class DeadlyPlatform(Platform):
    def __init__(self, x, y, group):
        super().__init__(x, y, group)

        self.image = death_platform
        self.rect = pygame.Rect(x, y, self.width, self.height)
