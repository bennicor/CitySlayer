import pygame


class Button:
    def __init__(self, screen, x, y, width, height, main_col="#0a2a59", outline_col="#082145", border_size=10):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.main_col = main_col
        self.outline_col = outline_col
        self.border_size = border_size

        self.button = pygame.Rect(self.x, self.y, self.width, self.height)
        
    def update(self):
        pygame.draw.rect(self.screen, pygame.Color(self.main_col), self.button)
        pygame.draw.rect(self.screen, pygame.Color(self.outline_col), self.button, self.border_size)

    # Проверяется нажатие на кнопку
    def collide(self, *pos):
        if self.button.collidepoint(pos):
            return True

    def hover(self):
        pass
