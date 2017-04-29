import tkinter as tk
from obj import *


if __name__ == '__main__':
    window = tk.Tk()
    canvas = tk.Canvas(window, width=500, height=500)
    canvas.pack()
    # canvas.create_oval(0, 0, 20, 16)
    # for x in range(8, 150, 5):
    #     piece = Bodies(canvas, x, 0)

    # headImage = tk.PhotoImage(file='test/head1/Right.gif')
    # head = canvas.create_image(150, 0, anchor=tk.NW, image=headImage)

    # o = Bodies(canvas, 100, 200)
    # print(canvas.coords(o.id))
    # h = Head(canvas, 150, 160)
    # print(canvas.coords(h.id))

    canvas.create_oval(100, 100, 105, 105, fill='red')

    window.mainloop()
