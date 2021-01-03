import pygame
import configparser
from random import choice
from helpers import restart


config = configparser.ConfigParser()
config.read("settings.ini")

width = config.getint("ENEMY", "width")
height = config.getint("ENEMY", "height")
range = config.getint("ENEMY", "range")
slow = config.getint("ENEMY", "slow_vel_x")
fast = config.getint("ENEMY", "fast_vel_x")
vel_y = config.getint("ENEMY", "vel_y")
jump_cd = config.getfloat("ENEMY", "jump_cd")
gravity = config.getfloat("PLAYER", "gravity")


class BaseEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y, group):
        super().__init__(group)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = pygame.Color("red")
        self.onGround = False
        
        self.vel_y = 0

        self.gravity = gravity

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def gravitation(self):
        if self.vel_y <= 12.5:
            self.vel_y += self.gravity

        self.rect.y += self.vel_y
    
    def collide(self, x_vel, y_vel, platforms, hero):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        hero_death = pygame.sprite.spritecollide(self, hero, False)

        if hits:
            if y_vel > 0:
                self.rect.bottom = hits[0].rect.top
                self.onGround = True
                self.vel_y = 0
            
            if y_vel < 0:
                self.rect.top = hits[0].rect.bottom
                self.vel_y = 0
            
            if x_vel > 0:
                self.rect.right = hits[0].rect.left
            
            if x_vel < 0:
                self.rect.left = hits[0].rect.right
    
        if hero_death:
            restart()

    def update(self, platforms, hero):
        pass


class SlowWalkEnemy(BaseEnemy):
    def __init__(self, x, y, group):
        super().__init__(x, y, group)
        self.speed = choice([-slow, slow])
        self.range = range
        self.counter =  0

    def update(self, dt, platforms, hero):
        self.gravitation()
        self.collide(0, self.vel_y, platforms, hero)

        if abs(self.counter) >= self.range:
            self.speed = -self.speed

        self.rect = self.rect.move(self.speed, 0)
        self.collide(self.speed, 0, platforms, hero)
        self.counter += self.speed


class FastWalkEnemy(BaseEnemy):
    def __init__(self, x, y, group):
        super().__init__(x, y, group)
        self.color = pygame.Color("yellow")
        self.width = width * 0.7
        self.height = height * 1.2

        self.speed = choice([-fast, fast])
        self.range = range
        self.counter =  0

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def update(self, dt, platforms, hero):
        self.gravitation()
        self.collide(0, self.vel_y, platforms, hero)

        if abs(self.counter) >= self.range:
            self.speed = -self.speed

        self.rect = self.rect.move(self.speed, 0)
        self.collide(self.speed, 0, platforms, hero)
        self.counter += self.speed


class JumpEnemy(BaseEnemy):
    def __init__(self, x, y, group):
        super().__init__(x, y, group)
        self.color = pygame.Color("purple")
        self.width = width * 1.3
        self.height = height

        self.jump_done = False
        self.jump_cd = jump_cd
        self.speed = choice([-fast, fast])

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def update(self, dt, platforms, hero):
        global jump_cd

        if self.onGround and not self.jump_done:
            self.vel_y = -vel_y
            self.jump_done = True
            self.onGround = False

        # Добавляем ограничение по времени
        if self.jump_done:
            self.jump_cd -= dt
            
            if self.jump_cd <= 0:
                self.jump_cd = jump_cd
                self.speed = choice([-fast, fast])
                self.jump_done = False

        self.gravitation()
        self.collide(0, self.vel_y, platforms, hero)

        if not self.onGround:
            self.rect = self.rect.move(self.speed, 0)
        self.collide(self.speed, 0, platforms, hero)
