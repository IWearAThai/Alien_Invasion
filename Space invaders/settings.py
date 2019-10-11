from pygame import mixer
from pygame import time


class Settings:
    """Stores settings for Alien Invasion"""
    def __init__(self):
        # screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.stars_limit = 8
        print('Automatic screen resolution: ' + str(self.screen_width) + ' ' + str(self.screen_height))
        self.bg_color = (0, 0, 0)

        # ship settings
        self.ship_speed_factor = None
        self.ship_limit = 3

        # bullet settings
        self.bullet_speed_factor = None
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 255, 255)
        self.bullets_allowed = 5

        # bunker settings
        self.bunker_block_size = 10
        self.bunker_color = (0, 255, 0)

        # beam settings
        self.beam_speed_factor = None
        self.beams_allowed = 1

        # sound settings
        self.audio_channels = 5
        self.ship_channel = mixer.Channel(0)
        self.alien_channel = mixer.Channel(1)
        self.death_channel = mixer.Channel(2)
        self.ufo_channel = mixer.Channel(3)
        self.music_channel = mixer.Channel(4)
        self.normal_music_interval = 725
        self.music_interval = self.normal_music_interval
        self.music_speedup = 25
        self.bgm = [
            mixer.Sound('sound/bgm_1.wav'),
            mixer.Sound('sound/bgm_2.wav'),
            mixer.Sound('sound/bgm_3.wav'),
            mixer.Sound('sound/bgm_4.wav')
        ]
        self.bgm_index = None
        self.last_beat = None

        # alien settings
        self.normal_alien_speed = 2
        self.alien_speed_limit = None
        self.alien_base_limit = None
        self.alien_speed_factor = None
        self.ufo_speed = None
        self.last_ufo = None
        self.ufo_min_interval = 10000
        self.fleet_drop_speed = 10
        self.fleet_direction = None
        self.alien_points = None
        self.ufo_point_values = [250, 300, 500]
        self.beam_stamp = None
        self.beam_time = 1000

        # How quickly the game speeds up
        self.speedup_scale = 1.1

        # initialize dynamics
        self.initialize_dynamic_settings()
        self.initialize_audio_settings()

    def initialize_dynamic_settings(self):
        """Initialize that change while the game is active"""
        self.ship_speed_factor = 6
        self.bullet_speed_factor = 10
        self.beam_speed_factor = 2
        self.alien_speed_factor = self.normal_alien_speed
        self.alien_speed_limit = self.alien_speed_factor * 5
        self.alien_base_limit = self.alien_speed_limit / 2
        self.ufo_speed = self.alien_speed_factor * 2

        # scoring
        self.alien_points = {'1': 50, '2': 100, '3': 200}

        # fleet_direction : 1 represents right, -1 represents left
        self.fleet_direction = 1

    def initialize_audio_settings(self):
        """Initialize pygame audio settings"""
        mixer.init()
        mixer.set_num_channels(self.audio_channels)
        self.music_channel.set_volume(0.7)

    def continue_bgm(self):
        """Create the background music by playing sound over the music channel"""
        if not self.last_beat:  # Music just started, initialize markers
            self.bgm_index = 0
            self.music_channel.play(self.bgm[self.bgm_index])
            self.last_beat = time.get_ticks()
        elif abs(self.last_beat - time.get_ticks()) > self.music_interval and not self.music_channel.get_busy():
            # Music continuing
            self.bgm_index = (self.bgm_index + 1) % len(self.bgm)
            self.music_channel.play(self.bgm[self.bgm_index])
            self.last_beat = time.get_ticks()

    def stop_bgm(self):
        """Stop whatever background music is currently playing"""
        self.music_channel.stop()
        self.last_beat = None
        self.bgm_index = None

    def increase_base_speed(self):
        """Increase the starting speed for aliens"""
        if self.normal_alien_speed < self.alien_base_limit:
            self.normal_alien_speed *= self.speedup_scale
            self.normal_music_interval -= self.music_speedup

    def increase_alien_speed(self):
        """Increase alien and music speed"""
        self.alien_speed_factor *= self.speedup_scale
        self.music_interval -= self.music_speedup

    def reset_alien_speed(self):
        """Reset alien and music speed back to its base value"""
        self.alien_speed_factor = self.normal_alien_speed
        self.music_interval = self.normal_music_interval
