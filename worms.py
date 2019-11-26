from random import choice, randint as rnd

from tkinter import Tk, Canvas, BOTH, mainloop, CENTER, Frame

root = Tk()
fr = Frame(root)
root.geometry('730x600')
canvas = Canvas(root, bg='white')
canvas.pack(fill=BOTH, expand=1)

GRAVITATION = 1                              # it is g = 9,8 in real world
WORM_ENERGY = 5
MAX_GUN_POWER = 15
JUMP_POWER = 3
WORM_NUMB = 2


class Object():
    def __init__():
        self.x = 0
        self.y = 0
        self.Vx = 0
        self.Vy = 0
        self.rx = 0
        self.ry = 0
        self.body = pg.Rect((x - rx, y - ry, 2*rx, 2*ry))
        self.coef_drag = 0                  # a = -coef_drag * V;    a = F/m
        self.hit_points = 0

    def motion(self):
        self.Vx += GRAVITATION
        self.Vx -= coef_drag * Vx
        self.Vy -= coef_drag * Vy
        self.body.move(Vx, Vy)

class Worm(Object):
    def special_charact(self):
        self.energy = WORM_ENERGY
        self.cos_a = 0
        self.sin_a = 0
        self.power = 0
        self.gun_type = ''

    def jump_right(self, event):
        self.Vx += JUMP_POWER               # the energy condition is checked
        self.Vy -= JUMP_POWER               # before the call
        self.energy -= 1
        self.motion()

    def jump_left(self, event):
        self.Vx -= JUMP_POWER
        self.Vy -= JUMP_POWER
        self.energy -= 1
        self.motion()

    def jump_up(self, event):
        self.Vy -= JUMP_POWER
        self.energy -= 1
        self.motion()

    def jump_down(self, event):
        self.Vy += JUMP_POWER
        self.energy -= 1
        self.motion()


class Bullet(Object):
    def special_charact(self):
        self.splesh = 0
        self.damage = 0
    
    def getting_old(self):
        self.hit_points -= 1


class Touch_bullet(Bullet):
    def relationships(self):
        is_touch = 0
        for point_x in range(int(self.x) - self.rx, int(self.x) + self.rx):
            h = int((self.r**2 - abs(int(self.x) - point_x)**2)**0.5)
            for point_y in range(int(self.y) - h, int(self.y) + h):
                is_touch += fild[point_x][point_y]
        
        if is_touch != 0:
            Game.collaps(self.x, self.y, self.splash, self.damage)


class Jump_bullet(Bullet):
    def special_charact(self):
        self.elastic = 0.6
    
    def relationships(self):
        min_range_1 = max(self.rx, self.ry)
        min_range_2 = max(self.rx, self.ry)
        min_x_1 = -1
        min_y_1 = -1
        min_x_2 = -1
        min_y_2 = -1

        for point_x in range(int(self.x) - self.rx, int(self.x) + self.rx):
            dx = -int(self.x) + point_x
            h = int((self.r**2 - abs(int(dx)**2)**0.5))
            for point_y in range(int(self.y) - h, int(self.y) + h):
                if Game.fild[point_x][point_y] != 0:
                    dy = point_y - self.y

                    if dx ** 2 + dy ** 2 < min_range_1 ** 2:
                        min_range_2 = min_range_1
                        min_range_1 = (dx ** 2 + dy ** 2) ** 0.5
                        min_x_2 = min_x_1
                        min_y_2 = min_y_1
                        min_x_1 = point_x
                        min_y_1 = point_y
                    elif dx ** 2 + dy ** 2 < min_range_2 ** 2:
                        min_range_2 = (dx ** 2 + dy ** 2) ** 0.5
                        min_x_2 = point_x
                        min_y_2= point_y

        if min_x_1 != -1 and min_x_2 != -1:
            if min_x_2 - min_x_1 == 0:
                cos_a = 0
            else:
                cos_a = (min_x_2 - min_x_1) / ((min_x_2 - min_x_1) ** 2
                        + (min_y_2 - min_y_1) ** 2) ** 0.5

            if min_y_2 - min_y_1 == 0:
                sin_a = 0
            else:
                sin_a = -(min_y_2 - min_y_1) / ((min_x_2 - min_x_1) ** 2
                        + (min_y_2 - min_y_1) ** 2) ** 0.5

            self.Vy -= GRAVITATION
            self.Vx += coef_drag * Vx
            self.Vy += coef_drag * Vy
            
            self.y += self.Vy
            self.x -= self.Vx
            
            self.Vy *= self.elastic
            self.Vx *= self.elastic
            instant_Vx = self.Vx
            self.Vx = self.Vx * cos_a + self.Vy * sin_a
            self.Vy = -instant_Vx * sin_a + self.Vy * cos_a
            self.Vy *= -1
            self.Vx = self.Vx * cos_a - self.Vy * sin_a
            self.Vy = instant_Vx * sin_a + self.Vy * cos_a


class Game():
    def __init__(self):
        self.worms = []
        self.bullets = []
        self.fild = []
        self.tern = 0
        self.wind_speed = 0
        self.worms.append(Warm(100, 500, 0, 0, 15, 15, 0, 100))
        self.worms.append(Warm(600, 500, 0, 0, 15, 15, 0, 100))

    def warm_fild_check(self):
        for warm in self.warms:
            is_touch = 0
            for point_x in range(int(warm.x) - warm.rx, int(warm.x) + warm.rx):
                h = int((warm.r**2 - abs(int(warm.x) - point_x)**2)**0.5)
                for point_y in range(int(warm.y) - h, int(warm.y) + h):
                    is_touch += fild[point_x][point_y]
        
            if is_touch != 0:
                if self.Vx**2 + self.Vy**2 > 50:
                    self.hit_points -= self.Vx + self.Vy 
                warm.Vx = 0
                warm.Vy = 0

    def bullet_check(self):
        for bullet in self.bullets:
            bullet.relationships()

    def aim(self, event):
        dx = event.x - self.warms[turn % WARM_NUMB].x
        dy = event.y - self.warms[turn % WARM_NUMB].y

        if dx == 0:
            self.warms[turn % WARM_NUMB].cos_a = 0
        else:
            self.warms[turn % WARM_NUMB].cos_a = dx / (dx ** 2 + dy ** 2) ** 0.5

        if dy == 0:
            self.warms[turn % WARM_NUMB].sin_a = 0
        else:
            self.warms[turn % WARM_NUMB].sin_a = dy / (dx ** 2 + dy ** 2) ** 0.5

    def shot_prepair(self, event):
        self.preparation = 1

    def power_up(self):
        if self.warms[turn % WARM_NUMB].power < MAX_GUN_POWER and self.preparation == 1:
            self.warms[turn % WARM_NUMB].power += 0.1

    def shot (self,event):
        # TODO
        self.balls.append(Ball())
        self.power = 0
        self.preparation = 0
        self.energy = WARM_ENERGY

    def new_game(self):
        self.first_create()
        self.first_drow()
        self.update()

        canvas.bind('<Motion>', self.warms[self.tern % WARM_NUMB].aim)
        canvas.bind('<Button-1>', self.warms[self.tern % WARM_NUMB].shot_prepair)
        self.warms[self.tern % WARM_NUMB].power_up()
        canvas.bind('<ButtonRelease-1>', self.warms[self.tern % WARM_NUMB].shot)
        canvas.bind('<Up>', self.warms[self.tern % WARM_NUMB].jump_up)
        canvas.bind('<Down>', self.warms[self.tern % WARM_NUMB].jump_down)
        canvas.bind('<Left>', self.warms[self.tern % WARM_NUMB].jump_left)
        canvas.bind('<Right>', self.warms[self.turn % WARM_NUMB].jump_right)
    
    def main(self):
        self.new_game()
        
