import random
import math


class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return '%i, %i' % (self.x, self.y)

    def __eq__(self, value):
        if self.x == value.x and self.y == value.y:
            return True
        return False

    def __add__(self, value):
        x = self.x + value.x
        y = self.y + value.y
        return Pos(x, y)

    # def __radd__(self, value):
    #     return self.__add__(self, value)


def distance(pos1, pos2):
    width = 400
    height = 400

    diffx = abs(pos1.x - pos2.x)
    diffy = abs(pos1.y - pos2.y)

    if diffx > width / 2:
        diffx = width - diffx
    if diffy > height / 2:
        diffy = height - diffy
    return diffx + diffy


class Direction:
    def __init__(self, direct):
        self.value = direct
        self.update(direct)

    def update(self, direct):
        self.value = direct
        if direct == 'Left':
            self.lt = 'Down'
            self.rt = 'Up'
            self.stepx = -5
            self.stepy = 0
        elif direct == 'Right':
            self.lt = 'Up'
            self.rt = 'Down'
            self.stepx = 5
            self.stepy = 0
        elif direct == 'Up':
            self.lt = 'Left'
            self.rt = 'Right'
            self.stepx = 0
            self.stepy = -5
        else:
            self.lt = 'Right'
            self.rt = 'Left'
            self.stepx = 0
            self.stepy = 5

    def __eq__(self, taget):
        if self.value == taget.value:
            return True
        return False

    def __neg__(self):
        if self.value == 'Left':
            return Direction('Right')
        elif self.value == 'Right':
            return Direction('Left')
        elif self.value == 'Up':
            return Direction('Down')
        else:
            return Direction('Up')

    def left(self):
        return Direction(self.lt)

    def right(self):
        return Direction(self.rt)


def rangePos(start, stop):
    # start = deepcopy(start)
    # stop = deepcopy(stop)

    stepx = 1
    stepy = 1
    if start.x > stop.x:
        stepx = -1
    if start.y > stop.y:
        stepy = -1

    res = []
    if start.x == stop.x:
        for y in range(start.y, stop.y, stepy):
            res.append(Pos(start.x, y))
    elif start.y == stop.y:
        for x in range(start.x, stop.x, stepx):
            res.append(Pos(x, start.y))

    return res


def randomPos(width, height):
    x = random.choice(range(50, width - 50, 5))
    y = random.choice(range(50, height - 50, 5))
    return Pos(x, y)


class Setting:
    def __init__(self, arrowControl=True, DBBY=True, speed=0):
        self.arrowControl = arrowControl
        self.DBBY = DBBY  # die by bit yourself
        self.speed = speed
        if speed == 0:
            self.TS = 0.04  # time sleep
        elif speed == -1:
            self.TS = 0.16
        else:
            self.TS = 0.01


if __name__ == '__main__':
    a = Pos(9, 2)
    b = Pos(5, 2)
    for i in rangePos(a, b):
        print(i)
    print()
    print(a)
