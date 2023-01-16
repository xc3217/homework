import pygame
from pygame.sprite import Sprite
class bonus_Bullet(Sprite):
    """一个对飞船发射的子弹进行管理的类"""
    def __init__(self,ai_settings,screen,ship,bonus):
        """在前所处的位置创建一个子弹对象"""
        super(bonus_Bullet,self).__init__()
        self.screen = screen
        self.bonus = bonus

        if bonus.type==0:
            self.rect = pygame.Rect(0, 0, ai_settings.bullet_width_bonus, ai_settings.bullet_height_bonus)
        if bonus.type==1:
            self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        # 小数格式的子弹位置
        self.y = float(self.rect.y)
        self.color = ai_settings.bullet_color
        self.ship_speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """向上移动子弹"""
        if self.bonus.type==0:
            self.y -= self.ship_speed_factor
        if self.bonus.type==1:
            self.y -= self.ship_speed_factor-0.5
        self.rect.y = self.y
        # if self.bonus.type==0:
        #     self.y -= self.ship_speed_factor
        #     self.rect.y = self.y
        # if self.bonus.type==1:
        #     for i in range(19):
        #         self.ys[i]-=self.ship_speed_factor
        #         self.rects[i].y=self.ys[i]

    def draw_bullet(self):
        """绘制子弹"""
        pygame.draw.rect(self.screen, self.color, self.rect)
        # if self.bonus.type == 0:
        #     pygame.draw.rect(self.screen, self.color, self.rect)
        # if self.bonus.type == 1:
        #     for i in range(19):
        #         pygame.draw.rect(self.screen, self.color, self.rects[i])
