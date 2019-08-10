# -*- encoding: utf-8 -*-

"""
@file: main.py
@time: 2019/8/10 15:53
@author: 姬小野
@version: 0.1
"""

import pygame
import sys
from pygame.locals import *
from random import *
import traceback


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
    ball = pygame.image.load('../image/ball.png').convert_alpha()  # 设置透明通道
    # icon = ball
    # pygame.display.set_icon(icon)
    shape_ball = width_ball, height_ball = 50, 50
    ball = pygame.transform.scale(ball, shape_ball)
    line = pygame.image.load('../image/line.png').convert_alpha()
    shape_line = width_line, height_line = 200, 30
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
    clock = pygame.time.Clock()
    start_sound.play()

    while running:
        # if pause:
        #     for event in pygame.event.get():
        #         if event.type == pygame.MOUSEBUTTONDOWN and event.pos
        #
        # else:
        #     pass
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
            game_over_sound.play()
            print('game over')
            speed_ball = [0, 0]

        # screen.fill((0, 255, 255))
        screen.blit(background, (0, 0))
        screen.blit(ball, position_ball)
        screen.blit(line, position_line)
        pygame.display.flip()  # 更新界面
        clock.tick(60)


if __name__ == "__main__":
    main()