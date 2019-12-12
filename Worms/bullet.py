class Bullet():
    def __init__(self, gun, canvas):
        self.canvas = canvas
        self.gun = gun
        self.splash = 0
        self.x = gun.x
        self.y = gun.y
        self.r = 0
        self.vx = 0
        self.vy = 0
        self.color = 'blue'
        self.body_id = 0
        self.activation = 0

    def collapse(self, field):
        for point_x in range(int(self.x) - self.splash,
                int(self.x) + self.splash):
            h = int((self.splash**2 - abs(int(self.x) - point_x)**2)**0.5)
            for point_y in range(int(self.y) - h, int(self.y) + h):
                field[point_x, point_y] = 0
        self.body_id = self.canvas.create_oval(
                self.x - self.splash,
                self.y - self.splash,
                self.x + self.splash,
                self.y + self.splash,
                fill='lightblue',
                outline='lightblue',
                )
        return(field)
