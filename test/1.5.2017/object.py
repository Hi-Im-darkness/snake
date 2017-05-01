import tkinter as tk
import time


class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, oPos):
        if self.x == oPos.x and self.y == oPos.y:
            return True
        return False


class Obj:
    def __init__(self, canvas, pos, color):
        self.canvas = canvas
        self.pos = pos
        self.color = color


class Head(Obj):
    def __init__(self, canvas, direct, pos, color='Green'):
        Obj.__init__(self, canvas, pos, color)
        self.changeDirect(direct)

    def changeDirect(self, direct):
        self.direct = direct
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
        self.image = tk.PhotoImage(file='Asset/%s/Head/%s.gif' % (self.color, self.direct))
        self.id = self.canvas.create_image(self.pos.x, self.pos.y, anchor=tk.CENTER, image=self.image)

    def move(self):
        self.canvas.move(self.id, self.stepx, self.stepy)
        self.pos = Pos(self.pos.x + self.stepx, self.pos.y + self.stepy)

    def delete(self):
        self.canvas.delete(self.id)


class Bodies(Obj):
    def __init__(self, canvas, pos, color='Green'):
        Obj.__init__(self, canvas, pos, color)
        self.image = tk.PhotoImage(file='Asset/%s/Body.gif' % color)
        self.id = self.canvas.create_image(self.pos.x, self.pos.y, anchor=tk.CENTER, image=self.image)


class Tail(Obj):
    def __init__(self, canvas, pos, color='Green'):
        Obj.__init__(self, canvas, pos, color)
        self.image = tk.PhotoImage(file='Asset/%s/Tail.gif' % color)
        self.id = self.canvas.create_image(self.pos.x, self.pos.y, anchor=tk.CENTER, image=self.image)

    def delete(self):
        self.canvas.delete(self.id)


class Snake:
    def __init__(self, canvas, pos, color='Green'):
        self.canvas = canvas
        self.lenght = 6

        self.bodies = []
        self.bodies.append(Tail(canvas, pos, color))

        self.bodyPos = []
        for x in range(pos.x, pos.x - 6 + 6 * self.lenght):
            self.bodyPos = [Pos(x, pos.y)] + self.bodyPos
            if (x - pos.x) in range(6, pos.x - 6 + 6 * self.lenght, 6):
                self.bodies = [Bodies(canvas, Pos(x, pos.y), color)] + self.bodies

        x = pos.x - 6 + 6 * self.lenght
        self.head = Head(canvas, 'Right', Pos(x, pos.y), color)

    def move(self):
        self.bodyPos = [self.head.pos] + self.bodyPos
        del self.bodyPos[-1]
        self.head.move()

        i = 5
        for body in self.bodies:
            taget = self.bodyPos[i]
            x = taget.x - body.pos.x
            y = taget.y - body.pos.y
            body.pos = taget
            self.canvas.move(body.id, x, y)
            i += 6

    def isDie(self):
        if self.head.pos in self.bodyPos:
            return True
        return False

    def grow(self):
        self.lenght += 1
        self.head.delete()

        self.bodies = [Bodies(self.canvas, self.head.pos, self.head.color)] + self.bodies

        x = self.head.pos.x
        y = self.head.pos.y
        if self.head.direct == 'Left':
            x = self.head.pos.x - 6
            for i in range(x + 5, x - 1, -1):
                self.bodyPos = [Pos(i, y)] + self.bodyPos
        elif self.head.direct == 'Right':
            x = self.head.pos.x + 6
            for i in range(x - 5, x + 1):
                self.bodyPos = [Pos(i, y)] + self.bodyPos
        elif self.head.direct == 'Up':
            y = self.head.pos.y - 6
            for i in range(y + 5, y - 1, -1):
                self.bodyPos = [Pos(x, i)] + self.bodyPos
        else:
            y = self.head.pos.y + 6
            for i in range(y - 5, y + 1):
                self.bodyPos = [Pos(x, i)] + self.bodyPos

        self.head = Head(self.canvas, self.head.direct, Pos(x, y), self.head.color)

    def getFood(self, food):
        headPos = self.head.pos
        tp = headPos.y - 13
        bm = headPos.y + 13
        lt = headPos.x - 13
        rt = headPos.x + 13

        foodPos = self.canvas.coords(food.id)
        if foodPos[1] >= tp and foodPos[3] <= bm:
            if foodPos[0] >= lt and foodPos[2] <= rt:
                return True
        return False

# class BotSnake(Snake):
#     def __init__(self, canvas, pos, color='Yellow'):
#         Snake.__init__(self, canvas, pos, color)

#     def autoMove(self)


class Foods:
    def __init__(self, canvas, pos, color='red'):
        self.point = 8
        self.canvas = canvas
        self.id = canvas.create_oval(0, 0, 5, 5, fill=color, outline=color)
        self.canvas.move(self.id, pos.x, pos.y)


class BigFoods:
    def __init__(self, canvas, pos, color='red'):
        self.point = 400
        self.canvas = canvas
        self.id = canvas.create_oval(0, 0, 30, 30, fill=color, outline=color)
        self.canvas.move(self.id, pos.x - 15, pos.y - 15)


if __name__ == '__main__':
    window = tk.Tk()
    canvas = tk.Canvas(window, width=600, height=600)
    canvas.pack()

    # h = Head(canvas, grid, 'Up', Pos(100, 100), 'Green')
    s = Snake(canvas, Pos(100, 100))

    while True:
        time.sleep(1)
        # canvas.bind_all('<KeyPress>', .keyPress)
        s.move()
        canvas.update()
    window.mainloop()
