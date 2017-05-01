import tkinter as tk
import time
from other import *


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
            del self.bodyPos[-1]

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
        anotherBP = enemy.bodyPos if enemy is not None else []
        if self.head.pos in self.bodyPos + anotherBP:
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


def keyPress(event):
    headD = s.head.direct.value
    if headD == 'Left' and (event.keysym == 'Right' or event.keysym == headD):
        return
    if headD == 'Right' and (event.keysym == 'Left' or event.keysym == headD):
        return
    if headD == 'Down' and (event.keysym == 'Up' or event.keysym == headD):
        return
    if headD == 'Up' and (event.keysym == 'Down' or event.keysym == headD):
        return

    s.head.changeDirect(event.keysym)


if __name__ == '__main__':
    window = tk.Tk()
    canvas = tk.Canvas(window, width=400, height=400)
    canvas.pack()

    s = Snake(canvas, 100, 100)

    while True:
        s.move()
        if s.isDie():
            break
        canvas.bind_all('<KeyPress>', keyPress)
        canvas.update()
        time.sleep(0.03)
    window.mainloop()
