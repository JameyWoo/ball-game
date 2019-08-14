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
    count_up = 0
    waigua = False  # 设一个外挂模式, 按g切换模式
    start_sound.play()

    # 读取文件中的分数
    scores = []
    with open('scores.txt', 'r', encoding='utf-8') as file:
        file_score = file.readlines()
        # print(file_score)
        for each in file_score:
            scores.append(int(each))
        # print(scores)
        # print(sorted(scores, reverse=True))
        scores = sorted(scores, reverse=True)[: 3]

    # 正式进入游戏前的选项画面
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 叉掉退出
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:  # 按q退出
                    pygame.quit()
                    sys.exit()

        screen.fill((255, 255, 255))
        screen.blit(background, (0, 0))
        start_game = pygame.font.Font('../font/font.ttf', 80)
        start_game_font = start_game.render("Ball Game", True, (0, 0, 0))
        start_game_loc = (120, 100)
        screen.blit(start_game_font, start_game_loc)
        restart = start_game.render("Play Game", True, (0, 0, 0))
        restart_loc = (120, 220)
        screen.blit(restart, restart_loc)
        restart_pos = restart.get_rect()
        game_exit = start_game.render("Exit Game", True, (0, 0, 0))
        game_exit_loc = (120, 360)
        screen.blit(game_exit, game_exit_loc)
        game_exit_pos = game_exit.get_rect()

        start_game_small = pygame.font.Font(None, 50)
        best_scores = start_game_small.render("Top 3 Scores", True, (0, 0, 0))
        screen.blit(best_scores, (500, 200))
        for i, each in enumerate(scores):
            score_dis = start_game_small.render(str(each), True, (0, 0, 0))
            score_loc = (530, 275 + 50 * i)
            screen.blit(score_dis, score_loc)

        # 奇怪的位置, 为什么初始时不是返回正确位置
        restart_pos.left, restart_pos.top = restart_loc
        game_exit_pos.left, game_exit_pos.top = game_exit_loc

        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            if restart_pos.left < pos[0] < restart_pos.right and \
                    restart_pos.top < pos[1] < restart_pos.bottom:
                # print('重新开始游戏')
                break
            elif game_exit_pos.left < pos[0] < game_exit_pos.right and \
                    game_exit_pos.top < pos[1] < game_exit_pos.bottom:
                # print('退出游戏')
                pygame.quit()
                sys.exit()

        pygame.display.flip()  # 更新界面
        clock.tick(60)  # 设置帧率60

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
            # 更新线的高度(难度设置), 1s中line向上移动3像素
            position_line.top -= 3
            count_up += 3
            if (count_up % 30 == 0):
                position_line.top += 30

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
                elif event.key == pygame.K_g:
                    waigua = not waigua
                    print('外挂模式' + "开启" if waigua else "关闭")


        position_ball = position_ball.move(speed_ball)  # 小球移动

        if position_ball.left < 0 or position_ball.right > width:  # 弹到左右边界
            speed_ball[0] = -speed_ball[0]
            knock_sound.play()
        elif position_ball.top < 0 or (waigua is True and position_ball.bottom > position_line.top):  # 弹到上边界
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
                with open('scores.txt', 'a+', encoding='utf-8') as file:
                    file.write(str(int(score)) + '\n')
                speed_ball = [0, 0]

        # 显示分数
        font = pygame.font.Font('../font/font.ttf', 60)
        score_dis = font.render('score: ' + str(int(score)), True, (255, 0, 0))
        score_dis_loc = (width - 300, 10)

        screen.fill((255, 255, 255))
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