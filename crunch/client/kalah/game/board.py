class Board:
    def __init__(self):
        self.board = {}

    def across(self, index):
        return index + (6 - index) * 2

    def configure(self):
        for i in range(7):
            if i == 6:
                self.board[i] = 0
                self.board[13] = 0
            else:
                self.board[i] = 3

    def new_board(self):
        self.configure()