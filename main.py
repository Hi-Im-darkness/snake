import tkinter as tk
import time
import _thread
from food import *
from snake import *
from other import *


class Player:
    def __init__(self, snake, food, setting=Setting(), enemy=None):
        self.snake = snake
        self.enemy = enemy
        self.setting = setting
        self.snake.changeSetting(setting)
        self.food = food
        self.score = 0

    def play(self):
        while True:
            snake = self.snake
            head = snake.head

            snake.move()
            if self.setting.arrowControl:
                snake.canvas.bind_all('<KeyPress-Left>', lambda e, d=Direction('Left'): head.changeDirect(d, e))
                snake.canvas.bind_all('<KeyPress-Right>', lambda e, d=Direction('Right'): head.changeDirect(d, e))
                snake.canvas.bind_all('<KeyPress-Up>', lambda e, d=Direction('Up'): head.changeDirect(d, e))
                snake.canvas.bind_all('<KeyPress-Down>', lambda e, d=Direction('Down'): head.changeDirect(d, e))
            else:
                snake.canvas.bind_all('<KeyPress-a>', lambda e, d=Direction('Left'): head.changeDirect(d, e))
                snake.canvas.bind_all('<KeyPress-d>', lambda e, d=Direction('Right'): head.changeDirect(d, e))
                snake.canvas.bind_all('<KeyPress-w>', lambda e, d=Direction('Up'): head.changeDirect(d, e))
                snake.canvas.bind_all('<KeyPress-s>', lambda e, d=Direction('Down'): head.changeDirect(d, e))

            if snake.getFood(self.food):
                self.food.add()
                self.score += 8
                snake.grow()
            if snake.isDie(self.enemy):
                snake.disappear()
                return

            snake.canvas.update()
            time.sleep(self.setting.TS)


class Bot(Player):
    def __init__(self, snake, food, setting=Setting(), enemy=None):
        Player.__init__(self, snake, food, setting, enemy)

    def play(self):
        while True:
            if self.snake.getFood(self.food):
                self.food.add()
                self.score += 8
                self.snake.grow()

            self.snake.move(self.food, self.enemy)

            if self.snake.isDie(self.enemy):
                self.snake.disappear()
                return

            self.snake.canvas.update()
            time.sleep(self.setting.TS)


def OnePlayer():
    snake = Snake(canvas, 100, 300)
    food = Foods(canvas)
    food.add()
    player = Player(snake, food)
    player.play()


def TwoPlayer():
    snake1 = Snake(canvas, 100, 100)
    snake2 = Snake(canvas, 100, 300, 'Right', 'Yellow')
    food = Foods(canvas)
    food.add()

    player1 = Player(snake1, food, Setting(), snake2)
    player2 = Player(snake2, food, Setting(arrowControl=False), snake1)

    _thread.start_new_thread(player1.play, ())
    _thread.start_new_thread(player2.play, ())


def PlayerVsBot():
    snake1 = Snake(canvas, 100, 100)
    snake2 = BotSnake(canvas, 100, 300)
    food = Foods(canvas)
    food.add()

    player = Player(snake1, food, Setting(DBBY=False), snake2)
    bot = Bot(snake2, food, Setting(DBBY=False), snake1)

    _thread.start_new_thread(player.play, ())
    _thread.start_new_thread(bot.play, ())


if __name__ == '__main__':
    window = tk.Tk()
    window.title('Snake')
    window.resizable(0, 0)
    canvas = tk.Canvas(window, width=400, height=400)
    canvas.pack()

    # OnePlayer()
    TwoPlayer()
    # PlayerVsBot()

    window.mainloop()
