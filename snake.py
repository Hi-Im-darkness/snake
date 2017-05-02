import tkinter as tk
import time
from other import *
from food import *


class Pieces:
    def __init__(self, canvas, x, y, color):
        self.canvas = canvas
        self.pos = Pos(x, y)
        self.color = color

    def delete(self):
        self.canvas.delete(self.id)

    def move(self, x, y):
        self.canvas.move(self.id, x, y)
        self.pos = self.pos + Pos(x, y)


class Head(Pieces):
    def __init__(self, canvas, x, y, direct, color='Green'):
        Pieces.__init__(self, canvas, x, y, color)
        self.id = None
        self.changeDirect(direct)

    def changeDirect(self, direct):
        self.direct = Direction(direct)
        self.image = tk.PhotoImage(file='Asset/%s/Head/%s.gif' % (self.color, self.direct.value))
        self.update()

    def update(self):
        if self.id is not None:
            self.canvas.delete(self.id)
        self.id = self.canvas.create_image(self.pos.x, self.pos.y, anchor=tk.CENTER, image=self.image)

    def frontPos(self):
        return self.pos + Pos(self.direct.stepx, self.direct.stepy)

    def leftPos(self):
        ltDirect = self.direct.left()
        return self.pos + Pos(ltDirect.stepx, ltDirect.stepy)

    def rightPos(self):
        rtDirect = self.direct.right()
        return self.pos + Pos(rtDirect.stepx, rtDirect.stepy)


class Bodies(Pieces):
    def __init__(self, canvas, x, y, color='Green'):
        Pieces.__init__(self, canvas, x, y, color)
        self.image = tk.PhotoImage(file='Asset/%s/Body.gif' % color)
        self.id = self.canvas.create_image(self.pos.x, self.pos.y, anchor=tk.CENTER, image=self.image)


class Tail(Pieces):
    def __init__(self, canvas, x, y, color='Green'):
        Pieces.__init__(self, canvas, x, y, color)
        self.image = tk.PhotoImage(file='Asset/%s/Tail.gif' % color)
        self.id = self.canvas.create_image(self.pos.x, self.pos.y, anchor=tk.CENTER, image=self.image)


class Snake:
    def __init__(self, canvas, x, y, direct='Right', color='Green'):
        self.canvas = canvas
        self.lenght = 2

        self.tail = Tail(canvas, x, y, color)
        x += Direction(direct).stepx
        y += Direction(direct).stepy
        self.head = Head(canvas, x, y, direct, color)
        self.bodies = []

        self.bodyPos = []
        for pos in rangePos(self.tail.pos, self.head.pos):
            self.bodyPos = [pos] + self.bodyPos

        for i in range(4):
            self.grow()

    def grow(self):
        self.lenght += 1

        self.bodies = [Bodies(self.canvas, self.head.pos.x, self.head.pos.y, self.head.color)] + self.bodies
        self.head.move(self.head.direct.stepx, self.head.direct.stepy)
        self.head.update()

        for pos in rangePos(self.bodies[0].pos, self.head.pos):
            self.bodyPos = [pos] + self.bodyPos

    def move(self):
        self.grow()
        self.lenght -= 1

        self.bodies[-1].delete()
        self.tail.delete()

        self.tail = Tail(self.canvas, self.bodies[-1].pos.x, self.bodies[-1].pos.y, self.bodies[-1].color)
        del self.bodies[-1]
        for i in range(5):
            self.bodyPos.pop()

        width = 400
        height = 400
        if self.head.pos.x > width:
            self.head.move(-width, 0)
        elif self.head.pos.x < 0:
            self.head.move(width, 0)
        elif self.head.pos.y > height:
            self.head.move(0, -height)
        elif self.head.pos.y < 0:
            self.head.move(0, height)

    def isDie(self, enemy=None):
        hurdle = enemy.bodyPos if enemy is not None else []
        if self.head.pos in self.bodyPos + hurdle:
            return True
        return False

    def getFood(self, food):
        headPos = self.head.pos
        tp = headPos.y - 13
        bm = headPos.y + 13
        lt = headPos.x - 13
        rt = headPos.x + 13

        nFoodPos = food.normal.pos
        if nFoodPos.y >= tp and nFoodPos.y <= bm:
            if nFoodPos.x >= lt and nFoodPos.x <= rt:
                food.normal.delete()
                return True
        return False


class BotSnake(Snake):
    def __init__(self, canvas, x, y, direct='Right', color='Yellow'):
        Snake.__init__(self, canvas, x, y, direct, color)

    def findDirect(self, food, enemy):
        isDie = True
        disDict = {}
        hurdle = [] if enemy is None else enemy.bodyPos
        for h in hurdle:
            print(h)
        hurdle += self.bodyPos

        for d in ('front', 'left', 'right'):
            getPos = getattr(self.head, '%sPos' % d)
            pos = getPos()
            if pos in hurdle:
                continue
            isDie = False
            dist = distance(pos, food.normal.pos)
            if dist in disDict:
                disDict[dist].append(d)
            else:
                disDict[dist] = [d]

        if isDie:
            return -1

        disList = list(disDict.keys())
        disList.sort()

        res = disDict[disList[0]][0]
        if res == 'front':
            return -1
        elif res == 'left':
            return self.head.direct.left().value
        else:
            return self.head.direct.right().value

    def move(self, food, enemy=None):
        direct = self.findDirect(food, enemy)
        if direct != -1:
            self.head.changeDirect(direct)
        Snake.move(self)


def keyPress(event):
    headD = s2.head.direct.value
    if headD == 'Left' and (event.keysym == 'Right' or event.keysym == headD):
        return
    if headD == 'Right' and (event.keysym == 'Left' or event.keysym == headD):
        return
    if headD == 'Down' and (event.keysym == 'Up' or event.keysym == headD):
        return
    if headD == 'Up' and (event.keysym == 'Down' or event.keysym == headD):
        return

    s2.head.changeDirect(event.keysym)


if __name__ == '__main__':
    window = tk.Tk()
    canvas = tk.Canvas(window, width=400, height=400)
    canvas.pack()

    s1 = BotSnake(canvas, 100, 100)
    s2 = BotSnake(canvas, 100, 300)
    f = Foods(canvas)
    f.add()

    while True:
        if s1.getFood(f):
            f.add()
            s1.grow()
        if s2.getFood(f):
            f.add()
            s2.grow()
        s1.move(f)
        s2.move(f)
        # if s2.isDie():
        #     break
        # canvas.bind_all('<KeyPress>', keyPress)
        canvas.update()
        time.sleep(0.0004)
    window.mainloop()
