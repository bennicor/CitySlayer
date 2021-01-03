import pygame
import configparser


config = configparser.ConfigParser()
config.read("settings.ini")

width = config.getint("ENEMY", "width")
height = config.getint("ENEMY", "height")


class BaseEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y, group):
        super().__init__(group)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
