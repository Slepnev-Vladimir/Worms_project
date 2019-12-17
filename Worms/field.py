import numpy


class Field:
    def __init__(self, canvas):
        self.field_list = numpy.zeros((800, 600))
        self.canvas = canvas
        self.start_position = [(150, 90), (650, 90), (190, 440), (610, 440)]

    def field_model(self):
        for x in range(100, 300):
            for y in range(100, 200):
                self.field_list[x, y] = 1

        for x in range(500, 700):
            for y in range(100, 200):
                self.field_list[x, y] = 1

        for y in range(200, 400):
            for x in range(400 - (y - 200) , 400 + (y - 200)):
                self.field_list[x, y] = 1

        for x in range(20, 780):
            for y in range(450, 600):
                self.field_list[x, y] = 1

        return(self.field_list)


    def field_visual(self):
        self.land_1 = self.canvas.create_polygon((100, 100), (300, 100), (300, 200), (100, 200), fill='green')
        self.land_2 = self.canvas.create_polygon((500, 100), (700, 100), (700, 200), (500, 200), fill='green')
        self.land_3 = self.canvas.create_polygon((200, 400), (400, 200), (600, 400), fill='green')
        self.land_4 = self.canvas.create_polygon((20, 450), (780, 450), (780, 600), (20, 600), fill='green')
        self.sun = self.canvas.create_oval((20, 20), (50, 50), fill = 'yellow')
