from gun import Gun

from bullet import Bullet

from constant import constant

import math


class Bazooka(Gun):
    def init(self):
        self.rifle = 1

    def new_bullet(self, event, bullets):
        bullet = BazookaBullet(self, self.canvas, self.game)
        bullet.init()
        self.angle = math.atan2((event.y - bullet.y), (event.x - bullet.x))
        bullet.vx = self.power * math.cos(self.angle)
        bullet.v0x = bullet.vx
        bullet.vy = self.power * math.sin(self.angle)
        bullet.x += self.r * math.cos(self.angle)
        bullet.y += self.r * math.sin(self.angle)
        bullet.power = self.power
        bullet.drag_coef = (bullet.power / bullet.maxpower) * 0.05 + 0.95
        self.preparation = 0
        self.power = 0
        bullets += [bullet]
        self.rifle -= 1
        return(bullets)

    def reloading(self):
        self.rifle = 1

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


class BazookaBullet(Bullet):
    def init(self):
        self.const = constant()
        self.splash = 20
        self.r = 5
        self.drag_coef = 0.99
        self.live = 1000
        self.x += self.r * math.cos(self.gun.angle)
        self.y += self.r * math.sin(self.gun.angle)
        self.angle = self.gun.angle
        self.color = 'blue'
        self.fuel_length = 0
        self.power = 0
        self.maxpower = 10
        self.body_id = self.canvas.create_polygon(
            (self.x + self.r * math.cos(self.angle),
             self.y + self.r * math.sin(self.angle)),
            (self.x - (math.cos(self.angle) + 0.5 * math.sin(self.angle)) * self.r * 3,
             self.y - (math.sin(self.angle) - 0.5 * math.cos(self.angle)) * self.r * 3),
            (self.x - (math.cos(self.angle) - 0.5 * math.sin(self.angle)) * self.r * 3,
             self.y - (math.sin(self.angle) + 0.5 * math.cos(self.angle)) * self.r * 3),
            fill=self.color
        )
        self.fuel_id = self.canvas.create_polygon(
            (self.x + self.r * math.cos(self.angle),
             self.y + self.r * math.sin(self.angle)),
            (self.x - (math.cos(self.angle) + 0.5 * math.sin(self.angle)) * self.r * 3,
             self.y - (math.sin(self.angle) - 0.5 * math.cos(self.angle)) * self.r * 3),
            (self.x - (math.cos(self.angle) - 0.5 * math.sin(self.angle)) * self.r * 3,
             self.y - (math.sin(self.angle) + 0.5 * math.cos(self.angle)) * self.r * 3),
            fill=self.color
        )

    def damage(self, worm):
        live = worm.live
        live -= int(max(0, 1.5 * (self.splash + worm.r
                                  - ((self.x - worm.x)**2 + (self.y - worm.y)**2)**0.5)))
        return(live)

    def charge_x(self, worm):
        vx = worm.vx
        delta = self.splash + worm.r
        dx = self.x - worm.x
        dy = self.y - worm.y

        if delta**2 > dx**2 + dy**2:
            dr = (dx**2 + dy**2)**0.5
            vx += 0.15 * (delta - dr * dx / (dr + 1))
        return(vx)

    def charge_y(self, worm):
        vy = worm.vy
        delta = self.splash + worm.r
        dx = self.x - worm.x
        dy = self.y - worm.y

        if delta**2 > dx**2 + dy**2:
            dr = (dx**2 + dy**2)**0.5
            vy += 0.15 * (delta - dr * dy / (dr + 1))
        return(vy)

    def move(self, field, wind):
        self.x += self.vx
        self.y += self.vy
        if self.vx != 0:
            self.angle = math.atan2(self.vy, self.v0x)
        is_touch = 0

        if (self.x + self.splash < 800
                and self.x - self.splash > 0
                and self.y + self.splash < 600
                and self.y - self.splash > 0):
            if self.y > self.r:
                for point_x in range(int(self.x) - self.r, int(self.x) + self.r):
                    h = int((self.r**2 - abs(int(self.x) - point_x)**2)**0.5)
                    for point_y in range(int(self.y) - h, int(self.y) + h):
                        is_touch += field[point_x, point_y]

        if is_touch != 0:
            self.live = 0
        else:
            self.vy += self.const['grav_const']
            self.vx = (self.vx - wind) * self.drag_coef + wind
            self.vy = self.vy * self.drag_coef

        self.live -= 1

    def hit_test(self, obj):
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r + obj.r) ** 2:
            self.live = 0

    def drowing(self):
        c = math.cos(self.angle)
        s = math.sin(self.angle)

        self.canvas.delete(self.body_id)
        self.canvas.delete(self.fuel_id)
        self.body_id = self.canvas.create_polygon(
            (self.x + self.r * math.cos(self.angle),
             self.y + self.r * math.sin(self.angle)),
            (self.x - (math.cos(self.angle) + 0.5 * math.sin(self.angle)) * self.r * 3,
             self.y - (math.sin(self.angle) - 0.5 * math.cos(self.angle)) * self.r * 3),
            (self.x - (math.cos(self.angle) - 0.5 * math.sin(self.angle)) * self.r * 3,
             self.y - (math.sin(self.angle) + 0.5 * math.cos(self.angle)) * self.r * 3),
            fill=self.color
        )
        if self.live < 990 and self.live > 0:
            self.fuel_id = self.canvas.create_polygon(
                (self.x - self.r * c,
                 self.y - self.r * s),
                (self.x - self.r * c - (c + 0.1 * s) * self.r * self.power,
                 self.y - self.r * s - (s - 0.1 * c) * self.r * self.power),
                (self.x - self.r * c - (c - 0.1 * s) * self.r * self.power,
                 self.y - self.r * s - (s + 0.1 * c) * self.r * self.power),
                fill='orange'
            )
        elif self.live > 0:
            self.fuel_id = self.canvas.create_polygon(
                (self.x - self.r * c,
                 self.y - self.r * s),
                (self.x - self.r * c - (c + 0.1 * s) * self.r * self.fuel_length * self.power,
                 self.y - self.r * s - (s - 0.1 * c) * self.r * self.fuel_length * self.power),
                (self.x - self.r * c - (c - 0.1 * s) * self.r * self.fuel_length * self.power,
                 self.y - self.r * s - (s + 0.1 * c) * self.r * self.fuel_length * self.power),
                fill='orange'
            )
            self.fuel_length += 0.1
        else:
            self.canvas.delete(self.body_id)
            self.canvas.delete(self.fuel_id)
