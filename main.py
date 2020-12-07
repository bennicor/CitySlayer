import pygame

pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)


class Hero:
    def __init__(self):
        self.vel = 5 # Скорость персонажа
        self.width = 50
        self.height = 50
        self.x = width // 2
        self.y = height - self.height
        self.isJump = False # Проверка на прыжок
        

    def draw(self):
        pygame.draw.rect(screen, pygame.Color("green"), (
                self.x, self.y, self.width, self.height
            ))

    def movement(self):
        state = pygame.key.get_pressed()

        if self.x > 0:
            # Перемещение
            if state[pygame.K_LEFT]:
                self.x -= self.vel
            # с ускорением
            if state[pygame.K_LSHIFT] and state[pygame.K_LEFT]:
                self.x -= self.vel * self.acceleration

        if self.x < width - self.vel - self.width:
            # в обратную сторону
            if state[pygame.K_RIGHT]:
                self.x += self.vel
            # с ускорением
            if state[pygame.K_LSHIFT] and state[pygame.K_RIGHT]:
                self.x += self.vel * self.acceleration

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
