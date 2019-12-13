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
        self.drag_coef = 0.99
        self.x = (rnd(10, 800//self.const['worms_number'] - 10)
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
        self.gun = Bazooka(self, self.canvas)

    def choose_grenade(self, event):
        self.canvas.delete(self.gun.body_id)
        self.gun = Grenade(self, self.canvas)
    
    def move(self, field, wind):
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
            self.vx = (self.vx - wind) * self.drag_coef + wind
            self.vy = self.vy * self.drag_coef

        self.gun.move()

    def move_left(self, event):
        if self.is_touch != 0 and self.energy >= 4:
            self.vx -= 0.4
            self.vy -= 0.4
            self.energy -= 4
            print('energy = ', self.energy)

    def move_right(self, event):
        if self.is_touch != 0 and self.energy >= 4:
            self.vx += 0.4
            self.vy -= 0.4
            self.energy -= 4
            print('energy = ', self.energy)

    def jump_left(self, event):
        if self.is_touch == 0:
            if self.energy >= 300:
                self.vx -= 2
                self.vy -= 2
                self.energy -= 300
        elif self.energy >= 100:
            self.energy -= 100
            self.vx -= 2
            self.vy -= 2
        print('energy = ', self.energy)

    def jump_right(self, event):
        if self.is_touch == 0:
            if self.energy >= 300:
                self.vx += 2
                self.vy -= 2
                self.energy -= 300
        elif self.energy >= 100:
            self.energy -= 100
            self.vx += 2
            self.vy -= 2
        print('energy = ', self.energy)

    def jump_up(self, event):
        if self.is_touch == 0:
            if self.energy >= 300:
                self.vy -= 2
                self.energy -= 300
        elif self.energy >= 100:
            self.energy -= 100
            self.vy -= 2
        print('energy = ', self.energy)

    def jump_down(self, event):
        if self.is_touch == 0:
            if self.energy >= 300:
                self.vy += 2
                self.energy -= 300
        elif self.energy >= 100:
            self.energy -= 100
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
