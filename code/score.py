import pygame
from settings import *


class Score():
    def __init__(self, surface):
        self.score = 0
        self.display_surface = surface
        self.screen_rect = surface.get_rect()
        self.pos = (self.screen_rect.centerx, 64)
        self.font = pygame.font.SysFont(None, 48)
        self.render_score()

    def update_score(self, newscore): self.score = newscore

    def render_score(self):
        self.score_str = str(self.score)
        self.score_image = self.font.render(self.score_str, True, (60, 60, 60))
        self.score_image.set_alpha(127)

    def add_score(self, num):
        self.score += num
        self.render_score()

    def draw(self):
        self.display_surface.blit(self.score_image, self.pos)


class Coin_count(Score):
    def __init__(self, surface):
        super().__init__(surface)
        self.coin_pos = (screen_width - 200, 64)

    def draw(self):
        self.display_surface.blit(self.score_image, self.coin_pos)

class Live_count(Score):
    def __init__(self, surface):
        super().__init__(surface)
        self.add_score(2)
        self.live_pos = (200, 64)

    def draw(self):
        self.display_surface.blit(self.score_image, self.live_pos)