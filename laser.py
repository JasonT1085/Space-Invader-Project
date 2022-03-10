import pygame as pg
from vector import Vector
from pygame.sprite import Sprite, Group
from copy import copy
from random import randint, choice
from alien import Alien
import Bunker


class Lasers:
    def __init__(self, game):
        self.game = game
        self.ship = game.ship
        self.stats = game.stats
        self.alien_fleet = game.alien_fleet
        self.lasers = Group()
        self.alien_lasers = Group()
        self.ufo = game.ufo
    def add(self, laser): self.lasers.add(laser)
    def empty(self): 
        self.lasers.empty()
        self.alien_lasers.empty()
    def fire(self): 
      new_laser = Laser(self.game)
      self.lasers.add(new_laser)

    def alien_shoot(self):
        if self.alien_fleet.fleet.sprites():
            random_alien = choice(self.alien_fleet.fleet.sprites())
            alien_laser = Laser(self.game)
            alien_laser.center = copy(random_alien.ul)
            alien_laser.v = Vector(0, 1) * self.game.settings.laser_speed_factor
            self.alien_lasers.add(alien_laser)
    
    def ufo_shoot(self):
        if self.ufo.ufo.sprites():
            ufo = self.ufo.ufo.sprites()[0]
            ufo_laser = Laser(self.game)
            ufo_laser.center = copy(ufo.ul)
            ufo_laser.v = Vector(0, 1) * self.game.settings.laser_speed_factor
            self.alien_lasers.add(ufo_laser)
            
    def update(self):
        for laser in self.lasers.copy():
            if laser.rect.bottom <= 0: self.lasers.remove(laser)
        for alien_laser in self.alien_lasers.copy():
            if alien_laser.rect.top >= self.game.settings.screen_height: self.alien_lasers.remove(alien_laser)

        collisions = pg.sprite.groupcollide(self.alien_fleet.fleet, self.lasers, False, True)
        
        ufoCollision = pg.sprite.groupcollide(self.ufo.ufo, self.lasers, False, True)
        for ufo in ufoCollision:
            self.stats.add_score(ufo.value)
            if not ufo.dying:
                ufo.hit()
        
        ASCollision = pg.sprite.spritecollide(self.ship, self.alien_lasers, True)
        if ASCollision:
            if not self.ship.dying:
                self.ship.hit()
                
        BunkerCollide = pg.sprite.groupcollide(self.game.blocks, self.lasers, True, True)
        ALcollision = pg.sprite.groupcollide(self.game.blocks, self.alien_lasers, True, True)
        for alien in collisions:
            self.stats.add_score(alien.value)
            if not alien.dying: 
                alien.hit()

        # if AScollision:
        #     if not self.game.ship.dying: self.game.ship.hit()
        
        if self.alien_fleet.length() == 0:  
            self.game.restart()
        elif self.alien_fleet.length() == 1:
            self.game.settings.alien_speed_factor = 3
            
        for laser in self.lasers:
            laser.update()
        for alien_laser in self.alien_lasers:
            alien_laser.update()
            
    def draw(self):
        for laser in self.lasers:
            laser.draw()
        for alien_laser in self.alien_lasers:
            alien_laser.draw()


class Laser(Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.w, self.h = self.settings.laser_width, self.settings.laser_height
        self.ship = game.ship

        self.rect = pg.Rect(0, 0, self.w, self.h)
        self.center = copy(self.ship.center)
        # print(f'center is at {self.center}')
        # self.color = self.settings.laser_color
        tu = 50, 255
        self.color = randint(*tu), randint(*tu), randint(*tu)
        self.v = Vector(0, -1) * self.settings.laser_speed_factor

    def update(self):
        self.center += self.v
        self.rect.x, self.rect.y = self.center.x, self.center.y

    def draw(self): pg.draw.rect(self.screen, color=self.color, rect=self.rect)
    