import pygame
from platforms import FloorPlatform, WallPlatform, MovingPlatform
from hero import Hero


pygame.init()
size = WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode(size)
level = [
       "###########################",
       "#                         #",
       "#                         #",
       "#                         #",
       "#                         #",
       "#                         #",
       "#       <<<<<             #",
       "#                         #",
       "#                         #",
       "#                         #",
       "#        >>>              #",
       "#                         #",
       "#                         #",
       "#                         #",
       "___________________________"]


# Выводим на экран все платформы на уровне
def render(level):
    x = y = 0

    for row in level:
        for col in row:
            if col == "_":
                pf = FloorPlatform(x, y, platform_sprites)
                platforms.append(pf)
            elif col == "#":
                pf = WallPlatform(x, y, platform_sprites)
                platforms.append(pf)
            elif col == ">":
                pf = MovingPlatform(x, y, platform_sprites, ">")
                platforms.append(pf)
            elif col == "<":
                pf = MovingPlatform(x, y, platform_sprites, "<")
                platforms.append(pf)

            x += pf.width
        y += pf.height
        x = 0

platform_sprites = pygame.sprite.Group()
platforms = [] # объекты, с которыми будет происходить взаимодействие

hero_sprites = pygame.sprite.Group()
hero = Hero((500, 100), hero_sprites)
render(level)

clock = pygame.time.Clock()
fps = 65
dt = 0
running = True

while running:
    screen.fill(pygame.Color("black"))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        hero.handle_event(event)

    platform_sprites.update()
    platform_sprites.draw(screen)

    hero_sprites.update(dt, platforms)
    hero_sprites.draw(screen)

    dt = clock.tick(fps) / 1000
    pygame.display.flip()
pygame.quit()
