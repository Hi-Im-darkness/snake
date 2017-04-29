class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, oPos):
        if self.x == oPos.x and self.y == oPos.y:
            return True
        return False


if __name__ == '__main__':
    l = [Pos(1, 1), Pos(2, 2)]
    print(Pos(1, 1) in l)
