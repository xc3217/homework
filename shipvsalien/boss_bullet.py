import pygame
from pygame.sprite import Sprite
class boss_Bullet(Sprite):
    """一个对飞船发射的子弹进行管理的类"""
    def __init__(self,ai_settings,screen,boss):
        """在前所处的位置创建一个子弹对象"""
        super(boss_Bullet,self).__init__()
        self.screen = screen
        #在（0,0）处创建一个表示子弹的矩形，再设置正确的位置
        self.rect = pygame.Rect(0,0,ai_settings.bullet_width,
                                ai_settings.bullet_height)
        self.rect.centerx = boss.rect.centerx
        self.rect.top = boss.rect.bottom
        #存储用小数表示的子弹位置
        self.y = float(self.rect.y)
        self.color = ai_settings.boss_bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """向下移动子弹"""
        #更新表示子弹位置的小数值
        self.y += self.speed_factor
        #更新表示子弹的rect各位置
        self.rect.y = self.y

    def draw_bullet(self):
        """定屏幕上绘制子弹"""
        pygame.draw.rect(self.screen,self.color,self.rect)
