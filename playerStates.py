import pygame

HERO_SPEED = 8.5
JUMP_FORCE = 21.5
DASH_SPEED = 20
WALL_JUMP = (30, -20)
GRAVITY = 1.5


# Инициализация классов состояния персонажа
class DashState:
    def __init__(self, velocity_x, next_state):
        self.dash_timer = .15 # Длительность рывка
        self.velocity_x = velocity_x
        self.next_state = next_state # Следующее состояние

    def handle_event(self, player, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.last_dir = "left"
                self.next_state = MoveState(-HERO_SPEED)
            elif event.key == pygame.K_RIGHT:
                player.last_dir = "right"
                self.next_state = MoveState(HERO_SPEED)
            elif event.key == pygame.K_a:
                player.last_dir = "left"
                self.next_state = MoveState(-HERO_SPEED)
            elif event.key == pygame.K_d:
                player.last_dir = "right"
                self.next_state = MoveState(HERO_SPEED)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.next_state = IdleState()
            elif event.key == pygame.K_RIGHT:
                self.next_state = IdleState()
            elif event.key == pygame.K_a:
                self.next_state = IdleState()
            elif event.key == pygame.K_d:
                self.next_state = IdleState()

    def update(self, player, dt, platforms):
        if not player.dash_done: # В воздухе может быть выполнен только один рывок
            self.dash_timer -= dt # Таймер
            self.velocity_x = DASH_SPEED

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
                self.next_state = MoveState(-HERO_SPEED)
            elif event.key == pygame.K_RIGHT:
                player.last_dir = "right"
                self.next_state = MoveState(HERO_SPEED)
            elif event.key == pygame.K_a:
                player.last_dir = "left"
                self.next_state = MoveState(-HERO_SPEED)
            elif event.key == pygame.K_d:
                player.last_dir = "right"
                self.next_state = MoveState(HERO_SPEED)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.next_state = IdleState()
            elif event.key == pygame.K_RIGHT:
                self.next_state = IdleState()
            elif event.key == pygame.K_a:
                self.next_state = IdleState()
            elif event.key == pygame.K_d:
                self.next_state = IdleState()

    def update(self, player, dt, platforms):
        if player.onGround:
            player.vel.y = -self.velocity_y
            player.onGround = False
            player.double_jump = True

        player.gravitation()
        player.collide(0, player.vel.y, platforms)
        player.state = self.next_state


class DoubleJumpState(JumpState):
    def __init__(self, velocity_y, next_state):
        super().__init__(velocity_y, next_state)

    def update(self, player, dt, platforms):
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
                self.next_state = MoveState(-HERO_SPEED)
            elif event.key == pygame.K_RIGHT:
                player.last_dir = "right"
                self.next_state = MoveState(HERO_SPEED)
            elif event.key == pygame.K_a:
                player.last_dir = "left"
                self.next_state = MoveState(-HERO_SPEED)
            elif event.key == pygame.K_d:
                player.last_dir = "right"
                self.next_state = MoveState(HERO_SPEED)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.next_state = IdleState()
            elif event.key == pygame.K_RIGHT:
                self.next_state = IdleState()
            elif event.key == pygame.K_a:
                self.next_state = IdleState()
            elif event.key == pygame.K_d:
                self.next_state = IdleState()

    def update(self, player, dt, platforms):
        # Игрок не может прыгать с большой скоростью
        if not player.wall_jump_done:
            self.velocity_x = self.velocity_x if player.last_dir == "left" else -self.velocity_x
            
            player.vel.x = self.velocity_x
            player.rect.x += self.velocity_x
            player.collide(player.vel.x, 0, platforms)

            player.vel.y = self.velocity_y
            player.gravitation()
            player.collide(0, player.vel.y, platforms)
        
            player.sliding_timer = 1
            player.timer_cd = .1

            player.wall_jump_done = True
            player.double_jump = True
            player.dash_done = False
            player.falling = True
            player.touched_wall = False
            player.onWall = False

            player.state = self.next_state
        else:
            player.state = self.next_state

class MoveState:
    def __init__(self, velocity_x):
        self.velocity_x = velocity_x

    def handle_event(self, player, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT and player.last_dir:
                return DashState(DASH_SPEED, player.state)
            elif event.key == pygame.K_LEFT:
                player.last_dir = "left"
                self.velocity_x = -HERO_SPEED
            elif event.key == pygame.K_RIGHT:
                player.last_dir = "right"
                self.velocity_x = HERO_SPEED
            elif event.key == pygame.K_a:
                player.last_dir = "left"
                self.velocity_x = -HERO_SPEED
            elif event.key == pygame.K_d:
                player.last_dir = "right"
                self.velocity_x = HERO_SPEED
            elif event.key == pygame.K_SPACE:
                if player.double_jump and not player.onWall:
                    return DoubleJumpState(JUMP_FORCE, player.state)
                elif player.isSliding and not player.wall_jump_done:
                    return WallJumpState(WALL_JUMP[0], WALL_JUMP[1], player.state)

                return JumpState(JUMP_FORCE, player.state)

        if event.type == pygame.KEYUP:
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

    def update(self, player, dt, platforms):
        # Если персонаж находится на стене и двигается в ее сторону, он начинает скользить
        if player.onWall and not player.onGround:
            if player.wall_pos == player.last_dir:
                player.isSliding = True
            else:
                player.isSliding = True
                
                if not player.falling:
                    player.timer(dt)

                player.sliding_timer = 1

        # Обновляем координаты персонажа и проверям на столкновения
        player.vel.x = self.velocity_x
        player.rect.x += player.vel.x
        player.collide(player.vel.x, 0, platforms)

        player.gravitation()
        player.collide(0, player.vel.y, platforms)


class IdleState:
    def handle_event(self, player, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.last_dir = "left"
                return MoveState(-HERO_SPEED)
            elif event.key == pygame.K_RIGHT:
                player.last_dir = "right"
                return MoveState(HERO_SPEED)
            elif event.key == pygame.K_a:
                player.last_dir = "left"
                return MoveState(-HERO_SPEED)
            elif event.key == pygame.K_d:
                player.last_dir = "right"
                return MoveState(HERO_SPEED)
            elif event.key == pygame.K_LSHIFT and player.last_dir:
                return DashState(DASH_SPEED, player.state)
            elif event.key == pygame.K_SPACE:
                if player.double_jump and not player.onWall:
                    return DoubleJumpState(JUMP_FORCE, player.state)
                elif player.isSliding and not player.wall_jump_done:
                    return WallJumpState(WALL_JUMP[0], WALL_JUMP[1], player.state)

                return JumpState(JUMP_FORCE, player.state)

    def update(self, player, dt, platforms):        
        player.gravitation()
        player.collide(0, player.vel.y, platforms)
