from board import Board


class Rules(Board):
    def __init__(self):
        Board.__init__(self)

    def valid_move(self, move, player):
        if move:
            if 1 <= move <= 6:
                move -= 1
                if player == 2:
                    move = self.across(move - 1)

                if self.board[move] > 0:
                    return True

        return False

    def game_over(self):
        pl1 = True
        pl2 = True

        for i in range(6):
            if self.board[i] > 0:
                pl1 = False
            if self.board[self.across(i)] > 0:
                pl2 = False

        return pl1 and pl2