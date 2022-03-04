from re import A
import pygame as pg
import sys
from alien import AlienFleet
from settings import Settings
from button import Button
from timer import Timer
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (130, 130, 130)



class LandingPage:
    def __init__(self, screen):
        self.screen = screen
        self.landing_page_finished = False
        self.play_button = Button(screen, "PLAY")
        self.bg = pg.image.load("spaceBG.jpg")
        headingFont = pg.font.Font("font.ttf", 192)
        subheadingFont = pg.font.Font("font.ttf", 122)
        font = pg.font.Font("font.ttf", 48)
        bgm = "music.mp3"
        pg.mixer.init()
        pg.mixer.music.load(bgm)
        pg.mixer.music.set_volume(0.2)
        pg.mixer.music.play(-1)
        self.alien_images = [pg.image.load(f'images/alien{n}.png') for n in range(4)]
        
        strings = [('SPACE', WHITE, headingFont), ('INVADERS', GREEN, subheadingFont),
                ('= 40 PTS', GREY, font), ('= 20 PTS', GREY, font),
                            ('= 10 PTS', GREY, font), ('= ???', GREY, font),
                ('', BLACK, font), ('HIGH SCORES', GREY, font)]

        self.texts = [self.get_text(msg=s[0], color=s[1], font=s[2]) for s in strings]
        
        self.posns = [150, 300]
        alien = [60 * x + 400 for x in range(4)]
        play_high = [x for x in range(650, 760, 80)]
        self.posns.extend(alien)
        self.posns.extend(play_high)

        centerx = self.screen.get_rect().centerx
        aliencenterx = self.screen.get_rect().centerx - 150
        n = len(self.texts)
        alienLen = len(self.alien_images)
        self.rects = [self.get_text_rect(text=self.texts[i], centerx=centerx, centery=self.posns[i]) for i in range(n)]
        self.alienrects = [self.get_alien_rect(alien=self.alien_images[i], centerx = aliencenterx, centery=self.posns[j]) for i in range(alienLen) for j in range(2,6)]
        # self.normal_timer = Timer(image_list=image_list, delay=1000, is_loop=True)
    
    def get_text(self, font, msg, color): return font.render(msg, True, color, BLACK)

    def get_text_rect(self, text, centerx, centery):
        rect = text.get_rect()
        rect.centerx = centerx
        rect.centery = centery
        return rect
    
    def get_alien_rect(self, alien, centerx, centery):
        rect = alien.get_rect()
        rect.centerx = centerx
        rect.centery = centery
        return rect

    def check_events(self):
        for e in pg.event.get():
            mouseX, mouseY = pg.mouse.get_pos()
            if e.type == pg.QUIT:
                sys.exit()
            if e.type == pg.MOUSEBUTTONDOWN: 
                if self.play_button.rect.collidepoint(mouseX,mouseY):
                    self.landing_page_finished = True  
                    
    def update(self):       # TODO make aliens move
        self.play_button.update_button()

    def show(self):
        while not self.landing_page_finished:
            self.update()
            self.draw()
            self.check_events()   # exits game if QUIT pressed

    def draw_text(self):
        n = len(self.texts)
        for i in range(n):
            self.screen.blit(self.texts[i], self.rects[i])
    
    def draw_alien(self):
        n = len(self.alien_images)
        for i in range(n):
            self.screen.blit(self.alien_images[i], self.alienrects[i])

    def draw(self):
        self.screen.blit(self.bg,(0,0))
        self.draw_text()
        self.draw_alien()   # TODO draw my aliens
        # self.lasers.draw()        
        self.play_button.draw_button() # TODO draw my button and handle mouse events
        pg.display.flip()
    
