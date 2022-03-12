HS_FILE = 'scores/highscore.txt'
import os
import time
prev_time = time.time()
FPS = 4
dt = (time.time() - prev_time) * FPS
class GameStats:
    def __init__(self, game):
        self.game = game
        self.settings = game.settings
        self.reset_stats()
        self.last_ships_left = self.ships_left
        self.score = 0
        self.level = 1
        self.hscore = 0
        self.load_highscore()
        
    def __del__(self): self.save_highscore()
    
    def load_highscore(self):
        #load high score
        try:
            with open(HS_FILE, 'r+') as f:
                self.hscore = int(f.read())
        except:
            with open(HS_FILE, 'w') as f:
                self.hscore = 0
    
    def save_highscore(self):
        with open(HS_FILE, 'w') as f:
            f.write(str(self.hscore))
    
    def get_score(self):
        return self.score
    
    def add_score(self, value):
        self.score+= value
        
    def reset_score(self):
        self.score = 0
        
    def get_level(self):
        return self.level
    
    def get_highscore(self):
        return self.hscore
    
    def get_ships_left(self):
        return self.last_ships_left
    
    def update(self):
        if self.score > self.hscore:
            self.hscore = self.score
    
    def reset_stats(self): self.ships_left = self.settings.ship_limit
    def ship_hit(self):
        self.ships_left -= 1
        n = self.ships_left
        print(f'SHIP HIT!', end=' ')
        if self.last_ships_left != self.ships_left:
            print(f'{self.ships_left} ship{"s" if n != 1 else ""} left')
            self.last_ships_left = self.ships_left
