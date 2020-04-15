# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import pyxel
import math
import time
import random

SCREEN_WIDTH = 255
SCREEN_HEIGHT = 120
BACKGROUND_COLOR = 0 # Black (refer supported colors)
BALL_SIZE = 2
BALL_SPEED = 2
BAT_SIZE = 8

class Utils:
    @staticmethod
    def randcolor():
        return random.randrange(1,15,1)

class Vec2:
    def __init__(self,x,y):
        self.x = x
        self.y = y

class Vec2_norm:
    def __init__(self,x,y):
        self.magnitude = math.sqrt(x*x + y*y)

        self.x = x / self.magnitude * BALL_SPEED
        self.y = y / self.magnitude * BALL_SPEED

class Ball:
    def __init__(self,px,py,vx,vy):
        self.position = Vec2(px,py)
        self.velocity = Vec2_norm(vx,vy)

    def update(self):
        self.position.x += self.velocity.x
        self.position.y += self.velocity.y

        if self.position.y >= SCREEN_HEIGHT - BALL_SIZE:
            self.velocity.y = -self.velocity.y

        if self.position.y <= BALL_SIZE:
            self.velocity.y = -self.velocity.y

class HitBox:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1 # x-coordinate of top left corner
        self.y1 = y1 # y-coordinate of top left corner
        self.x2 = x2 # x-coordinate of bottom right corner
        self.y2 = y2 # y-coordinate of bottom right corner

class Bat:
    color = 7

    def __init__(self,px,py):
        self.position = Vec2(px,py)
        self.velocity = 0
        self.hitbox = HitBox(
            self.position.x - BAT_SIZE / 4, # top left x coordinate
            self.position.y - BAT_SIZE, # top left y coordinate
            self.position.x + BAT_SIZE / 4, # bottom right x coordinate
            self.position.y + BAT_SIZE,  # bottom right y coordinate
        )

    def update(self):
        self.position.y += self.velocity

        self.hitbox = HitBox(
            self.position.x - BAT_SIZE / 4,
            self.position.y - BAT_SIZE,
            self.position.x + BAT_SIZE / 4,
            self.position.y + BAT_SIZE
        )

        if self.position.y < BAT_SIZE:
            self.position.y = BAT_SIZE
            self.velocity = 0

        if self.position.y >= SCREEN_HEIGHT - BAT_SIZE:
            self.position.y = SCREEN_HEIGHT - BAT_SIZE
            self.velocity = 0

        if pyxel.btnp(pyxel.KEY_W):
            Bat.color = Utils.randcolor()
            self.velocity = -2

        if pyxel.btnp(pyxel.KEY_S):
            Bat.color = Utils.randcolor()
            self.velocity = 2

class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.ball = Ball(20, 20, 2, 2)
        self.bats = [Bat(2,10), Bat(SCREEN_WIDTH - 2,10)]
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.ball.update()

        for bat in self.bats:
            bat.update()
            
            if (bat.hitbox.x1 < self.ball.position.x < bat.hitbox.x2 
            and bat.hitbox.y1 < self.ball.position.y < bat.hitbox.y2):
                self.ball.velocity.x = -self.ball.velocity.x
                

    def draw(self):
        pyxel.cls(BACKGROUND_COLOR)
        pyxel.circ(self.ball.position.x, self.ball.position.y, BALL_SIZE, 7)

        for bat in self.bats:
            pyxel.rect(
                bat.hitbox.x1,
                bat.hitbox.y1,
                bat.hitbox.x2,
                bat.hitbox.y2,
                Bat.color
            )

App()
