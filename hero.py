import pygame

WIDTH, HEIGHT = 1280, 720
HERO_SPEED = 8
GRAVITY = 2.5


# Класс персонажа
class Hero(pygame.sprite.Sprite):
    def __init__(self, x, y, group):
        super().__init__(group)
        self.xvel = self.yvel = 0 # Векторы скоростей
        self.width = 30
        self.height = 30
        self.x = x
        self.y = y

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(pygame.Color("green"))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.jumpCount = 30 # Параметр квадратичной функции для расчета траектории прыжка
        self.onGround = False
        self.left = self.right = self.up = False

    def update(self, platforms):
        # Перемещение по горизонтали
        if self.left:
            self.xvel = -HERO_SPEED
        elif self.right:
            self.xvel = HERO_SPEED

        if not(self.right or self.left):
            self.xvel = 0

        # Прыжок
        if self.up:
            if self.onGround:
                self.yvel = -self.jumpCount
                self.onGround = False

        self.gravitation(platforms)

    def collide(self, xvel, yvel, platforms):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits: # если есть пересечение платформы с игроком
            if yvel > 0:
                self.rect.bottom = hits[0].rect.top
                self.onGround = True
                self.yvel = 0
            
            if yvel < 0:
                self.rect.top = hits[0].rect.bottom
                self.yvel = 0
            
            if xvel > 0:
                self.rect.right = hits[0].rect.left
                self.xvel = 0

            if xvel < 0:
                self.rect.left = hits[0].rect.right
                self.xvel = 0

    def gravitation(self, platforms):
        # Реализация силы притяжения
        if self.yvel <= 12.5:  
            self.yvel += GRAVITY
        
        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms)

        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)
        print(self.yvel)
