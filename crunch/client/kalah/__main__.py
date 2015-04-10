import argparse
from kalah import Kalah, KalahNetwork
from player import *


def main(*args, **kwargs):

    parser = argparse.ArgumentParser()

    parser.add_argument('-pl1', '-PL1', '--player1', type=str, default='')

    parser.add_argument('-pl2', '-PL2', '--player2', type=str, default='')

    parser.add_argument('-n', '-N', '--network', help='play networked',
                        action='store_true')

    parser.add_argument('-s', '-S', '--server', type=str, default='localhost',
                        help='Server name')

    parser.add_argument('-p', '-P', '--port', type=int, default=31425,
                        help='Server port < default is >')

    args = parser.parse_args()

    print(args)

    player1 = Player if args.player1 == '' else HumanPlayer
    player2 = Player if args.player2 == '' else HumanPlayer

    if not args.network:
        game = Kalah(player1, player2)
    else:
        game = KalahNetwork(player1)

    game.start()
    game.match()
    game.end()

if __name__ == '__main__':
    main()