import pygame
from platforms import Platform
from hero import Hero


pygame.init()
size = WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode(size)
level = [
       "-------------------------",
       "-                       -",
       "-                       -",
       "-                       -",
       "-                       -",
       "-            --         -",
       "--                      -",
       "-                       -",
       "-                   --- -",
       "-      ---              -",
       "-                       -",
       "-                       -",
       "-                       -",
       "-   -----------        --",
       "-                       -",
       "-                -      -",
       "-                   --  -",
       "-                       -",
       "-                       -",
       "-------------------------"]


# Выводим на экран все платформы на уровне
def render(level):
    x = y = 0

    for row in level:
        for col in row:
            if col == "-":
                pf = Platform(x,y, all_sprites)
                platforms.append(pf)
                    
            x += pf.width
        y += pf.height
        x = 0

all_sprites = pygame.sprite.Group()
platforms = [] # объекты, с которыми будет происходить взаимодействие
hero = Hero(150, 40, all_sprites)
render(level)

clock = pygame.time.Clock()
fps = 60
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

    all_sprites.draw(screen)
    hero.update(platforms)

    clock.tick(fps)
    pygame.display.flip()
pygame.quit()
