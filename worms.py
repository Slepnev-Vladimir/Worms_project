from random import choice, randint as rnd

from tkinter import Tk, Canvas, BOTH, mainloop, CENTER, Frame

import math

import numpy

root = Tk()
fr = Frame(root)
root.geometry('800x600')
canvas = Canvas(root, bg='white')
canvas.pack(fill=BOTH, expand=1)
WORMS_NUMBER = 1
UPDATE_TIME = 30


class Field:
    def __init__(self):
        self.field_list = numpy.zeros((800, 600))

    def field_model(self):
        for x in range(100, 300):
            for y in range(150, 250):
                self.field_list[x, y] = 1

        for x in range(500, 700):
            for y in range(150, 250):
                self.field_list[x, y] = 1

        for y in range(250, 450):
            for x in range(400 - (y - 250) , 400 + (y - 250)):
                self.field_list[x, y] = 1

        for x in range(0, 800):
            for y in range(500, 600):
                self.field_list[x, y] = 1

        return(self.field_list)


    def field_visual(self):
        self.land_1 = canvas.create_polygon((100, 150), (300, 150), (300, 250), (100, 250))
        self.land_2 = canvas.create_polygon((500, 150), (700, 150), (700, 250), (500, 250))
        self.land_3 = canvas.create_polygon((200, 450), (400, 250), (600, 450))
        self.land_4 = canvas.create_polygon((0, 500), (800, 500), (800, 600), (0, 600))


class Worm:
    def __init__(self, num):
        self.energy = 3
        self.vx = 0
        self.vy = 0
        self.num = num
        self.live = 3
        self.r = 10
        self.x = rnd(20, 220) + 500 * num            # work only for 2 players
        self.y = 0
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

    def choose_bazooka1(self, event):
        canvas.delete(self.gun.body_id)
        self.gun = Bazooka1(self)
    
    def move(self, field):
        self.x += self.vx
        self.y += self.vy

        is_touch = 0
        if self.y > self.r:
            for point_x in range(int(self.x) - self.r, int(self.x) + self.r):
                h = int((self.r**2 - abs(int(self.x) - point_x)**2)**0.5)
                for point_y in range(int(self.y) - h, int(self.y) + h):
                    is_touch += field[point_x, point_y]

        if is_touch != 0:
            self.vy = 0
            self.vx = 0
        else:
            self.vy += 0.1

        self.gun.move()

    def move_left(self, event):
        if self.energy > 0:
            self.vx -= 2.5
            self.vy -= 2.5
        #    self.energy -= 1

    def move_right(self, event):
        if self.energy > 0:
            self.vx += 2.5
            self.vy -= 2.5
        #    self.energy -= 1

    def move_up(self, event):
        if self.energy > 0:
            self.vy -= 2.5
        #    self.energy -= 1

    def move_down(self, event):
        if self.energy > 0:
            self.vy += 2.5
        #    self.energy -= 1

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
        self.y = worm.y
        self.x = worm.x
        self.body_id = canvas.create_line(
                self.x,
                self.y,
                self.x + 20,
                self.y - 20,
                width=7)

    def shot_prepair(self, event):
        self.preparation = 1

    def targetting(self, event=0):
        if event:
            self.angle = math.atan2((event.y - self.y), (event.x - self.x))
        if self.preparation:
            canvas.itemconfig(self.body_id, fill='orange')
        else:
            canvas.itemconfig(self.body_id, fill='black')

    def power_up(self):
        if self.preparation == 1:
            if self.power < 30:
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
        self.preparation = 0
        self.power = 0
        bullets += [bullet]
        return(bullets)

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


class Bazooka1(Gun):
    def new_bullet(self, event, bullets):
        bullet = BazookaBullet1(self)
        bullet.init()
        self.angle = math.atan2((event.y - bullet.y), (event.x - bullet.x))
        bullet.vx = self.power * math.cos(self.angle)
        bullet.vy = self.power * math.sin(self.angle)
        self.preparation = 0
        self.power = 0
        bullets += [bullet]
        return(bullets)

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
        self.splash = 0
        self.x = gun.x
        self.y = gun.y
        self.r = 0
        self.vx = 0
        self.vy = 0
        self.color = 'blue'
        self.body_id = 0
        self.live = 100
        self.activation = 0

    def collapse(self, num, field):
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

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r + obj.r) ** 2 and self.live > 0 and self.activation > 3:
            self.live = 0
            return True
        else:
            return False


class BazookaBullet(Bullet):
    def init(self):
        self.splash = 15
        self.r = 5
        self.color = 'blue'
        self.body_id = canvas.create_oval(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.color,
                )

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
            self.vy += 0.1
        
        self.live -= 1
   
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


class BazookaBullet1(Bullet):
    def init(self):
        self.splash = 30
        self.r = 5
        self.color = 'red'
        self.body_id = canvas.create_oval(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.color,
                )

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
            self.vy += 0.1
        
        self.live -= 1
   
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

        for num in range(WORMS_NUMBER):
            self.worms.append(Worm(num))

    def bang_check(self):
        num = 0
        while num < len(self.bullets):
            is_touch = 0
            if (self.bullets[num].x + self.bullets[num].splash < 800
                    and self.bullets[num].x - self.bullets[num].splash > 0
                    and self.bullets[num].y + self.bullets[num].splash < 600
                    and self.bullets[num].y - self.bullets[num].splash > 0):
                for point_x in range(int(self.bullets[num].x) - self.bullets[num].r,
                        int(self.bullets[num].x) + self.bullets[num].r):
                    h = int((self.bullets[num].r**2 - abs(int(self.bullets[num].x)
                        - point_x)**2)**0.5)
                    for point_y in range(int(self.bullets[num].y) - h,
                            int(self.bullets[num].y) + h):
                        is_touch += self.field_list[point_x, point_y]

                if is_touch != 0:
                    self.field_list = self.bullets[num].collapse(num, self.field_list)

                if self.bullets[num].live <= 0:
                    self.field_list = self.bullets[num].collapse(num, self.field_list)
            if self.bullets[num].live <= 0:
                self.bullets.pop(num)
            
            num += 1

    def shot(self, event):
        self.bullets = self.worms[self.tern % WORMS_NUMBER].gun.new_bullet(event, self.bullets)
        self.tern += 1

    def motion(self):
        for num in range(WORMS_NUMBER):
            self.worms[num].move(self.field_list)

        for num in range(len(self.bullets)):
            self.bullets[num].move(self.field_list)

    def visualization(self):
        for num in range(WORMS_NUMBER):
            self.worms[num].drowing()

        for bullet in self.bullets:
            bullet.drowing()

    def shooting_processing(self):
        canvas.bind('<Motion>', self.worms[self.tern % WORMS_NUMBER].gun.targetting)
        canvas.bind('<Button-1>', self.worms[self.tern % WORMS_NUMBER].gun.shot_prepair)
        self.worms[self.tern % WORMS_NUMBER].gun.power_up()
        canvas.bind('<ButtonRelease-1>', self.shot)

    def walking_processing(self):
        canvas.bind('<Up>', self.worms[self.tern % WORMS_NUMBER].move_up)
        canvas.bind('<Up>', self.worms[self.tern % WORMS_NUMBER].move_up)
        canvas.bind('<Up>', self.worms[self.tern % WORMS_NUMBER].move_up)
        canvas.bind('<Down>', self.worms[self.tern % WORMS_NUMBER].move_down)
        canvas.bind('<Left>', self.worms[self.tern % WORMS_NUMBER].move_left)
        canvas.bind('<Right>', self.worms[self.tern % WORMS_NUMBER].move_right)

    def choose_weapon(self):
        canvas.bind('<q>', self.worms[self.tern % WORMS_NUMBER].choose_bazooka)
        canvas.bind('<w>', self.worms[self.tern % WORMS_NUMBER].choose_bazooka1)

    def main(self):
        self.shooting_processing()
        self.walking_processing()
        self.choose_weapon()
        self.motion()
        self.visualization()
        self.bang_check()
        root.after(UPDATE_TIME, self.main)


game = Game()
game.main()
mainloop()
