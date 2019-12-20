from explosion import Explosion

from constant import constant

import math


class Bullet():
    def __init__(self, gun, canvas, game):
        self.const = constant()
        self.canvas = canvas
        self.gun = gun
        self.game = game
        self.splash = 0
        self.x = gun.x
        self.y = gun.y
        self.r = 0
        self.vx = 0
        self.v0x = 0
        self.vy = 0
        self.color = 'blue'
        self.body_id = 0
        self.activation = 0

    def collapse(self, field):
        for point_x in range(
                max(int(self.x) - self.splash, 0),
                min(math.ceil(self.x) + self.splash, self.const['field_width'])
                ):
            h = math.ceil((self.splash**2 - abs(int(self.x) - point_x)**2)**0.5)
            for point_y in range(
                    max(int(self.y) - h, 0),
                    min(math.ceil(self.y) + h, self.const['field_height'])
                    ):
                field[point_x, point_y] = 0
        new_boom = Explosion(self.canvas)
        new_boom.start(self)
        self.game.boom.append(new_boom)
        return(field)
