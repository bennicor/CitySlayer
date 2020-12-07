import pygame


size = width, height = 500, 500
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
x, y = 0, 0
fps = 60
running = True

while running:
    screen.fill(pygame.Color("black"))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock.tick(fps)
    pygame.display.flip()
pygame.quit()