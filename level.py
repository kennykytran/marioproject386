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
                    tile = Tile((x,y), self.settings.tile_size, 'grey')
                    self.tiles.add(tile)
                if cell == 'P':
                    player = Player((x,y))
                    self.player.add(player)
                if cell == 'p':
                    tile = Tile((x,y), self.settings.tile_size, 'light green')
                    self.tiles.add(tile)
                if cell == 'H':
                    tile = Tile((x, y), self.settings.tile_size, 'green')
                    self.tiles.add(tile)
                if cell == 'B':
                    tile = Tile((x, y), self.settings.tile_size, 'brown')
                    self.tiles.add(tile)
                if cell == '?':
                    tile = Tile((x, y), self.settings.tile_size, 'orange')
                    self.tiles.add(tile)


    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.vector.x

        if player_x < self.settings.screen_width / 4 and direction_x < 0:
            self.world_shift = self.settings.player_speed
            player.speed = 0
        elif player_x > self.settings.screen_width * 3/4 and direction_x > 0:
            self.world_shift = -self.settings.player_speed
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = self.settings.player_speed

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.vector.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.vector.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.vector.x > 0:
                    player.rect.right = sprite.rect.left

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.vector.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.vector.y = 0
                elif player.vector.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.vector.y = 0


    def draw(self):
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.scroll_x()

        self.player.update()
        self.vertical_movement_collision()
        self.horizontal_movement_collision()
        self.player.draw(self.display_surface)
