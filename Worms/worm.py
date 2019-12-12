from constant import constant

from random import choice, randint as rnd

from tkinter import Tk, Canvas, BOTH, mainloop, CENTER, Frame

from bazooka import Bazooka, BazookaBullet

from grenade import Grenade, GrenadeBullet

import math


class Worm:
    def __init__(self, num, canvas):
        self.const = constant()
        self.canvas = canvas
        self.is_touch = 0
        self.energy = self.const['worm_energy']
        self.vx = 0
        self.vy = 0
        self.num = num
        self.live = 100
        self.r = 10                                 # if change, change move
        self.x = (rnd(0, 800//self.const['worms_number'])
                + num * (800//self.const['worms_number']))
        self.y = 20
        self.colors = ['blue', 'green', 'red', 'brown']
        self.gun = Bazooka(self, self.canvas)
        self.body_id = self.canvas.create_oval(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.colors[self.num])

    def choose_bazooka(self, event):
        self.canvas.delete(self.gun.body_id)
        self.gun = Bazooka(self)

    def choose_grenade(self, event):
        self.canvas.delete(self.gun.body_id)
        self.gun = Grenade(self, self.canvas)
    
    def move(self, field):
        self.x += self.vx
        self.y += self.vy

        self.is_touch = 0
        if (self.x + self.r < 800 
                and self.x - self.r > 0
                and self.y + self.r < 600
                and self.y - self.r > 0): 
            for point_x in range(int(self.x) - self.r, int(self.x) + self.r):
                h = int((self.r**2 - abs(int(self.x) - point_x)**2)**0.5)
                for point_y in range(int(self.y) - h, int(self.y) + h):
                    self.is_touch += field[point_x, point_y]
        else:
            self.live -= 1
        
        if self.is_touch == 296:            # depends on the size of the worm
            self.live -= 1
        
        if self.is_touch != 0:
            if self.vy**2 + self.vx**2 > 30:
                self.live -= int((self.vx**2 + self.vy**2)**0.5)
            self.vy = 0
            self.vx = 0
        else:
            self.vy += self.const['grav_const']

        self.gun.move()

    def move_left(self, event):
        if self.is_touch == 0:
            if self.energy >= 3:
                self.vx -= 2
                self.vy -= 2
                self.energy -= 3
        elif self.energy >= 1:
            self.energy -= 1
            self.vx -= 2
            self.vy -= 2
        print('energy = ', self.energy)

    def move_right(self, event):
        if self.is_touch == 0:
            if self.energy >= 3:
                self.vx += 2
                self.vy -= 2
                self.energy -= 3
        elif self.energy >= 1:
            self.energy -= 1
            self.vx += 2
            self.vy -= 2
        print('energy = ', self.energy)

    def move_up(self, event):
        if self.is_touch == 0:
            if self.energy >= 3:
                self.vy -= 2
                self.energy -= 3
        elif self.energy >= 1:
            self.energy -= 1
            self.vy -= 2
        print('energy = ', self.energy)

    def move_down(self, event):
        if self.is_touch == 0:
            if self.energy >= 3:
                self.vy += 2
                self.energy -= 3
        elif self.energy >= 1:
            self.energy -= 1
            self.vy += 2
        print('energy = ', self.energy)

    def drowing(self):
        self.canvas.delete(self.body_id)
        self.body_id = self.canvas.create_oval(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.colors[self.num])
        self.gun.drowing()
        if self.live < 0:
            self.canvas.delete(self.body_id)
