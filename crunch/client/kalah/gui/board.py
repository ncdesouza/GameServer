from gui import *


class Board(SquareGui):
    def __init__(self):
        self.board = {}
        for i in range(7):
            if i == 6:
                self.board[i] = House(blue, 100 * 7, 0)
                self.board[13] = House(red, 0, 0)
            else:
                self.board[i] = Store(blue, 100 + 100 * i, 100)
                self.board[self.across(i)] = Store(red, 100 + 100 * i, 0)
        SquareGui.__init__(self, color=black,
                           width=100 * 8, height=150 * 2, x=0, y=0)

    def across(self, x):
        return x + (6 - x) * 2

    def check(self, x, y):
        for piece in self.board.viewitems():
            if piece[1].check(x, y):
                return piece[0]

    def draw(self):
        Gui.draw(self)
        for piece in self.board.viewvalues():
            piece.draw()

    def draw_move(self, origin, dest):
        seed = self.board[origin].get_item()
        self.board[dest].put_item([seed])

    def draw_steal(self, piece, home):
        seeds = []
        seeds.extend(self.board[piece].get_items())
        seeds.extend(self.board[self.across(piece)].get_items())
        self.board[home].put_item(seeds)

    def draw_clean(self):
        for i in range(6):
            if self.board[i].items:
                self.board[6].put_item(self.board[i].get_items())
            if self.board[self.across(i)].items:
                self.board[13].put_item(self.board[self.across(
                    i)].get_items())


class House(SquareGui):
    def __init__(self, color, x, y, height=200):
        self.items = []
        SquareGui.__init__(self, color,
                           width=100, height=height, x=x, y=y,
                           padding=10)

    def put_item(self, items):
        self.items.extend(items)
        count = len(self.items)
        horz_count = int(
            math.floor((self.width - (self.padding * 2))
                       // self.items[0].width))
        vert_count = int(math.floor(
            (self.height - self.padding * 2) // self.items[0].height))
        i = 0
        j = 0
        for item in self.items:
            item.set_pos(x=(self.x + self.padding + item.radius) + (i *
                                                                    item.width),
                         y=(self.y + self.padding + item.radius) + (j *
                                                                    item.height))
            if i == horz_count - 1:
                i = 0
                j += 1
            else:
                i += 1
        self.draw()

    def draw(self):
        SquareGui.draw(self)
        for item in self.items:
            item.draw()

    def check(self, x, y):
        if self.x < x < (self.x + self.width):
            if self.y < y < (self.y + self.height):
                return True


class Store(House):
    def __init__(self, color, x, y):
        House.__init__(self, color, x, y, height=100)
        self.put_item([Seed(self, white) for i in range(3)])

    def get_item(self):
        seed = self.items.pop()
        self.draw()
        return seed

    def get_items(self):
        seeds = [self.items.pop() for i in range(len(self.items))]
        self.draw()
        return seeds


class Seed(CircleGui):
    def __init__(self, loc, color):
        CircleGui.__init__(self, color=color, radius=10,
                           x=loc.x + loc.padding, y=loc.y + loc.padding)

    def set_pos(self, x, y):
        self.x = x
        self.y = y
