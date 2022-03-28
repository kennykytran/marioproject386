

class Settings:
    def __init__(self):

        self.bg_color = 0, 0, 0

        self.level_map = [
        '                        ',
        '                        ',
        '                        ',
        '                        ',
        '                        ',
        'P                       ',
        'XXXXXXXXXXXXXXXXXXXXXXXX',
        'XXXXXXXXXXXXXXXXXXXXXXXX']
        self.tile_size = 64
        self.screen_width = 1200
        self.screen_height = len(self.level_map) * self.tile_size

        self.player_speed = 8
