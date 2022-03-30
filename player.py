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
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16

    def get_input(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vector.x = 1
        elif keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vector.x = -1
        else:
            self.vector.x = 0

        if keys[pg.K_SPACE]:
            self.jump()

    def apply_gravity(self):
        self.vector.y += self.gravity
        self.rect.y += self.vector.y

    def jump(self):
        self.vector.y = self.jump_speed


    def update(self):
        self.get_input()