from random import choice, randint as rnd

from tkinter import Tk, Canvas, BOTH, mainloop, CENTER, Frame

import math

root = Tk()
fr = Frame(root)
root.geometry('800x600')
canvas = Canvas(root, bg='white')
canvas.pack(fill=BOTH, expand=1)
speed = 1
dT = 10


class Target():
    """
    Responsible for creating a ractangle object that 
    You get prize for hiting it
    """
    def __init__(self, score):
        self.score = score
        self.prize = 1
        self.speed_x = rnd(-5, 5) / 5 * speed
        self.speed_y = rnd(-5, 5) / 5 * speed
        self.x = rnd(100, 700)
        self.y = rnd(100, 500)
        self.r = rnd(2, 50)
        self.colors = ['red', 'orange', 'yellow', 'green', 'blue']
        self.color = choice(self.colors)
        self.id = canvas.create_oval(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.color,
                width=0)

    def appear(self):
        canvas.delete(self.id)
        self.speed_x = rnd(-5, 5) / 5 * speed
        self.speed_y = rnd(-5, 5) / 5 * speed
        self.x = rnd(100, 700)
        self.y = rnd(100, 500)
        self.r = rnd(2, 50)
        self.colors = ['red', 'orange', 'yellow', 'green', 'blue']
        self.color = choice(self.colors)
        self.id = canvas.create_oval(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.color,
                width=0)

    def move(self):
        canvas.delete(self.id)

        if self.x > 700 - self.r and self.speed_x > 0 or self.x < self.r and self.speed_x < 0:
            self.speed_x *= rnd(1, 10) / (-5)

        if self.y > 600 - self.r and self.speed_y > 0 or self.y < self.r and self.speed_y < 0:
            self.speed_y *= rnd(1, 10) / (-5)

        self.x += self.speed_x
        self.y += self.speed_y

        self.id = canvas.create_oval(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.color,
                width=0)


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

    def appear(self, vx, vy):
        self.x = 20
        self.y = 450
        self.elastic = 0.6
        self.g = 0.1
        self.live = 1000
        self.r = 5
        self.vx = vx
        self.vy = vy
        self.color = choice(['blue', 'green', 'red', 'brown'])
        self.id = canvas.create_oval(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.color)

    def move(self):
        canvas.delete(self.id)

        self.vy -= self.g
        self.y -= self.vy
        self.x += self.vx

        if self.y > 500:
            self.vy += self.g
            self.vy *= -self.elastic
            self.vx *= self.elastic
            self.y = 500

        if self.x > 800:
            self.vx *= -self.elastic
            self.vy *= self.elastic
            self.x = 800

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

    def hit_test(self, obj):
        return abs(obj.x - self.x) <= (self.r + obj.r) and abs(obj.y - self.y) <= (self.r + obj.r)


class Gun:
    def __init__(self):
        self.x = 20
        self.y = 450
        self.len_x = 20
        self.len_y = 20
        self.id = canvas.create_line(
                self.x,
                self.y,
                self.x + self.len_x,
                self.y - self.len_y,
                fill='black',
                width=7)

    def drowing(self, power, angle):
        canvas.delete(self.id)
        self.len_x = max(power, 3) * 10 * math.cos(angle)
        self.len_y = -max(power, 3) * 10 * math.sin(angle)

        if power != 0:
            self.id = canvas.create_line(
                    self.x,
                    self.y,
                    self.x + self.len_x,
                    self.y - self.len_y,
                    fill='orange',
                    width=7)
        else:
            self.id = canvas.create_line(
                    self.x,
                    self.y,
                    self.x + self.len_x,
                    self.y - self.len_y,
                    fill='black',
                    width=7)


class Game():
    def __init__(self):
        self.bullet = 0
        self.score = 0
        self.score_text = canvas.create_text(
                                10,
                                10,
                                text=self.score,
                                justify=CENTER,
                                font="Verdana 10")
        self.gun = Gun()
        self.gun_x = 20
        self.preparation = 0
        self.gun_y = 450
        self.angle = 0
        self.power = 0
        self.targets = [Target(self.score) for numb in range(5)]
        self.balls = []
        for target in self.targets:
            target.appear()

    def hit_check(self):
        for ball in self.balls:
            for target in self.targets:
                if (ball.x - target.x) ** 2 + (ball.y - target.y) ** 2 < (ball.r + target.r) ** 2:
                    self.score += 1
                    canvas.delete(self.score_text)
                    self.score_text = canvas.create_text(
                                10,
                                10,
                                text=self.score,
                                justify=CENTER,
                                font="Verdana 10")

                    canvas.delete(target.id)
                    self.targets.pop(self.targets.index(target))

    def new_ball(self, event):
        self.balls.append(Ball())
        this_ball = self.balls[len(self.balls) - 1]
        vx = self.power * math.cos(self.angle)
        vy = self.power * math.sin(self.angle)
        this_ball.appear(vx, -vy)
        self.power = 0
        self.preparation = 0
        self.bullet += 1

    def shot_prepair(self, event):
        self.preparation = 1

    def targetting(self, event):
        self.angle = math.atan((event.y - self.gun_y) / (event.x - self.gun_x))

    def ball_to_old(self):
        numb = 0

        while numb < len(self.balls):
            self.balls[numb].move()

            if self.balls[numb].live <= 0:
                canvas.delete(self.balls[numb].id)
                self.balls.pop(numb)

            numb += 1

    def power_up(self):
        if self.power < 15 and self.preparation == 1:
            self.power += 0.1

    def targets_dinamics(self):
        for target in self.targets:
            target.move()

    def end_check(self):
        if len(self.targets) == 0:
            self.end_text = canvas.create_text(
                                400,
                                300,
                                text='you destroyed all targets in ' + str(self.bullet) + ' shots',
                                justify=CENTER,
                                font="Verdana 25")
        else:
            root.after(dT, self.main)

    def main(self):
        self.targets_dinamics()
        canvas.bind('<Motion>', self.targetting)
        canvas.bind('<Button-1>', self.shot_prepair)
        self.power_up()
        canvas.bind('<ButtonRelease-1>', self.new_ball)
        self.ball_to_old()
        self.gun.drowing(self.power, self.angle)
        self.hit_check()
        self.end_check()


game = Game()
game.main()
mainloop()
