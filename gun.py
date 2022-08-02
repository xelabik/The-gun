import math
from random import choice
from random import randint as rnd

import pygame

# main

FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
screen_color = (170, 200, 227)
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


class Ball:
    def __init__(self, screen: pygame.Surface, x: int = 40, y: int = 450) -> None:
        """
        ball constructor

        Args:
            x - start horizontal point
            y - start vertical poit
            screen - game field 800 x 600
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 10
        self.vy = -100
        self.color = BLACK
        self.live = 30

    def move(self) -> None:
        """
        move ball per unit of time .

        move the ball in one redraw frame. update self.x and self.y depending on:
        1) self.vx и self.vy,
        2) gravity,
        3) reflection from walls and ground.
        """
        self.vy += 1  # gravity
        if self.x + self.vx > 800 or self.x + self.vx < 0:
            self.vx = -self.vx
        if self.y + self.vy > 600:
            self.vy = -self.vy
            # dampening of inertia during contact with the ground
            self.vx = self.vx / 3
            self.vy = self.vy / 3

        self.x += self.vx
        self.y += self.vy

    def draw(self) -> None:
        """
        draw the ball
        """
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj) -> bool:
        """checks collision ball with target.

        Args:
            obj: target, which collision checking .
        Returns:
            if ball hit the target return true . else return False.
        """
        x_check = abs(self.x - obj.x) - (self.r + obj.r)
        y_check = abs(self.y - obj.y) - (self.r + obj.r)
        if x_check < 0 and y_check < 0:
            return True
        else:
            return False


class Gun:
    def __init__(self, screen) -> None:
        """
        ball constructor

        Args:
            screen - game field 800 x 600
        """
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY

    def fire2_start(self, event) -> None:
        """
        up the flag when user push mouse button
        Args:
            event: MOUSEBUTTONDOWN
        """
        self.f2_on = 1

    def fire2_end(self, event) -> None:
        """
        Shut with ball when MOUSE left BUTTON UP

        Start velocity (vx and vy) depend on mouse position

        Args:
            event: mouse position
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event) -> None:
        """
        takes aim. Depend on mouse cursor position.
        Args:
            event: MOUSEMOTION (mouse position x,y)
        """
        if event:
            self.an = math.atan((event.pos[1]-450) / (event.pos[0]-20))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self) -> None:
        """
        draw the gun
        """
        st: int = [40, 450]
        fnx = (40 + math.cos(self.an) * (self.f2_power + 30))
        fny = (450 + math.sin(self.an) * (self.f2_power + 30))
        pygame.draw.line(screen, self.color, (st[0], st[1]), (fnx, fny), 7)

    def power_up(self) -> None:
        """
        increases power of shoot
        """
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    def __init__(self, screen: pygame.Surface, x: int = 400, y: int = 450) -> None:
        """
        target constructor

        Args:
        x - start horizontal point
        y - start vertical poit
        screen - game field 800 x 600
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.color = RED
        self.live = 1
        self.points = 1

    def new_target(self) -> None:
        """
        new target initiation
        """
        x = self.x = rnd(300, 780)
        y = self.y = rnd(50, 550)
        r = self.r = rnd(5, 25)
        color = self.color = RED
        self.live = 1

    def hit(self, points) -> int:
        """
        score calculation.
        Args:
            points: game score

        Returns:
            Int: game score
        """
        points += self.points
        return points

    def draw(self) -> None:
        """
        draw the ball
        """
        self.screen = screen
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
points = 0
balls = []
targets = []
count_targets = 4
gameCountFlag = 0

clock = pygame.time.Clock()
gun = Gun(screen)

for t in range(count_targets):
    target = Target(screen)
    target.new_target()
    targets.append(target)

finished = False
while not finished:
    screen.fill(screen_color)

    gun.draw()
    # score
    font = pygame.font.Font(None, 36)
    text = font.render("Score: " + str(points), True, BLACK)
    screen.blit(text, [30, 30])
    # targets draw
    for target in targets:
        if target.live:
            target.draw()
    # balls(bullets) draw
    for b in balls:
        if abs(b.vx) > 1:
            b.draw()

    pygame.display.update()
    clock.tick(FPS)
    # mouse event manager
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)
    # actions after event
    for b in balls:
        b.move()
        for target in targets:
            if b.hittest(target) and target.live:
                target.live = 0
                gameCountFlag += 1
                points = target.hit(points)
                #print(points)
                if gameCountFlag == count_targets:
                    gameCountFlag = 0
                    for t in range(count_targets):
                        target = Target(screen)
                        target.new_target()
                        targets.append(target)

    gun.power_up()

pygame.quit()
