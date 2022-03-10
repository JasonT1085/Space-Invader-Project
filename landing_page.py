from re import A
import pygame as pg
import sys
from alien import AlienFleet
from settings import Settings
from button import Button
from timer import Timer
import wave
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (130, 130, 130)



class LandingPage:
    def __init__(self, screen, game):
        alien1_images = [pg.image.load(f'images/alien0_{n}.png') for n in range(2)]
        alien2_images = [pg.image.load(f'images/alien1_{n}.png') for n in range(2)]
        alien3_images = [pg.image.load(f'images/alien2_{n}.png') for n in range(2)]
        self.ufo_image = pg.image.load(f'images/alien3.png')
        timer1 = Timer(image_list=alien1_images, delay=1000, is_loop=True)
        timer2 = Timer(image_list=alien2_images, delay=1000, is_loop=True)
        timer3 = Timer(image_list=alien3_images, delay=1000, is_loop=True)
        
        self.screen = screen
        self.settings = game.settings
        self.landing_page_finished = False
        self.score_toggle = False
        self.play_button = Button(screen, "PLAY", centery = 650)
        self.hs_button = Button(screen, "HIGHSCORE", centery = 700)
        self.bg = pg.image.load("spaceBG.jpg")
        headingFont = pg.font.Font("font.ttf", 192)
        subheadingFont = pg.font.Font("font.ttf", 100)
        font = pg.font.Font("font.ttf", 48)
        bgm = "music.mp3"
        self.file_wav = wave.open('invadermusic.wav')
        pg.mixer.init()
        pg.mixer.music.load(bgm)
        pg.mixer.music.set_volume(0.2)
        pg.mixer.music.play(-1)
        self.alien_images = [alien1_images, alien2_images, alien3_images]
        self.timer = [timer1, timer2, timer3]
        
        strings = [('SPACE', WHITE, headingFont), ('INVADERS', GREEN, subheadingFont),
                ('= 40 PTS', GREY, font), ('= 20 PTS', GREY, font),
                            ('= 10 PTS', GREY, font), ('= ???', GREY, font),
                ('', BLACK, font), ('', BLACK, font)]

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
        self.alienrects = [self.get_alien_rect(timer=self.timer[i], centerx = aliencenterx, centery=self.posns[j]) for i in range(alienLen) for j in range(2,5)]
        self.uforect = self.get_ufo_rect(alien=self.ufo_image, centerx = aliencenterx, centery = self.posns[5])
        # self.normal_timer = Timer(image_list=image_list, delay=1000, is_loop=True)
    
    def get_text(self, font, msg, color): return font.render(msg, True, color, BLACK)

    def get_text_rect(self, text, centerx, centery):
        rect = text.get_rect()
        rect.centerx = centerx
        rect.centery = centery
        return rect
    
    def get_alien_rect(self, timer, centerx, centery):
        image = timer.image()
        rect = image.get_rect()
        rect.centerx = centerx
        rect.centery = centery
        return rect
    def get_ufo_rect(self, alien, centerx, centery):
        rect = alien.get_rect()
        rect.centerx = centerx
        rect.centery = centery
        return rect
    
    def toggle_scores(self):
        font = pg.font.Font("font.ttf", 32)
        self.highScorerect = self.get_text_rect(text =self.texts[7], centerx = 30, centery = self.settings.screen_height - 30 )
        self.highScore = font.render('HIGHSCORE: 1800', True, WHITE)
        self.screen.blit(self.highScore, self.highScorerect)
    
    def check_events(self):
        for e in pg.event.get():
            mouseX, mouseY = pg.mouse.get_pos()
            if e.type == pg.QUIT:
                sys.exit()
            if e.type == pg.MOUSEBUTTONDOWN: 
                if self.play_button.rect.collidepoint(mouseX,mouseY):
                    self.landing_page_finished = True
                    pg.mixer.music.stop()
                    pg.mixer.init()
                elif self.hs_button.rect.collidepoint(mouseX,mouseY):
                    if not self.score_toggle: self.score_toggle = True
                    else: self.score_toggle = False
                    
                    
    def update(self):       
        self.play_button.update_button()
        self.hs_button.update_button()

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
      for i in range(3):  
        image = self.timer[i].image()
        self.screen.blit(image, self.alienrects[i])

    def draw_ufo(self):
        self.screen.blit(self.ufo_image, self.uforect)

    def draw(self):
        self.screen.blit(self.bg,(0,0))
        self.draw_text()
        self.draw_alien()   # TODO draw my aliens
        self.draw_ufo()
        # self.lasers.draw()        
        self.play_button.draw_button() # TODO draw my button and handle mouse events
        self.hs_button.draw_button()
        if self.score_toggle: self.toggle_scores()
        pg.display.flip()
    
