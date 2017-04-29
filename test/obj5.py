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


class Object:
    def __init__(self, canvas, grid, direct, x, y):
        self.canvas = canvas
        self.grid = grid
        self.pos = Pos(x, y)
        self.grid[self.pos.x][self.pos.y] = 1
        self.stepx = 1
        self.stepy = 0
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


class Bodies(Object):
    def __init__(self, canvas, grid, direct, x=0, y=-3, color='green'):
        Object.__init__(self, canvas, grid, direct, x, y)
        if color == 'green':
            color = '#66cc33'
        else:
            color = '#e7db1f'
        self.id = canvas.create_oval(0, 0, 14, 14, fill=color, outline=color)
        canvas.move(self.id, x - 13, y - 7)

    def move(self):
        self.canvas.move(self.id, self.stepx, self.stepy)
        self.pos = Pos(self.pos.x + self.stepx, self.pos.y + self.stepy)


class Head(Object):
    def __init__(self, canvas, grid, direct, x=0, y=0, color='green'):
        self.color = color
        Object.__init__(self, canvas, grid, direct, x, y)
        self.grid[self.pos.x][self.pos.y] = 0

    def changeDirect(self, direct):
        Object.changeDirect(self, direct)
        if self.color == 'green':
            self.headImage = tk.PhotoImage(file='asset/head1/%s.gif' % direct)
        else:
            self.headImage = tk.PhotoImage(file='asset/head2/%s.gif' % direct)
        self.id = canvas.create_image(self.pos.x - 13, self.pos.y - 10, anchor=tk.NW, image=self.headImage)

    def move(self):
        self.grid[self.pos.x][self.pos.y] = 1
        self.canvas.move(self.id, self.stepx, self.stepy)
        self.pos = Pos(self.pos.x + self.stepx, self.pos.y + self.stepy)


class Tail(Object):
    def __init__(self, canvas, grid, direct, x=0, y=-5, color='green'):
        Object.__init__(self, canvas, grid, direct, x, y)
        if color == 'green':
            color = '#66cc33'
        else:
            color = '#e7db1f'
        self.id = canvas.create_oval(0, 0, 10, 10, fill=color, outline=color)
        canvas.move(self.id, x - 13, y - 5)

    def move(self):
        self.grid[self.pos.x][self.pos.y] = 0
        self.canvas.move(self.id, self.stepx, self.stepy)
        pos = Pos(self.pos.x + self.stepx, self.pos.y + self.stepy)
        if self.grid[pos.x][pos.y] == 1:
            self.pos = pos


class Snakes:
    def __init__(self, canvas, grid, x=0, y=0, color='green'):
        self.canvas = canvas
        self.lenght = 6
        self.color = color
        self.grid = grid

        self.pieces = [Head(canvas, grid, 'Right', x - 7 + 5 * self.lenght, y, color)]
        for i in range(x - 12 + 5 * self.lenght, x - 2, -5):
            self.pieces.append(Bodies(canvas, grid, 'Right', i, y, color))
        self.pieces.append(Tail(canvas, grid, 'Right', x, y, color))

        for i in range(x + 1, x - 7 + 5 * self.lenght):
            self.grid[i][y] = 1

        self.inProcess = []

    def move(self):
        rm = []
        for process in self.inProcess:
            x = process[0]
            y = process[1]
            direct = process[2]
            index = process[3]
            pos = self.canvas.coords(self.pieces[index].id)
            if index == self.lenght - 1:
                pos[0] -= 5
                pos[1] -= 5
            elif index in range(1, self.lenght - 1):
                pos[0] -= 3
                pos[1] -= 3
            if pos[0] == x and pos[1] == y:
                self.pieces[index].changeDirect(direct)
                if index == self.lenght - 1:
                    rm.append(process)
                else:
                    process[3] += 1

        for pro in rm:
            self.inProcess.remove(pro)

        for o in self.pieces:
            o.move()

    def isDie(self):
        head = self.pieces[0]
        if self.grid[head.pos.x][head.pos.y] == 1:
            return True
        return False

    def keyPress(self, event):
        head = self.pieces[0]
        if head.direct == 'Left' and (event.keysym == 'Right' or event.keysym == head.direct):
            return
        if head.direct == 'Right' and (event.keysym == 'Left' or event.keysym == head.direct):
            return
        if head.direct == 'Down' and (event.keysym == 'Up' or event.keysym == head.direct):
            return
        if head.direct == 'Up' and (event.keysym == 'Down' or event.keysym == head.direct):
            return

        pos = self.canvas.coords(self.pieces[0].id)
        self.inProcess.append(pos + [event.keysym, 0])

    def grow(self):
        self.lenght += 1
        head = self.pieces[0]
        self.pieces[0].delete()

        x = head.pos.x
        y = head.pos.y
        direct = head.direct
        color = head.color

        self.pieces[0] = Bodies(self.canvas, self.grid, direct, x, y, color)
        x = x * 2 - self.pieces[1].pos.x
        y = y * 2 - self.pieces[1].pos.y

        for i in range(head.pos.x, x):
            self.grid[i][y] = 1
        for i in range(head.pos.y, y):
            self.grid[x][i] = 1
        for i in range(head.pos.x, x, -1):
            self.grid[i][y] = 1
        for i in range(head.pos.y, y, -1):
            self.grid[x][i] = 1

        self.pieces = [Head(self.canvas, self.grid, direct, x, y, color)] + self.pieces


class Foods:
    def __init__(self, canvas, x=0, y=0, color='red'):
        self.canvas = canvas
        self.id = canvas.create_oval(0, 0, 5, 5, fill=color, outline=color)
        self.canvas.move(self.id, x, y)


if __name__ == '__main__':
    window = tk.Tk()
    canvas = tk.Canvas(window, width=400, height=400)
    canvas.pack()

    grid = [[0 for i in range(400)] for i in range(400)]

    s = Snakes(canvas, grid, 4, 4)
    s.grow()
    while True:
        canvas.bind_all('<KeyPress>', s.keyPress)
        s.move()
        if s.isDie():
            break
        canvas.update()
        time.sleep(0.01)
    window.mainloop()
