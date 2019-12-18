from random import randint as rnd

from constant import constant


class Cloud:
    def __init__(self, num, canvas):
        self.const = constant()
        self.canvas = canvas
        self.vx = 0
        self.vy = 0
        self.num = num
        self.r = 10                                 # if change, change move
        self.drag_coef = 0.99
        self.color = 'white'
        self.x = (rnd(0, 800//self.const['clouds_number'])
                  + num * (800//self.const['clouds_number']))
        self.y = rnd(0, 50)
        self.body_id1 = self.canvas.create_oval(
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r,
            fill=self.color,
            outline=self.color)
        self.body_id2 = self.canvas.create_oval(
            self.x - self.r - 10,
            self.y - self.r,
            self.x + self.r - 10,
            self.y + self.r,
            fill=self.color,
            outline=self.color)
        self.body_id3 = self.canvas.create_oval(
            self.x - self.r - 5,
            self.y - self.r - 5,
            self.x + self.r - 5,
            self.y + self.r - 5,
            fill=self.color,
            outline=self.color)
        self.body_id4 = self.canvas.create_oval(
            self.x - self.r + 10,
            self.y - self.r,
            self.x + self.r + 10,
            self.y + self.r,
            fill=self.color,
            outline=self.color)

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
        self.canvas.delete(self.body_id1)
        self.canvas.delete(self.body_id2)
        self.canvas.delete(self.body_id3)
        self.canvas.delete(self.body_id4)
        self.body_id1 = self.canvas.create_oval(
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r,
            fill=self.color,
            outline=self.color)
        self.body_id2 = self.canvas.create_oval(
            self.x - self.r - 10,
            self.y - self.r,
            self.x + self.r - 10,
            self.y + self.r,
            fill=self.color,
            outline=self.color)
        self.body_id3 = self.canvas.create_oval(
            self.x - self.r - 5,
            self.y - self.r - 5,
            self.x + self.r - 5,
            self.y + self.r - 5,
            fill=self.color,
            outline=self.color)
        self.body_id4 = self.canvas.create_oval(
            self.x - self.r + 10,
            self.y - self.r,
            self.x + self.r + 10,
            self.y + self.r,
            fill=self.color,
            outline=self.color)
