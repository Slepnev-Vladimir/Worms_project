import random as rnd

import tkinter as tk

import pygame as pg

root = Tk()
fr = Frame(root)
root.geometry('730x600')
canvas = Canvas(root, bg='white')
canvas.pack(fill=BOTH, expand=1)

GRAVITATION = 1                              # it is g = 9,8 in real world
WORM_ENERGY = 5
JUMP_POWER = 3

class Object():
    def __init__():
        self.x = 0
        self.y = 0
        self.Vx = 0
        self.Vy = 0
        self.rx = 0
        self.ry = 0
        self.body = pg.Rect((x - rx, y - ry, 2*rx, 2*ry))
        self.coef_drag = 0                  # a = -coef_drag * V;    a = F/m
        self.hit points = 0

    def motion(self):
        self.Vx += GRAVITATION
        self.Vx -= coef_drag * Vx
        self.Vy -= coef_drag * Vy
        self.body.move(Vx, Vy)

class Worm(Object):
    def special_charact(self):
        self.energy = WORM_ENERGY

    def jump_right(self, event):
        self.Vx += JUMP_POWER               # the energy condition is checked
        self.Vy -= JUMP_POWER               # before the call
        self.energy -= 1
        self.motion()

    def jump_left(self, event):
        self.Vx -= JUMP_POWER
        self.Vy -= JUMP_POWER
        self.energy -= 1
        self.motion()

    def jump_up(self, event):
        self.Vy -= JUMP_POWER
        self.energy -= 1
        self.motion()

    def jump_down(self, event):
        self.Vy += JUMP_POWER
        self.energy -= 1
        self.motion()


class Gun(Object):
    def special_charact(self):
        self.cos_a = 0
        self.sin_a = 0
        self.power = 0
        self.gun_type = ''

    def aim(self, event):
        # TODO: take from gun4.py and rewrite on pygame

    def shot_prepair(self, event):
        # TODO: take from gun4.py and rewrite on pygame

    def shot (self,event)
        # TODO: take from gun4.py and rewrite on pygame


class Bullet(Object):
    def special_charact(self):
        self.splesh = 0
        self.damage = 0

    def buzooka_relationships(self):
        # TODO: need to come up with

    def grenade_relationships(self):
        # TODO: need to come up with

    def rifle_relationships(self):
        # TODO: need to come up with

