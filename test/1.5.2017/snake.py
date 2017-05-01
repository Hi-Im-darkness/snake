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

    def delete(self):
        self.canvas.delete(self.id)


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
        if self.pos.x > 400:
            self.canvas.move(self.id, -400, 0)
            self.pos.x -= 400
        elif self.pos.x < 0:
            self.canvas.move(self.id, 400, 0)
            self.pos.x += 400
        elif self.pos.y > 400:
            self.canvas.move(self.id, 0, -400)
            self.pos.y -= 400
        elif self.pos.y < 0:
            self.canvas.move(self.id, 0, 400)
            self.pos.y += 400


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


class Snake:
    def __init__(self, canvas, pos, color='Green'):
        self.canvas = canvas
        self.lenght = 10

        self.bodies = []
        self.bodies.append(Tail(canvas, pos, color))

        self.bodyPos = []
        for x in range(pos.x, pos.x - 5 + 5 * self.lenght):
            self.bodyPos = [Pos(x, pos.y)] + self.bodyPos
            if (x - pos.x) in range(1, pos.x - 5 + 5 * self.lenght, 5):
                self.bodies = [Bodies(canvas, Pos(x, pos.y), color)] + self.bodies

        x = pos.x - 5 + 5 * self.lenght
        self.head = Head(canvas, 'Right', Pos(x, pos.y), color)

    def move(self):
        self.grow()
        self.lenght -= 1

        self.bodies[-1].delete()
        self.bodies[-2].delete()

        self.bodies[-2] = Tail(self.canvas, self.bodies[-2].pos, self.bodies[-2].color)
        del self.bodies[-1]
        for i in range(5):
            del self.bodyPos[-1]

        if self.head.pos.x > 400:
            self.canvas.move(self.head.id, -400, 0)
            self.head.pos.x -= 400
        elif self.head.pos.x < 0:
            self.canvas.move(self.head.id, 400, 0)
            self.head.pos.x += 400
        elif self.head.pos.y > 400:
            self.canvas.move(self.head.id, 0, -400)
            self.head.pos.y -= 400
        elif self.head.pos.y < 0:
            self.canvas.move(self.head.id, 0, 400)
            self.head.pos.y += 400

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
            x = self.head.pos.x - 5
            for i in range(x + 5, x, -1):
                self.bodyPos = [Pos(i, y)] + self.bodyPos
        elif self.head.direct == 'Right':
            x = self.head.pos.x + 5
            for i in range(x - 5, x):
                self.bodyPos = [Pos(i, y)] + self.bodyPos
        elif self.head.direct == 'Up':
            y = self.head.pos.y - 5
            for i in range(y + 5, y, -1):
                self.bodyPos = [Pos(x, i)] + self.bodyPos
        else:
            y = self.head.pos.y + 5
            for i in range(y - 5, y):
                self.bodyPos = [Pos(x, i)] + self.bodyPos

        self.head = Head(self.canvas, self.head.direct, Pos(x, y), self.head.color)

    def getFood(self, food):
        headPos = self.head.pos
        tp = headPos.y - 13
        bm = headPos.y + 13
        lt = headPos.x - 13
        rt = headPos.x + 13

        foodPos = self.canvas.coords(food.normal.id)
        if foodPos[1] >= tp and foodPos[3] <= bm:
            if foodPos[0] >= lt and foodPos[2] <= rt:
                food.normal.delete()
                return True
        return False


class BotSnake(Snake):
    def __init__(self, canvas, pos, color='Yellow'):
        Snake.__init__(self, canvas, pos, color)
        self.step = None

    def huntFood(self, food):
        self.food = food
        taget = food.normal
        head = self.head
        if head.direct == 'Left' or head.direct == 'Right':
            if head.pos.y < taget.pos.y:
                self.step = [Pos(taget.pos.x, head.pos.y), 'Down']
            elif head.pos.y > taget.pos.y:
                self.step = [Pos(taget.pos.x, head.pos.y), 'Up']
        else:
            if head.pos.x < taget.pos.x:
                self.step = [Pos(head.pos.x, taget.pos.y), 'Right']
            elif head.pos.x > taget.pos.x:
                self.step = [Pos(head.pos.x, taget.pos.y), 'Left']

    def isBlock(self, hurdle):
        x = self.head.pos.x + self.head.stepx * 5
        y = self.head.pos.y + self.head.stepy * 5
        nextPos = Pos(x, y)
        if nextPos in hurdle:
            return True
        return False

    def move(self):
        if self.step is not None:
            turnPoint = self.step[0]
            direct = self.step[1]
            if self.head.pos == turnPoint:
                self.head.changeDirect(direct)
                self.step = None

        if self.isBlock(self.bodyPos):
            if self.head.direct == 'Left' or self.head.direct == 'Right':
                self.head.changeDirect('Up')
                if self.isBlock(self.bodyPos):
                    self.head.changeDirect('Down')
            else:
                self.head.changeDirect('Left')
                if self.isBlock(self.bodyPos):
                    self.head.changeDirect('Right')
            self.huntFood(self.food)

        Snake.move(self)


if __name__ == '__main__':
    window = tk.Tk()
    canvas = tk.Canvas(window, width=400, height=400)
    canvas.pack()

    # h = Head(canvas, grid, 'Up', Pos(100, 100), 'Green')
    s = Snake(canvas, Pos(100, 100))

    while True:
        time.sleep(0.01)
        # canvas.bind_all('<KeyPress>', .keyPress)
        s.move()
        canvas.update()
    window.mainloop()
