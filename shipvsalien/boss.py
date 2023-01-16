import pygame
from pygame.sprite import Sprite

class Boss(Sprite):
    def __init__(self,screen,ai_settings):
        """初始化飞船并设置飞船的初始位置"""
        super(Boss,self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        """加载飞船并获取其外接矩形"""
        self.image = pygame.image.load('image/boss.bmp')
        #缩放图片
        self.image = pygame.transform.scale(self.image,(512,250))
        #获取边界
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        #将每艘飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.top =self.screen_rect.top
        #在飞船的属性center中存储小数值
        self.centerX = float (self.rect.centerx)
        self.centerY = float(self.rect.centery)

        #飞船血量即其他属性
        self.blood = 50
        self.boss_direction = -1
        self.boss_drop_direction = 1
    def update(self,ai_settings):
        """根据移动标志调整飞船的位置"""
        #根据self.center更新rect对象
        self.centerX += self.ai_settings.alien_speed_factor * self.boss_direction
        self.centerY += self.ai_settings.fleet_drop_speed * self.boss_drop_direction
        self.rect.centerx = self.centerX
        self.rect.centery = self.centerY
        self.boss_drop_direction *= -1
    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image,self.rect)

    def check_edge(self):
        """如果外星人位于屏幕边缘，就返回True"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True



