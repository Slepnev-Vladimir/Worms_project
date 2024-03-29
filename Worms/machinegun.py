from gun import Gun

from random import randint as rnd

from bullet import Bullet

from constant import constant

import math


class Machinegun(Gun):
    def init(self):
        self.const = constant()
        self.rifle = 50

    def new_bullet(self, event, bullets):
        bullet = MachinegunBullet(self, self.canvas, self.game)
        bullet.init()
        self.angle = (math.atan2((event.y - bullet.y), (event.x - bullet.x))
                      + rnd(-15, 15) / 100)
        bullet.vx = 5 * math.cos(self.angle)
        bullet.vy = 5 * math.sin(self.angle)
        bullet.x += self.r * math.cos(self.angle)
        bullet.y += self.r * math.sin(self.angle)
        self.preparation = 0
        bullets += [bullet]
        self.rifle -= 1
        return(bullets)

    def reloading(self):
        self.rifle = 50

    def en_cost(self):
        return(600)

    def drowing(self):
        self.canvas.delete(self.body_id)
        self.body_id = self.canvas.create_line(
            self.x,
            self.y,
            self.x + max(self.power, 10) * math.cos(self.angle),
            self.y + max(self.power, 10) * math.sin(self.angle),
            width=7,
            )
        if self.worm.live < 0:
            self.canvas.delete(self.body_id)


class MachinegunBullet(Bullet):
    def init(self):
        self.const = constant()
        self.splash = 5
        self.r = 2
        self.drag_coef = 0.997
        self.live = 1000
        self.x += self.r * math.cos(self.gun.angle)
        self.y += self.r * math.sin(self.gun.angle)
        if self.vx != 0:
            self.angle = math.atan2(self.vy, self.vx)
        self.color = 'green'
        self.body_id = self.canvas.create_oval(
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r,
            fill=self.color,
            )

    def damage(self, worm):
        live = worm.live
        if (self.x - worm.x) ** 2 + (self.y - worm.y) ** 2 <= (self.r + worm.r) ** 2:
            live -= 1
        return(live)

    def charge_x(self, worm):
        vx = worm.vx
        delta = self.splash + worm.r
        dx = self.x - worm.x
        dy = self.y - worm.y

        if delta**2 > dx**2 + dy**2:
            dr = (dx**2 + dy**2)**0.5
            vx -= 0.01 * dx / abs(dx) * (delta - dr * dx / (dr + 1))
        return(vx)

    def charge_y(self, worm):
        vy = worm.vy
        delta = self.splash + worm.r
        dx = self.x - worm.x
        dy = self.y - worm.y

        if delta**2 > dx**2 + dy**2:
            dr = (dx**2 + dy**2)**0.5
            vy -= 0.01 * dx / abs(dx) * (delta - dr * dy / (dr + 1))
        return(vy)

    def move(self, field, wind):
        self.x += self.vx
        self.y += self.vy
        if self.vx != 0:
            self.angle = math.atan2(self.vy, self.vx)
        is_touch = 0

        for point_x in range(
                max(int(self.x) - self.r, 0),
                min(int(self.x) + self.r, self.const['field_width'])
                ):
            h = int((self.r**2 - abs(int(self.x) - point_x)**2)**0.5)
            for point_y in range(
                    max(int(self.y) - h, 0),
                    min(int(self.y) + h, self.const['field_height'])
                    ):
                is_touch += field[point_x, point_y]

        if is_touch != 0:
            self.live = 0
        else:
            self.vy += self.const['grav_const'] / 2
            self.vx = (self.vx - wind) * self.drag_coef + wind
            self.vy = self.vy * self.drag_coef
        self.live -= 1

    def hit_test(self, obj):
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r + obj.r) ** 2:
            self.live = 0

    def drowing(self):
        self.canvas.delete(self.body_id)
        self.body_id = self.canvas.create_oval(
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r,
            fill=self.color,
            )
        if self.live < 0:
            self.canvas.delete(self.body_id)
