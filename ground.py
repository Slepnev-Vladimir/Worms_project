from random import choice, randint as rnd

from tkinter import Tk, Canvas, BOTH, mainloop, CENTER, Frame

root = Tk()
fr = Frame(root)
root.geometry('800x600')
canvas = Canvas(root, bg='white')
canvas.pack(fill=BOTH, expand=1)


def field_model():
    field = []

    for x in range(0, 800):
        field.append([])
        for y in range(0, 600):
            field[x].append(0)

    for x in range(100, 300):
        for y in range(150, 250):
            field[x][y] = 1

    for x in range(500, 700):
        for y in range(150, 250):
            field[x][y] = 1

    for y in range(250, 450):
        for x in range(400 - (y - 250) , 400 + (y - 250)):
            field[x][y] = 1

    for x in range(0, 800):
        for y in range(500, 600):
            field[x][y] = 1

    return(field)


def field_visual():
    land_1 = canvas.create_polygon((100, 150), (300, 150), (300, 250), (100, 250))
    land_2 = canvas.create_polygon((500, 150), (700, 150), (700, 250), (500, 250))
    land_3 = canvas.create_polygon((200, 450), (400, 250), (600, 450))
    land_4 = canvas.create_polygon((0, 500), (800, 500), (800, 600), (0, 600))


class Gun:
    def __init__(self, numb):
        self.energy = 3
        self.vx = 0
        self.vy = 0
        self.numb = numb
        self.live = 3
        self.r = 5
        self.x = rnd(20, 220) + 500 * numb            # work only for 2 players
        self.y = 0
        self.colors = ['blue', 'green', 'red', 'brown']
        self.body_id = canvas.create_oval(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.colors[self.numb])

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

        self.drowing()

    def move_left(self, event):
        if self.energy > 0:
            self.vx -= 2.5
#            self.vy -= 2.5
        #    self.energy -= 1

    def move_right(self, event):
        if self.energy > 0:
            self.vx += 2.5
#            self.vy -= 2.5
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
                fill=self.colors[self.numb])


class Bang():
    def __init__(self, field):
        self.field = field
        self.r = 15

    def collapse(self, event):
        for point_x in range(int(event.x) - self.r, int(event.x) + self.r):
            h = int((self.r**2 - abs(int(event.x) - point_x)**2)**0.5)
            for point_y in range(int(event.y) - h, int(event.y) + h):
                self.field[point_x][point_y] = 0

        self.body_id = canvas.create_oval(
                event.x - self.r,
                event.y - self.r,
                event.x + self.r,
                event.y + self.r,
                fill='white',
                outline='white',
                )

        return(self.field)


class Game():
    def __init__(self):
        self.field = field_model()
        self.is_fild = 0
        self.gun = []
        self.gun_numb = 1
        bang = Bang(self.field)

        for numb in range(self.gun_numb):
            self.gun.append(Gun(numb))

    def is_bang(self, event):
        bang = Bang(self.field)
        self.field = bang.collapse(event) 

    def main(self):
        self.gun[0].move(self.field)
        canvas.bind('<Button-1>', self.is_bang)
        canvas.bind('<Up>', self.gun[0].move_up)
        canvas.bind('<Down>', self.gun[0].move_down)
        canvas.bind('<Left>', self.gun[0].move_left)
        canvas.bind('<Right>', self.gun[0].move_right)

        root.after(30, self.main)


field_visual()
game = Game()
game.main()
mainloop()
