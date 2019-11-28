# The program contains the code of the game, in which the player
# should click on the moving figures with left mouse button and
# get points for it. To save the score, click on the button "save"
# with right mouse button.

from tkinter import Tk, Canvas, BOTH, mainloop, CENTER

from random import randrange as rnd, choice

import math

root = Tk()
root.geometry('800x600')

canv = Canvas(root, bg='white')
canv.pack(fill=BOTH, expand=1)

speed = 1              # the speed of all objects
T = 500000               # the life time of every object
dT = 10                # the drowing speed
BALLS_NUMB = 10000
RECTANGLES_NUMB = 0

def fild():
    fild = []
    for x in range(0, 800):
        fild.append([])
        for y in range(0, 600):
            fild[x].append(rnd(0, 2))
    return(fild)


fild =  fild()


class Rectangle():
    """Responsible for creating a ractangle object that"""
    """whose trajectory is a sine wave y = y0 + ampl * sin(3 * x / ampl),"""
    """You get prize for hiting it"""
    def __init__(self, score):
        self.score = score
        self.prize = 3
        self.speed_x = speed
        self.y0 = rnd(100, 500)
        self.ampl = rnd(100, 200)
        self.x = rnd(100, 700)
        self.y = self.ampl * math.sin(3 * self.x / self.ampl) + self.y0
        self.r = rnd(20, 40)
        self.colors = ['red', 'orange', 'yellow', 'green', 'blue']
        self.color = choice(self.colors)
        self.rectangle_id = canv.create_rectangle(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.color,
                width=0)

    def appear(self):
        canv.delete(self.rectangle_id)
        self.speed_x = speed
        self.y0 = rnd(100, 500)
        self.ampl = rnd(100, 200)
        self.x = rnd(100, 700)
        self.y = self.ampl * math.sin(3 * self.x / self.ampl) + self.y0
        self.r = rnd(20, 40)
        self.colors = ['red', 'orange', 'yellow', 'green', 'blue']
        self.color = choice(self.colors)
        self.rectangle_id = canv.create_rectangle(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.color,
                width=0)
        root.after(T, self.appear)

    def move(self):
        canv.delete(self.rectangle_id)

        if self.x > 700 or self.x < 100:
            self.speed_x *= -1

        self.x += self.speed_x
        self.y = self.ampl * math.sin(3 * self.x / self.ampl) + self.y0

        if self.y < 100:
            self.y = 200 - self.y

        if self.y > 500:
            self.y = 1000 - self.y

        self.rectangle_id = canv.create_rectangle(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.color,
                width=0)


class Ball():
    """Responsible for creating a ractangle object that"""
    """You get prize for hiting it"""
    def __init__(self, score):
        self.score = score
        self.prize = 1
        self.speed_x = rnd(-5, 5) / 5 * speed
        self.speed_y = rnd(-5, 5) / 5 * speed
        self.x = rnd(100, 700)
        self.y = rnd(100, 500)
        #self.r = rnd(30, 50)
        self.r = 20
        self.colors = ['red', 'orange', 'yellow', 'green', 'blue']
        self.color = choice(self.colors)
        self.ball_id = canv.create_oval(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.color,
                width=0)

    def appear(self):
        canv.delete(self.ball_id)
        self.speed_x = rnd(-5, 5) / 5 * speed
        self.speed_y = rnd(-5, 5) / 5 * speed
        self.x = rnd(100, 700)
        self.y = rnd(100, 500)
        # self.r = rnd(30, 50)
        self.r = 20
        self.colors = ['red', 'orange', 'yellow', 'green', 'blue']
        self.color = choice(self.colors)
        self.ball_id = canv.create_oval(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.color,
                width=0)
        root.after(T, self.appear)

    def move(self):
        canv.delete(self.ball_id)

        if self.x > 700 - self.r and self.speed_x > 0 or self.x < self.r and self.speed_x < 0:
            self.speed_x *= rnd(1, 10) / (-5)

        if self.y > 600 - self.r and self.speed_y > 0 or self.y < self.r and self.speed_y < 0:
            self.speed_y *= rnd(1, 10) / (-5)

        self.x += self.speed_x
        self.y += self.speed_y

        self.ball_id = canv.create_oval(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.color,
                width=0)


class Main():
    def __init__(self):
        """responsible for creating a start text, save button"""
        """specifying the number of objects"""
        """and opening the score file"""
        self.score = 0
        self.balls = [Ball(self.score) for numb in range(BALLS_NUMB)]
        self.rectangles = [Rectangle(self.score) for numb in range(RECTANGLES_NUMB)]

        canv.create_rectangle(
                        630,
                        0,
                        730,
                        75,
                        fill="green",
                        width=0)
        canv.create_text(
                        680,
                        33,
                        text='save',
                        justify=CENTER,
                        font="Verdana 30")
        self.start_text = canv.create_text(
                        350,
                        300,
                        text='enter your name',
                        justify=CENTER,
                        font="Verdana 50",
                        tag="text")
        self.name = input()
        canv.delete(self.start_text)

        self.table = open('score.txt', 'r')
        self.player_check = 0
        self.best_list = []

        for line in self.table:
            self.best_list.append(line[:-1])

            if line[:-1] == self.name:
                self.player_numb = len(self.best_list) - 1
                self.player_check = 1

        if self.player_check == 0:
            self.best_list.append(self.name)
            self.best_list.append(self.score)
            self.player_numb = len(self.best_list) - 2

        for ball in self.balls:
            ball.appear()

        for rectangle in self.rectangles:
            rectangle.appear()

    def change_list(self):
        """add the score of the player if it is better then his last score"""
        if int(self.best_list[self.player_numb + 1]) < int(self.score):
            self.best_list[self.player_numb + 1] = self.score

    def save(self, event):
        """save the score in file if player press oh save button"""
        if event.x > 630 and event.y < 75:
            new_list = open('score.txt', 'w')

            for i in self.best_list:
                new_list.write(str(i) + '\n')
            new_list.close()

    def check(self, event):
        """check if the object is hit"""
        for ball in self.balls:
            if (event.x - ball.x) ** 2 + (event.y - ball.y) ** 2 < ball.r ** 2:
                Main.change_score(self, 1)

        for rectangle in self.rectangles:
            if abs(event.x - rectangle.x) < rectangle.r and abs(event.y - rectangle.y) < rectangle.r:
                Main.change_score(self, 3)

    def change_score(self, prize):
        """change the score if you hit the object"""
        self.score += prize
        canv.delete('text')
        canv.create_text(
                    100,
                    100,
                    text=self.score,
                    justify=CENTER,
                    font="Verdana 100",
                    tag="text")

    def main(self):
        for ball in self.balls:
            ball.move()
            points_numb = 0
#            for point_x in range(int(ball.x) - ball.r, int(ball.x) + ball.r):
#                h = int((ball.r**2 - abs(int(ball.x) - point_x)**2)**0.5)
#                for point_y in range(int(ball.y) - h, int(ball.y) + h):
#                    points_numb += fild[point_x][point_y]
#            print(points_numb)


        for rectangle in self.rectangles:
            rectangle.move()

        canv.bind('<Button-1>', self.check)
        self.change_list()
        canv.bind('<Button-3>', self.save)
        root.after(dT, self.main)


game = Main()
game.main()
mainloop()
