import pygame
from pygame.sprite import Sprite

class Bonus(Sprite):
    def __init__(self,screen):
        self.type=0
        self.ready=False
        self.CD=False
        self.fast = False
        self.fastcd = False
        self.icecd = False
        self.ice = False
        self.bonus_point=0
        self.bonus_num=0
        self.BONUS = pygame.USEREVENT + 1
        self.CDTIME = pygame.USEREVENT + 2
        self.FASTBONUS = pygame.USEREVENT + 3
        self.FASTCD = pygame.USEREVENT + 4
        self.ICEBONUS = pygame.USEREVENT + 5
        self.ICETIME = pygame.USEREVENT + 6

        super(Bonus, self).__init__()
        self.screen = screen
        self.image = pygame.image.load('image/bonusimg.bmp')
        self.image = pygame.transform.scale(self.image, (77, 77))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.centerX = float(self.rect.centerx)
        self.centerY = float(self.rect.centery)

    def blitme(self):
        self.screen.blit(self.image,self.rect)

    def update(self,stats,sb):
        if self.type==0:
            if self.ready==False and self.CD==False:
                if stats.totalkill == 0:
                    self.bonus_point = 0
                elif stats.totalkill % 10 == 0:
                    self.bonus_point = 10
                elif stats.totalkill % 10 != 0:
                    self.bonus_point=stats.totalkill%10

        if self.type==1:
            if stats.totalkill==0:
                self.bonus_point=0
            elif stats.totalkill % 10 == 0 and stats.totalkill!=stats.totalkill0 and self.bonus_point<3:

                self.bonus_point+=1
                sb.prep_bonuses()
            stats.totalkill0=stats.totalkill


