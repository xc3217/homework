import pygame
from pygame.sprite import Sprite
from random import random

class Alien(Sprite):
    """表示单个外星人的类"""
    def __init__(self, ai_settings, screen):
        """初始化外星人并设置其初始位置"""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        self.fleet_drop_speed = 20
        # fleet_directio为1表示右移，为-1表示左移
        self.fleet_direction = 1
        self.if_more = False
        self.if_shield = False
        self.if_fenlie = False


    def loading(self):
        if self.if_more:
            self.image = pygame.image.load('image/alien3.bmp')
        elif self.if_shield:
            self.image = pygame.image.load('image/alien4.bmp')
        elif self.if_fenlie:
            self.image = pygame.image.load('image/alien2.bmp')
        else:
            self.image = pygame.image.load('image/alien.bmp')
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()

        # 开始每一个外星人都在屏幕的左上角
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        # 用来存储准确的位置，用其更新rect.x
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def blitme(self):
        """在制定位置绘制外星人"""
        self.screen.blit(self.image, self.rect)

    def check_edge(self):
        """如果外星人位于屏幕边缘，就返回True"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """向右移动外星人"""
        if  self.if_more or self.if_shield:
            self.x += self.ai_settings.alien_speed_factor * self.fleet_direction * self.ai_settings.special_speed_factor
        else:
            self.x += self.ai_settings.alien_speed_factor * self.fleet_direction
        a = random()
        if(a<0.005):
            self.y += self.fleet_drop_speed
        self.rect.x = self.x
        self.rect.y = self.y



