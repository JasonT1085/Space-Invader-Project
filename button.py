import pygame as pg

class Button():
    def __init__(self, screen, msg):
        
        self.screen = screen
        self.screen_rect = screen.get_rect()
        
        self.width, self.height = 200, 50
        self.button_color = (0, 0, 0)
        self.text_color = (255,255,255)
        self.font = pg.font.Font("font.ttf", 48)
        
        self.rect = pg.Rect(0, 650, self.width, self.height)
        self.rect.centerx = self.screen_rect.centerx
        self.msg = msg
        self.prep_msg(self.msg)
        
    def prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def update_button(self):
        mouseX, mouseY = pg.mouse.get_pos()
        if self.rect.collidepoint(mouseX,mouseY):
            self.text_color = (0,255,0)
            self.msg_image = self.font.render(self.msg, True, self.text_color, self.button_color)
        elif not self.rect.collidepoint(mouseX,mouseY):
            self.text_color = (255,255,255)
            self.msg_image = self.font.render(self.msg, True, self.text_color, self.button_color)
    
    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
