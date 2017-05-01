import tkinter as tk
import random
import time
import os
from snake import Pos


def randomPos(width, height):
    x = random.choice(range(50, width - 50, 5))
    y = random.choice(range(50, height - 50, 5))
    return Pos(x, y)


class NormalFood:
    def __init__(self, canvas, pos, color='red'):
        self.point = 8
        self.canvas = canvas
        self.pos = pos
        self.id = canvas.create_oval(0, 0, 5, 5, fill=color, outline=color)
        self.canvas.move(self.id, pos.x, pos.y)

    def delete(self):
        self.canvas.delete(self.id)


class BigFood:
    def __init__(self, canvas, pos, color='red'):
        self.point = 400
        self.start = time.time()
        self.canvas = canvas
        self.pos = pos
        self.id = canvas.create_oval(0, 0, 30, 30, fill=color, outline=color)
        self.canvas.move(self.id, pos.x - 15, pos.y - 15)

    def delete(self):
        self.canvas.delete(self.id)

    def run(self):
        while self.id is not None:
            after = time.time()
            if after - self.start >= 3:
                self.delete()


class Foods:
    def __init__(self, canvas):
        self.canvas = canvas
        self.normal = None
        self.big = None

        self.count = 0

    def addNormal(self):
        if self.normal is not None:
            self.canvas.delete(self.normal.id)

        self.normal = NormalFood(self.canvas, randomPos(350, 350))
        self.count += 1

    def addBig(self):
        self.big = BigFood(self.canvas, randomPos(350, 350))

    def add(self):
        # if self.normal is not None:
        #     self.normal.delete()

        self.normal = NormalFood(self.canvas, randomPos(350, 350))
        self.count += 1


def main():
    window = tk.Tk()
    window.title('Snake')
    window.resizable(0, 0)
    canvas = tk.Canvas(window, width=600, height=600)
    canvas.pack()

    f = Foods(canvas)
    while True:
        f.add()
        canvas.update()
        time.sleep(1)

    window.mainloop()


if __name__ == '__main__':
    main()
