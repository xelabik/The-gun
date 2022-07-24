import math
from random import choice
from random import randint as rnd

import pygame


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

        movement of the ball in one redraw frame. update self.x and self.y depending on:
        1) self.vx и self.vy,
        2) gravity,
        3) reflection from walls and ground.
        """

        self.vy += 1  # gravity
        print(self.vx, self.vy, self.x, self.y)
        if self.x + self.vx > 800 or self.x + self.vx < 0:
            self.vx = -self.vx
        if self.y + self.vy > 600:
            self.vy = -self.vy

        self.x += self.vx
        self.y += self.vy
        # dampening of inertia during contact with the ground
        if self.y + self.vy > 600:
            self.vx = self.vx / 3
            self.vy = self.vy / 3
            print("it is work")

        if abs(self.vx) < 1 or abs(self.vy) < 1:
            pass

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
        """checks collision ball with target, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        # FIXME



        return False


class Gun:
    def __init__(self, screen) :
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event) -> bool :
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

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.pos[1]-450) / (event.pos[0]-20))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        pass
        # FIXIT don't know how to do it

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target(Ball):
    # self.points = 0
    # self.live = 1
    # FIXME: don't work!!! How to call this functions when object is created?
    # self.new_target()

    def new_target(self):
        # new target initiation
        x = self.x = rnd(600, 780)
        y = self.y = rnd(300, 550)
        r = self.r = rnd(10, 50)
        color = self.color = RED

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        """
        self.screen = screen
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )
        # remove print
        print("I printed new target")
        """

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
target = Target(screen)
finished = False

while not finished:
    screen.fill(screen_color)

    gun.draw()
    target.draw()
    for b in balls:
        b.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for b in balls:
        b.move()
        if b.hittest(target) and target.live:
            target.live = 0
            target.hit()
            target.new_target()
    gun.power_up()

pygame.quit()
