

class Settings:
    def __init__(self):

        self.bg_color = 0, 0, 0

        self.level_map = [
        '                                                                                                                                                                                              ',
        '                                                                                                                                                                                              ',
        '                                                                                                                                                                                              ',
        '              ?                                                                              BBBBBBB   BBB?                                                                                   ',
        '                                                                                                                                                                                              ',
        '                                                                                                                                                                                              ',
        '        ?   B?B?B                                         HH         HH                   B?B             B                                                                                   ',
        '                                                  HH      pp         pp                                                                                                                       ',
        '                                HH                pp      pp         pp                                                                                                                       ',
        'P                               pp                pp      pp         pp                                                                                                                       ',
        'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  XXXXXXXXXXXXXXX   XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  XXXXXXXXXXXX',
        'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  XXXXXXXXXXXXXXX   XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  XXXXXXXXXXXX']
        self.tile_size = 64
        self.screen_width = 1600
        # self.screen_height = 900
        self.screen_height = len(self.level_map) * self.tile_size

        self.player_speed = 8
