import pygame


class Sound:
    def __init__(self):
        pygame.mixer.init()
        self.coin = pygame.mixer.Sound('../sounds/smb_coin.wav')
        self.death = pygame.mixer.Sound('../sounds/smb_mariodie.wav')
        self.jump = pygame.mixer.Sound('../sounds/smb_jump-small.wav')
        self.end_theme = pygame.mixer.Sound('../sounds/smb_gameover.wav')
        self.powerup = pygame.mixer.Sound('../sounds/smb_powerup.wav')
        self.stomp = pygame.mixer.Sound('../sounds/smb_stomp.wav')
        self.pipe = pygame.mixer.Sound('../sounds/smb_pipe.wav')

    def play_music(self, music, volume=0.3):
        pygame.mixer.music.unload()  # stop previous music playing before beginning another
        pygame.mixer.music.load(music)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1, 0.0)

    def busy(self): return pygame.mixer.get_busy()

    def play_sound(self, sound): pygame.mixer.Sound.play(sound)

    def play_bg(self):
        pygame.mixer.quit()
        pygame.mixer.init(round(44100))
        self.play_music('../sounds/maintheme.wav')

    def play_game_over(self):
        self.stop_bg()  # no more background music
        self.play_sound(self.end_theme)
        while self.busy():  # stays here until end_theme finishes playing
            pass

    def stop_bg(self): pygame.mixer.music.stop()

    def play_coin(self): self.play_sound(self.coin)

    def play_power_up(self): self.play_sound(self.powerup)

    def play_jump(self): self.play_sound(self.jump)

    def play_stomp(self): self.play_sound(self.stomp)

    def play_pipe(self): self.play_sound(self.pipe)

    def play_death(self):
        pygame.mixer.stop()
        self.play_sound(self.death)
