import tkinter as tk
import time
import random
from obj import *


class Game:
    window = tk.Tk()
    window.title('Snake')
    window.resizable(0, 0)
    canvas = tk.Canvas(window, width=600, height=600)
    canvas.pack()

    grid = [[0 for i in range(600)] for i in range(600)]

    def __init__(self):
        self.snake = Snakes(self.canvas, Game.grid, 100, 300)
        self.food = None
        self.die = False
        self.addFood()

    def addFood(self):
        if self.food is not None:
            self.canvas.delete(self.food.id)

        while True:
            x = random.randint(50, 550)
            y = random.randint(50, 550)
            if Game.grid[x][y] != 1:
                break

        self.food = Foods(Game.canvas, Game.grid, x, y)

    def play(self):
        if self.snake.getFood(self.food):
            self.addFood()
            self.snake.grow()
        self.snake.move()
        Game.canvas.bind_all('<KeyPress>', self.snake.keyPress)
        if self.snake.isDie():
            self.die = True
        Game.canvas.update()


if __name__ == '__main__':
    g = Game()
    while True:
        g.play()
        if g.die:
            break
        time.sleep(0.01)
    g.window.mainloop()
