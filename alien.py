import pygame as pg
from vector import Vector
from pygame.sprite import Sprite, Group, GroupSingle
from timer import Timer
from random import randint, choice
import time

FONT = "font.ttf"
class AlienFleet:
    alien_exploding_images = [pg.image.load(f'images/alien_explode{n}.png') for n in range(5)]
    alien1_images = [pg.image.load(f'images/alien0_{n}.png') for n in range(2)]
    alien2_images = [pg.image.load(f'images/alien1_{n}.png') for n in range(2)]
    alien3_images = [pg.image.load(f'images/alien2_{n}.png') for n in range(2)]
    ufo_image = pg.image.load(f'images/alien3.png')

    def __init__(self, game, v=Vector(1, 0)):
        
        self.invaderSound4 = pg.mixer.Sound('invadermusic4.wav')
        self.invaderSound4.set_volume(0.05)
        self.game = game
        self.ship = self.game.ship
        self.settings = game.settings
        self.screen = self.game.screen
        self.screen_rect = self.screen.get_rect()
        self.v = v
        alien1 = Alien( '3', self.game, image_list=AlienFleet.alien1_images)
        alien2 = Alien( '2', self.game, image_list=AlienFleet.alien2_images)
        alien3 = Alien( '1', self.game, image_list=AlienFleet.alien3_images)
        self.alien_h1, self.alien_w1 = alien1.rect.height, alien1.rect.width
        self.alien_h2, self.alien_w2 = alien2.rect.height, alien2.rect.width
        self.alien_h3, self.alien_w3 = alien3.rect.height, alien3.rect.width
        self.timer = pg.time.get_ticks()
        self.moveTime = 500
        self.fleet = Group()
        self.create_fleet()

    def reset_moveTime(self):
        self.moveTime = 500
        self.timer = pg.time.get_ticks()
        
    def create_fleet(self):
        n_cols = self.get_number_cols(alien_width=self.alien_w1)
        n_rows = self.get_number_rows(ship_height=self.ship.rect.height,
                                      alien_height=self.alien_h1)
        count = 0
        for row in range(n_rows):
            for col in range(n_cols):
                self.create_alien(row=row, col=col, count=count)
            count+=1

    def set_ship(self, ship): self.ship = ship
    def create_alien(self, row, col, count):
        x = self.alien_w1 * (2 * col + 1)
        y = self.alien_h1 * (2 *row + 1)
        alien1_images = AlienFleet.alien1_images
        x2 = self.alien_w2 * (2 *col + 1)
        y2 = self.alien_h2 * (2 *row + 1)
        alien2_images = AlienFleet.alien2_images
        x3 = self.alien_w3 * (2 *col + 1)
        y3 = self.alien_h3 * (2 *row + 1)
        alien3_images = AlienFleet.alien3_images        
        # alien = Alien(game=self.game, ul=(x, y), v=self.v, image_list=images, 
        #               start_index=randint(0, len(images) - 1))
        alien = Alien( '3', game=self.game, ul=(x, y), v=self.v, image_list=alien1_images)
        alien2 = Alien( '2', game=self.game, ul=(x2, y2), v=self.v, image_list=alien2_images)
        alien3 = Alien( '1', game=self.game, ul=(x3, y3), v=self.v, image_list=alien3_images)
        if(count < 1):
            self.fleet.add(alien)
        elif(count<=2):
            self.fleet.add(alien2)
        elif(count<=4):
            self.fleet.add(alien3)

    def empty(self): self.fleet.empty()
    def get_number_cols(self, alien_width):
        spacex = self.settings.screen_width - 2 * alien_width
        return int(spacex / (2 * alien_width))

    def get_number_rows(self, ship_height, alien_height):
        spacey = self.settings.screen_height - 3 * alien_height - ship_height
        return int(spacey / (2 * alien_height))

    def length(self): return len(self.fleet.sprites())

    def change_v(self, v):
        for alien in self.fleet.sprites():
            alien.change_v(v)

    def check_bottom(self): 
      for alien in self.fleet.sprites():
        if alien.check_bottom():
            self.ship.hit()
            break
      
    def check_edges(self): 
      for alien in self.fleet.sprites():
        if alien.check_edges(): return True
      return False

    def update(self):
        if self.game.currentTime - self.timer > self.moveTime:
            delta_s = Vector(0, 0)    # don't change y position in general
            if self.check_edges():
                self.v.x *= -1
                self.change_v(self.v)
                delta_s = Vector(0, self.settings.fleet_drop_speed)
            if pg.sprite.spritecollideany(self.ship, self.fleet) or self.check_bottom():
                if not self.ship.is_dying(): self.ship.hit() 
            for alien in self.fleet.sprites():
                alien.toggle_image()
                pg.mixer.Channel(0).play(self.invaderSound4)
                alien.update(delta_s=delta_s)
            self.timer += self.moveTime
            
    def draw(self):
        for alien in self.fleet.sprites():
            alien.draw()


class Alien(Sprite):
    def __init__(self, tier, game, image_list, start_index=0, ul=(0, 100), v=Vector(1, 0)):
        super().__init__()
        self.alienDeath = pg.mixer.Sound("Alien_death.mp3")
        self.alienDeath.set_volume(0.5)
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.image = pg.image.load('images/alien0.png')
        self.screen_rect = self.screen.get_rect()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = ul
        self.ul = Vector(ul[0], ul[1])   # position
        self.v = v                       # velocity
        self.image_list = image_list
        self.index = 0
        self.exploding_timer = Timer(image_list=AlienFleet.alien_exploding_images, delay=200, 
                                     start_index=start_index, is_loop=False)
        self.normal_timer = Timer(image_list=image_list, delay=1000, is_loop=True)
        self.timer = self.normal_timer
        self.dying = False
        self.value = 0
        if tier == '1': self.value = 10
        elif tier == '2': self.value = 20
        elif tier == '3': self.value = 40

    def change_v(self, v): self.v = v
    def check_bottom(self): return self.rect.bottom >= self.screen_rect.bottom
    def check_edges(self):
        r = self.rect
        return r.right >= self.screen_rect.right or r.left <= 0

    def hit(self): 
      self.timer = self.exploding_timer
      self.dying = True
      self.alienDeath.play()
    
    def toggle_image(self):
        self.index += 1
        if self.index >= len(self.image_list):
            self.index = 0
        self.image = self.image_list[self.index]
    
    def update(self, delta_s=Vector(0, 0)):
        if self.dying and self.timer.is_expired():
          self.game.stats.score+= self.value
          self.kill()
          self.settings.alien_speed_factor+= 0.01
        
        self.ul += delta_s
        self.ul += self.v * self.settings.alien_speed_factor
        self.rect.x, self.rect.y = self.ul.x, self.ul.y

        
    def draw(self):
      if self.dying:  
        image = self.timer.image()
        rect = image.get_rect()
        rect.x, rect.y = self.rect.x, self.rect.y
        self.screen.blit(image, rect)
      else:
        self.screen.blit(self.image, self.rect)

pg.mixer.init()
ufoSound = pg.mixer.Sound('ufo_lowpitch.wav')
ufoSound.set_volume(0.1)

class UFOSpawner():
    def __init__(self, game, v = Vector(1,0)):
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.v = v
        self.settings = game.settings
        self.ufo = GroupSingle()
        self.playOnce = True
        self.resetTimer = False
        self.spawnCheck = False
        
    def reset(self):
        self.playOnce = True
        self.resetTimer = False
        self.spawnCheck = False
        
    def check_edges(self):
        for ufo in self.ufo.sprites():
            return True if ufo.check_sides() else False
        
    def update(self):
        if self.resetTimer and not self.spawnCheck:
            self.timeCalled = self.game.currentTime
            self.spawnCheck = True
        delta_s = Vector(0, 0)
        for ufo in self.ufo.sprites():
            ufo.update(delta_s=delta_s)
            if self.check_edges():
                ufo.kill()
        if self.spawnCheck and len(self.ufo) == 0:
            self.UFO_timer()
    def UFO_timer(self):
        
        now = pg.time.get_ticks()
        passed = now - self.timeCalled 
        
        if passed > 10000 and len(self.ufo) ==  0 and randint(1,10) == 1:
            self.ufo.add(ufo(game=self.game, side=choice(['right', 'left'])))
            pg.mixer.Channel(1).play(ufoSound)
            self.spawnCheck = False
            self.resetTimer = False
            
    def draw(self):
        for ufo in self.ufo.sprites():
            ufo.draw()
        
class ufo(Sprite):
    def __init__(self, game, side, start_index=0, ul=(0,0), v=Vector(1, 0)):
        super().__init__()
        images = [pg.image.load(f'images/alien3.png') for n in range(1)]
        self.image = pg.image.load('images/alien3.png')
        self.alienDeath = pg.mixer.Sound("ufoDeath.wav")
        self.alienDeath.set_volume(0.5)
        self.alienExplosion = pg.mixer.Sound("ufoExplosion.wav")
        self.alienExplosion.set_volume(0.5)
        
       # self.prevTimer = pg.time.get_ticks()
        self.value = randint(500,1000)
        self.v = v
        self.side = side
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.screen_rect = self.screen.get_rect()
        self.rect = self.image.get_rect()
        self.ul = Vector(ul[0], ul[1])
        self.rect.left, self.rect.top = ul        
        self.image_list = images
        self.normal_timer = Timer(image_list=self.image_list, delay=1000, is_loop=True)
        self.timer = self.normal_timer
        self.dying = False
        self.showText = False
        self.deathTimer= pg.time.get_ticks()
        if side == 'right':
            self.ul.x = self.settings.screen_width
            self.speed = -1
        elif side == 'left':
            self.ul.x = 0
            self.speed = 1
            
    def play_sound(self):
        r = self.rect
        
        if self.side == 'right' and r.right >= 0 and not self.dying:
            ufoSound.play()
        elif self.side == 'left' and r.left <= self.screen_rect.right and not self.dying:
            ufoSound.play()
            
    def check_sides(self):
        r = self.rect
        if self.side == 'right' and r.right <= 0:
            return r.right <= 0
        elif self.side == 'left' and r.left >= self.screen_rect.right:
            return r.left >= self.screen_rect.right 

    def hit(self): 
      self.dying = True
      pg.mixer.Channel(3).play(self.alienDeath)
      pg.mixer.Channel(4).play(self.alienExplosion)
    
    def get_ul(self):
        return self.ul
            
    
    def update(self, delta_s=Vector(0, 0)):
        if self.dying and not self.showText:
          self.game.stats.score+= self.value
          self.showText = True
          self.deathTimer = pg.time.get_ticks()
        self.ul += delta_s
        self.ul += self.v * self.speed
        self.rect.x += self.speed
        self.rect.x, self.rect.y = self.ul.x, self.ul.y
        if self.showText:
            self.ufoDeath(self.value)
        
        
    def draw(self):
      if self.showText: return
      image = self.timer.image()
      rect = image.get_rect()
      rect.x, rect.y = self.rect.x, self.rect.y
      self.screen.blit(image, rect)
      
    def ufoDeath(self, score):
        self.text = Text(FONT, 20, str(score), (255,255,255),
                         self.rect.x, self.rect.y + 6)
        now = pg.time.get_ticks()
        passed = now - self.deathTimer
        if passed <= 600:
            self.text.draw(self.game.screen)
        elif 600 < passed:
            self.kill()

class Text(object):
    def __init__(self, textFont, size, message, color, xpos, ypos):
        self.font = pg.font.Font(textFont, size)
        self.scoremsg = self.font.render(message, True, color)
        self.rect = self.scoremsg.get_rect(topleft=(xpos, ypos))

    def draw(self, screen):
        screen.blit(self.scoremsg, self.rect)