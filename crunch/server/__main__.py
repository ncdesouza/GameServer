import argparse
from time import sleep
from server import KalahServer


def main(*args, **kwargs):

    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '-S', '--server', type=str, default='localhost',
                        help='Server name')

    parser.add_argument('-p', '-P', '--port', type=int, default=31425,
                        help='Server port < default is >')

    args = parser.parse_args()

    print("launching Kalah Server")
    server = KalahServer(args.server, args.port)
    print('KalahServer running')
    while True:
        server.Pump()
        sleep(0.0001)


if __name__ == '__main__':
    main()