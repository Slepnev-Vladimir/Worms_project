from random import choice, randint as rnd

from tkinter import Tk, Canvas, BOTH, mainloop, CENTER, Frame

root = Tk()
fr = Frame(root)
root.geometry('730x600')
canvas = Canvas(root, bg='white')
canvas.pack(fill=BOTH, expand=1)
speed = 1
dT = 10


class Ball:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.elastic = 0
        self.g = 0
        self.live = 0
        self.r = 0
        self.vx = 0
        self.vy = 0
        self.color = choice(['blue', 'green', 'red', 'brown'])
        self.id = canvas.create_oval(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.color)

    def appear(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.elastic = 0.6
        self.g = 0.1
        self.live = 1000
        self.r = 10
        self.vx = vx
        self.vy = vy
        self.color = choice(['blue', 'green', 'red', 'brown'])
        self.id = canvas.create_oval(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.color)

    def move(self, fild):
        canvas.delete(self.id)

        self.vy -= self.g
        min_range_1 = self.r
        min_range_2 = self.r
        min_index_1 = -1
        min_index_2 = -1

        for point in fild:
            x = point[0]
            y = point[1]
            dx = x - self.x
            dy = y - self.y

            if dx ** 2 + dy ** 2 < min_range_1 ** 2:
                min_range_2 = min_range_1
                min_range_1 = (dx ** 2 + dy ** 2) ** 0.5
                min_index_2 = min_index_1
                min_index_1 = fild.index(point)
            elif dx ** 2 + dy ** 2 < min_range_2 ** 2:
                min_range_2 = (dx ** 2 + dy ** 2) ** 0.5
                min_index_2 = fild.index(point)

        if min_index_1 != -1 and min_index_2 != -1:
            min_numb = min(min_index_1, min_index_2)
            max_numb = max(min_index_1, min_index_2)
            y1 = fild[min_numb][1]
            y2 = fild[max_numb][1]
            x1 = fild[min_numb][0]
            x2 = fild[max_numb][0]

            if x2 - x1 == 0:
                cos_a = 0
            else:
                cos_a = (x2 - x1) / ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

            if y2 - y1 == 0:
                sin_a = 0
            else:
                sin_a = -(y2 - y1) / ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

            self.vy += self.g
            self.y += self.vy
            self.x -= self.vx
            self.vy *= self.elastic
            self.vx *= self.elastic
            instant_vx = self.vx
            self.vx = self.vx * cos_a + self.vy * sin_a
            self.vy = -instant_vx * sin_a + self.vy * cos_a
            self.vy *= -1
            self.vx = self.vx * cos_a - self.vy * sin_a
            self.vy = instant_vx * sin_a + self.vy * cos_a

        self.y -= self.vy
        self.x += self.vx

        if self.live <= 0:
            canvas.delete(self.id)
        else:
            self.live -= 1

        self.id = canvas.create_oval(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.color)


class Gun:
    def __init__(self, numb):
        self.energy = 3
        self.vx = 0
        self.vy = 0
        self.numb = numb
        self.live = 3
        self.r = 15
        self.x = rnd(20, 220) + 500 * numb            # work only for 2 players
        self.y = 0
        self.len_x = 20
        self.len_y = 20
        self.colors = ['blue', 'green', 'red', 'brown']
        self.body_id = canvas.create_oval(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.colors[self.numb])

        self.gun_id = canvas.create_line(
                self.x,
                self.y,
                self.x + self.len_x,
                self.y - self.len_y,
                fill='black',
                width=7)

    def move(self, fild, power, cos_a, sin_a):
        touch = 0
        self.x += self.vx
        self.y += self.vy

        for point in fild:
            dx = self.x - point[0]
            dy = self.y - point[1]

            if dx ** 2 + dy ** 2 < self.r ** 2:
                touch = 1

        if touch == 0:
            self.vy += 0.1
        else:
            self.vy = 0
            self.vx = 0

        self.drowing(power, cos_a, sin_a)

    def move_left(self, event):
        if self.energy > 0:
            self.vx -= 2
            self.vy -= 2
            self.energy -= 1

    def move_right(self, event):
        if self.energy > 0:
            self.vx += 2
            self.vy -= 2
            self.energy -= 1

    def move_up(self, event):
        if self.energy > 0:
            self.vy -= 2
            self.energy -= 1

    def move_down(self, event):
        if self.energy > 0:
            self.vy += 2
            self.energy -= 1

    def drowing(self, power, cos_a, sin_a):
        canvas.delete(self.body_id)
        canvas.delete(self.gun_id)
        self.len_x = max(power, 3) * 10 * cos_a
        self.len_y = -max(power, 3) * 10 * sin_a

        self.body_id = canvas.create_oval(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.colors[self.numb])

        if power != 0:
            self.gun_id = canvas.create_line(
                    self.x,
                    self.y,
                    self.x + self.len_x,
                    self.y - self.len_y,
                    fill='orange',
                    width=7)
        else:
            self.gun_id = canvas.create_line(
                    self.x,
                    self.y,
                    self.x + self.len_x,
                    self.y - self.len_y,
                    fill='black',
                    width=7)


class Game():
    def __init__(self):
        self.start_text = ''
        self.fild = [[10, 600]]
        self.is_fild = 0
        self.is_create = 0
        self.game_over = 0
        self.cos_a = 0
        self.sin_a = 0
        self.gun = []
        self.gun_numb = 2
        self.live_text = []
        self.turn = 1
        self.preparation = 0

        for numb in range(self.gun_numb):
            self.gun.append(Gun(numb))
            self.live_text.append('')

        self.angle = 0
        self.power = 0
        self.balls = []

    def hit_check(self):
        for ball in self.balls:
            for numb in range(self.gun_numb):
                dx = ball.x - self.gun[numb].x
                dy = ball.y - self.gun[numb].y
                r = ball.r + self.gun[numb].r

                if dx ** 2 + dy ** 2 < r ** 2 and ball.live < 977:
                    self.gun[numb].live -= 1
                    canvas.delete(self.live_text[numb])
                    self.live_text[numb] = canvas.create_text(
                                10 * (numb + 1),
                                10,
                                text=self.gun[numb].live,
                                justify=CENTER,
                                font="Verdana 10",
                                fill=self.gun[numb].colors[numb])

                    if self.gun[numb].live != 0:
                        canvas.delete(ball.id)
                        self.balls.pop(self.balls.index(ball))
                    else:
                        canvas.delete(self.gun[numb].gun_id)
                        canvas.delete(self.gun[numb].body_id)

                if self.gun[numb].y > 600:
                    self.gun[numb].live = 0

    def new_ball(self, event):
        self.balls.append(Ball())
        this_ball = self.balls[len(self.balls) - 1]
        vx = self.power * self.cos_a
        vy = self.power * self.sin_a
        a = self.gun_numb
        this_ball.appear(self.gun[self.turn % a].x, self.gun[self.turn % a].y, vx, -vy)
        self.power = 0
        self.preparation = 0
        self.gun[self.turn % a].energy = 3
        self.turn += 1

    def shot_prepair(self, event):
        self.preparation = 1

    def targetting(self, event):
        a = self.gun_numb
        dx = event.x - self.gun[self.turn % a].x
        dy = event.y - self.gun[self.turn % a].y

        if dx == 0:
            self.cos_a = 0
        else:
            self.cos_a = dx / (dx ** 2 + dy ** 2) ** 0.5

        if dy == 0:
            self.sin_a = 0
        else:
            self.sin_a = dy / (dx ** 2 + dy ** 2) ** 0.5

    def ball_to_old(self):
        numb = 0

        while numb < len(self.balls):
            self.balls[numb].move(self.fild)

            if self.balls[numb].live <= 0:
                canvas.delete(self.balls[numb].id)
                self.balls.pop(numb)

            numb += 1

    def power_up(self):
        if self.power < 15 and self.preparation == 1:
            self.power += 0.1

    def create_fild(self, event):
        if event.x < 10:
            self.is_fild = 1

        if event.x > 720:
            self.is_fild = -1
            self.fild.append([720, 600])
            canvas.create_polygon(self.fild)

        if self.is_fild == 1:
            self.fild.append([event.x, event.y])

    def main(self):
        canvas.delete(self.start_text)

        if self.is_fild != -1:
            self.start_text = canvas.create_text(
                        365,
                        300,
                        text="to create a battlefild, slowly swipe from the left to the right of the canvas",
                        justify=CENTER,
                        font="Verdana 14")

            canvas.bind('<Motion>', self.create_fild)
        else:
            canvas.bind('<Motion>', self.targetting)

            for numb in range(self.gun_numb):
                self.gun[numb].move(self.fild, self.power, self.cos_a, self.sin_a)

        canvas.bind('<Button-1>', self.shot_prepair)
        self.power_up()
        canvas.bind('<ButtonRelease-1>', self.new_ball)
        canvas.bind('<Up>', self.gun[self.turn % self.gun_numb].move_up)
        canvas.bind('<Down>', self.gun[self.turn % self.gun_numb].move_down)
        canvas.bind('<Left>', self.gun[self.turn % self.gun_numb].move_left)
        canvas.bind('<Right>', self.gun[self.turn % self.gun_numb].move_right)
        self.ball_to_old()
        self.gun[self.turn % self.gun_numb].drowing(self.power, self.cos_a, self.sin_a)
        self.hit_check()

        self.game_over = 0

        for numb in range(self.gun_numb):
            if self.gun[numb].live == 0:
                self.game_over = 1
                lost_numb = numb

        if self.game_over == 0:
            root.after(dT, self.main)
        else:
            canvas.create_text(
                            365,
                            300,
                            text=str(lost_numb + 1)+" player lost",
                            justify=CENTER,
                            font="Verdana 30",
                            fill=self.gun[lost_numb].colors[lost_numb])


game = Game()
game.main()
mainloop()
