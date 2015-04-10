import jpype
import os
import pygame


class Player:
    def __init__(self, playerID):
        self.playerID = playerID

    def move(self, board):
        moves = []
        for i in range(6):
            if board[i] > 0 and self.playerID == 1:
                moves.append(i+1)
            elif board[i + (6 - i) * 2] > 0 and self.playerID == 2:
                moves.append(i+1)

        move = moves.pop()
        print('P:' + str(self.playerID) + ' M:' + str(move))
        return move, self.playerID


class AIPlayer(Player):
    def __init__(self, playerID):
        jpype.startJVM(jpype.getDefaultJVMPath(), "-ea",
            "-Djava.class.path=%s" % os.path.abspath("."))
        Move = jpype.JClass("kalah.Move")
        self.jmove = Move(playerID)

        Player.__init__(self, playerID)

    def move(self, board):
        return self.jmove.makeMove(board), self.playerID

    def __exit__(self, exc_type, exc_val, exc_tb):
        jpype.shutdownJVM()


class HumanPlayer(Player):
    def __init__(self, playerID, gui):
        self.gui = gui
        Player.__init__(self, playerID)

    def move(self, board):
        move = None
        while move is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    move = self.gui.check(mouse[0], mouse[1])
                    if self.playerID == 1 and 0 <= move <= 5:
                        move += 1
                    elif self.playerID == 2 and 7 <= move <= 12:
                        move += ((6 - move) * 2) + 1
                    else:
                        move = None
        print('P:' + str(self.playerID) + ' M:' + str(move))
        return move, self.playerID
