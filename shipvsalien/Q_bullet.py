import pygame
from pygame.sprite import Sprite
class Q_Bullet(Sprite):
    """一个对飞船发射的子弹进行管理的类"""
    def __init__(self,ai_settings,screen,ship):
        """在前所处的位置创建一个子弹对象"""
        super(Q_Bullet,self).__init__()
        self.screen = screen

        # 先在(0,0)创建一个子弹，然后再修改位置
        # 因为子弹并非基于图像，所以就需要调用方法创建矩形
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width_big, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        # 小数格式的子弹位置
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.ship_speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """向上移动子弹"""
        self.y -= self.ship_speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        """绘制子弹"""
        pygame.draw.rect(self.screen, self.color, self.rect)