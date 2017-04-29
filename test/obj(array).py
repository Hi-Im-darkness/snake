import tkinter as tk
import time


class Animation:
    pass


class Head:
    def __init__(self, canvas, grid, x=0, y=0, color='green'):
        self.canvas = canvas
        self.grid = grid
        self.grid[x][y] = 1
        self.direct = 'Right'
        if color == 'green':
            self.headImage = tk.PhotoImage(file='asset/head1/Right.gif')
        else:
            self.headImage = tk.PhotoImage(file='asset/head2/Right.gif')
        self.id = canvas.create_image(0, 0, anchor=tk.NW, image=self.headImage)
        canvas.move(self.id, 20 * x, 20 * y)


class Bodies:
    def __init__(self, canvas, grid, x=0, y=0, color='green'):
        self.canvas = canvas
        if color == 'green':
            color = '#66cc33'
        else:
            color = '#e7db1f'
        self.id = canvas.create_oval(0, 0, 14, 14, fill=color, outline=color)


if __name__ == '__main__':
    window = tk.Tk()
    canvas = tk.Canvas(window, width=600, height=600)
    canvas.pack()

    grid = [[0 for i in range(30)] for i in range(30)]

    head = Head(canvas, grid, 5, 5)

    window.mainloop()
