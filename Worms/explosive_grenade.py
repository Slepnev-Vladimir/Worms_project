from random import randint as rnd

from gun import Gun

from bullet import Bullet

from constant import constant

import math


class ExplosiveGrenade(Gun):
    def init(self):
        self.rifle = 1

    def new_bullet(self, event, bullets):
        self.rifle -= 1
        bullet = ExplosiveGrenadeBullet(self, self.canvas, self.game)
        bullet.init()
        self.angle = math.atan2((event.y - bullet.y), (event.x - bullet.x))
        bullet.vx = self.power * math.cos(self.angle)
        bullet.vy = self.power * math.sin(self.angle)
        bullet.x += self.r * math.cos(self.angle)
        bullet.y += self.r * math.sin(self.angle)
        bullets += [bullet]

        for num in range(3):
            bullet = ExplosiveBullet(self, self.canvas, self.game)
            bullet.init()
            self.angle = math.atan2((event.y - bullet.y), (event.x - bullet.x))
            bullet.vx = self.power * math.cos(self.angle)
            bullet.vy = self.power * math.sin(self.angle)
            bullet.x += self.r * math.cos(self.angle)
            bullet.y += self.r * math.sin(self.angle)
            bullets += [bullet]

        self.preparation = 0
        self.power = 0
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


class ExplosiveGrenadeBullet(Bullet):
    def init(self):
        self.const = constant()
        self.live = 200
        self.elastic = 0.6
        self.splash = 15
        self.r = 5
        self.drag_coef = 0.99
        self.x += self.r * math.cos(self.gun.angle)
        self.y += self.r * math.sin(self.gun.angle)
        self.color = 'orange'
        self.body_id = self.canvas.create_oval(
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r,
            fill=self.color,
            )

    def damage(self, worm):
        live = worm.live
        delta = self.splash + worm.r
        dx = self.x - worm.x
        dy = self.y - worm.y
        live -= int(max(0, (delta - (dx**2 + dy**2)**0.5)))
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
            h = int((self.r**2 - abs(int(self.x) - point_x)**2)**0.5)
            dx = -int(self.x) + point_x
            for point_y in range(
                    max(int(self.y) - h, 0),
                    min(int(self.y) + h, self.const['field_height'])
                    ):
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
        if self.min_x_2 - self.min_x_1 == 0:
            cos_a = 0
        else:
            cos_a = (self.min_x_2 - self.min_x_1) / ((self.min_x_2
                                                      - self.min_x_1) ** 2 + (self.min_y_2 - self.min_y_1) ** 2) ** 0.5

        if self.min_y_2 - self.min_y_1 == 0:
            sin_a = 0
        else:
            sin_a = (self.min_y_2 - self.min_y_1) / ((self.min_x_2
                                                      - self.min_x_1) ** 2 + (self.min_y_2 - self.min_y_1) ** 2) ** 0.5

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


class ExplosiveBullet(Bullet):
    def init(self):
        self.const = constant()
        self.live = 250
        self.elastic = 0.6
        self.splash = 10
        self.r = 5
        self.drag_coef = 0.99
        self.x += self.r * math.cos(self.gun.angle)
        self.y += self.r * math.sin(self.gun.angle)
        self.color = 'orange'
        self.body_id = self.canvas.create_oval(
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r,
            fill=self.color,
            )

    def explosion(self):
        self.elastic = 0.9
        self.r = 3
        self.vx = rnd(-2, 2)
        self.vy = -rnd(1, 2)

    def damage(self, worm):
        live = worm.live
        delta = self.splash + worm.r
        dx = self.x - worm.x
        dy = self.y - worm.y
        live -= int(max(0, (delta - (dx**2 + dy**2)**0.5)))
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
            h = int((self.r**2 - abs(int(self.x) - point_x)**2)**0.5)
            dx = -int(self.x) + point_x
            for point_y in range(
                    max(int(self.y) - h, 0),
                    min(int(self.y) + h, self.const['field_height'])
                    ):
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
        if self.min_x_1 != -1 and self.min_x_2 != -1:
            self.collision()
        else:
            self.vx = (self.vx - wind) * self.drag_coef + wind
            self.vy = self.vy * self.drag_coef

    def collision(self):
        if self.min_x_2 - self.min_x_1 == 0:
            cos_a = 0
        else:
            cos_a = (self.min_x_2 - self.min_x_1) / ((self.min_x_2
                                                      - self.min_x_1) ** 2 + (self.min_y_2 - self.min_y_1) ** 2) ** 0.5

        if self.min_y_2 - self.min_y_1 == 0:
            sin_a = 0
        else:
            sin_a = (self.min_y_2 - self.min_y_1) / ((self.min_x_2
                                                      - self.min_x_1) ** 2 + (self.min_y_2 - self.min_y_1) ** 2) ** 0.5

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
        if self.live == 50:
            self.explosion()
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
