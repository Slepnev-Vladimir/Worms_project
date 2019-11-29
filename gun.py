from random import randrange as rnd, choice
import tkinter as tk
import math
import time

root = tk.Tk()
fr = tk.Frame(root)
root.geometry('800x600')
canv = tk.Canvas(root, bg='white')
canv.pack(fill=tk.BOTH, expand=1)

class worm():
    def __init__(self):
        self.x = 50
        self.y = 400
        self.vx = 1
        self.vy = 0
        self.r = 15
        self.live = 3
        self.id = canv.create_oval(
				self.x - self.r,
				self.y - self.r,
				self.x + self.r,
				self.y + self.r,
				fill = 'red'
		)
    def move(self):
        if self.live:
            self.x += self.vx
            self.y += self.vy
            canv.move(self.id, self.vx, self.vy)
        else:
            canv.coords(self.id, -10, -10, -10, -10)
            self.x = -10
            self.y = -10
    def hit(self):
        self.live -= 1


class ball():
    def __init__(self, g):
        """ Конструктор класса ball

        Args:
        g - пушка, из которой производится выстрел
        """
        self.x = g.x
        self.y = g.y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(['blue', 'green', 'red', 'brown'])
        self.id = canv.create_oval(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.color
        )
        self.live = 300
        self.activation = 0

    def set_coords(self):
        canv.coords(
                self.id,
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r
        )

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.vx -= self.vx * 0.01
        self.vy += 0.2
        self.vy -= self.vy * 0.01
        if (self.x >= 800 - self.r and self.vx > 0) or (self.x <= self.r and self.vx < 0) :
            self.vx = - self.vx * 0.75
        if (self.y >= 600 - self.r and self.vy > 0) or (self.y <= self.r and self.vy <0) :
            self.vy = - self.vy * 0.75
        self.x += self.vx
        self.y += self.vy
        canv.move(self.id, self.vx, self.vy)
        self.activation += 1
        self.live -= 1
        if self.live < 0:
            canv.delete(self.id)

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



class gun():
    def __init__(self, w) :
        """w - червячок, который держит оружие"""
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.x = w.x
        self.y = w.y
        self.balls = []
        self.id = canv.create_line(w.x, w.y, w.x + 30, w.y - 30, width=7)

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        new_ball = ball(self)
        new_ball.r += 5
        self.an = math.atan2((event.y-new_ball.y), (event.x-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = self.f2_power * math.sin(self.an)
        self.balls += [new_ball]
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event=0):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan2((event.y-self.y), (event.x-self.x))
        if self.f2_on:
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')
        canv.coords(self.id, self.x, self.y,
                    self.x + max(self.f2_power, 20) * math.cos(self.an),
                    self.y + max(self.f2_power, 20) * math.sin(self.an)
                    )

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')

    def move(self, w):
        self.x = w.x
        self.y = w.y


def new_game(event=''):
    g1.balls = []
    g2.balls
    root.bind('<s>', switch)
    canv.bind('<Button-1>', g1.fire2_start)
    canv.bind('<ButtonRelease-1>', g1.fire2_end)
    canv.bind('<Motion>', g1.targetting)
    root.bind('<r>', replay)
    while True:
        for b in g1.balls:
            b.move()
            if b.hittest(w1) and w1.live:
                b.live = 0
                w1.hit()
            if b.hittest(w2) and w2.live:
                b.live = 0
                w2.hit()
        for b in g2.balls:
            b.move()
            if b.hittest(w1) and w1.live:
                b.live = 0
                w1.hit()
            if b.hittest(w2) and w2.live:
                b.live = 0
                w2.hit()
        canv.update()
        time.sleep(0.03)
        w1.move()
        w2.move()
        g1.move(w1)
        g2.move(w2)
        g1.targetting()
        g1.power_up()
        g2.targetting()
        g2.power_up()
    canv.delete(gun)
    root.after(3000, new_game)


def switch(event):
    global switch_count
    if switch_count % 2 == 0:
        canv.bind('<Button-1>', g1.fire2_start)
        canv.bind('<ButtonRelease-1>', g1.fire2_end)
        canv.bind('<Motion>', g1.targetting)
    else:
        canv.bind('<Button-1>', g2.fire2_start)
        canv.bind('<ButtonRelease-1>', g2.fire2_end)
        canv.bind('<Motion>', g2.targetting)
    switch_count += 1

def replay(event):
	print(event.keycode)

switch_count = 1
balls = []
w1 = worm()
w2 = worm()
w2.vx = 0
g1 = gun(w1)
g2 = gun(w2)
new_game()

tk.mainloop()
