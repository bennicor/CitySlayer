import pygame


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, group):
        super().__init__(group)
        self.width = 52
        self.height = 35
        self.color = "#FF6262"

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(pygame.Color(self.color))
        self.rect = pygame.Rect(x, y, self.width, self.height)
