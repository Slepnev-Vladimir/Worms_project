from random import choice, randint as rnd

from tkinter import Tk, Canvas, BOTH, mainloop, CENTER, Frame

from bazooka import Bazooka, BazookaBullet

from grenade import Grenade, GrenadeBullet

from worm import Worm

from field import Field

from cloud import Cloud

from constant import constant

import math

import numpy


class Game():
    def __init__(self):
        self.const = constant()
        self.root = Tk()
        self.fr = Frame(self.root)
        self.root.geometry('800x600')
        self.canvas = Canvas(self.root, bg='lightblue')
        self.canvas.pack(fill=BOTH, expand=1)

        self.field = Field(self.canvas)
        self.field_list = self.field.field_model()
        self.is_fild = 0
        self.worms = []
        self.guns = []
        self.clouds = []
        self.bullets = []
        self.field.field_visual()
        self.wind = rnd(-3, 3)
        self.tern = 0
        self.tern_end = 0
        self.worms_number = self.const['worms_number']
        self.is_shot = 0
        self.event = 0

        self.expl_count = 0
        self.expl_x = 0
        self.expl_y = 0
        self.explode = 0
        self.expl_splash = 0

        for num in range(self.const['worms_number']):
            self.worms.append(Worm(num, self.canvas))

        for num in range(self.const['clouds_number']):
            self.clouds.append(Cloud(num, self.canvas))

    def bang_check(self):
        num = 0
        while num < len(self.bullets):
            if self.bullets[num].live <= 0:
                if (self.bullets[num].x + self.bullets[num].splash < 800 
                        and self.bullets[num].x - self.bullets[num].splash > 0
                        and self.bullets[num].y + self.bullets[num].splash < 600
                        and self.bullets[num].y - self.bullets[num].splash > 0): 
                    self.field_list = self.bullets[num].collapse(self.field_list)
                    for worm in self.worms:
                        worm.live = self.bullets[num].damage(worm)
                        worm.vx = self.bullets[num].charge_x(worm)
                        worm.vy = self.bullets[num].charge_y(worm)
                        print('hp = ', worm.live)
                self.bullets.pop(num)
            num += 1
            
        num = 0
        while num < len(self.worms):
            if self.worms[num].live <= 0:
                self.worms.pop(num)
                self.worms_number -= 1
                self.tern -= 1
            num += 1
    
    def is_hit(self):
        for worm in self.worms:
            for bullet in self.bullets:
                bullet.hit_test(worm)

    def next_tern(self):
        self.tern += 1
        self.wind = rnd(-3, 3)
        self.tern = self.tern % self.worms_number
        for worm in self.worms:
            worm.energy = self.const['worm_energy']
        print('wind = ', self.wind)
        print('next tern, tern = ', self.tern)

    def shot_start(self, event):
        self.event = event
        if self.worms[self.tern].gun.preparation == 1:
            self.is_shot = 1

    def shot(self):
        if self.worms[self.tern].gun.rifle > 0 and self.is_shot == 1:
            self.bullets = self.worms[self.tern].gun.new_bullet(self.event, self.bullets)
        else:
            self.is_shot = 0
            self.worms[self.tern].gun.reloading()

    def motion(self):
        for num in range(self.worms_number):
            self.worms[num].move(self.field_list, self.wind)

        for num in range(len(self.bullets)):
            self.bullets[num].move(self.field_list, self.wind)

        for cloud in self.clouds:
            cloud.move(self.field_list, self.wind)

    def visualization(self):
        for cloud in self.clouds:
            cloud.drowing()

        for num in range(self.worms_number):
            self.worms[num].drowing()

        for bullet in self.bullets:
            bullet.drowing()

    def shooting_processing(self):
        self.canvas.bind('<Motion>', self.worms[self.tern].gun.targetting)
        self.canvas.bind('<Button-1>', self.worms[self.tern].gun.shot_prepair)
        self.worms[self.tern].gun.power_up()
        self.canvas.bind('<ButtonRelease-1>', self.shot_start)

    def walking_processing(self):
        self.canvas.bind('<Shift-Up>', self.worms[self.tern].jump_up)
        self.canvas.bind('<Shift-Down>', self.worms[self.tern].jump_down)
        self.canvas.bind('<Shift-Left>', self.worms[self.tern].jump_left)
        self.canvas.bind('<Shift-Right>', self.worms[self.tern].jump_right)

        self.canvas.bind('<Left>', self.worms[self.tern].move_left)
        self.canvas.bind('<Right>', self.worms[self.tern].move_right)

    def choose_weapon(self):
        self.canvas.bind('<q>', self.worms[self.tern].choose_bazooka)
        self.canvas.bind('<w>', self.worms[self.tern].choose_grenade)
        self.canvas.bind('<e>', self.worms[self.tern].choose_machinegun)

    def is_tern_end(self, event):
        self.worms[self.tern].energy = 0
        self.tern_end = 1

    def main(self):
        self.shooting_processing()
        self.shot()
        self.walking_processing()
        self.choose_weapon()
        self.motion()
        self.visualization()
        self.bang_check()
        self.is_hit()
        self.canvas.bind('<p>', self.is_tern_end)

        if self.worms_number > 1:
            if (self.worms[self.tern].energy <= 0
                    and self.worms[self.tern].gun.preparation == 0
                    and self.tern_end == 1):
                self.next_tern()
                self.tern_end = 0
            self.root.after(self.const['update_time'], self.main)
        else:
            print('gg wp')


game = Game()
game.main()
mainloop()
