import pygame

WIDTH, HEIGHT = 52, 35

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
