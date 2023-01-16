import pygame
from pygame.sprite import Group
from Settings import settings
from ship import Ship
import game_functions as gf
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from bonus import Bonus
from boss import Boss

def run_game():
    #初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings = settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    # messagebox.showinfo("按键提示", "初始设置如下：按下空格为发射子弹，Q为玩家小技能，E为第二种bonus机制的按键,"
    #                                 "玩家可操控上下左右按键来控制飞船移动。")

    pygame.display.set_caption("Alien Invasion")

    pygame.mixer.music.load(ai_settings.bg_music)
    pygame.mixer.music.set_volume(ai_settings.load)
    pygame.mixer.music.play(-1)#循环播放
    #创建一个同于储存游戏统计信息的实例

    stats = GameStats(ai_settings)
    #打开最高分文件
    with open("maxscore.txt" , "a+") as max_num:
        max_num.seek(0)
        high = max_num.read()
        high = high.strip()
        if high != "":
            stats.high_score = int(high)

    #创建一艘飞船
    ship = Ship(screen, ai_settings)
    #创建一个用于储存子弹的编组
    bullets = Group()
    Q_bullets = Group()
    bonus_bullets =Group()
    boss_bullets = Group()
    #创建外星人
    boss = Boss(screen, ai_settings)
    aliens = Group()
    aliens_more = Group()
    aliens_shield = Group()
    aliens_fenlie = Group()

    # 创建开始界面
    start_button = Button(ai_settings, screen, 250, 500, "开始游戏", 1)
    intro_button = Button(ai_settings, screen, 350, 500, "简介", 1)
    set_button = Button(ai_settings, screen, 450, 500, "设置", 1)
    exit_button = Button(ai_settings, screen, 550, 500, "退出", 1)
    #创建Play按钮
    play_button = Button(ai_settings, screen, 375,500,"Play",0)
    bonus_button0 = Button(ai_settings, screen, 375, 350, "狂热",1)
    bonus_button1 = Button(ai_settings, screen, 375, 650, "蓄锐",1)
    #创建Bonus对象
    bonus=Bonus(screen)
    #创建道具
    fastprop = Group()
    iceprop = Group()
    Qprop = Group()
    #创建记分板
    sb = Scoreboard(ai_settings, screen, stats, bonus)

    #开始游戏的主循环
    while True:
        gf.check_events(ai_settings, screen, stats, sb,
                        start_button,intro_button,set_button,exit_button,
                        play_button,bonus_button0,bonus_button1, ship,
                 aliens,  aliens_more, aliens_shield,aliens_fenlie,
                        bullets,Q_bullets,bonus_bullets,
                        bonus,boss)
        if stats.game_active:
            ship.update(ai_settings)
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens,
                    aliens_more, aliens_shield,aliens_fenlie,
                            bullets, Q_bullets, bonus_bullets,boss_bullets,
                              fastprop, iceprop, Qprop, boss, bonus)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens,
                   aliens_more, aliens_shield,aliens_fenlie, bullets,bonus, boss)
            gf.update_ship_prop(ai_settings, screen, stats, sb, ship,
                                fastprop, iceprop, Qprop, bullets, bonus)
            if stats.if_boss == True:
                gf.update_boss(ai_settings,screen, boss,boss_bullets,stats )

        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens,
                  aliens_more, aliens_shield,aliens_fenlie,
                         bullets,Q_bullets,bonus_bullets,boss_bullets,
                         fastprop, iceprop, Qprop,
                         bonus,start_button,intro_button,set_button,exit_button,
                         play_button,bonus_button0,bonus_button1,boss)

        bonus.update(stats,sb)
if __name__ == "__main__":
    run_game()