import pygame.font
from pygame.sprite import Group
from ship import Ship
from bonus import Bonus

class Scoreboard():
    """显示得分信息的类"""
    def __init__(self, ai_settings, screen, stats,bonus):
        """初始化显示得分涉及的属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats
        self.bonus=bonus

        #显示得分信息时使用的字体设置
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        #准备包含最高得分和当前得分的图像

        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        #self.prep_kill()
        self.prep_ships()
        self.prep_bonuses()

    # def prep_kill(self):
    #     """把总击杀转化为一副图像"""
    #     total_kill = int(round(self.stats.totalkill,-1))
    #     total_kill_str = "{:,}".format(total_kill)
    #     self.kill_image = self.font.render(total_kill_str,True,self.text_color,
    #                                       self.ai_settings.bg_color)
    #     self.kill_rect = self.kill_image.get_rect()
    #     self.kill_rect.right = self.screen_rect.right-20
    #     self.kill_rect.top = self.level_rect.bottom+10

    def prep_score(self):
        """将得分转化为一副渲染的图像"""
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str,True, self.text_color,
                                            self.ai_settings.bg_color)

        #将得分放在屏幕右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """将最高得分转换为渲染的图像"""
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self .font.render(high_score_str, True,
                                                  self.text_color, self.ai_settings.bg_color)
        #将最高得分放在屏幕顶部中央
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.left = self.screen_rect.left + 20
        self.high_score_rect.top = 20

    def prep_level(self):
        """将等级转化为渲染的图像"""
        self.level_image = self.font.render(str(self.stats.level), True,
                                            self.text_color, self.ai_settings.bg_color)

        """将等级放在得分下方"""
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """显示余下的飞船"""
        self.ships = Group()
        self.screen_rect = self.screen.get_rect()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.screen, self.ai_settings)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 730
            self.ships.add(ship)

    def prep_bonuses(self):
        """显示余下bonus攻击次数"""
        self.bonuses=Group()
        self.screen_rect = self.screen.get_rect()
        for bonus_number in range(self.bonus.bonus_point):
            bonus = Bonus(self.screen)
            bonus.rect.x = 20 + bonus_number * (bonus.rect.width+25)
            bonus.rect.y = 630
            self.bonuses.add(bonus)

    def show_score(self):
        """在屏幕上显示得分"""
        self.screen.blit(self.score_image,self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        #self.screen.blit(self.kill_image, self.kill_rect)
        #绘制飞船
        self.ships.draw(self.screen)
        if self.bonus.type==1:
            self.bonuses.draw(self.screen)
