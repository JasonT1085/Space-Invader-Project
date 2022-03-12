import sys
import pygame as pg
from vector import Vector
from laser import Laser
from random import randint
from time import sleep

LEFT, RIGHT, UP, DOWN, STOP = 'left', 'right', 'up', 'down', 'stop'

dirs = {LEFT: Vector(-1, 0),
        RIGHT: Vector(1, 0),
        UP: Vector(0, -1),
        DOWN: Vector(0, 1),
        STOP: Vector(0, 0)}

dir_keys = {pg.K_LEFT: LEFT, pg.K_a: LEFT,
            pg.K_RIGHT: RIGHT, pg.K_d: RIGHT,
            pg.K_UP: UP, pg.K_w: UP,
            pg.K_DOWN: DOWN, pg.K_s: DOWN}

def reset():
    pg.event.clear()

def check_events(game):
    UFO_SPAWNTIME = pg.USEREVENT + 1
    pg.time.set_timer(UFO_SPAWNTIME, 5000)
    ship = game.ship
    ALIENLASER = pg.USEREVENT + 1
    pg.time.set_timer(ALIENLASER, 10000)
    UFOLASER = pg.USEREVENT + 1
    pg.time.set_timer(UFOLASER, 2500)
    
    laserEffect = pg.mixer.Sound("shoot.mp3")
    laserEffect.set_volume(0.2)
    for e in pg.event.get():
        if e.type == pg.QUIT:
            sys.exit()
        if e.type == UFOLASER:
            game.lasers.ufo_shoot()
            pg.mixer.Channel(6).play(laserEffect)
        if e.type == UFO_SPAWNTIME and randint(1,10) == 1 and len(game.ufo.ufo) == 0:
            game.ufo.resetTimer = True
        if e.type == ALIENLASER and randint(1,2) == 1:
            game.lasers.alien_shoot()
            laserEffect.play()
        elif e.type == pg.KEYDOWN:
            if e.key in dir_keys:
                v = dirs[dir_keys[e.key]]
                ship.inc_add(v)
            elif e.key == pg.K_SPACE:
              game.lasers.fire()
              laserEffect.play()
        elif e.type == pg.KEYUP:
            if e.key in dir_keys:
                v = dirs[dir_keys[e.key]]
                ship.inc_add(-v)
