import pygame
from pygame.sprite import Sprite
from random import random

class Prop(Sprite):
    """表示单个外星人的类"""
    def __init__(self, ai_settings, screen):
        """初始化外星人并设置其初始位置"""
        super(Prop, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        self.prop_drop_speed = 20

        self.if_fast = False
        self.if_ice = False
        self.if_Q = False


    def loading(self):
        if self.if_fast:
            self.image = pygame.image.load('./image/fastprop.bmp')
        elif self.if_ice:
            self.image = pygame.image.load('./image/ice.bmp')
        elif self.if_Q:
            self.image = pygame.image.load('./image/Q_bonus.png')
        self.image = pygame.transform.scale(self.image, (75, 75))
        self.rect = self.image.get_rect()

        # 开始每一个外星人都在屏幕的左上角
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        # 用来存储准确的位置，用其更新rect.x
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def blitme(self):
        """在指定位置绘制道具"""
        self.screen.blit(self.image, self.rect)

    def check_edge(self):
        """如果外星人位于屏幕边缘，就返回True"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """向下移动道具"""
        a = random()
        if(a<0.005):
            self.y += self.prop_drop_speed
        self.rect.y = self.y



