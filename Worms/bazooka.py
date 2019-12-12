from gun import Gun

from bullet import Bullet

from constant import constant

import math

class Bazooka(Gun):
    def new_bullet(self, event, bullets):
        bullet = BazookaBullet(self, self.canvas)
        bullet.init()
        self.angle = math.atan2((event.y - bullet.y), (event.x - bullet.x))
        bullet.vx = self.power * math.cos(self.angle)
        bullet.vy = self.power * math.sin(self.angle)
        bullet.x += self.r * math.cos(self.angle)
        bullet.y += self.r * math.sin(self.angle)
        self.preparation = 0
        self.power = 0
        bullets += [bullet]
        return(bullets)

    def energy_cost(self):
        return(6)

    def drowing(self):
        self.canvas.delete(self.body_id)
        self.body_id = self.canvas.create_line(
                self.x,
                self.y,
                self.x + max(self.power, 10) * math.cos(self.angle),
                self.y + max(self.power, 10) * math.sin(self.angle),
                width=7,
                )
        if self.live < 0:
            self.canvas.delete(self.body_id)


class BazookaBullet(Bullet):
    def init(self):
        self.const = constant()
        self.splash = 20
        self.r = 5
        self.live = 1000
        self.x += self.r * math.cos(self.gun.angle)
        self.y += self.r * math.sin(self.gun.angle)
        self.color = 'blue'
        self.body_id = self.canvas.create_oval(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.color,
                )

    def damage(self, worm):
        live = worm.live
        live -= int(max(0, 1.5 * (self.splash + worm.r
            - ((self.x - worm.x)**2 + (self.y - worm.y)**2)**0.5)))
        return(live)
    
    def charge_x(self, worm):
        vx = worm.vx
        if (self.splash + worm.r)**2 > (self.x - worm.x)**2 + (self.y - worm.y)**2:
            vx += 0.15 * (self.splash + worm.r - ((self.x - worm.x)**2
                    + (self.y - worm.y)**2)**0.5) * (worm.x - self.x) / (((self.x
                    - worm.x)**2 + (self.y - worm.y)**2)**0.5 + 1)
        return(vx)

    def charge_y(self, worm):
        vy = worm.vy
        if (self.splash + worm.r)**2 > (self.x - worm.x)**2 + (self.y - worm.y)**2:
            vy += 0.15 * (self.splash + worm.r - ((self.x - worm.x)**2
                    + (self.y - worm.y)**2)**0.5) * (self.x - worm.x) / (((self.x
                    - worm.x)**2 + (self.y - worm.y)**2)**0.5 + 1)
        return(vy)
    
    def move(self, field):
        self.x += self.vx
        self.y += self.vy
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
            self.vy = 0
            self.vx = 0
            self.live = 0
        else:
            self.vy += self.const['grav_const']
        
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