from constant import constant

from bazooka import Bazooka

from grenade import Grenade

from machinegun import Machinegun

from explosive_grenade import ExplosiveGrenade


class Worm:
    def __init__(self, x, y, num, canvas, game):
        self.const = constant()
        self.canvas = canvas
        self.game = game

        self.is_touch = 0
        self.energy = self.const['worm_energy']
        self.live = 100
        self.num = num

        self.vx = 0
        self.vy = 0
        self.x = x
        self.y = y
        self.drag_coef = 1

        self.r = 10                                 # if change, change move
        self.colors = ['blue', 'green', 'red', 'brown']
        self.gun = Bazooka(self, self.canvas, self.game)
        self.gun.init()

        self.body_id = self.canvas.create_oval(
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r,
            fill=self.colors[self.num])
        self.hp_id = self.canvas.create_rectangle(self.x - 10,
                                                  self.y - 15,
                                                  self.x - 10 + 20 * self.live / 100,
                                                  self.y - 10,
                                                  fill='chartreuse2',
                                                  outline='black'
                                                  )
        self.losthp_id = self.canvas.create_rectangle(self.x - 10 + 20 * self.live / 100,
                                                      self.y - 15,
                                                      self.x + 10,
                                                      self.y - 10,
                                                      fill='black',
                                                      outline='black'
                                                      )
        self.energy_id = self.canvas.create_rectangle(self.x - 10,
                                                      self.y - 22,
                                                      self.x - 10 + 20 * self.energy / self.const['worm_energy'],
                                                      self.y - 17,
                                                      fill='royalblue2',
                                                      outline='black'
                                                      )
        self.lostenergy_id = self.canvas.create_rectangle(self.x - 10 + 20 * self.energy / self.const['worm_energy'],
                                                          self.y - 22,
                                                          self.x + 10,
                                                          self.y - 17,
                                                          fill='black',
                                                          outline='black'
                                                          )
        self.required_energy_id = self.canvas.create_rectangle(self.x - 10 + 20 * self.gun.energy_cost() / self.const['worm_energy'],
                                                               self.y - 22,
                                                               self.x - 10 + 20 * self.gun.energy_cost() / self.const['worm_energy'],
                                                               self.y - 17,
                                                               fill='white',
                                                               outline='white'
                                                               )

    def choose_bazooka(self, event):
        self.canvas.delete(self.gun.body_id)
        self.gun = Bazooka(self, self.canvas, self.game)
        self.gun.init()

    def choose_grenade(self, event):
        self.canvas.delete(self.gun.body_id)
        self.gun = Grenade(self, self.canvas, self.game)
        self.gun.init()

    def choose_machinegun(self, event):
        self.canvas.delete(self.gun.body_id)
        self.gun = Machinegun(self, self.canvas, self.game)
        self.gun.init()

    def choose_explosive_grenade(self, event):
        self.canvas.delete(self.gun.body_id)
        self.gun = ExplosiveGrenade(self, self.canvas, self.game)
        self.gun.init()

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
                self.live -= int((self.vx**2 + self.vy**2)**1)
            self.vy = 0
            self.vx = 0
        else:
            self.vy += self.const['grav_const']
            self.vx = (self.vx - wind) * self.drag_coef + wind
            self.vy = self.vy * self.drag_coef

        self.gun.move()

    def move_left(self, event):
        if self.is_touch != 0 and self.energy >= 4:
            self.vx -= 0.3
            self.vy -= 0.3
            self.energy -= 4
            print('energy = ', self.energy)

    def move_right(self, event):
        if self.is_touch != 0 and self.energy >= 4:
            self.vx += 0.3
            self.vy -= 0.3
            self.energy -= 4
            print('energy = ', self.energy)

    def jump_left(self, event):
        if self.is_touch == 0:
            if self.energy >= 300:
                self.vx -= 1.5
                self.vy -= 1.5
                self.energy -= 300
        elif self.energy >= 100:
            self.energy -= 100
            self.vx -= 1.5
            self.vy -= 1.5
        print('energy = ', self.energy)

    def jump_right(self, event):
        if self.is_touch == 0:
            if self.energy >= 300:
                self.vx += 1.5
                self.vy -= 1.5
                self.energy -= 300
        elif self.energy >= 100:
            self.energy -= 100
            self.vx += 1.5
            self.vy -= 1.5
        print('energy = ', self.energy)

    def jump_up(self, event):
        if self.is_touch == 0:
            if self.energy >= 300:
                self.vy -= 1.5
                self.energy -= 300
        elif self.energy >= 100:
            self.energy -= 100
            self.vy -= 1.5
        print('energy = ', self.energy)

    def jump_down(self, event):
        if self.is_touch == 0:
            if self.energy >= 300:
                self.vy += 1.5
                self.energy -= 300
        elif self.energy >= 100:
            self.energy -= 100
            self.vy += 1.5
        print('energy = ', self.energy)

    def drowing(self):
        self.canvas.delete(self.body_id)
        self.canvas.delete(self.hp_id)
        self.canvas.delete(self.losthp_id)
        self.canvas.delete(self.energy_id)
        self.canvas.delete(self.lostenergy_id)
        self.canvas.delete(self.required_energy_id)
        self.body_id = self.canvas.create_oval(
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r,
            fill=self.colors[self.num],
            outline=self.outline)
        self.hp_id = self.canvas.create_rectangle(self.x - 10,
                                                  self.y - 15,
                                                  self.x - 10 + 20 * self.live / 100,
                                                  self.y - 10,
                                                  fill='chartreuse2',
                                                  outline='black'
                                                  )
        self.losthp_id = self.canvas.create_rectangle(self.x - 10 + 20 * self.live / 100,
                                                      self.y - 15,
                                                      self.x + 10,
                                                      self.y - 10,
                                                      fill='black',
                                                      outline='black'
                                                      )
        self.energy_id = self.canvas.create_rectangle(self.x - 10,
                                                      self.y - 22,
                                                      self.x - 10 + 20 * self.energy / self.const['worm_energy'],
                                                      self.y - 17,
                                                      fill='royalblue2',
                                                      outline='black'
                                                      )
        self.lostenergy_id = self.canvas.create_rectangle(self.x - 10 + 20 * self.energy / self.const['worm_energy'],
                                                          self.y - 22,
                                                          self.x + 10,
                                                          self.y - 17,
                                                          fill='black',
                                                          outline='black'
                                                          )
        self.required_energy_id = self.canvas.create_rectangle(self.x - 10 + 20 * self.gun.energy_cost() / self.const['worm_energy'],
                                                               self.y - 22,
                                                               self.x - 10 + 20 * self.gun.energy_cost() / self.const['worm_energy'],
                                                               self.y - 17,
                                                               fill='white',
                                                               outline='white'
                                                               )
        self.gun.drowing()
        if self.live < 0:
            self.canvas.delete(self.body_id)
            self.canvas.delete(self.hp_id)
            self.canvas.delete(self.losthp_id)
            self.canvas.delete(self.energy_id)
            self.canvas.delete(self.lostenergy_id)
            self.canvas.delete(self.required_energy_id)
