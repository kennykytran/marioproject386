import pygame as pg
from tiles import Tile
from pygame.sprite import Group, GroupSingle
from settings import Settings
from player import Player

class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.settings = Settings()
        self.setup_level(self.settings.level_map)
        self.world_shift = 0

    def setup_level(self, layout):
        self.tiles = Group()
        self.player = GroupSingle()
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * self.settings.tile_size
                y = row_index * self.settings.tile_size
                if cell == 'X':
                    tile = Tile((x,y),self.settings.tile_size)
                    self.tiles.add(tile)
                if cell == 'P':
                    player = Player((x,y))
                    self.player.add(player)

    def draw(self):
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.player.update()
        self.player.draw(self.display_surface)