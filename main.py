import pygame


pygame.init()
size = WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode(size)


# Класс персонажа
class Hero:
    def __init__(self):
        self.vel = 3 # Скорость персонажа
        self.width = 50
        self.height = 50
        self.x = WIDTH // 2
        self.y = HEIGHT - self.height
        self.isJump = False # Проверка на прыжок
        self.jumpCount = 10 # Параметр квадратичной функции для расчета траектории прыжка
    
    def draw(self):
        pygame.draw.rect(screen, pygame.Color("green"), (
                self.x, self.y, self.width, self.height
            ))

    def movement(self):
        state = pygame.key.get_pressed()

        # Перемещение
        if state[pygame.K_LEFT] and self.x > 0:
            self.x -= self.vel
        elif state[pygame.K_RIGHT] and self.x < WIDTH - self.width:
            self.x += self.vel

        # Прыжок
        if not(self.isJump): 
            if state[pygame.K_SPACE]:
                self.isJump = True
        else:
            if self.jumpCount >= -10:
                self.y -= (self.jumpCount * abs(self.jumpCount)) * 0.2
                self.jumpCount -= 1
            else: 
                self.jumpCount = 10
                self.isJump = False


clock = pygame.time.Clock()
fps = 60
hero = Hero()
running = True

while running:
    screen.fill(pygame.Color("black"))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    hero.draw()
    hero.movement()

    clock.tick(fps)
    pygame.display.flip()
pygame.quit()
