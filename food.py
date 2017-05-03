import tkinter as tk
from other import *


class NormalFood:
    def __init__(self, canvas, x, y, color='red'):
        self.point = 8
        self.canvas = canvas
        self.pos = Pos(x, y)
        self.id = canvas.create_oval(0, 0, 8, 8, fill=color, outline=color)
        self.canvas.move(self.id, x - 4, y - 4)

    def delete(self):
        self.canvas.delete(self.id)


class Foods:
    def __init__(self, canvas):
        self.canvas = canvas
        self.normal = None

    def add(self):
        if self.normal is not None:
            self.normal.delete()

        pos = randomPos(400, 400)
        self.normal = NormalFood(self.canvas, pos.x, pos.y)
