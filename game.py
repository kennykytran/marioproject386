import pygame as pg
import sys
from settings import Settings
from tiles import Tile
from pygame.sprite import Group
from level import Level


class Game:

    def __init__(self):
        pg.init()
        self.settings = Settings()
        self.screen = pg.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.bg_color = self.settings.bg_color
        pg.display.set_caption('Mario')
        self.level = Level(self.settings.level_map, self.screen)
        self.clock = pg.time.Clock()


    def restart(self): pass

    def update(self): pass

    def draw(self):
        self.screen.fill(self.bg_color)
        self.level.draw()

    def play(self):
        self.finished = False
        while not self.finished:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
            self.draw()
            pg.display.update()
            self.clock.tick(60)
def main():
    g = Game()
    g.play()

if __name__ == '__main__':
    main()
