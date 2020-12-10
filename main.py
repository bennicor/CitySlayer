import pygame


pygame.init()
size = WIDTH, HEIGHT = 1280, 720
HERO_SPEED = 10 # Скорость персонажа
GRAVITY = 3.5 # Сила гравитации
PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"
screen = pygame.display.set_mode(size)
level = [
       "-------------------------",
       "-                       -",
       "-                       -",
       "-                       -",
       "-            --         -",
       "-                       -",
       "--                      -",
       "-                       -",
       "-                   --- -",
       "-                       -",
       "-                       -",
       "-      ---              -",
       "-                       -",
       "-   -----------        -",
       "-                       -",
       "-                -      -",
       "-                   --  -",
       "-                       -",
       "-                       -",
       "-------------------------"]

def render(level):
    x=y=0 # координаты

    for row in level: # вся строка
        for col in row: # каждый символ
            if col == "-":
                #создаем блок, заливаем его цветом и рисеум его
                pygame.draw.rect(screen, pygame.Color("green"), (
                        x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT
                    ))
                    
            x += PLATFORM_WIDTH #блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT    #то же самое и с высотой
        x = 0                   #на каждой новой строчке начинаем с нуля


class Platform:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)



# Класс персонажа
class Hero:
    def __init__(self):
        self.xvel = 0 # Векторная скорость персонажа
        self.yvel = 0
        self.width = 50
        self.height = 80
        self.x = WIDTH // 2
        self.y = HEIGHT - self.height
        self.jumpCount = 10 # Параметр квадратичной функции для расчета траектории прыжка
        self.onGround = False
        self.left = self.right = self.up = False

    def draw(self):
        pygame.draw.rect(screen, pygame.Color("green"), (
                self.x, self.y, self.width, self.height
            ))

    def movement(self):
        # Перемещение по горизонтали
        if self.left:
            self.xvel = -HERO_SPEED
        
        if self.right:
            self.xvel = HERO_SPEED

        if not(self.right or self.left):
            self.xvel = 0

        self.x += self.xvel

        # Перемещение по вертикали
        if self.up:
            if self.onGround:
                self.yvel = -self.jumpCount
                
        if not self.onGround:
            self.yvel += GRAVITY
            
        
        self.y += self.yvel


        # state = pygame.key.get_pressed()

        # # Перемещение влево
        # if self.x > 0:
        #     if state[pygame.K_LEFT]:
        #         self.x -= self.vel
            
        #     if state[pygame.K_LSHIFT] and state[pygame.K_LEFT]:
        #         self.x -= self.vel * self.acceleration

        # # Перемещение вправо
        # if self.x < WIDTH - self.width:
        #     if state[pygame.K_RIGHT]:
        #         self.x += self.vel

        #     if state[pygame.K_LSHIFT] and state[pygame.K_RIGHT]:
        #         self.x += self.vel * self.acceleration

        # # Прыжок
        # if not(self.isJump): 
        #     if state[pygame.K_SPACE]:
        #         self.isJump = True
        # else:
        #     if self.jumpCount >= -10:
        #         self.y -= (self.jumpCount * abs(self.jumpCount)) * 0.25
        #         self.jumpCount -= 1
        #     else: 
        #         self.jumpCount = 10
        #         self.isJump = False


clock = pygame.time.Clock()
fps = 60
hero = Hero()
running = True

while running:
    screen.fill(pygame.Color("black"))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                hero.left = True
            elif event.key == pygame.K_RIGHT:
                hero.right = True
            elif event.key == pygame.K_SPACE:
                hero.up = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                hero.left = False
            elif event.key == pygame.K_RIGHT:
                hero.right = False
            elif event.key == pygame.K_SPACE:
                hero.up = False

    render(level)
    hero.draw()
    hero.movement()

    clock.tick(fps)
    pygame.display.flip()
pygame.quit()
