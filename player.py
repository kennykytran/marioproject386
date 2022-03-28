import pygame as pg
from pygame.sprite import Sprite
from settings import Settings



class Player(Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pg.Surface((32, 64))
        self.settings = Settings()
        self.image.fill('red')
        self.rect = self.image.get_rect(topleft = pos)
        self.vector = pg.math.Vector2(0,0)

    def get_input(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_RIGHT or pg.K_d]:
            self.vector.x = 1
        elif keys[pg.K_LEFT or pg.K_a]:
            self.vector.x = -1
        else:
            self.vector.x = 0

    def update(self):
        self.get_input()
        self.rect.x += self.vector.x * self.settings.player_speed