class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        print(self.x, self.y)

    def __eq__(self, taget):
        if self.x == taget.x and self.y == taget.y:
            return True
        return False

    def distance(self, taget):
        return (self.x - taget.x) ** 2 + (self.y - taget.y) ** 2


class Direction:
    def __init__(self, direct):
        self.value = direct
        self.update(direct)

    def update(self, direct):
        self.value = direct
        if direct == 'Left':
            self.stepx = -1
            self.stepy = 0
        elif direct == 'Right':
            self.stepx = 1
            self.stepy = 0
        elif direct == 'Up':
            self.stepx = 0
            self.stepy = -1
        else:
            self.stepx = 0
            self.stepy = 1
