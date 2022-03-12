import pygame as pg
from vector import Vector
from pygame.sprite import Sprite, Group
from copy import copy
from random import randint
from timer import CommandTimer

class Block(Sprite):
    def __init__(self,size, color, x, y):
        super().__init__()
        self.image = pg.Surface((size,size))
        self.image.fill(color)
        
        self.rect = self.image.get_rect(topleft = (x,y))

        
        
shape = [
'  xxxxxxxxx',
' xxxxxxxxxxx',
'xxxxxxxxxxxxx',
'xxxxxxxxxxxxx',
'xxxxxxxxxxxxx',
'xxxx     xxxx',
'xxx       xxx']