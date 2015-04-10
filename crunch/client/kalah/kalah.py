import pygame
from time import sleep
from PodSixNet.Connection import ConnectionListener, connection
from gui import KalahGui
from player import Player, HumanPlayer, AIPlayer


class Board:
    def __init__(self):
        self.board = [3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 0]

    def set(self):
        for i in range(14):
            if i == 6 or i == 13:
                self.board[i] = 0
            else:
                self.board[i] = 3

    def clean(self):
        for i in range(6):
            self.board[6] += self.board[i]
            self.board[13] += self.board[i + ((6 - i) * 2)]
            self.board[i] = 0
            self.board[i + ((6 - i) * 2)] = 0

    def transfer(self, origin, dest):
        self.board[origin] -= 1
        self.board[dest] += 1

    def steal(self, home, dest, across):
        self.board[home] += self.board[dest] + self.board[across]
        self.board[dest] = 0
        self.board[across] = 0


class Game(Board):
    def __init__(self):
        self.turn = 0
        Board.__init__(self)

    def start(self):
        self.set()

    def set(self):
        Board.set(self)
        self.turn = 1

    def match(self):
        while not self.game_over():
            self.play()

    def play(self):
        pass

    def game_over(self):
        return False

    def reset(self):
        self.set()

    def rematch(self):
        self.reset()
        self.match()

    def restart(self):
        self.start()

    def end(self):
        sleep(5)

    def home(self, dest):
        return dest == 6 or dest == 13

    def opponents_home(self, pid, dest):
        return (pid == 1 and dest == 13) or (pid == 2 and dest == 6)

    def special_move(self, dest, pid, across):
        if self.board[dest] == 1 and self.board[across] > 0:
            if pid == 1 and dest < 6 or pid == 2 and dest > 6:
                return True
        return False


class Kalah(Game):
    def __init__(self, player1, player2):
        Game.__init__(self)

        pygame.init()
        self.clock = pygame.time.Clock()

        self.gui = KalahGui(self.board)

        self.players = {}
        if player1 == Player or player1 == AIPlayer:
            self.players[1] = player1(1).move
        elif player1 == HumanPlayer:
            self.players[1] = player1(1, self.gui).move
        else:
            self.players[1] = player1

        if player2 == Player or player2 == AIPlayer:
            self.players[2] = player2(2).move
        elif player2 == HumanPlayer:
            self.players[2] = player2(2, self.gui).move
        else:
            self.players[2] = player2

    def set(self):
        Game.set(self)
        self.gui.draw_pl1_score()
        self.gui.draw_pl2_score()

    def play(self):
        self.clock.tick(60)

        move = self.players[self.turn](self.board)
        if move:
            self.validate(*move)

    def validate(self, move, pid):
        if self.board[(move - 1)
                      if pid == 1 else
                      (move-1 + (6 - (move-1)) * 2)] > 0:
            self.turn = self.move(move, pid)

    def move(self, move, pid, turn):
        origin = move - 1

        if pid == 2:
            origin += (6 - origin) * 2

        dest = origin + 1

        count = self.board[origin]

        for i in range(count):
            if self.opponents_home(pid, dest):
                dest += 1

            if dest > 13:
                dest = 0

            self.transfer(origin, dest)
            self.gui.draw_move(origin, dest)

            if self.home(dest):
                self.gui.draw_pl1_score()
                self.gui.draw_pl2_score()

            if i < count - 1:
                dest += 1
            sleep(1)

        across = dest + (6 - dest) * 2
        home = 7 * turn - 1

        if not self.home(dest):
            if self.special_move(pid, dest, across):
                self.steal(home, dest, across)
                self.gui.draw_steal(dest, home)
            sleep(0.5)
            return 1 if turn == 2 else 2
        elif self.home(dest):
            sleep(0.5)
            return 1 if turn == 1 else 2

    def game_over(self):
        pl1 = True
        pl2 = True
        for i in range(6):
            if self.board[i] != 0:
                pl1 = False
            if self.board[i + (6 - i) * 2] != 0:
                pl2 = False

        if pl1 or pl2:
            self.clean()
            self.gui.draw_clean()

        return pl1 or pl2

    def end(self):
        sleep(10)


class KalahNetwork(ConnectionListener, Kalah):
    def __init__(self, player):
        self.connected = False
        self.waiting = True
        self.gid = 0
        self.pid = 0
        self.data = {}

        self.Connect()

        while self.waiting:
            self.listen()

        player1 = player if self.pid == 1 else self.listen
        player2 = player if self.pid == 2 else self.listen
        Kalah.__init__(self, player1, player2)
        self.players[0] = self.listen

    def listen(self, data=None):
        connection.Pump()
        self.Pump()
        sleep(0.01)

    def Network_connected(self, data):
        # self.waiting = False
        self.connected = True
        print(data)

    def Network_error(self, data):
        print "error:", data['error'][1]

    def Network_disconnected(self, data):
        self.connected = False

    def Network_start(self, data):
        self.turn = data['turn']
        self.pid = data['pid']
        self.gid = data['gid']
        self.waiting = False

    def validate(self, move, pid):
        msg = dict(action='move', move=move, pid=pid, gid=self.gid)
        connection.Send(msg)
        self.turn = 0

    def Network_move(self, data):
        self.turn = self.move(data['move'], data['pid'], data['pid'])
        # self.turn = data['turn']

    def Network_invalid(self, data):
        self.turn = data['turn']
