import pygame as pg
from vector import Vector
from pygame.sprite import Sprite, Group, GroupSingle
from timer import Timer
from random import randint, choice

class AlienFleet:
    alien_exploding_images = [pg.image.load(f'images/alien_explode{n}.png') for n in range(2)]
    alien1_images = [pg.image.load(f'images/alien0_{n}.png') for n in range(2)]
    alien2_images = [pg.image.load(f'images/alien1_{n}.png') for n in range(2)]
    alien3_images = [pg.image.load(f'images/alien2_{n}.png') for n in range(2)]
    ufo_image = pg.image.load(f'images/alien3.png')

    def __init__(self, game, v=Vector(1, 0)):
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
        self.fleet = Group()
        self.create_fleet()

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
        y = self.alien_h1 * (2 * row + 1)
        alien1_images = AlienFleet.alien1_images
        x2 = self.alien_w2 * (2 * col + 1)
        y2 = self.alien_h2 * (2 * row + 1)
        alien2_images = AlienFleet.alien2_images
        x3 = self.alien_w3 * (2 * col + 1)
        y3 = self.alien_h3 * (2 * row + 1)
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
        delta_s = Vector(0, 0)    # don't change y position in general
        if self.check_edges():
            self.v.x *= -1
            self.change_v(self.v)
            delta_s = Vector(0, self.settings.fleet_drop_speed)
        if pg.sprite.spritecollideany(self.ship, self.fleet) or self.check_bottom():
            if not self.ship.is_dying(): self.ship.hit() 
        for alien in self.fleet.sprites():
            alien.update(delta_s=delta_s)
            
    def draw(self):
        for alien in self.fleet.sprites():
            alien.draw()


class Alien(Sprite):
    def __init__(self, tier, game, image_list, start_index=0, ul=(0, 100), v=Vector(1, 0)):
        super().__init__()
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
            
    def update(self, delta_s=Vector(0, 0)):
        if self.dying and self.timer.is_expired():
          self.kill()
          self.settings.alien_speed_factor+= 0.01
        
        self.ul += delta_s
        self.ul += self.v * self.settings.alien_speed_factor
        self.rect.x, self.rect.y = self.ul.x, self.ul.y

        
    def draw(self):  
      image = self.timer.image()
      rect = image.get_rect()
      rect.x, rect.y = self.rect.x, self.rect.y
      self.screen.blit(image, rect)
      # self.screen.blit(self.image, self.rect)

class UFOSpawner():
    def __init__(self, game, v = Vector(1,0)):
        self.game = game
        self.screen = game.screen
        self.v = v
        self.settings = game.settings
        self.UFO_spawn_time = randint(40, 80)
        self.ufo = GroupSingle()
        self.UFO_timer()
        
    def UFO_timer(self):   
        if pg.time.get_ticks() % 500 == 0 and randint(1,2) == 1:
            self.ufo.add(ufo(game=self, side=choice(['right', 'left'])))
            
    def update(self):
        delta_s = Vector(0, 0)
        for ufo in self.ufo.sprites():
            ufo.update(delta_s=delta_s)
        
    def draw(self):
        for ufo in self.ufo.sprites():
            ufo.draw()
        
class ufo(Sprite):
    def __init__(self, game, side, start_index=0, ul=(0, 50), v=Vector(1, 0)):
        super().__init__()
        images = [pg.image.load(f'images/alien3.png') for n in range(1)]
        self.image = pg.image.load('images/alien3.png')
        
        self.v = v
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.screen_rect = self.screen.get_rect()
        self.rect = self.image.get_rect()
        self.ul = Vector(ul[0], ul[1])
        self.rect.left, self.rect.top = ul        
        self.image_list = images
        self.exploding_timer = Timer(image_list=AlienFleet.alien_exploding_images, delay=200, 
                                     start_index=start_index, is_loop=False)
        self.normal_timer = Timer(image_list=self.image_list, delay=1000, is_loop=True)
        self.timer = self.normal_timer
        self.dying = False
        if side == 'right':
            self.ul.x = self.settings.screen_width
            self.speed = -1
        elif side == 'left':
            self.ul.x = 0
            self.speed = 1

    def hit(self): 
      self.timer = self.exploding_timer
      self.dying = True
    
    def get_ul(self):
        return self.ul
            
    
    def update(self, delta_s=Vector(0, 0)):
        if self.dying and self.timer.is_expired():
          self.kill()
        self.ul += delta_s
        self.ul += self.v * self.speed
        self.rect.x += self.speed
        self.rect.x, self.rect.y = self.ul.x, self.ul.y
        
    def draw(self):  
      image = self.timer.image()
      rect = image.get_rect()
      rect.x, rect.y = self.rect.x, self.rect.y
      self.screen.blit(image, rect)