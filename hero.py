import pygame
import configparser
from pygame.math import Vector2
from playerStates import IdleState
from platforms import *


config = configparser.ConfigParser()
config.read("settings.ini")

gravity = config.getfloat('PLAYER', 'gravity')
sliding_speed = config.getfloat('PLAYER', 'sliding_speed')
width = config.getint("PLAYER", "width")
height = config.getint("PLAYER", "height")

# Класс персонажа
class Hero(pygame.sprite.Sprite):
    def __init__(self, pos, *group):
        super().__init__(group)
        self.vel = Vector2(0, 0)
        self.pos = Vector2(pos)
        self.width = width
        self.height = height
        self.gravity = gravity
        self.end = False
        self.onGround = False

        self.sounds = True

        # Инициализация sliding
        self.onWall = False
        self.wall_pos = ""
        self.isSliding = False
        self.wall_first_touch = True
        self.sliding_timer = .7
        self.falling = False
        self.touched_wall = False

        # Инициализация wall jump
        self.wall_jump_timer = .3
        self.wall_jump_done = False
        self.timer_cd = .1

        # Инициализация dash
        self.last_dir = ""
        self.dash_timer = .25
        self.dash_done = False

        self.double_jump = False

        self.state = IdleState()

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(pygame.Color("green"))
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)

    def dash_cooldown(self, dt):
        self.dash_timer -= dt

        if self.dash_timer <= 0 and self.onGround:
            self.dash_timer = .3
            self.dash_done = False

    def sliding(self, dt):
        self.sliding_timer -= dt

        if self.wall_first_touch:
            self.vel.y = 0
            self.gravity = sliding_speed
            self.wall_first_touch = False

        if self.sliding_timer <= 0:
            self.falling = True
            self.wall_first_touch = True

    def wall_jump_cd(self, dt):
        self.wall_jump_timer -= dt

        if self.wall_jump_timer <= 0:
            self.wall_jump_timer = .3
            self.wall_jump_done = False

    # Позволяет игроку делать прыжок в противоположную сторону
    def timer(self, dt):
        self.timer_cd -= dt

        self.vel.y = 0
        self.gravity = 0

        if self.timer_cd <= 0:
            self.timer_cd = .1
            self.falling = True
            self.wall_jump_done = True

    def gravitation(self):
        # Реализация силы притяжения
        if self.vel.y <= 12.5:
            self.vel.y += self.gravity

        self.rect.y += self.vel.y

    def collide(self, xvel, yvel, platforms):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        self.onGround = False
        
        if hits: # если есть пересечение платформы с игрокоместь
            if isinstance(hits[0], MovingPlatform):   # Если  пересечение с двигающейся платформой, персонаж двигается вместе с ней
                self.rect.x += hits[0].x

            if yvel > 0:
                self.rect.bottom = hits[0].rect.top
                self.onGround = True
                self.vel.y = 0
            
            if yvel < 0:
                self.rect.top = hits[0].rect.bottom
                self.vel.y = 0
            
            if xvel > 0:
                if not self.onGround and hits[0].can_wall_jump:
                    self.onWall = True
                    self.wall_pos = "right"

                    if not self.touched_wall:
                        self.falling = False
                        self.touched_wall = True

                self.rect.right = hits[0].rect.left
            
            if xvel < 0:
                if not self.onGround and hits[0].can_wall_jump:
                    self.onWall = True
                    self.wall_pos = "left"

                    if not self.touched_wall:
                        self.falling = False
                        self.touched_wall = True

                self.rect.left = hits[0].rect.right

    def handle_event(self, event):
        new_state = self.state.handle_event(self, event)
        # Провераяем, если новое состояние отлично от текущего
        self.state = new_state if new_state is not None else self.state

    def update(self, dt, platforms):
        if self.onGround:
            self.onWall = False
            self.sliding_timer = .7
            self.wall_jump_timer = .3
            self.falling = False
            self.double_jump = False
            self.wall_jump_done = False
            self.touched_wall = False
            self.wall_first_touch = True

        self.isSliding = False
        self.state.update(self, dt, platforms)
            
        # Если персонаж коснулся земли, возобновляем возможность рывка
        if self.dash_done:
            self.dash_cooldown(dt) # Ограничиваем частоту нажатий

        # Если персонаж находится на стене, начинается скольжение
        if self.isSliding and not self.falling:
            self.sliding(dt)
        else:
            self.gravity = gravity

        if self.wall_jump_done:
            self.wall_jump_cd(dt) # Ограничиваем частоту прыжков
