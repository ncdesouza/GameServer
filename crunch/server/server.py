from time import sleep
from weakref import WeakKeyDictionary
from PodSixNet.Channel import Channel
from PodSixNet.Server import Server


class Board:
    def __init__(self):
        self.board = [3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 0]

    def reset(self):
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
    def __init__(self, gid):
        Board.__init__(self)
        self.gid = gid
        self.players = {}
        self.turn = 0

    def playing(self):
        if len(self.players) < 2:
            return False

    def add_player(self, channel):
        self.players[len(self.players) + 1] = channel

        if len(self.players) == 2:
            self.start()
            return True
        return False

    def start(self):
        self.turn = 1
        for pid, player in self.players.viewitems():
            msg = dict(action='start', pid=pid, gid=self.gid, turn=self.turn)
            player.Send(msg)

    def play(self):
        pass

    def over(self):
        pass

    def restart(self):
        pass

    def home(self, dest):
        return dest == 6 or dest == 13

    def opponents_home(self, pid, dest):
        return (pid == 1 and dest == 13) or (pid == 2 and dest == 6)

    def special_move(self, dest, pid, across):
        if self.board[dest] == 1 and self.board[across] > 0:
            if pid == 1 and dest < 6 or pid == 2 and dest > 6:
                return True
        return False


class PlayerChannel(Channel):
    def Network(self, data):
        print(data)

    def Network_start(self):
        pass

    def Network_move(self, data):
        print(data)
        for player in self._server.games[data['gid']].players.values():
            player.Send(data)


class KalahServer(Server):

    channelClass = PlayerChannel

    def __init__(self, server='localhost', port=31425):
        Server.__init__(self, localaddr=(server, port))
        self.clients = WeakKeyDictionary()
        self.client_count = 0

        self.games = {}
        self.game_count = 0

        self.new_game()

    def Connected(self, channel, addr):
        self.add_client(channel, addr)

    def add_client(self, client, addr):
        self.clients[client] = True
        self.client_count += 1

        next_game = self.games[self.game_count].add_player(client)
        if next_game:
            self.new_game()

    def rm_client(self, client):
        del self.clients[client]

    def new_game(self):
        self.game_count += 1
        self.games[self.game_count] = Game(self.game_count)

    def join_game(self, player, gid):
        self.games[gid].add_player(player)

    def rm_game(self, gid):
        del self.games[gid]

    def poll(self):
        for gid, game in self.games.viewitems():
            if game.over():
                self.rm_game(gid)
        self.Pump()
        sleep(0.001)
