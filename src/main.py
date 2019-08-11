# -*- encoding: utf-8 -*-

"""
@file: main.py
@time: 2019/8/10 15:53
@author: 姬小野
@version: 0.1
"""

import pygame
import sys
import time


def main():
    pygame.init()
    pygame.mixer.init()
    pygame.display.init()
    pygame.key.set_repeat(100, 10)  # 设置重复响应间隔位10ms
    bg_size = width, height = 800, 600  # 设置游戏窗口大小
    screen = pygame.display.set_mode(bg_size)
    pygame.display.set_caption("弹球小游戏")  # 设置标题

    # 设置各种图形
    background = pygame.image.load('../image/plane.png').convert_alpha()
    ball = pygame.image.load('../image/logo.ico').convert_alpha()  # 设置透明通道
    # icon = ball
    # pygame.display.set_icon(icon)
    shape_ball = width_ball, height_ball = 50, 50
    ball = pygame.transform.scale(ball, shape_ball)
    line = pygame.image.load('../image/line.png').convert_alpha()
    shape_line = width_line, height_line = 200, 10
    line = pygame.transform.scale(line, shape_line)
    # 设置暂停按钮
    pause_nor_img = pygame.image.load('../image/pause_nor.png').convert_alpha()
    pause_pressed_img = pygame.image.load('../image/pause_pressed.png').convert_alpha()
    pause_position = pause_nor_img.get_rect()
    pause_position.right, pause_position.top = width - 10, 10


    # 关键图形的位置
    position_ball = ball.get_rect()  # 小球的位置
    speed_ball = [-4, 4]  # 小球移动速度
    position_line = line.get_rect()
    position_line.bottom = height

    # 设置游戏音乐
    start_sound = pygame.mixer.Sound('../sound/start.wav')
    knock_sound = pygame.mixer.Sound('../sound/fire.wav')
    knock_sound.set_volume(0.2)
    game_over_sound = pygame.mixer.Sound('../sound/game_over.wav')

    running = True
    pause = False
    is_game_over = False
    clock = pygame.time.Clock()
    last_time = time.time()
    score = 0.0
    # start_sound.play()

    while running:
        now_time = time.time()
        # print(last_time - now_time)
        if not is_game_over and last_time - now_time < -1.0:  # 每隔一秒更新一次速度
            speed_ball[0] += 0.2 if speed_ball[0] > 0 else -0.2
            speed_ball[1] += 0.2 if speed_ball[1] > 0 else -0.2
            last_time = now_time
            score += speed_ball[0] if speed_ball[0] > 0 else -speed_ball[0]
            score += speed_ball[1] if speed_ball[1] > 0 else -speed_ball[1]
            # print(speed_ball, 'score: ', score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 叉掉退出
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:  # 按q退出
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RIGHT:  # 右方向键移动
                    if position_line.right + 10 > width:  # 右边界
                        position_line.right = width
                        continue
                    position_line.right += 10
                elif event.key == pygame.K_LEFT:  # 左方向键移动
                    if position_line.left - 10 < 0:  # 左边界
                        position_line.left = 0
                        continue
                    position_line.left -= 10


        position_ball = position_ball.move(speed_ball)  # 小球移动

        if position_ball.left < 0 or position_ball.right > width:  # 弹到左右边界
            speed_ball[0] = -speed_ball[0]
            knock_sound.play()
        elif position_ball.top < 0:  # 弹到上边界
            speed_ball[1] = -speed_ball[1]
            knock_sound.play()
        # 弹到line
        elif position_ball.right > position_line.left and \
                position_ball.left < position_line.right and \
                position_ball.bottom > position_line.top:
            # print('弹到了line')
            knock_sound.play()
            speed_ball[1] = -speed_ball[1]
        elif position_ball.bottom > position_line.top:
            if is_game_over == False:
                game_over_sound.play()
                is_game_over = True
                speed_ball = [0, 0]

        # 显示分数
        font = pygame.font.Font('../font/font.ttf', 60)
        score_dis = font.render('score: ' + str(int(score)), True, (255, 0, 0))
        score_dis_loc = (width - 300, 10)

        screen.blit(background, (0, 0))
        screen.blit(score_dis, score_dis_loc)
        screen.blit(ball, position_ball)
        screen.blit(line, position_line)
        if is_game_over:  # 游戏结束, 两个选项, 重新开始还是退出游戏
            game_over = pygame.font.Font('../font/font.ttf', 80)
            game_over_font = game_over.render("Game Over", True, (0, 0, 0))
            game_over_loc = (240, 150)
            screen.blit(game_over_font, game_over_loc)
            restart = game_over.render("Restart Game", True, (0, 0, 0))
            restart_loc = (240, 220)
            screen.blit(restart, restart_loc)
            restart_pos = restart.get_rect()
            game_exit = game_over.render("Exit Game", True, (0, 0, 0))
            game_exit_loc = (240, 300)
            screen.blit(game_exit, game_exit_loc)
            game_exit_pos = game_exit.get_rect()

            # 奇怪的位置, 为什么初始时不是返回正确位置
            restart_pos.left, restart_pos.top = restart_loc
            game_exit_pos.left, game_exit_pos.top = game_exit_loc

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if restart_pos.left < pos[0] < restart_pos.right and \
                        restart_pos.top < pos[1] < restart_pos.bottom:
                    # print('重新开始游戏')
                    main()
                elif game_exit_pos.left < pos[0] < game_exit_pos.right and \
                        game_exit_pos.top < pos[1] < game_exit_pos.bottom:
                    # print('退出游戏')
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()  # 更新界面
        clock.tick(60)  # 设置帧率60


if __name__ == "__main__":
    main()