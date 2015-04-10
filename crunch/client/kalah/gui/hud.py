import pygame

from gui import *


class Hud(SquareGui):
    def __init__(self, game):
        self.game = game
        self.pl1_score = PlayerScore(game[6], black, 400, 'right')
        self.pl2_score = PlayerScore(game[13], black, 0, 'left')
        self.turn = 0
        SquareGui.__init__(self, color=black,
                           width=100 * 8, height=100, x=0, y=200)

    def draw(self):
        SquareGui.draw(self)
        self.pl1_score.draw()
        self.pl2_score.draw()
        # self.draw_turn()
        pygame.display.update()

    def draw_turn(self):
        if self.turn == 1:
            color = blue
        elif self.turn == 2:
            color = red
        else:
            color = grey

        CircleGui(color=white, radius=50,
                  x=int((100 * 8 // 2) - 50), y=200,
                  padding=10, inner_color=color)

    def draw_pl1_score(self):
        self.pl1_score.score = self.game[6]
        self.pl1_score.draw()

    def draw_pl2_score(self):
        self.pl2_score.score = self.game[13]
        self.pl2_score.draw()

    def set_turn(self, turn):
        self.turn = turn


class PlayerScore(SquareGui):
    def __init__(self, score, color, x, text_align):
        self.score = score
        self.text_align = text_align
        SquareGui.__init__(self, color=color, width=100 * 8 // 2,
                           height=100, x=x, y=200, padding=5)

    def draw(self):
        SquareGui.draw(self)
        font = pygame.font.Font(None, 50)

        txt = font.render("%02i" % self.score, 1, white)
        txt_w, txt_h = txt.get_rect()[2:]

        if self.text_align == "left":
            txt_x = self.x + self.padding + 5
            txt_y = self.y + self.padding
        elif self.text_align == "right":
            txt_x = self.x + self.width - self.padding - 5 - txt_w
            txt_y = self.y + self.padding
        else:
            txt_x = int(self.x + self.width//2 - txt_w//2)
            txt_y = int(self.y + self.height//2 - txt_h//2)

        self.screen.blit(txt, (txt_x, txt_y))

        pygame.display.update()