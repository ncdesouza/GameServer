import pygame
from board import Board
from hud import Hud


class KalahGui(Board, Hud):
    def __init__(self, game):
        self.screen = pygame.display.set_mode((100 * 8, 300))
        Board.__init__(self)
        Hud.__init__(self, game)

    def draw_clean(self):
        Board.draw_clean(self)
        self.draw_pl1_score()
        self.draw_pl2_score()