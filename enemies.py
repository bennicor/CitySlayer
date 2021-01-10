import pygame
import configparser
import json
from random import choice
from platforms import DeadlyPlatform
from helpers import load_image


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

enemy = load_image('data/enemies/enemy.png', 10, 10)

class BaseEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y, group):
        super().__init__(group)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.group = group
        self.color = pygame.Color("red")
        self.onGround = False
        
        self.vel_y = 0

        self.gravity = gravity

        self.rect = pygame.Rect(x, y, self.width, self.height)

    def death(self):
        self.group.remove(self)

    def gravitation(self):
        if self.vel_y <= 12.5:
            self.vel_y += self.gravity

        self.rect.y += self.vel_y
    
    def collide(self, x_vel, y_vel, platforms, hero_group, hero):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        hero_death = pygame.sprite.spritecollide(self, hero_group, False)

        if hits:
            if isinstance(hits[0], DeadlyPlatform):
                self.death()

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
            hero.dead = True

    def update(self, dt, platforms, hero_group, hero):
        pass


class SlowWalkEnemy(BaseEnemy):
    enemy = load_image('data/enemies/enemy.png', width, height)

    def __init__(self, x, y, group):
        super().__init__(x, y, group)
        self.speed = choice([-slow, slow])
        self.range = range
        self.counter =  0

        self.image = SlowWalkEnemy.enemy

    def update(self, dt, platforms, hero_group, hero):
        self.gravitation()
        self.collide(0, self.vel_y, platforms, hero_group, hero)

        if abs(self.counter) >= self.range:
            self.speed = -self.speed

        self.rect = self.rect.move(self.speed, 0)
        self.collide(self.speed, 0, platforms, hero_group, hero)
        self.counter += self.speed


class FastWalkEnemy(BaseEnemy):
    enemy = load_image('data/enemies/enemy.png', width, int(height * 1.2))

    def __init__(self, x, y, group):
        super().__init__(x, y, group)
        self.color = pygame.Color("yellow")
        self.width = width
        self.height = height * 1.2

        self.speed = choice([-fast, fast])
        self.range = range
        self.counter =  0

        self.image = FastWalkEnemy.enemy
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def update(self, dt, platforms, hero_group, hero):
        self.gravitation()
        self.collide(0, self.vel_y, platforms, hero_group, hero)

        if abs(self.counter) >= self.range:
            self.speed = -self.speed

        self.rect = self.rect.move(self.speed, 0)
        self.collide(self.speed, 0, platforms, hero_group, hero)
        self.counter += self.speed


class JumpEnemy(BaseEnemy):
    enemy = load_image('data/enemies/enemy.png', int(width * 1.5), height)

    def __init__(self, x, y, group):
        super().__init__(x, y, group)
        self.color = pygame.Color("purple")
        self.width = width * 1.3
        self.height = height

        self.jump_done = False
        self.jump_cd = jump_cd
        self.speed = choice([-fast, fast])

        self.image = JumpEnemy.enemy
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def update(self, dt, platforms, hero_group, hero):
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
        self.collide(0, self.vel_y, platforms, hero_group, hero)

        if not self.onGround:
            self.rect = self.rect.move(self.speed, 0)
        self.collide(self.speed, 0, platforms, hero_group, hero)
