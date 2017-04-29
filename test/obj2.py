import tkinter as tk
import time


class Action:
    def __init__(self, canvas, grid, x, y):
        self.canvas = canvas
        self.grid = grid
        self.x = x
        self.y = y
        self.grid[self.x][self.y] = 1

    def delete(self):
        self.canvas.delete(self.id)
        self.grid[self.x][self.y] = 0


class Bodies(Action):
    def __init__(self, canvas, grid, x=0, y=-3, color='green'):
        Action.__init__(self, canvas, grid, x, y)
        if color == 'green':
            color = '#66cc33'
        else:
            color = '#e7db1f'
        self.id = canvas.create_oval(0, 0, 14, 14, fill=color, outline=color)
        canvas.move(self.id, x - 13, y - 7)


class Head(Action):
    def __init__(self, canvas, grid, x=0, y=0, direct='Right', color='green'):
        Action.__init__(self, canvas, grid, x, y)
        self.color = color
        self.direct = direct
        if color == 'green':
            self.headImage = tk.PhotoImage(file='asset/head1/%s.gif' % direct)
        else:
            self.headImage = tk.PhotoImage(file='asset/head2/%s.gif' % direct)
        self.id = canvas.create_image(0, 0, anchor=tk.NW, image=self.headImage)
        if direct == 'Up':
            canvas.move(self.id, x - 13, y - 15)
        else:
            canvas.move(self.id, x - 13, y - 10)

    def changeDirect(self, direct):
        self.direct = direct
        if self.color == 'green':
            self.headImage = tk.PhotoImage(file='asset/head1/%s.gif' % direct)
        else:
            self.headImage = tk.PhotoImage(file='asset/head2/%s.gif' % direct)
        if direct == 'Up':
            self.id = canvas.create_image(self.x - 13, self.y - 15, anchor=tk.NW, image=self.headImage)
        else:
            self.id = canvas.create_image(self.x - 13, self.y - 10, anchor=tk.NW, image=self.headImage)


class Snakes:
    def __init__(self, canvas, grid, x=0, y=0, color='green'):
        self.canvas = canvas
        self.grid = grid
        self.lenght = 60
        self.color = color

        self.head = Head(canvas, grid, x + self.lenght, y, 'Right', color)
        self.bodies = []
        for i in range(x - 1 + self.lenght, x - 1, -1):
            self.bodies.append(Bodies(canvas, grid, i, y, color))

    # def move(self):
    #     self.grow()
    #     self.canvas.delete(self.pieces[-1].id)
    #     del self.pieces[-1]
    #     pos = self.canvas.coords(self.pieces[-1].id)
    #     self.canvas.delete(self.pieces[-1].id)
    #     # self.pieces[-1] = Tail(self.canvas, pos[0] + 2, pos[1] - 3)

    # def isDie(self):
    #     head = self.pieces[0]
    #     headPos = self.canvas.coords(head.id)
    #     if head.direct == 'Left':
    #         x = headPos[0] + 5
    #         y = headPos[1] + 10
    #     elif head.direct == 'Down':
    #         x = headPos[0] + 10
    #         y = headPos[1] + 21
    #     elif head.direct == 'Right':
    #         x = headPos[0] + 21
    #         y = headPos[1] + 10
    #     else:
    #         x = headPos[0] + 10
    #         y = headPos[1] + 5

    #     for body in self.pieces[3:]:
    #         pos = self.canvas.coords(body.id)
    #         if x > pos[0] and x < pos[2]:
    #             if y > pos[1] and y < pos[3]:
    #                 return True
    #     return False

    # def keyPress(self, event):
    #     head = self.pieces[0]
    #     if head.direct == 'Left' and (event.keysym == 'Right' or event.keysym == head.direct):
    #         return
    #     if head.direct == 'Right' and (event.keysym == 'Left' or event.keysym == head.direct):
    #         return
    #     if head.direct == 'Down' and (event.keysym == 'Up' or event.keysym == head.direct):
    #         return
    #     if head.direct == 'Up' and (event.keysym == 'Down' or event.keysym == head.direct):
    #         return

    #     head.changeDirect(event.keysym)

    def grow(self):
        self.lenght += 1
        self.head.delete()

        self.bodies = [Bodies(self.canvas, self.grid, self.head.x, self.head.y, self.color)] + self.bodies

        if self.head.direct == 'Up':
            self.head.y -= 1
            self.head.y -= 3
        elif self.head.direct == 'Down':
            self.head.y += 1
            self.head.y -= 3
        elif self.head.direct == 'Left':
            self.head.x -= 1
        else:
            self.head.x += 1
        self.head = Head(self.canvas, self.grid, self.head.x, self.head.y, self.head.direct, self.color)


class Foods:
    def __init__(self, canvas, x=0, y=0, color='red'):
        self.canvas = canvas
        self.id = canvas.create_oval(0, 0, 5, 5, fill=color, outline=color)
        self.canvas.move(self.id, x, y)


if __name__ == '__main__':
    window = tk.Tk()
    canvas = tk.Canvas(window, width=600, height=600)
    canvas.pack()

    grid = [[0 for i in range(600)] for i in range(600)]

    s = Snakes(canvas, grid, 100, 100)
    s.head.changeDirect('Down')
    while True:
        s.grow()
        canvas.update()
        time.sleep(0.08)
    # print(s.pieces)
    # s.grow()
    # while True:
    #     canvas.bind_all('<KeyPress>', s.keyPress)
    #     s.move()
    #     if s.isDie():
    #         break
    #     canvas.update()
    #     time.sleep(0.01)
    window.mainloop()
