# -*- encoding: utf-8 -*-

"""
@file: pause.py
@time: 2019/8/10 19:37
@author: 姬小野
@version: 0.1
"""
import pygame

class Pause(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.pause_nor = pygame.image.load('../image/pause_nor.png').convert_alpha()
        self.pause_pressed = pygame.image.load('../image/pause_pressed.png').convert_alpha()
        self.resume_nor = pygame.image.load('../image/resume_nor.png').convert_alpha()
        self.resume_pressed = pygame.image.load('../image/resume_pressed.png').convert_alpha()
