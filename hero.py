import pygame
from pygame.math import Vector2

WIDTH, HEIGHT = 1280, 720
HERO_SPEED = 8
GRAVITY = 1.5


class DashState:
    def __init__(self, velocity_x, next_state):
        self.dash_timer = .2  # The dash will last .5 seconds.
        self.velocity_x = velocity_x
        self.next_state = next_state

    def handle_event(self, player, event):
        # Can queue the Move- or IdleState as the
        # next state after the dashing.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.next_state = MoveState(-HERO_SPEED)
            elif event.key == pygame.K_d:
                self.next_state = MoveState(HERO_SPEED)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                self.next_state = IdleState()
            elif event.key == pygame.K_d:
                self.next_state = IdleState()

    def update(self, player, dt, platforms=[]):
        # Decrement the timer each frame.
        self.dash_timer -= dt
        # Update the position of the player.
        player.pos.x += self.velocity_x
        player.rect.center = player.pos

        if self.dash_timer <= 0:  # Once the timer is done...
            # switch to the queued state.
            player.state = self.next_state


class MoveState:
    def __init__(self, velocity_x):
        self.velocity_x = velocity_x

    def handle_event(self, player, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                return DashState(-8, player.state)
            elif event.key == pygame.K_e:
                return DashState(8, player.state)
            elif event.key == pygame.K_LEFT:
                self.velocity_x = -HERO_SPEED
            elif event.key == pygame.K_RIGHT:
                self.velocity_x = HERO_SPEED
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and self.velocity_x < 0:
                player.temp_dir = "left"
                return IdleState()
            elif event.key == pygame.K_RIGHT and self.velocity_x > 0:
                player.temp_dir = "right"
                return IdleState()

    def update(self, player, dt, platforms=[]):
        player.vel.x = self.velocity_x
        player.rect.x += self.velocity_x


class IdleState:
    def handle_event(self, player, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                return MoveState(-HERO_SPEED)
            elif event.key == pygame.K_RIGHT:
                return MoveState(HERO_SPEED)
            elif event.key == pygame.K_q:
                return DashState(-8, player.state)
            elif event.key == pygame.K_e:
                return DashState(8, player.state)

    def update(self, player, dt, platforms=[]):
        player.vel.x = 0

# Класс персонажа
class Hero(pygame.sprite.Sprite):
    def __init__(self, pos, *group):
        super().__init__(group)
        self.vel = Vector2(0, 0)
        self.pos = Vector2(pos)
        self.width = 30
        self.height = 50
        self.state = IdleState()

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(pygame.Color("green"))
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)

        self.jumpCount = 20
        self.onGround = False
        self.temp_dir = ""

    def gravitation(self):
        # Реализация силы притяжения
        if self.vel.y <= 12.5:
            self.vel.y += GRAVITY

        self.rect.y += self.vel.y

    def collide(self, xvel, yvel, platforms):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        # self.onGround = False
        if hits: # если есть пересечение платформы с игроком
            if yvel > 0:
                self.rect.bottom = hits[0].rect.top
                self.onGround = True
                self.vel.y = 0
            
            if yvel < 0:
                self.rect.top = hits[0].rect.bottom
                self.vel.y = 0
            
            if xvel > 0:
                # self.rect.right = hits[0].rect.left
                self.vel.x = 0

            if xvel < 0:
                # self.rect.left = hits[0].rect.right
                self.vel.x = 0

    def handle_event(self, event):
        new_state = self.state.handle_event(self, event)
        self.state = new_state if new_state is not None else self.state

    def update(self, dt, platforms):
        self.state.update(self, dt)
        self.gravitation()
        print(self.vel.x, self.vel.y)
        self.collide(self.vel.x, 0, platforms)
        self.collide(0, self.vel.y, platforms)
