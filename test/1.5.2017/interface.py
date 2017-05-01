from tkinter import ttk
import tkinter as tk


if __name__ == '__main__':
    window = tk.Tk()
    window.title('Snake')
    # window.resizable(0, 0)

    new = ttk.Button(window, text='NEW GAME').grid(column=400, row=400)
    canvas = tk.Canvas(window, width=450, height=600)
    canvas.grid()
    canvas.create_rectangle(25, 75, 425, 475)
    window.mainloop()
