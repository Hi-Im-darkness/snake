import tkinter as tk
import time


class Animation:
    def __init__(self):
        self.x = 1
        self.y = 0

    def changeDirect(self, direct):
        if direct == 'Left':
            self.x = -1
            self.y = 0
        elif direct == 'Right':
            self.x = 1
            self.y = 0
        elif direct == 'Up':
            self.x = 0
            self.y = -1
        else:
            self.x = 0
            self.y = 1

    def move(self):
        self.canvas.move(self.id, self.x, self.y)


class Bodies(Animation):
    def __init__(self, canvas, x=0, y=-3, color='green'):
        Animation.__init__(self)
        self.canvas = canvas
        if color == 'green':
            color = '#66cc33'
        else:
            color = '#e7db1f'
        self.id = canvas.create_oval(0, 0, 14, 14, fill=color, outline=color)
        canvas.move(self.id, x, y + 3)


class Head(Animation):
    def __init__(self, canvas, x=0, y=0, color='green'):
        Animation.__init__(self)
        self.color = color
        self.canvas = canvas
        self.direct = 'Right'
        if color == 'green':
            self.headImage = tk.PhotoImage(file='asset/head1/Right.gif')
        else:
            self.headImage = tk.PhotoImage(file='asset/head2/Right.gif')
        self.id = canvas.create_image(0, 0, anchor=tk.NW, image=self.headImage)
        canvas.move(self.id, x, y)

    def changeDirect(self, direct):
        Animation.changeDirect(self, direct)
        self.direct = direct
        x, y = self.canvas.coords(self.id)
        if self.color == 'green':
            self.headImage = tk.PhotoImage(file='asset/head1/%s.gif' % direct)
        else:
            self.headImage = tk.PhotoImage(file='asset/head2/%s.gif' % direct)
        self.id = canvas.create_image(x, y, anchor=tk.NW, image=self.headImage)


class Tail(Animation):
    def __init__(self, canvas, x=0, y=-5, color='green'):
        Animation.__init__(self)
        self.canvas = canvas
        if color == 'green':
            color = '#66cc33'
        else:
            color = '#e7db1f'
        self.id = canvas.create_oval(0, 0, 10, 10, fill=color, outline=color)
        canvas.move(self.id, x, y + 5)


class Snakes:
    def __init__(self, canvas, x=0, y=0, color='green'):
        self.canvas = canvas
        self.lenght = 3
        self.color = color

        self.pieces = [Head(canvas, x + 3 + 5 * (self.lenght - 2), y, color)]
        for i in range(x + 3 + 5 * (self.lenght - 3), x + -2, -5):
            self.pieces.append(Bodies(canvas, i, y, color))
        self.pieces.append(Tail(canvas, x, y, color))

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

    s = Snakes(canvas, 4, 4)
    # print(s.pieces)
    while True:
        canvas.bind_all('<KeyPress>', s.keyPress)
        s.move()
        # if s.isDie():
        #     break
        canvas.update()
        time.sleep(0.01)
    window.mainloop()
