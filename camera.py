import pygame
import configparser
import json

config = configparser.ConfigParser()
config.read("setting.ini")

width, height = json.loads(config.get("MAIN", "res"))
h_width, h_height = json.loads(config.get("PLAYER", "size"))
speed = config.getint("CAMERA", "speed")


class Camera(object):
    def __init__(self):
        self.true_scroll = self.scroll = [0, 0]
        self.speed = speed
        self.x_offset = width // 2 + h_width
        self.y_offset = height // 2 + h_height

    def apply(self, target):
        target.rect.x -= self.scroll[0] // self.speed
        target.rect.y -= self.scroll[1] // self.speed

    def update(self, target):
        self.true_scroll[0] += (target.rect.x - self.true_scroll[0] - self.x_offset) / 2
        self.true_scroll[1] += (target.rect.y - self.true_scroll[1] - self.y_offset) / 2
        self.scroll = self.true_scroll.copy()
        self.scroll[0] = int(self.scroll[0])
        self.scroll[1] = int(self.scroll[1])
