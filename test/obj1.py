import tkinter as tk
import time


class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, value):
        if self.x == value.x and self.y == value.y:
            return True
        return False


class Animation:
    def __init__(self, canvas, grid, direct, x, y):
        self.canvas = canvas
        self.grid = grid
        self.direct = direct
        self.pos = Pos(x, y)
        self.grid[self.pos.x][self.pos.y] = 1
        self.changeDirect(direct)

    def delete(self):
        self.canvas.delete(self.id)
        self.grid[self.pos.x][self.pos.y] = 0

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

    def move(self):
        self.canvas.move(self.id, self.stepx, self.stepy)
        self.grid[self.pos.x][self.pos.y] = 0
        self.pos.x += self.stepx
        self.pos.y += self.stepy
        self.grid[self.pos.x][self.pos.y] = 1


class Bodies(Animation):
    def __init__(self, canvas, grid, direct, x=0, y=-3, color='green'):
        Animation.__init__(self, canvas, grid, direct, x, y)
        if color == 'green':
            color = '#66cc33'
        else:
            color = '#e7db1f'
        self.id = canvas.create_oval(0, 0, 14, 14, fill=color, outline=color)
        canvas.move(self.id, x - 13, y - 7)


class Head(Animation):
    def __init__(self, canvas, grid, direct, x=0, y=0, color='green'):
        self.color = color
        Animation.__init__(self, canvas, grid, direct, x, y)

    def changeDirect(self, direct):
        Animation.changeDirect(self, direct)
        if self.color == 'green':
            self.headImage = tk.PhotoImage(file='asset/head1/%s.gif' % direct)
        else:
            self.headImage = tk.PhotoImage(file='asset/head2/%s.gif' % direct)
        self.id = canvas.create_image(self.pos.x - 13, self.pos.y - 10, anchor=tk.NW, image=self.headImage)


class Snakes:
    def __init__(self, canvas, grid, x=0, y=0, color='green'):
        self.canvas = canvas
        self.lenght = 30
        self.color = color

        self.head = Head(canvas, grid, 'Right', x + self.lenght, y, color)
        self.bodies = []
        for i in range(x - 1 + self.lenght, x - 1, -1):
            self.bodies.append(Bodies(canvas, grid, 'Right', i, y, color))

        # self.pieces = [Head(canvas, x + 3 + 5 * (self.lenght - 2), y, color)]
        # for i in range(x + 3 + 5 * (self.lenght - 3), x + -2, -5):
        #     self.pieces.append(Bodies(canvas, i, y, color))
        # self.pieces.append(Tail(canvas, x, y, color))

        self.inProcess = []

    def move(self):
        rm = []
        for process in self.inProcess:
            headPos = process[0]
            direct = process[1]
            index = process[2]
            # pos = self.canvas.coords(self.pieces[index].id)
            # if index == self.lenght - 1:
            #     pos[0] -= 5
            #     pos[1] -= 5
            # elif index in range(1, self.lenght - 1):
            #     pos[0] -= 3
            #     pos[1] -= 3

            print(headPos, self.bodies[index].pos)
            if headPos == self.bodies[index].pos:
                self.bodies[index].changeDirect(direct)
                if index == self.lenght - 2:
                    rm.append(process)
                else:
                    process[2] += 1

        for pro in rm:
            self.inProcess.remove(pro)

        self.head.move()
        for piece in self.bodies:
            piece.move()

    def isDie(self):
        head = self.pieces[0]
        headPos = self.canvas.coords(head.id)
        if head.direct == 'Left':
            x = headPos[0] + 5
            y = headPos[1] + 10
        elif head.direct == 'Down':
            x = headPos[0] + 10
            y = headPos[1] + 21
        elif head.direct == 'Right':
            x = headPos[0] + 21
            y = headPos[1] + 10
        else:
            x = headPos[0] + 10
            y = headPos[1] + 5

        for body in self.pieces[3:]:
            pos = self.canvas.coords(body.id)
            if x > pos[0] and x < pos[2]:
                if y > pos[1] and y < pos[3]:
                    return True
        return False

    def keyPress(self, event):
        if self.head.direct == 'Left' and (event.keysym == 'Right' or event.keysym == self.head.direct):
            return
        if self.head.direct == 'Right' and (event.keysym == 'Left' or event.keysym == self.head.direct):
            return
        if self.head.direct == 'Down' and (event.keysym == 'Up' or event.keysym == self.head.direct):
            return
        if self.head.direct == 'Up' and (event.keysym == 'Down' or event.keysym == self.head.direct):
            return

        self.head.changeDirect(event.keysym)
        self.inProcess.append([self.head.pos, event.keysym, 0])

    def grow(self, lenght=1):
        self.lenght += lenght
        head = self.pieces[0]
        headPos = self.canvas.coords(head.id)
        add = []
        if head.direct == 'Right':
            self.canvas.move(head.id, 5 * lenght, 0)
            for x in range(int(headPos[0]), int(headPos[0]) + 5 * lenght, 5):
                add.append(Bodies(self.canvas, x, headPos[1], self.color))
        elif head.direct == 'Left':
            for x in range(int(headPos[0]), int(headPos[0]) - 5 * lenght, -5):
                add.append(Bodies(self.canvas, x, headPos[1], self.color))
            self.canvas.move(head.id, -5 * lenght, 0)
        elif head.direct == 'Down':
            for y in range(int(headPos[1]), int(headPos[1]) + 5 * lenght, 5):
                add.append(Bodies(self.canvas, headPos[0], y, self.color))
            self.canvas.move(head.id, 0, 5 * lenght)
        else:
            for y in range(int(headPos[1]) + 5 * lenght, int(headPos[1]), -5):
                add.append(Bodies(self.canvas, headPos[0], y, self.color))
            self.canvas.move(head.id, 0, -5 * lenght)
        self.pieces = [self.pieces[0]] + add + self.pieces[1:]


class Foods:
    def __init__(self, canvas, x=0, y=0, color='red'):
        self.canvas = canvas
        self.id = canvas.create_oval(0, 0, 5, 5, fill=color, outline=color)
        self.canvas.move(self.id, x, y)


if __name__ == '__main__':
    window = tk.Tk()
    canvas = tk.Canvas(window, width=600, height=600)
    canvas.pack()

    grid = [[0 for i in range(601)] for i in range(601)]

    s = Snakes(canvas, grid, 100, 100)

    # print(s.pieces)
    while True:
        canvas.bind_all('<KeyPress>', s.keyPress)
        print(s.inProcess)
        s.move()
        # if s.isDie():
        #     break
        canvas.update()
        time.sleep(0.01)
    window.mainloop()
