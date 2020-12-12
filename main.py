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
hero = Hero(300, 40, all_sprites)
render(level)

clock = pygame.time.Clock()
fps = 60
dash = False
running = True

while running:
    screen.fill(pygame.Color("black"))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and not dash:
                hero.left = True
                hero.temp_dir = "left"
            elif event.key == pygame.K_RIGHT and not dash:
                hero.right = True
                hero.temp_dir = "right"
            elif event.key == pygame.K_SPACE:
                hero.jump()
            elif event.key == pygame.K_LSHIFT and hero.temp_dir:
                dash = True
                timer = .2

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                hero.left = False
            elif event.key == pygame.K_RIGHT:
                hero.right = False

    # Засекается таймер, определяющий длительность рывка
    if dash:
        timer -= dt

        if timer > 0:
            hero.dash_speed = 15
            hero.dash()
        else:
            dash = False

    all_sprites.draw(screen)

    # Во время рывка все остальные процессы останавливаются
    if not dash:
        hero.update(platforms)
    else:
        hero.yvel = 0
        hero.collide(hero.dash_speed, 0, platforms)

    dt = clock.tick(fps) / 1000
    pygame.display.flip()
pygame.quit()
