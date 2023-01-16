import pygame.image
class settings():
    """储存外星人入侵的所有设置的类"""
    def __init__(self):
        """初始化游戏里的静态设置"""
        #屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        #背景色
        self.bg_color = (255,255,255)
        self.bg = pygame.image.load("../shipvsalien/image/bg.jpg")
        self.background = pygame.transform.scale(self.bg, (1200, 800))
        #飞船的设置
        self.ship_speed_factor = 1.5
        self.ship_limit = 3
        #子弹设置
        self.bullet_speed_factor = 1.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60,60,60
        self.boss_bullet_color = 255,0,0
        self.bullet_allowed = 5
        self.bullet_width_big = 700
        self.bullet_width_bonus = 70
        self.bullet_height_bonus = 30
        #外星人设置
        self.alien_speed_factor = 3
        self.special_speed_factor = 1.5
        self.special_score_factor = 10
        self.special_drop_speed = 20
        self.fleet_drop_speed = 20
        # fleet_directio为1表示右移，为-1表示左移
        self.fleet_direction = 1

        #以什么样的速度加快游戏节奏
        self.speedup_scale = 1.01
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

        #音效设置
        self.bullet_music = 'music/bullet.wav'
        self.boom_music = 'music/boom.wav'
        self.bg_music = 'music/bg_music.mp3'

        #音量设置
        self.load = 0.5

    def initialize_dynamic_settings(self):
        """初始化随着游戏进行而变化的设置"""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0

        #计分
        self.alien_points = 50


    def increase_speed(self):
        """提高速度设置"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
