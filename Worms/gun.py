import math


class Gun():
    def __init__(self, worm, canvas, game):
        self.canvas = canvas
        self.worm = worm
        self.game = game
        self.live = self.worm.live
        self.power = 0
        self.preparation = 0
        self.angle = 0
        self.r = worm.r              # need to create bullet
        self.y = worm.y
        self.x = worm.x
        self.body_id = self.canvas.create_line(
                self.x,
                self.y,
                self.x + 20,
                self.y - 20,
                width=7)

    def shot_prepair(self, event):
        if (self.worm.energy >= self.worm.gun.energy_cost()
                and self.preparation != 1):
            self.preparation = 1
            self.worm.energy -= self.worm.gun.energy_cost()
            print('energy = ', self.worm.energy)

    def targetting(self, event=0):
        if event:
            self.angle = math.atan2((event.y - self.y), (event.x - self.x))
        if self.preparation:
            self.canvas.itemconfig(self.body_id, fill='orange')
        else:
            self.canvas.itemconfig(self.body_id, fill='black')

    def power_up(self):
        if self.preparation == 1:
            if self.power < 10:
                self.power += 0.5
            self.canvas.itemconfig(self.body_id, fill='orange')
        else:
            self.canvas.itemconfig(self.body_id, fill='black')
    
    def move(self):
        self.x = self.worm.x
        self.y = self.worm.y
        self.live = self.worm.live
