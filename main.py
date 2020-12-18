import pygame
from platforms import Platform, WallPlatform
from hero import Hero


pygame.init()
size = WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode(size)
level = [
       "#########################",
       "#    #        #         #",
       "#    #        #         #",
       "#    #        #         #",
       "#    #        #         #",
       "#    #        #         #",
       "#    #        #         #",
       "#    #        #         #",
       "#    #        #         #",
       "#    #        #         #",
       "#    #        #         #",
       "#    #        #         #",
       "#    #      #           #",
       "#    #      #           #",
       "#    #      #           #",
       "#    #      #           #",
       "#    #      #           #",
       "#                       #",
       "#                       #",
       "#########################"]


# Выводим на экран все платформы на уровне
def render(level):
    x = y = 0

    for row in level:
        for col in row:
            if col == "-":
                pf = Platform(x,y, all_sprites)
                platforms.append(pf)
            elif col == "#":
                pf = WallPlatform(x, y, all_sprites)
                platforms.append(pf)

            x += pf.width
        y += pf.height
        x = 0

all_sprites = pygame.sprite.Group()
platforms = [] # объекты, с которыми будет происходить взаимодействие
hero = Hero((500, 100), all_sprites)
render(level)

clock = pygame.time.Clock()
fps = 60
dt = 0
running = True

while running:
    screen.fill(pygame.Color("black"))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        hero.handle_event(event)

    all_sprites.update(dt, platforms)
    all_sprites.draw(screen)

    dt = clock.tick(fps) / 1000
    pygame.display.flip()
pygame.quit()
