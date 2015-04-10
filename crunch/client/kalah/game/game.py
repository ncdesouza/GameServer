from actions import Actions
from rules import Rules
from board import Board


class Game(Board, Actions, Rules):
    def __init__(self):
        Board.__init__(self)
        Actions.__init__(self)
        Rules.__init__(self)
        self.players = {}
        self.turn = 0
        self.game_over = True

    def setup(self):
        self.new()

    def new(self):
        Board.configure(self)
        self.game_over = False

    def play(self):
        while not self.game_over:

            move = self.players[self.turn].move()

            if self.valid_move(move, self.turn):
                self.turn = self.move(move, self.turn)

            if self.turn == 0:
                self.game_over = True

        self.end()

    def end(self):
        self.quit()

    def replay(self):
        self.new()

    def reset(self):
        self.setup()

    def quit(self):
        exit(0)
