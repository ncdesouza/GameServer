from board import Board


class Actions(Board):
    def __init__(self):
        Board.__init__(self)

    def move(self, move, player):
        move -= 1

        if player == 2:
            move = self.across(move)

        for item in range(self.board[move]):
            pass
