from object import *
import tkinter as tk
import time
import random


class Game:
    window = tk.Tk()
    window.title('Snake')
    window.resizable(0, 0)
    canvas = tk.Canvas(window, width=400, height=400)
    canvas.pack()

    def __init__(self):
        self.snake = Snake(Game.canvas, Pos(100, 100))
        self.food = None
        self.die = False
        self.addFood()

    def keyPress(self, event):
        head = self.snake.head
        if head.direct == 'Left' and (event.keysym == 'Right' or event.keysym == head.direct):
            return
        if head.direct == 'Right' and (event.keysym == 'Left' or event.keysym == head.direct):
            return
        if head.direct == 'Down' and (event.keysym == 'Up' or event.keysym == head.direct):
            return
        if head.direct == 'Up' and (event.keysym == 'Down' or event.keysym == head.direct):
            return

        head.changeDirect(event.keysym)

    def addFood(self):
        if self.food is not None:
            self.canvas.delete(self.food.id)

        while True:
            x = random.randint(50, 350)
            y = random.randint(50, 350)
            if Pos(x, y) not in self.snake.bodyPos:
                break

        self.food = Foods(Game.canvas, Pos(x, y))

    def play(self):
        if self.snake.getFood(self.food):
            self.addFood()
            self.snake.grow()

        self.snake.move()
        Game.canvas.bind_all('<KeyPress>', self.keyPress)
        if self.snake.isDie():
            self.die = True
        Game.canvas.update()


if __name__ == '__main__':
    g = Game()
    while True:
        g.play()
        # print(len(g.snake.bodies))
        # print(len(g.snake.bodyPos))
        # print()
        if g.die:
            break
        time.sleep(0.01)

    Game.window.mainloop()
