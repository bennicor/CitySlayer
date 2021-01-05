import pygame

WIDTH = HEIGHT = 48

class Camera(object):
    def __init__(self):
        self.true_scroll = self.scroll = [0, 0]

    def apply(self, target):
        target.rect.x -= self.scroll[0] / 30
        target.rect.y -= self.scroll[1] / 30


    def update(self, target):
        self.true_scroll[0] += (target.rect.x - self.true_scroll[0] - 682 ) / 2
        self.true_scroll[1] += (target.rect.y - self.true_scroll[1] - 408) / 2
        self.scroll = self.true_scroll.copy()
        self.scroll[0] = int(self.scroll[0])
        self.scroll[1] = int(self.scroll[1])
 #