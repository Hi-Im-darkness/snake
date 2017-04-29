import tkinter as tk

if __name__ == '__main__':
    window = tk.Tk()
    window.title('Snake')
    window.resizable(0, 0)
    canvas = tk.Canvas(window, width=600, height=600)
    canvas.pack()

    i1 = tk.PhotoImage(file='Body.gif')
    i2 = tk.PhotoImage(file='Head/Right.gif')
    i3 = tk.PhotoImage(file='Tail.gif')
    canvas.create_image(79, 100, anchor=tk.NW, image=i3)
    canvas.create_image(85, 100, anchor=tk.NW, image=i1)
    canvas.create_image(91, 100, anchor=tk.NW, image=i1)
    canvas.create_image(97, 100, anchor=tk.NW, image=i1)
    canvas.create_image(103, 100, anchor=tk.NW, image=i1)
    canvas.create_image(109, 100, anchor=tk.NW, image=i2)

    window.mainloop()