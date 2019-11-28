from random import randrange as rnd, choice
import tkinter as tk
import math
import time

root = tk.Tk()
fr = tk.Frame(root)
root.geometry('800x600')
canv = tk.Canvas(root, bg='white')
canv.pack(fill=tk.BOTH, expand=1)


class ball():
    def __init__(self, g):
        """ Конструктор класса ball

        Args:
        g - пушка, из которой производится выстрел
        """
        self.x = g.xgun
        self.y = g.ygun
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
        self.live = 30

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
            self.vx = - self.vx * 0.9
        if (self.y >= 600 - self.r and self.vy > 0) or (self.y <= self.r and self.vy <0) :
            self.vy = - self.vy * 0.9
        self.x += self.vx
        self.y += self.vy
        canv.move(self.id, self.vx, self.vy)

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r + obj.r) ** 2 :
            return True
        else :
            return False


class gun():
    def __init__(self) :
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.xgun = 40
        self.ygun = 450
        self.id = canv.create_line(20,450,50,420,width=7)

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = ball(self)
        new_ball.r += 5
        self.an = math.atan2((event.y-new_ball.y), (event.x-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = self.f2_power * math.sin(self.an)
        balls += [new_ball]
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event=0):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan2((event.y-self.ygun), (event.x-self.xgun))
        if self.f2_on:
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')
        canv.coords(self.id, self.xgun, self.ygun,
                    self.xgun + max(self.f2_power, 20) * math.cos(self.an),
                    self.ygun + max(self.f2_power, 20) * math.sin(self.an)
                    )

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')
    def gun_up(self, event) :
        if self.ygun >= 5 :
            self.ygun -= 5
    def gun_left(self, event) :
        if self.xgun >= 5 :
            self.xgun -= 5
    def gun_down(self, event) :
        if self.ygun <= 585 :
            self.ygun += 5
    def gun_right(self, event) :
        if self.xgun <= 785 :
            self.xgun += 5


class target():
    def __init__(self) :
        self.live = 1
        self.vx = rnd(-15, 15)
        self.vy = rnd(-15, 15)
        self.id = canv.create_oval(0,0,0,0)

    def new_target(self) :
        """ Инициализация новой цели. """
        self.x = rnd(600, 780)
        self.y = rnd(300, 550)
        self.r = rnd(15, 50)
        self.color = choice(['red', 'green', 'yellow', 'black'])
        canv.coords(self.id, self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r)
        canv.itemconfig(self.id, fill = self.color)

    def target_move(self) :
        self.x += self.vx
        self.y += self.vy
        canv.move(self.id, self.vx, self.vy)
        if (self.x >= 800 - self.r and self.vx > 0) or (self.x <= self.r and self.vx < 0) :
            self.vx = - self. vx
        if (self.y >= 600 - self.r and self.vy > 0) or (self.y <= self.r and self.vy < 0) :
            self.vy = - self.vy
    def hit(self, points=1):
        """Попадание шарика в цель."""
        canv.coords(self.id, -10, -10, -10, -10)


def new_game(event=''):
    global gun, t1, t2, screen1, balls, bullet, points, points_count
    t1.new_target()
    t2.new_target()
    bullet = 0
    balls = []
    canv.bind('<Button-1>', g1.fire2_start)
    canv.bind('<ButtonRelease-1>', g1.fire2_end)
    canv.bind('<Motion>', g1.targetting)
    root.bind('<r>', replay)
    root.bind('<w>', g1.gun_up)
    root.bind('<a>', g1.gun_left)
    root.bind('<s>', g1.gun_down)
    root.bind('<d>', g1.gun_right)
    tau = 3000
    t1.live = 1
    t2.live = 1
    while t1.live or t2.live or balls:
        t1.target_move()
        t2.target_move()
        for b in balls:
            b.move()
            if b.hittest(t1) and t1.live:
                t1.live = 0
                t1.hit()
                canv.itemconfig(screen1, text='Вы уничтожили первую цель за ' + str(bullet) + ' выстрелов')
                root.after(3000, delete_text)
            if b.hittest(t2) and t2.live:
                t2.live = 0
                t2.hit()
                canv.itemconfig(screen1, text='Вы уничтожили вторую цель за ' + str(bullet) + ' выстрелов')
                root.after(3000, delete_text)
            if t1.live == 0 and t2.live == 0:
                points += 1
                canv.itemconfig(points_count, text = points)
                canv.bind('<Button-1>', '')
                canv.bind('<ButtonRelease-1>', '')
                if bullet > 6 :
                    t = 5000
                    canv.itemconfig(screen1, text='Вашей "меткости" могли бы позавидовать имперские штурмовики и даже бойцы XCOM!')
                    root.after(5000, delete_text)
                for bb in balls :
                    canv.delete(bb.id)
                    balls = []
        canv.update()
        time.sleep(0.03)
        g1.targetting()
        g1.power_up()
    canv.delete(gun)
    root.after(tau, new_game)

def delete_text() :
    canv.itemconfig(screen1, text = '')
    
def replay(event) :
	print(event.keycode)
	t1.live = 0
	t2.live = 0
    
t1 = target()
t2 = target()
screen1 = canv.create_text(400, 300, text = '', font = '28')
points = 0
points_count = canv.create_text(30,30,text = points,font = '28')
g1 = gun()
bullet = 0
balls = []
canv.itemconfig(screen1, text = 'Для перезапуска игры нажмите R')
root.after(3000, delete_text)
new_game()

tk.mainloop()
