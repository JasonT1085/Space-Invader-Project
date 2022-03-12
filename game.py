from re import X
import pygame as pg
from landing_page import LandingPage
from sys import exit
import game_functions as gf
from time import sleep
from game_stats import GameStats
from laser import Lasers
from ship import Ship
from alien import AlienFleet, UFOSpawner
from settings import Settings
from random import randint, choice
import Bunker
from barrier import Barriers
from scoreboard import Scoreboard
import time
clock = pg.time.Clock()
FPS = 60
class Game:
    RED = (255, 0, 0)

    def __init__(self):
        
        pg.init()
        self.prevTime = pg.time.get_ticks()
        self.bg = pg.image.load("spaceBG.jpg")
        self.settings = Settings()
        self.stats = GameStats(game=self)
        self.screen = pg.display.set_mode((self.settings.screen_width,
                                           self.settings.screen_height))
        self.bg_color = self.settings.bg_color
        self.sb = Scoreboard(game=self)
        pg.display.set_caption("Alien Invasion")
        self.ship = Ship(game=self)
        self.alien_fleet = AlienFleet(game=self)
        self.ufo = UFOSpawner(game=self)
        self.lasers = Lasers(game=self)
        self.ship.set_alien_fleet(self.alien_fleet)
        self.ship.set_lasers(self.lasers)
        self.shape = Bunker.shape
        self.block_size = 6
        self.blocks = pg.sprite.Group()
        self.bunker_amount = 5
        self.bunker_positions = [num * (self.settings.screen_width / self.bunker_amount) for num in range(self.bunker_amount)]
        self.create_bunker_set(self.settings.screen_width / 20 , 620, *self.bunker_positions)

    
    def create_bunker(self, x_start, y_start, offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == 'x':
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
                    block = Bunker.Block(self.block_size,(0,255,0),x,y)
                    self.blocks.add(block)
    
    def create_bunker_set(self,x_start, y_start, *offset):
        for offset_x in offset:
            self.create_bunker(x_start, y_start, offset_x)


    def restart(self):
        if self.stats.ships_left  == 0: 
          self.game_over()
        print("restarting game")
        self.blocks.empty()
        self.create_bunker_set(self.settings.screen_width / 10 , 620, *self.bunker_positions   )
        self.lasers.empty()
        self.ufo.ufo.empty()
        self.ufo.reset()
        self.alien_fleet.empty()
        self.alien_fleet.create_fleet()
        self.alien_fleet.reset_moveTime()
        self.ship.center_bottom()
        self.ship.reset_timer()
        self.stats.reset_score()
        self.stats.level = 1
        sleep(0.5)

    def update(self):
        self.ship.update()
        self.alien_fleet.update()
        self.lasers.update()
        self.ufo.update()
        self.sb.update()
        self.stats.update()
        pg.display.update()
        
                
    def draw(self):
        self.screen.blit(self.bg,(0,0))
        
        self.sb.draw()
        self.ship.draw()
        self.alien_fleet.draw()
        self.lasers.draw()
        self.blocks.draw(self.screen)
        self.ufo.draw()
        pg.display.flip()

    def play(self):
        self.finished = False
        while not self.finished:
            self.currentTime = pg.time.get_ticks()
            self.update() 
            self.draw()
            gf.check_events(game=self)   # exits game if QUIT pressed
        self.game_over()

    def game_over(self): 
      print('\nGAME OVER!\n\n')  
      exit()    # can ask to replay here instead of exiting the game

def main():
    g = Game()
    lp = LandingPage(screen=g.screen, game=g)
    lp.show()
    g.play()


if __name__ == '__main__':
    main()
