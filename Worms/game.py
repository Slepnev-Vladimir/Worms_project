from random import randint as rnd

from tkinter import Tk, Canvas, mainloop, Frame, BOTH

from worm import Worm

from field import Field

from cloud import Cloud

from constant import constant


class Game():
    def __init__(self):
        self.const = constant()
        self.root = Tk()
        self.fr = Frame(self.root)
        self.root.geometry(str(self.const['field_width']) + 'x' + str(self.const['field_height']))
        self.canvas = Canvas(self.root, bg='skyblue')
        self.canvas.pack(fill=BOTH, expand=1)

        self.field = Field(self.canvas)
        self.field_list = self.field.field_model()
        self.is_field = 0
        self.worms = []
        self.guns = []
        self.clouds = []
        self.bullets = []
        self.boom = []
        self.field.field_visual()
        self.wind = rnd(-3, 3)
        self.turn = 0
        self.turn_end = 0
        self.worms_number = self.const['worms_number']
        self.is_shot = 0
        self.event = 0
        self.canvas.bind('<p>', self.is_turn_end)
        self.canvas.bind('<ButtonRelease-1>', self.shot_start)

        if len(self.const) < len(self.field.start_position):
            print('too many worms for this map')
        else:
            for num in range(self.const['worms_number']):
                self.worms.append(
                                  Worm(
                                       self.field.start_position[num][0],
                                       self.field.start_position[num][1],
                                       num,
                                       self.canvas,
                                       self,
                                       )
                                  )
        for num in range(self.worms_number):
            self.worms[num].player_number = num + 1

        for num in range(self.const['clouds_number']):
            self.clouds.append(Cloud(num, self.canvas))

        self.shooting_processing()
        self.walking_processing()
        self.choose_weapon()

    def bang_check(self):
        num = 0
        while num < len(self.bullets):
            if self.bullets[num].live <= 0:
                self.field_list = self.bullets[num].collapse(self.field_list)
                for worm in self.worms:
                    worm.live = self.bullets[num].damage(worm)
                    worm.vx = self.bullets[num].charge_x(worm)
                    worm.vy = self.bullets[num].charge_y(worm)
                self.bullets.pop(num)
            num += 1

        num = 0
        while num < len(self.worms):
            if self.worms[num].live <= 0:
                self.worms[num].drowing()
                self.worms.pop(num)
                self.worms_number -= 1
                if num == self.turn:
                    self.is_shot = 0
                if num < self.turn:
                    self.turn -= 1
                if self.turn == len(self.worms):
                    self.turn = 0
            num += 1

    def is_hit(self):
        for worm in self.worms:
            for bullet in self.bullets:
                bullet.hit_test(worm)

    def next_turn(self):
        self.turn += 1
        self.wind = rnd(-3, 3)
        self.turn = self.turn % self.worms_number
        for worm in self.worms:
            worm.energy = self.const['worm_energy']
        self.walking_processing()
        self.choose_weapon()
        self.shooting_processing()

    def shot_start(self, event):
        self.event = event
        if self.worms[self.turn].gun.preparation == 1:
            self.is_shot = 1

    def shot(self):
        if self.worms[self.turn].gun.rifle > 0 and self.is_shot == 1:
            self.bullets = self.worms[self.turn].gun.new_bullet(self.event, self.bullets)
        else:
            self.is_shot = 0
            self.worms[self.turn].gun.reloading()

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
            if self.turn == num:
                self.worms[num].outline = 'white'
            else:
                self.worms[num].outline = 'black'
            self.worms[num].drowing()

        for bullet in self.bullets:
            bullet.drowing()

        for expl in self.boom:
            expl.drowing()
            self.boom = [active for active in self.boom if not active.count < 0]

    def shooting_processing(self):
        self.canvas.bind('<Motion>', self.worms[self.turn].gun.targetting)
        self.canvas.bind('<Button-1>', self.worms[self.turn].gun.shot_prepair)

    def walking_processing(self):
        self.canvas.bind('<Shift-Up>', self.worms[self.turn].jump_up)
        self.canvas.bind('<Shift-Down>', self.worms[self.turn].jump_down)
        self.canvas.bind('<Shift-Left>', self.worms[self.turn].jump_left)
        self.canvas.bind('<Shift-Right>', self.worms[self.turn].jump_right)

        self.canvas.bind('<Left>', self.worms[self.turn].move_left)
        self.canvas.bind('<Right>', self.worms[self.turn].move_right)

    def choose_bazooka(self, event):
        self.worms[self.turn].choose_bazooka(event)
        self.shooting_processing()

    def choose_grenade(self, event):
        self.worms[self.turn].choose_grenade(event)
        self.shooting_processing()

    def choose_machinegun(self, event):
        self.worms[self.turn].choose_machinegun(event)
        self.shooting_processing()

    def choose_explosive_grenade(self, event):
        self.worms[self.turn].choose_explosive_grenade(event)
        self.shooting_processing()

    def choose_weapon(self):
        self.canvas.bind('<q>', self.choose_bazooka)
        self.canvas.bind('<w>', self.choose_grenade)
        self.canvas.bind('<e>', self.choose_machinegun)
        self.canvas.bind('<r>', self.choose_explosive_grenade)

    def is_turn_end(self, event):
        self.turn_end = 1

    def main(self):
        self.worms[self.turn].gun.power_up()
        self.shot()
        self.motion()
        self.visualization()
        self.bang_check()
        self.is_hit()

        if self.worms_number > 1:
            if (self.is_shot == 0
                    and self.worms[self.turn].gun.preparation == 0
                    and self.turn_end == 1):
                self.next_turn()
                self.turn_end = 0
            self.root.after(self.const['update_time'], self.main)
        elif self.worms_number == 1:
            message = 'player ' + str(self.worms[0].player_number) + ' wins'
            self.canvas.create_text(400, 300, text=message, font='28')


game = Game()
game.main()
mainloop()
