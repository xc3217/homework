import sys
import pygame
from random import random
from bullet import Bullet
from shipvsalien.alien import Alien
from time import sleep
from Q_bullet import Q_Bullet
from bonus_bullet import bonus_Bullet
from prop import Prop
from boss_bullet import boss_Bullet
from tkinter import *
from tkinter.messagebox import *

#tkinter弹窗初始化
root0 = Tk()
root0.title('游戏简介')
root0.geometry("250x200+400+300")
root0.resizable(False, False)
r0 = 0

root1 = Tk()
root1.title('设置')
root1.geometry("350x300+300+200")
r1 = 0

def Quit0():
    global r0
    root0.withdraw()
    root0.quit()
    r0=1

def Quit1():
    global r1
    root1.withdraw()
    root1.quit()
    r1=1

root0.protocol('WM_DELETE_WINDOW', Quit0)
root1.protocol('WM_DELETE_WINDOW', Quit1)


#事件块
def check_events(ai_settings, screen, stats, sb,
                 start_button,intro_button,set_button,exit_button,play_button,bonus_button0,bonus_button1,
                 ship,aliens,  aliens_more, aliens_shield,aliens_fenlie,
                 bullets,Q_bullets,bonus_bullets,
                 bonus, boss):
    """响应键鼠事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:  # 表示按下按键
            check_keydown_events(event, ai_settings, screen,sb, ship, bullets,Q_bullets,bonus_bullets,bonus, stats)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:  # 按下鼠标
            mouse_x, mouse_y = pygame.mouse.get_pos()
            s = check_start_button(ai_settings, stats, start_button, intro_button, set_button, exit_button, mouse_x,mouse_y)
            r = check_bonus_button(stats, bonus_button0, bonus_button1, bonus, mouse_x, mouse_y, s)
            check_play_button(ai_settings, screen, stats, sb, play_button, ship,aliens,  aliens_more, aliens_shield,aliens_fenlie, bullets, mouse_x, mouse_y,boss,r)
        elif bonus.type==0:
            if bonus.bonus_point == 10:
                bonus.bonus_point = 0
                bonus.ready = True
                pygame.time.set_timer(bonus.BONUS, 10000, 1)
            elif event.type == bonus.BONUS:
                bonus.ready = False
                bonus.CD = True
                pygame.time.set_timer(bonus.CDTIME, 20000, 1)
            elif event.type == bonus.CDTIME:
                bonus.CD = False

        if bonus.fast == True and bonus.fastcd == False :
            ai_settings.bullet_speed_factor = 3
            pygame.time.set_timer(bonus.FASTBONUS, 10000, 1)
            bonus.fastcd = True
        elif event.type == bonus.FASTBONUS :
            ai_settings.bullet_speed_factor = 1.5
            bonus.fast = False
            pygame.time.set_timer(bonus.FASTCD, 2000, 1)
        elif event.type == bonus.FASTCD :
            bonus.fastcd = False

        if bonus.ice == True and bonus.icecd == False:
            ai_settings.alien_speed_factor = 1
            pygame.time.set_timer(bonus.ICEBONUS, 10000, 1)
            bonus.icecd = True
        elif event.type == bonus.ICEBONUS:
            ai_settings.alien_speed_factor = 3
            bonus.ice = False
            pygame.time.set_timer(bonus.ICETIME, 2000, 1)
        elif event.type == bonus.ICETIME:
            bonus.icecd = False


# 响应按下按键
def check_keydown_events(event, ai_settings, screen,sb,ship, bullets,Q_bullets, bonus_bullets,bonus,stats):
    """响应按键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE and bonus.ready==False:
        fire_bullet(ai_settings, screen, ship, bullets, stats)
    elif event.key == pygame.K_q and stats.Q_bullet > 0:
        fire_Q_bullet(ai_settings,screen,ship,Q_bullets,stats)
        stats.Q_bullet -= 1
    elif event.key == pygame.K_SPACE and bonus.ready==True and bonus.CD == False:
        bonus_bullet(ai_settings,screen,ship,bonus_bullets,stats,bonus)
    elif bonus.type==1 and event.key==pygame.K_e and bonus.bonus_point > 0:
        bonus_bullet(ai_settings, screen, ship, bonus_bullets, stats, bonus)
        bonus.bonus_point-=1
        sb.prep_bonuses()

# 响应抬起按键
def check_keyup_events(event, ship):
    """响应按键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False

#开始界面
def check_start_button(ai_settings,stats,start_button,intro_button,set_button,exit_button,mouse_x, mouse_y):
    global r0
    global r1
    global r2
    active = stats.start_active
    button_clicked0 = start_button.rect.collidepoint(mouse_x,mouse_y)
    button_clicked1 = intro_button.rect.collidepoint(mouse_x, mouse_y)
    button_clicked2 = set_button.rect.collidepoint(mouse_x, mouse_y)
    button_clicked3 = exit_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked0 and stats.start_active:
        stats.start_active = False
        stats.bonus_active = True
    elif button_clicked1 and stats.start_active:
        bt1=Button(root0, text='概况',width=30, command=cmx1).place(x=15,y=20)
        bt2=Button(root0, text='敌人分类',width=30, command=cmx2).place(x=15,y=60)
        bt3=Button(root0, text='奖励机制', width=30,command=cmx3).place(x=15,y=100)
        bt4=Button(root0, text='道具掉落', width=30,command=cmx4).place(x=15,y=140)
        root1.withdraw()
        r1=1
        if r0:
            root0.deiconify()
        root0.mainloop()
    elif button_clicked2 and stats.start_active:
        sca=Scale(root1,label='音量',
                          from_=0,to=10,
                          resolution=1,
                          orient=HORIZONTAL,
                          )
        sca.place(x=15,y=20)

        bt = Button(root1, text='保存', width=10, command=lambda: cmx5(ai_settings, sca))
        bt.place(x=15, y=220)

        root0.withdraw()
        r0=1
        if r1:
            root1.deiconify()
        root1.mainloop()

    elif button_clicked3 and stats.start_active:
        sys.exit()
    if active!=stats.start_active:
        return 0
    elif stats.start_active == False:
        return 1

#响应点击bonus按钮
def check_bonus_button(stats, bonus_button0,bonus_button1, bonus,mouse_x, mouse_y,decide):
    """玩家选择bonus种类"""
    active = stats.bonus_active
    if decide:
        button_clicked0 = bonus_button0.rect.collidepoint(mouse_x, mouse_y)
        button_clicked1 = bonus_button1.rect.collidepoint(mouse_x, mouse_y)
    else:
        button_clicked0 = False
        button_clicked1 = False
    if button_clicked0 and stats.bonus_active:
        bonus.type=0
        stats.bonus_active = False
    if button_clicked1 and stats.bonus_active:
        bonus.type=1
        stats.bonus_active = False
    if active!=stats.bonus_active:
        return 0
    elif stats.bonus_active == False:
        return 1


# 响应点击play按钮
def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens,
                       aliens_more, aliens_shield,aliens_fenlie, bullets, mouse_x, mouse_y,boss,decide):
    """在玩家点击play开启游戏"""
    if decide:
        button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    else:
        button_clicked = False

    # 能检测是否点击在play方块处
    if button_clicked and not stats.game_active and not stats.start_active:
        # 隐藏光标
        pygame.mouse.set_visible(False)
        # 重置游戏
        stats.game_active = True
        stats.reset_stats()

        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        aliens.empty()
        bullets.empty()

        create_fleet(ai_settings, screen ,ship, aliens,
                     aliens_more, aliens_shield,aliens_fenlie,
                     stats, boss)
        ship.center_ship()
    ai_settings.initialize_dynamic_settings()

# 刷新块
def update_screen(ai_setting, screen, stats, sb, ship, aliens,
                  aliens_more, aliens_shield,aliens_fenlie,
                  bullets,Q_bullets,bonus_bullets,boss_bullets,
                  fastprop, iceprop, Qprop,
                  bonus,start_button,intro_button,set_button,exit_button,
                  play_button,bonus_button0,bonus_button1
                  , boss):
    screen.fill(ai_setting.bg_color)
    screen.blit(ai_setting.background, (0, 0))
    # 绘制所有子弹
    for bullet in bullets:
        bullet.draw_bullet()
    for q in Q_bullets:
        q.draw_bullet()
    for b in bonus_bullets:
        b.draw_bullet()
    if stats.if_boss == True:
        for bullet in boss_bullets:
            bullet.draw_bullet()

    # 显示飞船
    if bonus.ready!=True:
        ship.blitme()
    else:
        ship.bonus_blitme()

    if stats.if_boss == True:
        boss.blitme()

    # 显示外星人
    """这个draw方法就相当于是对每一个用一下blit"""
    draw(screen, aliens, aliens_more, aliens_shield, aliens_fenlie, fastprop, iceprop, Qprop)

    # 显示得分
    sb.show_score()

    # 显示开始界面
    if stats.start_active:
        start_button.draw_button()
        intro_button.draw_button()
        set_button.draw_button()
        exit_button.draw_button()
    # 如果到Bonus选择阶段，显示Bonus按钮
    if stats.bonus_active and stats.start_active == False:
        bonus_button0.draw_button()
        bonus_button1.draw_button()
    # 如果游戏未开始，显示Play按钮
    if stats.game_active == False and stats.bonus_active == False and stats.start_active == False:
        play_button.draw_button()
    # 让最近绘制的屏幕可见
    pygame.display.flip()

def update_bullets(ai_settings, screen, stats, sb, ship, aliens,
                    aliens_more, aliens_shield,aliens_fenlie,
                   bullets,Q_bullets,bonus_bullets,boss_bullets,
                   fastprop, iceprop, Qprop, boss, bonus):
    bullets.update()
    Q_bullets.update()
    bonus_bullets.update()
    if stats.if_boss == True:
        boss_bullets.update()
    """更新子弹位置并删除已经消失的子弹"""
    for bullet in bullets:
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    for bullet in Q_bullets:
        if bullet.rect.bottom <= 0:
            Q_bullets.remove(bullet)

    for bullet in bonus_bullets:
        if bullet.rect.bottom <= 0:
            bonus_bullets.remove(bullet)

    for bullet in boss_bullets:
        if bullet.rect.bottom >= 800:
            boss_bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens,
                                   aliens_more, aliens_shield,aliens_fenlie,
                                  bullets,Q_bullets,bonus_bullets,boss_bullets,
                                  fastprop, iceprop, Qprop, boss)

    check_boss_bullet_collision(ai_settings, screen, stats, sb, ship, aliens,
                                aliens_more, aliens_shield, aliens_fenlie, bullets, bonus, boss_bullets, boss)

    check_bullet_boss_collision(ai_settings, screen, stats, sb, ship,
                                bullets, Q_bullets, bonus_bullets, boss)

def update_aliens(ai_settings, screen, stats, sb, ship, aliens,
                   aliens_more, aliens_shield,aliens_fenlie,
                  bullets, bonus, boss):
    check_fleet_deges(ai_settings, aliens,  aliens_more, aliens_shield,aliens_fenlie,boss)
    aliens.update()
    aliens_more.update()
    aliens_shield.update()
    aliens_fenlie.update()

    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens,
                         aliens_more, aliens_shield,aliens_fenlie, bullets,bonus)

    # 检测外星人和飞船的碰撞
    """方法接受两个实参，一个是单个对象，另一个是编组，简单判断"""
    intersect_normal = pygame.sprite.spritecollideany(ship, aliens)
    intersect_more = pygame.sprite.spritecollideany(ship, aliens_more)
    intersect_shield = pygame.sprite.spritecollideany(ship, aliens_shield)
    intersect_fenlie = pygame.sprite.spritecollideany(ship,aliens_fenlie)
    if intersect_normal  or intersect_more or intersect_shield or intersect_fenlie:
        ship_hit(ai_settings, screen, stats, sb, ship, aliens,
                  aliens_more, aliens_shield,aliens_fenlie, bullets,bonus, boss)

def update_ship_prop(ai_settings, screen, stats, sb, ship,
                  fastprop, iceprop, Qprop, bullets,bonus):
    fastprop.update()
    iceprop.update()
    Qprop.update()

    # 检测外星人和飞船的碰撞
    """方法接受两个实参，一个是单个对象，另一个是编组，简单判断"""
    intersect_fast = pygame.sprite.spritecollideany(ship, fastprop)
    collisions = pygame.sprite.spritecollide(ship, fastprop, True)
    intersect_ice = pygame.sprite.spritecollideany(ship, iceprop)
    collisions = pygame.sprite.spritecollide(ship,iceprop,True)
    intersect_Q = pygame.sprite.spritecollideany(ship, Qprop)
    collisions = pygame.sprite.spritecollide(ship,Qprop,True)
    if intersect_fast :
        bonus.fast = True
    if intersect_Q and stats.Q_bullet < 3:
        stats.Q_bullet += 1
    if intersect_ice:
        bonus.ice = True

def update_boss(ai_settings, screen, boss, boss_bullets, stats):
    boss.update(ai_settings)
    change_boss_direction(ai_settings, boss)
    boss_bullet(ai_settings, screen, boss, boss_bullets, stats)

#碰撞检测
def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens,
                                   aliens_more, aliens_shield,aliens_fenlie,
                                  bullets,Q_bullets,bonus_bullets,boss_bullets,
                                  fastprop, iceprop, Qprop, boss):
    # 检测是否击中外星人，击中则删除对应的子弹和外星人
    check_bullet_alien_collisions_part(ai_settings, screen, stats, sb, ship, aliens,
                                       bullets,Q_bullets,bonus_bullets, "")

    check_high_score(stats, sb)
    # 检测是否击中"盾牌"外星人
    for alien in aliens_more:
        collide_list = pygame.sprite.spritecollide(alien, bullets, True)
        collide_listQ = pygame.sprite.spritecollide(alien, Q_bullets, True)
        collide_listb = pygame.sprite.spritecollide(alien, bonus_bullets, True)

        if collide_list or collide_listQ or collide_listb:
            a = random()
            if a <= 0.7:
                randomprop = Prop(ai_settings,screen)
                if 0 < a <= 0.3 :
                    randomprop.if_Q = True
                    Qprop.add(randomprop)
                    randomprop.loading()
                if 0.3 < a <= 0.5 :
                    randomprop.if_fast = True
                    fastprop.add(randomprop)
                if a > 0.5 :
                    randomprop.if_ice = True
                    iceprop.add(randomprop)
                randomprop.loading()
                randomprop.x = alien.rect.x
                randomprop.y = alien.rect.y
                randomprop.rect.centerx = alien.rect.centerx
                randomprop.rect.centery = alien.rect.centery
            aliens_more.remove(alien)
            stats.score += 100

    for alien in aliens_shield:
        """方法：精灵&编组，第三个参数是删掉编组中的元素，能进行删除"""
        collide_list = pygame.sprite.spritecollide(alien, bullets, True)
        collide_listQ = pygame.sprite.spritecollide(alien,Q_bullets,True)
        collide_listb = pygame.sprite.spritecollide(alien, bonus_bullets, True)

        if collide_list or collide_listQ or collide_listb:
            # 删掉之前的盾牌外星人，换成一个普通的外星人
            alien_normal = Alien(ai_settings, screen)
            alien_normal.loading()
            alien_normal.fleet_direction = alien.fleet_direction
            alien_normal.x = alien.x  # 如果这个不给，就会刷新在屏幕左边
            alien_normal.y = alien.y
            alien_normal.rect.centerx = alien.rect.centerx
            alien_normal.rect.centery = alien.rect.centery
            aliens.add(alien_normal)
            aliens_shield.remove(alien)

    for alien1 in aliens_fenlie:
        collide_list1 = pygame.sprite.spritecollide(alien1, bullets,True)
        collide_list1Q = pygame.sprite.spritecollide(alien1, Q_bullets, True)
        collide_list1b = pygame.sprite.spritecollide(alien1, bonus_bullets, True)
        if collide_list1 or collide_list1Q or collide_list1b:
            # 删掉之前的盾牌外星人，换成一个普通的外星人
            alien_normal1 = Alien(ai_settings, screen)
            alien_normal2 = Alien(ai_settings, screen)

            alien_normal1.loading()
            alien_normal2.loading()

            alien_normal1.fleet_direction = alien1.fleet_direction
            alien_normal1.x = alien1.x - 100  # 如果这个不给，就会刷新在屏幕左边
            alien_normal1.y = alien1.y
            alien_normal1.rect.centerx = alien1.rect.centerx
            alien_normal1.rect.centery = alien1.rect.centery

            alien_normal2.fleet_direction = alien1.fleet_direction *-1
            alien_normal2.x = alien1.x +100  # 如果这个不给，就会刷新在屏幕左边
            alien_normal2.y = alien1.y
            alien_normal2.rect.centerx = alien1.rect.centerx
            alien_normal2.rect.centery = alien1.rect.centery

            aliens.add(alien_normal1)
            aliens.add(alien_normal2)
            aliens_fenlie.remove(alien1)
    # 外星人为空
    if not len(aliens)  and not len(aliens_more) and not len(aliens_shield) and not len(aliens_fenlie)  and not stats.if_boss:
        start_new_level(ai_settings, screen, stats, ship, aliens,
                         aliens_more, aliens_shield,aliens_fenlie, sb,
                        bullets, Q_bullets, bonus_bullets,boss_bullets,
                        boss)
        if stats.ships_left <3:
            r=pygame.time.get_ticks()
            if r%2==0:
                stats.ships_left +=1
            sb.prep_ships()

def check_bullet_alien_collisions_part(ai_settings, screen, stats, sb,
                                       ship, aliens, bullets,Q_bullets,bonus_bullets, different):
    # 对每一种外星人都适用（除了子弹）
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for alien in collisions.values():
            stats.totalkill += 1
            if different == "more":
                stats.score += ai_settings.alien_points * ai_settings.special_score_factor
            else:
                stats.score += ai_settings.alien_points

            sb.prep_score()
            Sound = pygame.mixer.Sound(ai_settings.boom_music)
            Sound.set_volume(0.3)
            Sound.play()

    collisions = pygame.sprite.groupcollide(Q_bullets,aliens,True,True)
    if collisions:
        for alien in collisions.values():
            stats.totalkill += 1
            if different == "more":
                stats.score += ai_settings.alien_points * ai_settings.special_score_factor
            else:
                stats.score += ai_settings.alien_points

            sb.prep_score()
            Sound = pygame.mixer.Sound(ai_settings.boom_music)
            Sound.set_volume(0.3)
            Sound.play()

    collisions = pygame.sprite.groupcollide(bonus_bullets, aliens, True, True)
    if collisions:
        for alien in collisions.values():
            #stats.totalkill += 1
            if different == "more":
                stats.score += ai_settings.alien_points * ai_settings.special_score_factor
            else:
                stats.score += ai_settings.alien_points

            sb.prep_score()
            Sound = pygame.mixer.Sound(ai_settings.boom_music)
            Sound.set_volume(0.3)
            Sound.play()

def check_bullet_boss_collision(ai_settings, screen, stats, sb, ship,
                                bullets, Q_bullets, bonus_bullets, boss):
    if stats.if_boss == True:
        collisions = pygame.sprite.spritecollide(boss, bullets, True)
        if collisions :
            boss.blood -= 1
        collisions1 = pygame.sprite.spritecollide(boss,Q_bullets,True)
        if collisions1 :
            boss.blood -= 5
        collisions2 = pygame.sprite.spritecollide(boss, bonus_bullets, True)
        if collisions2:
            boss.blood -= 3

    if boss.blood <= 0:
        stats.if_boss = False
        stats.score += 5000
        boss.blood = 50
        ship.blood = 50


def check_boss_bullet_collision(ai_settings, screen , stats, sb, ship,aliens,
                     aliens_more, aliens_shield, aliens_fenlie, bullets, bonus, boss_bullets, boss):
    collisions = pygame.sprite.spritecollide(ship, boss_bullets, True)
    if collisions:
        ship.blood -= 1
        if ship.blood <= 0:
            ship_hit(ai_settings, screen, stats, sb, ship, aliens,
                     aliens_more, aliens_shield, aliens_fenlie, bullets, bonus,
                     boss)
            ship.blood = 50

def ship_hit(ai_settings, screen, stats, sb, ship, aliens,
              aliens_more, aliens_shield,aliens_fenlie, bullets,bonus,
             boss):
    """响应外星人撞到船"""
    if stats.ships_left > 0:
        stats.ships_left -= 1
        # 更新记分牌
        sb.prep_ships()
        # 这里的逻辑是撞到了外星人就需要重新开始，将下一个飞船固定在中间并重新生成外星人
        bullets.empty()
        aliens.empty()
        aliens_more.empty()
        aliens_shield.empty()
        aliens_fenlie.empty()
        create_fleet(ai_settings, screen, ship, aliens,
                      aliens_more, aliens_shield,aliens_fenlie,stats, boss)
        ship.center_ship()
        sleep(0.5)
    else:
        with open("maxscore.txt" , "w") as max_num:
            print(max_num)
            highest = str(stats.high_score)
            max_num.write(highest)
        #stats.bonus_active = True
        pygame.time.set_timer(bonus.BONUS,0)
        pygame.time.set_timer(bonus.CDTIME,0)
        bonus.ready = False
        bonus.CD = False
        bonus.bonus_point = 0
        sb.prep_bonuses()
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_fleet_deges(ai_settings, aliens, aliens_more, aliens_shield,aliens_fenlie,boss):
    """有外星人得到边界时"""
    for alien in aliens.sprites():
        if alien.check_edge():
            change_fleet_direction(ai_settings, alien)
    for alien in aliens_more.sprites():
        if alien.check_edge():
            change_fleet_direction(ai_settings, alien)
    for alien in aliens_shield.sprites():
        if alien.check_edge():
            change_fleet_direction(ai_settings, alien)
    for alien in aliens_fenlie.sprites():
        if alien.check_edge():
            change_fleet_direction(ai_settings,alien)

def change_fleet_direction(ai_settings, alien):
    """将外星人下调，并改变方向"""
    if  alien.if_more or alien.if_shield or alien.if_fenlie:
        alien.rect.y += ai_settings.special_drop_speed
    else:
        alien.rect.y += ai_settings.fleet_drop_speed
    alien.fleet_direction *= -1

def change_boss_direction(ai_settings, boss):
    if boss.check_edge():
        boss.boss_direction *= -1

def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens,
                         aliens_more, aliens_shield,aliens_fenlie, bullets,bonus):
    """检查是否有外星人到达底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 按照和飞船撞到外星人一样处理
            ship_hit(ai_settings, screen, stats, sb, ship, aliens,aliens_more,aliens_shield,aliens_fenlie, bullets,bonus)
            break

    for alien in aliens_more.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 按照和飞船撞到外星人一样处理
            ship_hit(ai_settings, screen, stats, sb, ship, aliens,aliens_more,aliens_shield,aliens_fenlie, bullets,bonus)
            break
    for alien in aliens_shield.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 按照和飞船撞到外星人一样处理
            ship_hit(ai_settings, screen, stats, sb, ship, aliens,aliens_more,aliens_shield,aliens_fenlie, bullets,bonus)
            break

    for alien in aliens_fenlie.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 按照和飞船撞到外星人一样处理
            ship_hit(ai_settings, screen, stats, sb, ship, aliens,aliens_more,aliens_shield,aliens_fenlie, bullets,bonus)
            break



#子弹块
def fire_bullet(ai_settings, screen, ship, bullets, stats):
    if len(bullets) < ai_settings.bullet_allowed:
        # 创建一颗子弹，加到编组中
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
        fire_music(ai_settings.bullet_music, stats)

def boss_bullet(ai_settings, screen, boss, boss_bullets, stats):
    if len(boss_bullets) < 5:
        new_bullet1 = boss_Bullet(ai_settings, screen, boss)
        boss_bullets.add(new_bullet1)

def fire_Q_bullet(ai_settings, screen, ship,Q_bullets, stats):
    newQ_bullet = Q_Bullet(ai_settings,screen,ship)
    Q_bullets.add(newQ_bullet)
    fire_music(ai_settings.bullet_music,stats)

def bonus_bullet(ai_settings, screen, ship,bonus_bullets, stats,bonus):
    if bonus.type==0:
        newbonus_bullet =bonus_Bullet(ai_settings,screen,ship,bonus)
        bonus_bullets.add(newbonus_bullet)
        fire_music(ai_settings.bullet_music, stats)
    if bonus.type==1:
        newbonus_bullet0 = bonus_Bullet(ai_settings, screen, ship,bonus)
        newbonus_bullet0.rect.left=60
        bonus_bullets.add(newbonus_bullet0)
        newbonus_bullet1 = bonus_Bullet(ai_settings, screen, ship,bonus)
        newbonus_bullet1.rect.left = 120
        bonus_bullets.add(newbonus_bullet1)
        newbonus_bullet2 = bonus_Bullet(ai_settings, screen, ship,bonus)
        newbonus_bullet2.rect.left = 180
        bonus_bullets.add(newbonus_bullet2)
        newbonus_bullet3 = bonus_Bullet(ai_settings, screen, ship,bonus)
        newbonus_bullet3.rect.left = 240
        bonus_bullets.add(newbonus_bullet3)
        newbonus_bullet4 = bonus_Bullet(ai_settings, screen, ship,bonus)
        newbonus_bullet4.rect.left = 300
        bonus_bullets.add(newbonus_bullet4)
        newbonus_bullet5 = bonus_Bullet(ai_settings, screen, ship,bonus)
        newbonus_bullet5.rect.left = 360
        bonus_bullets.add(newbonus_bullet5)
        newbonus_bullet6 = bonus_Bullet(ai_settings, screen, ship,bonus)
        newbonus_bullet6.rect.left = 420
        bonus_bullets.add(newbonus_bullet6)
        newbonus_bullet7 = bonus_Bullet(ai_settings, screen, ship,bonus)
        newbonus_bullet7.rect.left = 480
        bonus_bullets.add(newbonus_bullet7)
        newbonus_bullet8 = bonus_Bullet(ai_settings, screen, ship,bonus)
        newbonus_bullet8.rect.left = 540
        bonus_bullets.add(newbonus_bullet8)
        newbonus_bullet9 = bonus_Bullet(ai_settings, screen, ship,bonus)
        newbonus_bullet9.rect.left = 600
        bonus_bullets.add(newbonus_bullet9)
        newbonus_bullet10 = bonus_Bullet(ai_settings, screen, ship,bonus)
        newbonus_bullet10.rect.left = 660
        bonus_bullets.add(newbonus_bullet10)
        newbonus_bullet11 = bonus_Bullet(ai_settings, screen, ship,bonus)
        newbonus_bullet11.rect.left = 720
        bonus_bullets.add(newbonus_bullet11)
        newbonus_bullet12 = bonus_Bullet(ai_settings, screen, ship,bonus)
        newbonus_bullet12.rect.left = 780
        bonus_bullets.add(newbonus_bullet12)
        newbonus_bullet13 = bonus_Bullet(ai_settings, screen, ship,bonus)
        newbonus_bullet13.rect.left = 840
        bonus_bullets.add(newbonus_bullet13)
        newbonus_bullet14 = bonus_Bullet(ai_settings, screen, ship,bonus)
        newbonus_bullet14.rect.left = 900
        bonus_bullets.add(newbonus_bullet14)
        newbonus_bullet15 = bonus_Bullet(ai_settings, screen, ship,bonus)
        newbonus_bullet15.rect.left = 960
        bonus_bullets.add(newbonus_bullet15)
        newbonus_bullet16 = bonus_Bullet(ai_settings, screen, ship,bonus)
        newbonus_bullet16.rect.left = 1020
        bonus_bullets.add(newbonus_bullet16)
        newbonus_bullet17 = bonus_Bullet(ai_settings, screen, ship,bonus)
        newbonus_bullet17.rect.left = 1080
        bonus_bullets.add(newbonus_bullet17)
        newbonus_bullet18= bonus_Bullet(ai_settings, screen, ship,bonus)
        newbonus_bullet18.rect.left = 1140
        bonus_bullets.add(newbonus_bullet18)

        fire_music(ai_settings.bullet_music, stats)

def fire_music(path, stats):
    sound = pygame.mixer.Sound(path)
    if (stats.level > 10):
        sound.set_volume(0.5)
    else:
        sound.set_volume(0.05* stats.level)
    sound.play()



#创建外星人块
def get_number_alien_x(ai_settings, alien_width):
    """计算一行有多少个外星人"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    """计算能容纳多少行外星人"""
    # 意思是在上边留一个高度，下边距离飞船两个的距离，防止贴脸
    available_space_y = (ai_settings.screen_height - 3 * alien_height - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens,  aliens_more, aliens_shield,aliens_fenlie,
                 alien_number, row_number, if_more=False, if_shield=False, if_fenlie=False):
    """创建一个外星人并放置在编组中"""
    alien = Alien(ai_settings, screen)

    # 特殊外星人判断
    if if_more:
        alien.if_more = True
    elif if_shield:
        alien.if_shield = True
    elif if_fenlie:
        alien.if_fenlie = True
    alien.loading()


    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number

    if if_more:
        aliens_more.add(alien)
    elif if_shield:
        aliens_shield.add(alien)
    elif if_fenlie:
        aliens_fenlie.add(alien)
    else:
        aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens,
                  aliens_more, aliens_shield, aliens_fenlie,
                 stats, boss ):
    """创建外星人群"""
    alien = Alien(ai_settings, screen)  # 第一个对象是用来计算相关数据的
    alien.loading()
    number_aliens_x = get_number_alien_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.width, alien.rect.height)
    if stats.level % 10 != 0:
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                a = random()
                if a > 0.3:
                    if a < 0.5:
                        # 道具外星人
                        create_alien(ai_settings, screen, aliens,  aliens_more,
                                 aliens_shield,aliens_fenlie, alien_number, row_number, if_more=True)
                    elif 0.5 < a < 0.6:
                        # 盾牌外星人
                        create_alien(ai_settings, screen, aliens,  aliens_more,
                                 aliens_shield,aliens_fenlie, alien_number, row_number, if_shield=True)
                    elif 0.6 < a <0.9:
                        #分裂外星人
                        create_alien(ai_settings,screen,aliens,aliens_more,
                                 aliens_shield,aliens_fenlie,alien_number,row_number, if_fenlie=True)
                    else:
                        #普通外星人
                        create_alien(ai_settings, screen, aliens,  aliens_more,
                                 aliens_shield,aliens_fenlie, alien_number, row_number)

    else:
        stats.if_boss = True

#其余功能
def check_high_score(stats, sb):
    """检查是否出现最高分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def draw(screen,aliens,aliens_more,aliens_shield,aliens_fenlie,fastprop,doublebprop,Qprop):
    """这个draw方法就相当于是对每一个用一下blit"""
    aliens.draw(screen)
    aliens_more.draw(screen)
    aliens_shield.draw(screen)
    aliens_fenlie.draw(screen)

    fastprop.draw(screen)
    doublebprop.draw(screen)
    Qprop.draw(screen)

def start_new_level(ai_settings, screen, stats, ship, aliens,
                     aliens_more, aliens_shield,aliens_fenlie, sb, bullets,Q_bullets, bonus_bullets, boss_bullets, boss):
    # 提升一个等级
    stats.level += 1
    sb.prep_level()
    # 删除子弹并新建一群外星人
    bullets.empty()
    Q_bullets.empty()
    bonus_bullets.empty()
    ai_settings.increase_speed()
    create_fleet(ai_settings, screen, ship, aliens,
                  aliens_more, aliens_shield,aliens_fenlie,stats,boss)

def cmx1():
 	mx1 = showinfo(title='概况', message='使用↑←↓→+SPACE模式，E为释放强化攻击；\n玩家每轮游戏可获得三层护盾，敌人到达屏幕底端或与玩家控制的飞机相撞扣除一条命，护盾全部失去且本体死亡后游戏结束；\n随着敌人波次增加，敌人移动速度提高，数量增加，玩家移速和子弹飞行速度增加')

def cmx2():
    mx2 = showinfo(title='敌人分类',message='小型敌人：血量为1，\n大型敌人：首次被命中会分裂为数个小型敌人，\nBOSS：每十关会出现，向玩家发射子弹，需被命中数次后才能击败')

def cmx3():
    mx3 = showinfo(title='奖励机制',message='可选择两种奖励机制：\n“狂热”：使玩家每击杀十个敌人立即进入十秒的强化时间，持续期间子弹增大，结束后进入二十秒的冷却时间（击杀不进行强化计数）；\n“蓄锐”：使玩家每击杀十个敌人获得一次强化攻击机会（按E发射一排子弹），最多累积三次')

def cmx4():
    mx4 = showinfo(title='道具掉落',message='击杀敌人有概率掉落三种道具：\n加速道具：生效期间提高玩家移动速度，\n冷冻道具：生效期间降低所有敌人移动速度，\n爆炸道具：提供一次发射特大号子弹的机会（按Q触发），\n每个道具有内置掉落冷却时间')

def cmx5(ai_settings,sca):
    mx5 = askokcancel("保存", "你确定要保存吗")
    if mx5:
        pygame.mixer.music.set_volume(ai_settings.load * sca.get() * 0.1)
        pygame.mixer.music.play(-1)
    return mx5