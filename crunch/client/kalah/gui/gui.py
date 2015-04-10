import pygame
import math
from time import sleep

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)
grey = (125, 125, 125)
pink = (255, 200, 200)


class Gui:
    def __init__(self, color,
                 width=None, height=None, x=None, y=None):

        self.screen = pygame.display.get_surface()

        self.color = color

        if width is None:
            self.width = self.screen.get_width()
        else:
            self.width = width

        if height is None:
            self.height = self.screen.get_height()
        else:
            self.height = height

        if x is not None:
            self.x = x
        else:
            self.x = int(math.floor(self.screen.get_width() / 2)
                         - math.floor(self.width / 2))

        if y is not None:
            self.y = y
        else:
            self.y = int(math.floor(self.screen.get_height() / 2)
                         - math.floor(self.height / 2))

        self.draw()

    def draw(self):
        pygame.draw.rect(self.screen, self.color,
                         (self.x, self.y, self.width, self.height))
        pygame.display.update()


class SquareGui(Gui):
    def __init__(self, color,
                 width=None, height=None, x=None, y=None,
                 padding=None, inner_color=black):
        self.padding = padding
        self.inner_color = inner_color
        Gui.__init__(self, color, width, height, x, y)

    def draw(self):
        Gui.draw(self)
        if self.padding is not None:
            pygame.draw.rect(self.screen, self.inner_color,
                             (self.x + self.padding,
                              self.y + self.padding,
                              self.width - int(self.padding * 2),
                              self.height - int(self.padding * 2))
                             )
        pygame.display.update()


class CircleGui(Gui):
    def __init__(self, color,
                 radius, x=None, y=None,
                 padding=None, inner_color=black):
        self.radius = radius
        self.padding = padding
        self.inner_color = inner_color
        Gui.__init__(self, color, width=radius*2, height=radius*2,
                     x=x + radius, y=y + radius)

    def draw(self):
        pygame.draw.circle(self.screen, self.color,
                           (self.x, self.y),
                           self.radius)

        if self.padding is not None:
            pygame.draw.circle(self.screen, self.inner_color,
                               (self.x, self.y),
                               self.radius - self.padding)
        pygame.display.update()

    def center(self):
        pass

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((400, 400))

    test = SquareGui(color=red,
                     width=200, height=200, x=0, y=0,
                     padding=10)
    test2 = SquareGui(color=red,
                      width=200, height=200, x=200, y=200)

    test3 = CircleGui(color=blue,
                      radius=100,
                      x=0, y=200,
                      padding=10)

    test4 = CircleGui(color=blue,
                      radius=100,
                      x=200, y=0)
    sleep(3)


