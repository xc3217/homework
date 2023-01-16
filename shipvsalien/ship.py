import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self,screen,ai_settings):
        """初始化飞船并设置飞船的初始位置"""
        super(Ship,self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        """加载飞船并获取其外接矩形"""
        self.image = pygame.image.load('image/ship1.bmp')
        self.bonusimg = pygame.image.load('image/bonusimg.bmp')
        #缩放图片
        self.image = pygame.transform.scale(self.image,(102,77))
        self.bonusimg = pygame.transform.scale(self.bonusimg, (77, 77))
        #获取边界
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        #将每艘飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom =self.screen_rect.bottom
        #在飞船的属性center中存储小数值
        self.centerX = float (self.rect.centerx)
        self.centerY = float(self.rect.centery)
        #移动标志
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

        #boss战血量
        self.blood = 25
    def update(self,ai_settings):
        """根据移动标志调整飞船的位置"""
        if self.moving_right and self.rect.right<self.screen_rect.right:
            self.centerX += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left>0 :
            self.centerX -= self.ai_settings.ship_speed_factor
        if self.moving_up and self.rect.top > 0:
            self.centerY -= self.ai_settings.ship_speed_factor
        if self.moving_down and self.rect.centery + float(self.rect.height)/2 < self.screen_rect.bottom:
            self.centerY += self.ai_settings.ship_speed_factor
        #根据self.center更新rect对象
        self.rect.centerx = self.centerX
        self.rect.centery = self.centerY

    def center_ship(self):
        # 将每艘飞船放在屏幕底部中央
        self.centerX = self.screen_rect.centerx
        self.centerY = self.screen_rect.bottom-self.rect.height/2

        # 根据self.center更新rect对象
        self.rect.centerx = self.centerX
        self.rect.centery = self.centerY

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image,self.rect)

    def bonus_blitme(self):
        self.screen.blit(self.bonusimg, self.rect)



