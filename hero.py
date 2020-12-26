import pygame
from pygame.math import Vector2
from playerStates import IdleState
from platforms import *

WIDTH, HEIGHT = 1280, 720
GRAVITY = 1.45


# Класс персонажа
class Hero(pygame.sprite.Sprite):
    def __init__(self, pos, *group):
        super().__init__(group)
        self.vel = Vector2(0, 0)
        self.pos = Vector2(pos)
        self.width = 30
        self.height = 50
        self.onGround = False
        self.gravity = GRAVITY

        self.onWall = False
        self.wall_pos = ""

        self.last_dir = ""
        self.dash_cd = .3
        self.dash_done = False

        self.double_jump = False

        self.state = IdleState()

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(pygame.Color("green"))
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)

    def dash_cooldown(self, dt):
        self.dash_cd -= dt

        if self.dash_cd <= 0 and self.onGround:
            self.dash_cd = .3
            self.dash_done = False
                
    def gravitation(self):
        # Реализация силы притяжения
        if self.vel.y <= 12.5:
            self.vel.y += self.gravity

        self.rect.y += self.vel.y

    def collide(self, xvel, yvel, platforms):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        self.onGround = False
        
        if hits: # если есть пересечение платформы с игроком
            # Если есть пересечение с двигающейся платформой, персонаж двигается вместе с ней
            if isinstance(hits[0], MovingPlatform):
                self.rect.x += hits[0].x

            if xvel > 0:
                if not self.onGround and hits[0].can_wall_jump:
                    self.onWall = True
                    self.wall_pos = "right"

                self.rect.right = hits[0].rect.left

            if xvel < 0:
                if not self.onGround and hits[0].can_wall_jump:
                    self.onWall = True
                    self.wall_pos = "left"

                self.rect.left = hits[0].rect.right

            if yvel > 0:
                self.rect.bottom = hits[0].rect.top
                self.onGround = True
                self.double_jump = False
                self.onWall = False
                self.vel.y = 0
            
            if yvel < 0:
                self.rect.top = hits[0].rect.bottom
                self.vel.y = 0

    def handle_event(self, event):
        new_state = self.state.handle_event(self, event)
        # Провераяем, если новое состояние отлично от текущего
        self.state = new_state if new_state is not None else self.state

    def update(self, dt, platforms):
        self.state.update(self, dt, platforms)

        # Если персонаж коснулся земли, возобновляем возможность рывка
        if self.dash_done:
            self.dash_cooldown(dt) # Ограничиваем частоту нажатий
