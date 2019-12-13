from random import choice, randint as rnd

from tkinter import Tk, Canvas, BOTH, mainloop, CENTER, Frame

from constant import constant

import math


class Cloud:
    def __init__(self, num, canvas):
        self.const = constant()
        self.canvas = canvas
        self.vx = 0
        self.vy = 0
        self.num = num
        self.r = 10                                 # if change, change move
        self.drag_coef = 0
        self.color = 'white'
        self.x = (rnd(0, 800//self.const['clouds_number'])
                + num * (800//self.const['clouds_number']))
        self.y = rnd(0, 50)
        self.body_id = self.canvas.create_oval(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.color)

    def move(self, field, wind):
        self.x += self.vx
        self.y += self.vy
        self.vx = (self.vx - wind) * self.drag_coef + wind
        self.vy = self.vy * self.drag_coef
        if self.x > 800:
            self.x = 0
        if self.x < 0:
            self.x = 800
        self.drowing()

    def drowing(self):
        self.canvas.delete(self.body_id)
        self.body_id = self.canvas.create_oval(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.color)
