from random import choice, randint as rnd

from tkinter import Tk, Canvas, BOTH, mainloop, CENTER, Frame

import math

root = Tk()
fr = Frame(root)
root.geometry('800x600')
canvas = Canvas(root, bg='white')
canvas.pack(fill=BOTH, expand=1)
WARMS_NUMBER = 1

class Field:
    def __init__(self):
        self.field_list = []

    def field_model(self):
        for x in range(0, 800):
            self.field_list.append([])
            for y in range(0, 600):
                self.field_list[x].append(0)

        for x in range(100, 300):
            for y in range(150, 250):
                self.field_list[x][y] = 1

        for x in range(500, 700):
            for y in range(150, 250):
                self.field_list[x][y] = 1

        for y in range(250, 450):
            for x in range(400 - (y - 250) , 400 + (y - 250)):
                self.field_list[x][y] = 1

        for x in range(0, 800):
            for y in range(500, 600):
                self.field_list[x][y] = 1

        return(self.field_list)


    def field_visual(self):
        self.land_1 = canvas.create_polygon((100, 150), (300, 150), (300, 250), (100, 250))
        self.land_2 = canvas.create_polygon((500, 150), (700, 150), (700, 250), (500, 250))
        self.land_3 = canvas.create_polygon((200, 450), (400, 250), (600, 450))
        self.land_4 = canvas.create_polygon((0, 500), (800, 500), (800, 600), (0, 600))


class Warm:
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
        self.body_id = canvas.create_oval(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.colors[self.num])

    def move(self, field):
        self.x += self.vx
        self.y += self.vy

        is_touch = 0
        if self.y > self.r:
            for point_x in range(int(self.x) - self.r, int(self.x) + self.r):
                h = int((self.r**2 - abs(int(self.x) - point_x)**2)**0.5)
                for point_y in range(int(self.y) - h, int(self.y) + h):
                    is_touch += field[point_x][point_y]

        if is_touch != 0:
            self.vy = 0
            self.vx = 0
        else:
            self.vy += 0.1

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


class Ball():
    def __init__(self, gun):
        self.splash = 15
        self.x = gun.x
        self.y = gun.y
        self.r = 5
        self.vx = 0
        self.vy = 0
        self.color = choice(['blue', 'green', 'red', 'brown'])
        self.body_id = canvas.create_oval(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.color
        )
        self.live = 300
        self.activation = 0

    def set_coords(self):
        canvas.coords(
                self.body_id,
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r
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
                        is_touch += field[point_x][point_y]

        if is_touch != 0:
            self.vy = 0
            self.vx = 0
            self.live = 0
        else:
            self.vy += 0.1
        
        canvas.move(self.body_id, self.vx, self.vy)
        
        self.activation += 1
        self.live -= 1
        if self.live < 0:
            canvas.delete(self.body_id)

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


class Gun():
    def __init__(self, worm):
        self.worm = worm
        self.power = 10
        self.preparation = 0
        self.angle = 1
        self.x = worm.x
        self.y = worm.y
        self.balls = []
        self.body_id = canvas.create_line(
                worm.x,
                worm.y,
                worm.x + 30,
                worm.y - 30,
                width=7)

    def shot_prepair(self, event):
        self.preparation = 1

    def targetting(self, event=0):
        if event:
            self.angle = math.atan2((event.y-self.y), (event.x-self.x))
        if self.preparation:
            canvas.itemconfig(self.body_id, fill='orange')
        else:
            canvas.itemconfig(self.body_id, fill='black')

    def power_up(self):
        if self.preparation:
            if self.power < 100:
                self.power += 1
            canv.itemconfig(self.body_id, fill='orange')
        else:
            canv.itemconfig(self.body_id, fill='black')
    
    def move(self):
        self.x = self.worm.x
        self.y = self.worm.y
    
    def drowing(self):
        canvas.delete(self.body_id)
        self.body_id = canvas.create_line(
                self.x,
                self.y,
                self.x + max(self.power, 20) * math.cos(self.angle),
                self.y + max(self.power, 20) * math.sin(self.angle),
                width=7,
                )


class Game():
    def __init__(self):
        self.field = Field()
        self.field_list = self.field.field_model()
        self.is_fild = 0
        self.warms = []
        self.guns = []
        self.balls = []
        self.field.field_visual()
        self.tern = 0

        for num in range(WARMS_NUMBER):
            self.warms.append(Warm(num))
            self.guns.append(Gun(self.warms[num]))

    def bang_check(self):
        num = 0
        while num < len(self.balls):
            is_touch = 0
            if (self.balls[num].x + self.balls[num].splash < 800
                    and self.balls[num].x - self.balls[num].splash > 0
                    and self.balls[num].y + self.balls[num].splash < 600
                    and self.balls[num].y - self.balls[num].splash > 0):
                for point_x in range(int(self.balls[num].x) - self.balls[num].r,
                        int(self.balls[num].x) + self.balls[num].r):
                    h = int((self.balls[num].r**2 - abs(int(self.balls[num].x)
                        - point_x)**2)**0.5)
                    for point_y in range(int(self.balls[num].y) - h,
                            int(self.balls[num].y) + h):
                        is_touch += self.field_list[point_x][point_y]

            if is_touch != 0:
                self.collapse(num)

            if self.balls[num].live <= 0:
                self.balls.pop(num)
                print(1)
            
            num += 1
        
    def collapse(self, num):
        for point_x in range(int(self.balls[num].x) - self.balls[num].splash, int(self.balls[num].x) + self.balls[num].splash):
            h = int((self.balls[num].splash**2 - abs(int(self.balls[num].x) - point_x)**2)**0.5)
            for point_y in range(int(self.balls[num].y) - h, int(self.balls[num].y) + h):
                self.field_list[point_x][point_y] = 0

        self.body_id = canvas.create_oval(
                self.balls[num].x - self.balls[num].splash,
                self.balls[num].y - self.balls[num].splash,
                self.balls[num].x + self.balls[num].splash,
                self.balls[num].y + self.balls[num].splash,
                fill='white',
                outline='white',
                )

    def shot(self, event):
        new_ball = Ball(self.guns[self.tern % WARMS_NUMBER])
        self.angle = math.atan2((event.y - new_ball.y), (event.x - new_ball.x))
        new_ball.vx = self.guns[self.tern % WARMS_NUMBER].power * math.cos(self.angle)
        new_ball.vy = self.guns[self.tern % WARMS_NUMBER].power * math.sin(self.angle)
        self.balls += [new_ball]
        self.guns[self.tern % WARMS_NUMBER].preparation = 0
        self.guns[self.tern % WARMS_NUMBER].power = 10

    def motion(self):
        for num in range(WARMS_NUMBER):
            self.warms[num].move(self.field_list)
            self.guns[num].move()

        for num in range(len(self.balls)):
            self.balls[num].move(self.field_list)

    def visualization(self):
        for num in range(WARMS_NUMBER):
            self.warms[num].drowing()
            self.guns[num].drowing()

    def main(self):
        canvas.bind('<Motion>', self.guns[self.tern % WARMS_NUMBER].targetting)
        canvas.bind('<Button-1>', self.guns[self.tern % WARMS_NUMBER].preparation)
        canvas.bind('<ButtonRelease-1>', self.shot)
        canvas.bind('<Up>', self.warms[self.tern % WARMS_NUMBER].move_up)
        canvas.bind('<Down>', self.warms[self.tern % WARMS_NUMBER].move_down)
        canvas.bind('<Left>', self.warms[self.tern % WARMS_NUMBER].move_left)
        canvas.bind('<Right>', self.warms[self.tern % WARMS_NUMBER].move_right)
        self.motion()
        self.visualization()
        self.bang_check()

        root.after(30, self.main)


game = Game()
game.main()
mainloop()
