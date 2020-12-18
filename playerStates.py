import pygame

HERO_SPEED = 7
JUMP_FORCE = 20
DASH_SPEED = 15
WALL_JUMP = (50, 20)

# Инициализация классов состояния персонажа
class WallJumpState:
    def __init__(self, vel_x, vel_y, next_state):
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.next_state = next_state

    def handle_event(self, player, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.dash_dir = "left"
                self.next_state = MoveState(-HERO_SPEED)
            elif event.key == pygame.K_RIGHT:
                player.dash_dir = "right"
                self.next_state = MoveState(HERO_SPEED)
            elif event.key == pygame.K_SPACE and player.onWall:
                player.wall_jump_done = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.next_state = IdleState()
            elif event.key == pygame.K_RIGHT:
                self.next_state = IdleState()

    def update(self, player, dt, platforms):
        # Если сделан прыжок от стены
        print(self.next_state)
        if player.wall_jump_done:
            player.vel.x = -self.vel_x if player.wall_pos == "right" else self.vel_x
            player.rect.x += player.vel.x
            player.collide(player.vel.x, 0, platforms)

            player.vel.y = -self.vel_y

        # Пока персонаж на стене
        if player.onWall:
            player.gravitation()
            player.collide(0, player.vel.y, platforms)
        
        # Если персонаж отпрыгнул от стены или соскользнул с нее
        if player.onWall_timer <= 0 or not player.onWall:
            player.state = self.next_state


class DashState:
    def __init__(self, velocity_x, next_state):
        self.dash_timer = .2 # Длительность рывка
        self.velocity_x = velocity_x
        self.next_state = next_state # Следующее состояние

    def handle_event(self, player, event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.next_state = IdleState()
            elif event.key == pygame.K_RIGHT:
                self.next_state = IdleState()

    def update(self, player, dt, platforms):
        if not player.dash_done: # В воздухе может быть выполнен только один рывок
            self.dash_timer -= dt # Таймер
            self.velocity_x = DASH_SPEED

            # В зависимости от последнего направления персонажа вектор скорости рывка меняется
            if player.dash_dir == "left":
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
    def __init__(self, vel_y, next_state):
        self.vel_y = vel_y
        self.next_state = next_state

    def handle_event(self, player, event):
        pass

    def update(self, player, dt, platforms):
        if player.onGround:
            player.vel.y = -self.vel_y
            player.onGround = False

        player.gravitation()
        player.collide(0, player.vel.y, platforms)
        player.state = self.next_state


class MoveState:
    def __init__(self, velocity_x):
        self.velocity_x = velocity_x

    def handle_event(self, player, event):
        if player.onWall:
            return WallJumpState(WALL_JUMP[0], WALL_JUMP[1], player.state)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT and player.dash_dir:
                return DashState(DASH_SPEED, player.state)
            elif event.key == pygame.K_LEFT:
                player.dash_dir = "left"
                self.velocity_x = -HERO_SPEED
            elif event.key == pygame.K_RIGHT:
                player.dash_dir = "right"
                self.velocity_x = HERO_SPEED
            elif event.key == pygame.K_SPACE:
                return JumpState(JUMP_FORCE, player.state)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and self.velocity_x < 0:
                return IdleState()
            elif event.key == pygame.K_RIGHT and self.velocity_x > 0:
                return IdleState()

    def update(self, player, dt, platforms):
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
                player.dash_dir = "left"
                return MoveState(-HERO_SPEED)
            elif event.key == pygame.K_RIGHT:
                player.dash_dir = "right"
                return MoveState(HERO_SPEED)
            elif event.key == pygame.K_LSHIFT and player.dash_dir:
                return DashState(DASH_SPEED, player.state)
            elif event.key == pygame.K_SPACE:
                return JumpState(JUMP_FORCE, player.state)

    def update(self, player, dt, platforms):
        player.gravitation()
        player.collide(0, player.vel.y, platforms)
