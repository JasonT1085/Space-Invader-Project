import pygame as pg
from vector import Vector
from pygame.sprite import Sprite, Group
from copy import copy
from random import randint
from timer import CommandTimer
# from alien import Alien
# from stats import Stats


class Barriers:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.barriers = Group()
        self.barrier_amount = 4
        self.barrier_positions = [num * (self.settings.screen_width / self.barrier_amount) for num in range(self.barrier_amount)]
        self.create_barrier_set(self.settings.screen_width / 10 , 620, *self.barrier_positions)
        
        # self.alien_fleet = game.alien_fleet
    def create_barrier_set(self,x_start, y_start, *offset):
        for offset_x in offset:
            self.create_barrier(x_start, y_start, offset_x)
    
    def create_barrier(self, x_start, y_start, offset_x):
        self.barriers.add(Barrier(game=self.game,ul = (x_start + offset_x, y_start)))
    
    def update(self): 
        for barrier in self.barriers:
            barrier.update()

    def draw(self): 
        for barrier in self.barriers:
            barrier.draw()


class Barrier(Sprite):
    def __init__(self, game, ul, wh = (4, 4)): 
        img_list = [pg.image.load(f'images/block{n}.png') for n in range(5)]
        self.game = game
        self.barrier_elements = Group()
        self.ul = ul
        self.wh = wh
        for row in range(wh[0]):
            for col in range(wh[1]):
                be = BarrierElement(game=game, img_list=img_list,
                    ul=(ul[0] + col, ul[1] + row), wh=self.wh)
                self.barrier_elements.add(be)
        
    def update(self): 
        collisions = pg.sprite.groupcollide(self.barrier_elements, 
                                            self.lasers, False, True)
        for be in collisions: 
            be.hit()

    def draw(self): 
        for be in self.barrier_elements:
            be.draw()


class BarrierElement(Sprite):
    def __init__(self, game, img_list, ul, wh): 
        self.ul = ul
        self.wh = wh
        self.rect = pg.Rect(ul[0], ul[1], wh[0], wh[1])
        self.timer = CommandTimer(image_list=img_list, is_loop=False)

    def update(self): pass

    def hit(self):
        self.timer.next_frame()
        if self.timer.is_expired():
            self.kill()

    def draw(self): 
        image = self.timer.image()
        rect = image.get_rect()
        rect.x, rect.y = self.rect.x, self.rect.y
        self.screen.blit(image, rect)
