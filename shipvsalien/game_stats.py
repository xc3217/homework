class GameStats():
    """跟踪游戏的统计信息"""
    def __init__(self,ai_settings):
        """初始化统计信息"""
        self.ai_settings = ai_settings
        self.reset_stats()
        #游戏刚启动时处于非活动状态
        self.start_active = True
        self.bonus_active = False
        self.game_active = False
        self.if_boss = False
        #游戏最高分
        self.high_score = 0
        #最高分储存文件
        #self.fire_num=0


    def reset_stats(self):
        """初始化在游戏运行期间可能变化的统计信息"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.totalkill = 0
        self.totalkill0 = 0
        self.level = 1
        self.Q_bullet = 3
        # self.bonus_bullet = 0