HS_FILE = 'highscore.txt'
from os import path
class GameStats:
    def __init__(self, game):
        self.game = game
        self.settings = game.settings
        self.reset_stats()
        self.last_ships_left = self.ships_left
        self.score = 0
        self.level = 0
        self.hscore = 0
        self.load_data()
        
    def load_data(self):
        #load high score
        try:
            with open(HS_FILE, 'r+') as f:
                self.hscore = int(f.read())
        except:
            with open(HS_FILE, 'w') as f:
                self.hscore = 0
    
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
            with open(HS_FILE, 'w') as f:
                f.write(str(self.hscore))
    
    def reset_stats(self): self.ships_left = self.settings.ship_limit
    def ship_hit(self):
        self.ships_left -= 1
        n = self.ships_left
        print(f'SHIP HIT!', end=' ')
        if self.last_ships_left != self.ships_left:
            print(f'{self.ships_left} ship{"s" if n != 1 else ""} left')
            self.last_ships_left = self.ships_left
