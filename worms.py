from random import choice, randint as rnd

from tkinter import Tk, Canvas, BOTH, mainloop, CENTER, Frame

import math

import numpy

root = Tk()
fr = Frame(root)
root.geometry('800x600')
canvas = Canvas(root, bg='white')
canvas.pack(fill=BOTH, expand=1)
WORMS_NUMBER = 2
UPDATE_TIME = 30
GRAV_CONST = 0.1
WORM_ENERGY = 10


class Field:
    def __init__(self):
        self.field_list = numpy.zeros((800, 600))

    def field_model(self):
        for x in range(100, 300):
            for y in range(100, 200):
                self.field_list[x, y] = 1

        for x in range(500, 700):
            for y in range(100, 200):
                self.field_list[x, y] = 1

        for y in range(200, 400):
            for x in range(400 - (y - 200) , 400 + (y - 200)):
                self.field_list[x, y] = 1

        for x in range(0, 800):
            for y in range(450, 600):
                self.field_list[x, y] = 1

        return(self.field_list)


    def field_visual(self):
        self.land_1 = canvas.create_polygon((100, 100), (300, 100), (300, 200), (100, 200))
        self.land_2 = canvas.create_polygon((500, 100), (700, 100), (700, 200), (500, 200))
        self.land_3 = canvas.create_polygon((200, 400), (400, 200), (600, 400))
        self.land_4 = canvas.create_polygon((0, 450), (800, 450), (800, 600), (0, 600))


class Worm:
    def __init__(self, num):
        self.is_touch = 0
        self.energy = WORM_ENERGY
        self.vx = 0
        self.vy = 0
        self.num = num
        self.live = 100
        self.r = 10                                 # if change, change move
        self.x = rnd(20, 220) + 500 * num           # work only for 2 players
        self.y = 20
        self.colors = ['blue', 'green', 'red', 'brown']
        self.gun = Bazooka(self)
        self.body_id = canvas.create_oval(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.colors[self.num])

    def choose_bazooka(self, event):
        canvas.delete(self.gun.body_id)
        self.gun = Bazooka(self)

    def choose_grenade(self, event):
        canvas.delete(self.gun.body_id)
        self.gun = Grenade(self)
    
    def move(self, field):
        self.x += self.vx
        self.y += self.vy

        self.is_touch = 0
        if (self.x + self.r < 800 
                and self.x - self.r > 0
                and self.y + self.r < 600
                and self.y - self.r > 0): 
            for point_x in range(int(self.x) - self.r, int(self.x) + self.r):
                h = int((self.r**2 - abs(int(self.x) - point_x)**2)**0.5)
                for point_y in range(int(self.y) - h, int(self.y) + h):
                    self.is_touch += field[point_x, point_y]
        else:
            self.live -= 1
        
        if self.is_touch == 296:            # depends on the size of the worm
            self.live -= 1
        
        if self.is_touch != 0:
            self.vy = 0
            self.vx = 0
        else:
            self.vy += GRAV_CONST

        self.gun.move()

    def move_left(self, event):
        if self.is_touch == 0:
            if self.energy >= 3:
                self.vx -= 2
                self.vy -= 2
                self.energy -= 3
        elif self.energy >= 1:
            self.energy -= 1
            self.vx -= 2
            self.vy -= 2
        print('energy = ', self.energy)

    def move_right(self, event):
        if self.is_touch == 0:
            if self.energy >= 3:
                self.vx += 2
                self.vy -= 2
                self.energy -= 3
        elif self.energy >= 1:
            self.energy -= 1
            self.vx += 2
            self.vy -= 2
        print('energy = ', self.energy)

    def move_up(self, event):
        if self.is_touch == 0:
            if self.energy >= 3:
                self.vy -= 2
                self.energy -= 3
        elif self.energy >= 1:
            self.energy -= 1
            self.vy -= 2
        print('energy = ', self.energy)

    def move_down(self, event):
        if self.is_touch == 0:
            if self.energy >= 3:
                self.vy += 2
                self.energy -= 3
        elif self.energy >= 1:
            self.energy -= 1
            self.vy += 2
        print('energy = ', self.energy)

    def drowing(self):
        canvas.delete(self.body_id)
        self.body_id = canvas.create_oval(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.colors[self.num])
        self.gun.drowing()
        if self.live < 0:
            canvas.delete(self.body_id)


class Gun():
    def __init__(self, worm):
        self.worm = worm
        self.live = self.worm.live
        self.power = 0
        self.preparation = 0
        self.angle = 0
        self.r = worm.r              # need to create bullet
        self.y = worm.y
        self.x = worm.x
        self.body_id = canvas.create_line(
                self.x,
                self.y,
                self.x + 20,
                self.y - 20,
                width=7)

    def shot_prepair(self, event):
        if (self.worm.energy >= self.worm.gun.energy_cost()
                and self.preparation != 1):
            self.preparation = 1
            self.worm.energy -= self.worm.gun.energy_cost()
            print('energy = ', self.worm.energy)

    def targetting(self, event=0):
        if event:
            self.angle = math.atan2((event.y - self.y), (event.x - self.x))
        if self.preparation:
            canvas.itemconfig(self.body_id, fill='orange')
        else:
            canvas.itemconfig(self.body_id, fill='black')

    def power_up(self):
        if self.preparation == 1:
            if self.power < 10:
                self.power += 0.5
            canvas.itemconfig(self.body_id, fill='orange')
        else:
            canvas.itemconfig(self.body_id, fill='black')
    
    def move(self):
        self.x = self.worm.x
        self.y = self.worm.y
        self.live = self.worm.live
    

class Bazooka(Gun):
    def new_bullet(self, event, bullets):
        bullet = BazookaBullet(self)
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
        canvas.delete(self.body_id)
        self.body_id = canvas.create_line(
                self.x,
                self.y,
                self.x + max(self.power, 10) * math.cos(self.angle),
                self.y + max(self.power, 10) * math.sin(self.angle),
                width=7,
                )
        if self.live < 0:
            canvas.delete(self.body_id)


class Grenade(Gun):
    def new_bullet(self, event, bullets):
        bullet = GrenadeBullet(self)
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
        canvas.delete(self.body_id)
        self.body_id = canvas.create_line(
                self.x,
                self.y,
                self.x + max(self.power, 10) * math.cos(self.angle),
                self.y + max(self.power, 10) * math.sin(self.angle),
                width=7,
                )
        if self.live < 0:
            canvas.delete(self.body_id)


class Bullet():
    def __init__(self, gun):
        self.gun = gun
        self.splash = 0
        self.x = gun.x
        self.y = gun.y
        self.r = 0
        self.vx = 0
        self.vy = 0
        self.color = 'blue'
        self.body_id = 0
        self.activation = 0

    def collapse(self, field):
        for point_x in range(int(self.x) - self.splash,
                int(self.x) + self.splash):
            h = int((self.splash**2 - abs(int(self.x) - point_x)**2)**0.5)
            for point_y in range(int(self.y) - h, int(self.y) + h):
                field[point_x, point_y] = 0

        self.body_id = canvas.create_oval(
                self.x - self.splash,
                self.y - self.splash,
                self.x + self.splash,
                self.y + self.splash,
                fill='white',
                outline='white',
                )
        return(field)


class BazookaBullet(Bullet):
    def init(self):
        self.splash = 20
        self.r = 5
        self.live = 1000
        self.x += self.r * math.cos(self.gun.angle)
        self.y += self.r * math.sin(self.gun.angle)
        self.color = 'blue'
        self.body_id = canvas.create_oval(
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
            self.vy += GRAV_CONST
        
        self.live -= 1

    def hit_test(self, obj):
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r + obj.r) ** 2:
            self.live = 0
   
    def drowing(self):
        canvas.delete(self.body_id)
        self.body_id = canvas.create_oval(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.color,
                )
        if self.live < 0:
            canvas.delete(self.body_id)


class GrenadeBullet(Bullet):
    def init(self):
        self.live = 200
        self.elastic = 0.6
        self.splash = 20
        self.r = 5
        self.x += self.r * math.cos(self.gun.angle)
        self.y += self.r * math.sin(self.gun.angle)
        self.color = 'red'
        self.body_id = canvas.create_oval(
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
    
    def is_collision(self, field):
        if (self.x + self.splash < 800
                and self.x - self.splash > 0
                and self.y + self.splash < 600
                and self.y - self.splash > 0): 
            min_range_1 = self.r
            min_range_2 = self.r
            self.min_x_1 = -1
            self.min_y_1 = -1
            self.min_x_2 = -1
            self.min_y_2 = -1

            for point_x in range(int(self.x) - self.r, int(self.x) + self.r):
                dx = -int(self.x) + point_x
                h = int((self.r**2 - abs(int(dx)**2)**0.5))
                for point_y in range(int(self.y) - h, int(self.y) + h):
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
                            self.min_y_2= point_y
        if self.min_x_1 != -1 and self.min_x_2 != -1:
            self.collision()

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

        self.vy -= GRAV_CONST
        self.vy *= self.elastic
        self.vx *= self.elastic
        
        instant_vx = self.vx
        self.vx = self.vx * cos_a + self.vy * sin_a
        self.vy = -instant_vx * sin_a + self.vy * cos_a
        
        self.vy *= -1
        
        instant_vx = self.vx
        self.vx = self.vx * cos_a - self.vy * sin_a
        self.vy = instant_vx * sin_a + self.vy * cos_a

    def move(self, field):
        self.vy += GRAV_CONST
        self.x += self.vx
        self.y += self.vy
        self.is_collision(field)
        self.live -= 1
   
    def hit_test(self, obj):
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r + obj.r) ** 2:
            self.vx = 0
            self.vy = 0
    
    def drowing(self):
        canvas.delete(self.body_id)
        self.body_id = canvas.create_oval(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.color,
                )
        if self.live < 0:
            canvas.delete(self.body_id)


class Game():
    def __init__(self):
        self.field = Field()
        self.field_list = self.field.field_model()
        self.is_fild = 0
        self.worms = []
        self.guns = []
        self.bullets = []
        self.field.field_visual()
        self.tern = 0
        self.worms_number = WORMS_NUMBER

        for num in range(WORMS_NUMBER):
            self.worms.append(Worm(num))

    def bang_check(self):
        num = 0
        while num < len(self.bullets):
            if self.bullets[num].live <= 0:
                if (self.bullets[num].x + self.bullets[num].splash < 800 
                        and self.bullets[num].x - self.bullets[num].splash > 0
                        and self.bullets[num].y + self.bullets[num].splash < 600
                        and self.bullets[num].y - self.bullets[num].splash > 0): 
                    self.field_list = self.bullets[num].collapse(self.field_list)
                    for worm in self.worms:
                        worm.live = self.bullets[num].damage(worm)
                        worm.vx = self.bullets[num].charge_x(worm)
                        worm.vy = self.bullets[num].charge_y(worm)
                        print('hp = ', worm.live)
                self.bullets.pop(num)
            num += 1
            
        num = 0
        while num < len(self.worms):
            if self.worms[num].live <= 0:
                self.worms.pop(num)
                self.worms_number -= 1
            num += 1
    
    def is_hit(self):
        for worm in self.worms:
            for bullet in self.bullets:
                bullet.hit_test(worm)

    def next_tern(self):
        self.tern += 1
        self.tern = self.tern % self.worms_number
        for worm in self.worms:
            worm.energy = WORM_ENERGY
        print('next tern, tern = ', self.tern)

    def shot(self, event):
        if self.worms[self.tern].gun.preparation == 1:
            self.bullets = self.worms[self.tern].gun.new_bullet(event, self.bullets)

    def motion(self):
        for num in range(self.worms_number):
            self.worms[num].move(self.field_list)

        for num in range(len(self.bullets)):
            self.bullets[num].move(self.field_list)

    def visualization(self):
        for num in range(self.worms_number):
            self.worms[num].drowing()

        for bullet in self.bullets:
            bullet.drowing()

    def shooting_processing(self):
        canvas.bind('<Motion>', self.worms[self.tern].gun.targetting)
        canvas.bind('<Button-1>', self.worms[self.tern].gun.shot_prepair)
        self.worms[self.tern].gun.power_up()
        canvas.bind('<ButtonRelease-1>', self.shot)

    def walking_processing(self):
        canvas.bind('<Up>', self.worms[self.tern].move_up)
        canvas.bind('<Down>', self.worms[self.tern].move_down)
        canvas.bind('<Left>', self.worms[self.tern].move_left)
        canvas.bind('<Right>', self.worms[self.tern].move_right)

    def choose_weapon(self):
        canvas.bind('<q>', self.worms[self.tern].choose_bazooka)
        canvas.bind('<w>', self.worms[self.tern].choose_grenade)

    def pass_tern(self, event):
        self.worms[self.tern].energy = 0

    def main(self):
        self.shooting_processing()
        self.walking_processing()
        self.choose_weapon()
        self.motion()
        self.visualization()
        self.bang_check()
        self.is_hit()
        canvas.bind('<p>', self.pass_tern)


        if self.worms_number > 1:
            if (self.worms[self.tern].energy <= 0
                    and self.worms[self.tern].gun.preparation == 0):
                self.next_tern()
            root.after(UPDATE_TIME, self.main)
        else:
            print('gg wp')


game = Game()
game.main()
mainloop()
