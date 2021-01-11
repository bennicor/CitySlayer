import pygame
import configparser
import json
import time
from helpers import load_sound, play_sound, get_length, stop_sound, load_image


config = configparser.ConfigParser()
config.read("settings.ini")

hero_speed = config.getfloat('PLAYER', 'hero_speed')
jump_force = config.getfloat('PLAYER', 'jump_force')
dash_speed = config.getint('PLAYER', 'dash_speed')
wall_jump = json.loads(config.get("PLAYER", "wall_jump"))

down_timer = config.getfloat("CAMERA", "down_timer")
width, height = json.loads(config.get("MAIN", "res"))
h_width, h_height = json.loads(config.get("PLAYER", "size"))
fps = config.getint("MAIN", "fps")

# Загрузка звуков
walk_sound = load_sound("data/sounds/walk.wav")
walk_sound.set_volume(0.5)
walk_time = get_length(walk_sound)
jump_sound = load_sound("data/sounds/jump.wav")
jump_sound.set_volume(0.4)
dash_sound = load_sound("data/sounds/dash.wav")
dash_sound.set_volume(0.4)
sliding_sound = load_sound("data/sounds/wall_slide.wav")
sliding_sound.set_volume(0.4)
slide_time = get_length(sliding_sound)

idle_right = [load_image('data/PassiveReaper_Right/PassiveIdleReaper-Sheet.png', h_width, h_height),
                 load_image('data/PassiveReaper_Right/PassiveIdleReaper-Sheet2.png', h_width, h_height),
                 load_image('data/PassiveReaper_Right/PassiveIdleReaper-Sheet3.png', h_width, h_height),
                 load_image('data/PassiveReaper_Right/PassiveIdleReaper-Sheet4.png', h_width, h_height),
                 load_image('data/PassiveReaper_Right/PassiveIdleReaper-Sheet5.png', h_width, h_height)]

idle_left = [load_image('data/PassiveReaper_Left/PassiveIdleReaper-Sheet.png', h_width, h_height),
                 load_image('data/PassiveReaper_Left/PassiveIdleReaper-Sheet2.png', h_width, h_height),
                 load_image('data/PassiveReaper_Left/PassiveIdleReaper-Sheet3.png', h_width, h_height),
                 load_image('data/PassiveReaper_Left/PassiveIdleReaper-Sheet4.png', h_width, h_height),
                 load_image('data/PassiveReaper_Left/PassiveIdleReaper-Sheet5.png', h_width, h_height)]

go_right = [load_image('data/Reaper_go_right/RunningReaper.png', h_width, h_height),
            load_image('data/Reaper_go_right/RunningReaper2.png', h_width, h_height),
            load_image('data/Reaper_go_right/RunningReaper3.png', h_width, h_height),
            load_image('data/Reaper_go_right/RunningReaper4.png', h_width, h_height),
            load_image('data/Reaper_go_right/RunningReaper6.png', h_width, h_height),
            load_image('data/Reaper_go_right/RunningReaper7.png', h_width, h_height)]

go_left = [load_image('data/Reaper_go_left/RunningReaper.png', h_width, h_height),
           load_image('data/Reaper_go_left/RunningReaper2.png', h_width, h_height),
           load_image('data/Reaper_go_left/RunningReaper3.png', h_width, h_height),
           load_image('data/Reaper_go_left/RunningReaper4.png', h_width, h_height),
           load_image('data/Reaper_go_left/RunningReaper6.png', h_width, h_height),
           load_image('data/Reaper_go_left/RunningReaper7.png', h_width, h_height)]

# Инициализация классов состояния персонажа
class DashState:
    def __init__(self, velocity_x, next_state, player):
        self.dash_timer = .15 # Длительность рывка
        self.velocity_x = velocity_x
        self.next_state = next_state # Следующее состояние

        if player.sounds and not player.dash_done:   # Воспроизводим звук
            play_sound(dash_sound)

    def handle_event(self, player, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.last_dir = "left"
                self.next_state = MoveState(-hero_speed)
            elif event.key == pygame.K_RIGHT:
                player.last_dir = "right"
                self.next_state = MoveState(hero_speed)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.next_state = IdleState()
            elif event.key == pygame.K_RIGHT:
                self.next_state = IdleState()

    def update(self, player, dt, platforms, camera=None):
        global walk_time, slide_time

        if not player.dash_done: # В воздухе может быть выполнен только один рывок                
            walk_time = get_length(walk_sound)
            slide_time = get_length(sliding_sound)
            self.dash_timer -= dt # Таймер
            self.velocity_x = dash_speed

            # В зависимости от последнего направления персонажа вектор скорости рывка меняется
            if player.last_dir == "left":
                self.velocity_x = -self.velocity_x

            player.rect.x += self.velocity_x
            player.collide(self.velocity_x, 0, platforms)
            
            # Если таймер истек
            if self.dash_timer <= 0:
                player.vel.y = 0
                player.dash_done = True
                player.state = self.next_state
        else:
            player.state = self.next_state


class JumpState:
    def __init__(self, velocity_y, next_state):
        self.velocity_y = velocity_y
        self.next_state = next_state

    def handle_event(self, player, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.last_dir = "left"
                self.next_state = MoveState(-hero_speed)
            elif event.key == pygame.K_RIGHT:
                player.last_dir = "right"
                self.next_state = MoveState(hero_speed)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.next_state = IdleState()
            elif event.key == pygame.K_RIGHT:
                self.next_state = IdleState()

    def update(self, player, dt, platforms, camera=None):
        global walk_time, slide_time

        walk_time = get_length(walk_sound)
        slide_time = get_length(sliding_sound)

        if player.onGround:
            if player.sounds:   # Воспроизводим звук
                play_sound(jump_sound)

            player.vel.y = -self.velocity_y
            player.onGround = False
            player.double_jump = True

        player.gravitation()
        player.collide(0, player.vel.y, platforms)
        player.state = self.next_state


class DoubleJumpState(JumpState):
    def __init__(self, velocity_y, next_state):
        super().__init__(velocity_y, next_state)

    def update(self, player, dt, platforms, camera=None):
        global walk_time, slide_time

        walk_time = get_length(walk_sound)
        slide_time = get_length(sliding_sound)

        if player.sounds:   # Воспроизводим звук
            play_sound(jump_sound)  

        player.vel.y = -self.velocity_y

        player.gravitation()
        player.collide(0, player.vel.y, platforms)

        player.double_jump = False
        player.state = self.next_state


class WallJumpState:
    def __init__(self, velocity_x, velocity_y, next_state):
        self.velocity_y = velocity_y
        self.velocity_x = velocity_x
        self.next_state = next_state

    def handle_event(self, player, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.last_dir = "left"
                self.next_state = MoveState(-hero_speed)
            elif event.key == pygame.K_RIGHT:
                player.last_dir = "right"
                self.next_state = MoveState(hero_speed)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.next_state = IdleState()
            elif event.key == pygame.K_RIGHT:
                self.next_state = IdleState()
            elif event.key == pygame.K_a:
                self.next_state = IdleState()
            elif event.key == pygame.K_d:
                self.next_state = IdleState()

    def update(self, player, dt, platforms, camera=None):
        global walk_time, slide_time

        # Игрок не может прыгать с большой скоростью
        if not player.wall_jump_done:
            walk_time = get_length(walk_sound)
            slide_time = get_length(sliding_sound)
            if player.sounds:   # Воспроизводим звук
                play_sound(jump_sound)

            self.velocity_x = self.velocity_x if player.last_dir == "left" else -self.velocity_x
            
            player.vel.x = self.velocity_x
            player.rect.x += self.velocity_x
            player.collide(player.vel.x, 0, platforms)

            player.vel.y = self.velocity_y
            player.gravitation()
            player.collide(0, player.vel.y, platforms)
        
            player.sliding_timer = .7
            player.timer_cd = .1

            player.wall_jump_done = True
            player.double_jump = True
            player.dash_done = False
            player.falling = True
            player.touched_wall = False
            player.onWall = False
            player.wall_first_touch = True

            player.state = self.next_state
        else:
            player.state = self.next_state

class MoveState:
    def __init__(self, velocity_x):
        global walk_time

        self.velocity_x = velocity_x
        self.anim_count = 0
        walk_time = get_length(walk_sound)

    def handle_event(self, player, event):
        global walk_time

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT and player.last_dir:
                return DashState(dash_speed, player.state, player)
            if event.key == pygame.K_LEFT:
                walk_time = get_length(walk_sound)
                player.go_left = True
                player.last_dir = "left"
                self.velocity_x = -hero_speed
            if event.key == pygame.K_RIGHT:
                walk_time = get_length(walk_sound)
                player.go_right = True
                player.last_dir = "right"
                self.velocity_x = hero_speed
            elif event.key == pygame.K_SPACE:
                if player.double_jump and not player.onWall:
                    return DoubleJumpState(jump_force, player.state)
                elif player.isSliding and not player.wall_jump_done:
                    return WallJumpState(wall_jump[0], wall_jump[1], player.state)

                return JumpState(jump_force, player.state)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.go_left = False
            if event.key == pygame.K_RIGHT:
                player.go_right = False
            if event.key == pygame.K_LEFT and self.velocity_x < 0:
                player.left = False
                return IdleState()
            elif event.key == pygame.K_RIGHT and self.velocity_x > 0:
                player.right = False
                return IdleState()
            if event.key == pygame.K_a and self.velocity_x < 0:
                return IdleState()
            elif event.key == pygame.K_d and self.velocity_x > 0:
                return IdleState()

    def update(self, player, dt, platforms, camera=None):
        global walk_time, slide_time

        # Воспроизводим звуки ходьбы
        if player.onGround and player.sounds:
            if walk_time >= get_length(walk_sound):
                play_sound(walk_sound)
                walk_time = 0
            else:
                walk_time += dt

        # Воспроизводим анимацию движения
        if self.anim_count >= fps:
            self.anim_count = 0

        if player.last_dir == 'right':
            player.image = go_right[self.anim_count // 10]

        if player.last_dir == 'left':
            player.image = go_left[self.anim_count // 10]
        self.anim_count += 1
        
        # Если персонаж находится на стене и двигается в ее сторону, он начинает скользить
        if player.onWall and not player.onGround:
            if player.wall_pos == player.last_dir:
                player.isSliding = True

                if player.sounds:
                    if slide_time >= get_length(sliding_sound):
                        play_sound(sliding_sound)
                        slide_time = 0
                    else:
                        slide_time += dt
            else:
                stop_sound()
                player.isSliding = True
                
                if not player.falling:
                    player.timer(dt)

                player.sliding_timer = .7

        # Обновляем координаты персонажа и проверям на столкновения
        player.vel.x = self.velocity_x
        player.rect.x += player.vel.x
        player.collide(player.vel.x, 0, platforms)

        player.gravitation()
        player.collide(0, player.vel.y, platforms)


class IdleState:
    def __init__(self):
        self.timer = down_timer
        self.anim_count = 0
        self.camera_down = False

    def handle_event(self, player, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.last_dir = "left"
                return MoveState(-hero_speed)
            elif event.key == pygame.K_RIGHT:
                player.last_dir = "right"
                return MoveState(hero_speed)
            elif event.key == pygame.K_LSHIFT and player.last_dir:
                return DashState(dash_speed, player.state, player)
            elif event.key == pygame.K_SPACE:
                if player.double_jump and not player.onWall:
                    return DoubleJumpState(jump_force, player.state)
                elif player.isSliding and not player.wall_jump_done:
                    return WallJumpState(wall_jump[0], wall_jump[1], player.state)

                return JumpState(jump_force, player.state)

    def update(self, player, dt, platforms, camera=None):
        # Воспроизводим анимацию покоя
        if self.anim_count >= fps:
            self.anim_count = 0

        if player.last_dir == 'right':
            player.image = idle_right[self.anim_count // 15]
        if player.last_dir == 'left':
            player.image = idle_left[self.anim_count // 15]

        self.anim_count += 1

        # Опускаем камеру при длительном нажатии клавиши
        keys = pygame.key.get_pressed()

        if keys[pygame.K_DOWN]:
            self.timer -= dt

            if self.timer <= 0 and not self.camera_down:
                camera.y_offset *= 0.4
                self.camera_down = True
        else:
            self.timer = down_timer
            self.camera_down = False
            camera.y_offset = height // 2 + h_height

        if player.onGround:
            stop_sound()
            
        player.gravitation()
        player.collide(0, player.vel.y, platforms)
