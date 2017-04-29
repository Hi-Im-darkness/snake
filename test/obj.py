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
        pos = Pos(self.pos.x + self.stepx, self.pos.y + self.stepy)
        if self.grid[pos.x][pos.y] == 1:
            self.pos = pos


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
        self.id = self.canvas.create_image(self.pos.x - 13, self.pos.y - 10, anchor=tk.NW, image=self.headImage)

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
        self.canvas.move(self.id, self.stepx, self.stepy)
        pos = Pos(self.pos.x + self.stepx, self.pos.y + self.stepy)
        if self.grid[pos.x][pos.y] == 1:
            self.grid[self.pos.x][self.pos.y] = 0
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
                pos[1] -= 5
                pos[0] -= 5
            elif index in range(1, self.lenght - 1):
                pos[1] -= 3
                pos[0] -= 3

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

    def getFood(self, food):
        head = self.pieces[0]
        tp = head.pos.y - 10
        bm = head.pos.y + 10
        lt = head.pos.x - 10
        rt = head.pos.x + 10

        if food.pos.x >= lt and food.pos.x <= rt:
            if food.pos.y >= tp and food.pos.y <= bm:
                return True
        return False

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
        # pass
        # self.lenght += 1
        # head = self.pieces[0]
        # head.delete()

        # x = head.pos.x
        # y = head.pos.y
        # direct = head.direct
        # color = head.color
        # self.pieces[0] = Bodies(self.canvas, self.grid, direct, x, y, color)

        # if head.direct == 'Right':
        #     for i in range(x, x + 5):
        #         self.grid[i][y] = 1
        #     x = x + 5
        # elif head.direct == 'Left':
        #     for i in range(x - 4, x + 1):
        #         self.grid[i][y] = 1
        #     x = x - 5
        # elif head.direct == 'Up':
        #     for i in range(y - 4, y + 1):
        #         self.grid[x][i] = 1
        #     y = y - 5
        # else:
        #     for i in range(y, y + 5):
        #         self.grid[x][i] = 1
        #     y = y + 5

        # self.pieces = [Head(self.canvas, self.grid, direct, x, y, color)] + self.pieces
        self.lenght += 1
        tail = self.pieces[-1]
        tail.delete()

        direct = tail.direct
        x = tail.pos.x
        y = tail.pos.y
        color = self.pieces[0].color

        if tail.direct == 'Left':
            x = x + 2
            self.pieces[-1] = Bodies(self.canvas, self.grid, direct, x, y, color)
            for i in range(x - 2, x + 4):
                self.grid[i][y] = 1
            x = x + 3
        elif tail.direct == 'Right':
            x = x - 2
            self.pieces[-1] = Bodies(self.canvas, self.grid, direct, x, y, color)
            for i in range(x - 3, x + 3):
                self.grid[i][y] = 1
            x = x - 3
        elif tail.direct == 'Up':
            y = y + 2
            self.pieces[-1] = Bodies(self.canvas, self.grid, direct, x, y, color)
            for i in range(y - 2, y + 4):
                self.grid[x][i] = 1
            y = y + 3
        else:
            y = y - 2
            self.pieces[-1] = Bodies(self.canvas, self.grid, direct, x, y, color)
            for i in range(y - 3, y + 3):
                self.grid[x][i] = 1
            y = y - 3

        self.pieces.append(Tail(self.canvas, self.grid, direct, x, y, color))


class Foods:
    def __init__(self, canvas, grid, x=0, y=0, color='red'):
        self.canvas = canvas
        self.pos = Pos(x, y)
        self.grid = grid
        self.grid[x][y] = '+'
        self.id = canvas.create_oval(0, 0, 5, 5, fill=color, outline=color)
        self.canvas.move(self.id, x, y)


if __name__ == '__main__':
    window = tk.Tk()
    canvas = tk.Canvas(window, width=400, height=400)
    canvas.pack()

    grid = [[0 for i in range(500)] for i in range(500)]

    s = Snakes(canvas, grid, 50, 200)

    # for i in range(10):
    # s.pieces[0].changeDirect('Down')
    # s.grow()

    while True:
        canvas.bind_all('<KeyPress>', s.keyPress)
        # for row in s.grid:
        #     print(row)
        # print('\n')
        for p in s.pieces:
        #     print(p.pos.x, p.pos.y)
            pos = canvas.coords(p.id)
            print(pos[0], pos[1])
        print('\n')
        s.move()
        if s.isDie():
            break
        canvas.update()
        time.sleep(0.01)
    window.mainloop()
