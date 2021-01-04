import pygame

WIDTH = HEIGHT = 48



class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


    # def update(self, target):
    #     self.dx = (target.rect.x + target.rect.w // 40 - WIDTH // 40)
    #     self.dy = (target.rect.y + target.rect.h // 40 - HEIGHT // 40)