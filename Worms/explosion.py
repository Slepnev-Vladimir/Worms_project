class Explosion():
    def __init__(self, canvas):
        self.canvas = canvas
        self.x = 0
        self.y = 0
        self.r = 0
        self.count = 0
        self.body_id = 0
    
    def start(self, bullet):
        self.x = bullet.x
        self.y = bullet.y
        self.r = bullet.splash
    def drowing(self):
        if self.count < self.r:
            self.body_id = self.canvas.create_oval((self.x - self.count, self.y - self.count),
                                            (self.x + self.count, self.y + self.count),
                                            fill = 'orange', outline = 'black'
                                            )
            self.count += 5
        else:
            self.body_id = self.canvas.create_oval((self.x - self.count, self.y - self.count),
                                            (self.x + self.count, self.y + self.count),
                                            fill = 'skyblue', outline = 'skyblue'
                                            )
            self.count = -1
