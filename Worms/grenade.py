from gun import Gun

from bullet import Bullet

from constant import constant

import math


class Grenade(Gun):
    def init(self):
        self.rifle = 1

    def new_bullet(self, event, bullets):
        bullet = GrenadeBullet(self, self.canvas, self.game)
        bullet.init()
        self.angle = math.atan2((event.y - bullet.y), (event.x - bullet.x))
        bullet.vx = self.power * math.cos(self.angle)
        bullet.vy = self.power * math.sin(self.angle)
        bullet.x += self.r * math.cos(self.angle)
        bullet.y += self.r * math.sin(self.angle)
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


class GrenadeBullet(Bullet):
    def init(self):
        self.min_x_1 = -1
        self.min_y_1 = -1
        self.min_x_2 = -1
        self.min_y_2 = -1

        self.const = constant()
        self.live = 200
        self.elastic = 0.6
        self.splash = 20
        self.r = 5
        self.drag_coef = 0.99
        self.x += self.r * math.cos(self.gun.angle)
        self.y += self.r * math.sin(self.gun.angle)
        self.color = 'red'
        self.body_id = self.canvas.create_oval(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.color,
                )

    def damage(self, worm):
        live = worm.live
        live -= int(
                    max(
                        0,
                        (self.splash + worm.r - ((self.x - worm.x)**2 + (self.y - worm.y)**2)**0.5)
                    )
                )
        return(live)

    def charge_x(self, worm):
        vx = worm.vx
        delta = self.splash + worm.r
        dx = self.x - worm.x
        dy = self.y - worm.y

        if delta**2 > dx**2 + dy**2:
            dr = (dx**2 + dy**2)**0.5
            vx -= 0.05 * dx / (abs(dx) + 1) * (delta - dr * dx / (dr + 1))
        return(vx)

    def charge_y(self, worm):
        vy = worm.vy
        delta = self.splash + worm.r
        dx = self.x - worm.x
        dy = self.y - worm.y

        if delta**2 > dx**2 + dy**2:
            dr = (dx**2 + dy**2)**0.5
            vy -= 0.05 * dy / (abs(dy) + 1) * (delta - dr * dy / (dr + 1))
        return(vy)

    def is_collision(self, field, wind):
        min_range_1 = self.r
        min_range_2 = self.r
        self.min_x_1 = -1
        self.min_y_1 = -1
        self.min_x_2 = -1
        self.min_y_2 = -1

        for point_x in range(
                max(int(self.x) - self.r, 0),
                min(int(self.x) + self.r, self.const['field_width'])
                ):
            dx = -int(self.x) + point_x
            h = int((self.r**2 - abs(int(self.x) - point_x)**2)**0.5)
            for point_y in range(
                    max(int(self.y) - h, 0),
                    min(int(self.y) + h, self.const['field_height'])
                    ):
                dy = point_y - self.y
                if field[point_x, point_y] != 0:
                    dy = point_y - self.y

                    if dx ** 2 + dy ** 2 < min_range_1 ** 2:
                        min_range_2 = min_range_1
                        min_range_1 = (dx ** 2 + dy ** 2) ** 0.5
                        self.min_x_2 = self.min_x_1
                        self.min_y_2 = self.min_y_1
                        self.min_x_1 = point_x
                        self.min_y_1 = point_y
                    elif dx ** 2 + dy ** 2 < min_range_2 ** 2:
                        min_range_2 = (dx ** 2 + dy ** 2) ** 0.5
                        self.min_x_2 = point_x
                        self.min_y_2 = point_y
        if self.min_x_1 != -1 and self.min_x_2 != -1:
            self.collision()
        else:
            self.vx = (self.vx - wind) * self.drag_coef + wind
            self.vy = self.vy * self.drag_coef

    def collision(self):
        dx = self.min_x_2 - self.min_x_1
        dy = self.min_y_2 - self.min_y_1
        dr = (dx**2 + dy**2)**0.5
        if dx == 0:
            cos_a = 0
        else:
            cos_a = dx / dr

        if dy == 0:
            sin_a = 0
        else:
            sin_a = dy / dr

        self.x -= self.vx
        self.y -= self.vy

        self.vy -= self.const['grav_const']
        self.vy *= self.elastic
        self.vx *= self.elastic

        instant_vx = self.vx
        self.vx = self.vx * cos_a + self.vy * sin_a
        self.vy = -instant_vx * sin_a + self.vy * cos_a

        self.vy *= -1

        instant_vx = self.vx
        self.vx = self.vx * cos_a - self.vy * sin_a
        self.vy = instant_vx * sin_a + self.vy * cos_a

        if self.vy < abs(sin_a):
            self.vy -= abs(sin_a)

    def move(self, field, wind):
        self.vy += self.const['grav_const']
        self.x += self.vx
        self.y += self.vy
        self.is_collision(field, wind)
        self.live -= 1

    def hit_test(self, obj):
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r + obj.r) ** 2:
            self.vx = 0
            self.vy = 0

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
