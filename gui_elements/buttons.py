import pygame


class Button:
    def __init__(self, screen, x, y, width, height, text, font, 
                main_col="#0a2a59", outline_col="#082145", m_hover_col="#123C79", out_hover_col="#0B2C5C", font_col="#c2c1bf", border_size=10):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = font
        self.font_col = font_col
        self.main_col = main_col
        self.outline_col = outline_col
        self.m_hover_col = m_hover_col
        self.out_hover_col = out_hover_col
        self.border_size = border_size

        self.button = pygame.Rect(self.x, self.y, self.width, self.height)
        
    def update(self, *pos):
        # Если курсор пользователя находится на кнопке, осветляем ее
        if self.button.collidepoint(pos):
            pygame.draw.rect(self.screen, pygame.Color(self.m_hover_col), self.button)
            pygame.draw.rect(self.screen, pygame.Color(self.out_hover_col), self.button, self.border_size)
        else:
            pygame.draw.rect(self.screen, pygame.Color(self.main_col), self.button)
            pygame.draw.rect(self.screen, pygame.Color(self.outline_col), self.button, self.border_size)
        
        self.render_text()

    # Проверяется нажатие на кнопку
    def collide(self, *pos):
        if self.button.collidepoint(pos):
            return True

    def render_text(self):
        text = self.font.render(self.text, 1, pygame.Color(self.font_col))
        text_rect = text.get_rect()
        text_rect.center = (self.x + self.width * 0.5, self.y + self.height * 0.5)
        self.screen.blit(text, text_rect)
