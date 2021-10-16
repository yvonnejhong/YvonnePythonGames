#Snake Tutorial Python

import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox
LENGTH = 500
ROW = 20
SPACE = LENGTH // ROW
class cube:
    rows = 20
    w = 500
    def __init__(self,start,dirnx=1,dirny=0,color=(255,0,0)):
        pass
        
    def move(self, dirnx, dirny):
        pass
    
    def draw(self, surface, eyes=False):
        pass
        

class snake:
    def __init__(self, color, pos):
        pass

    def move(self):
        pass
        
    def reset(self, pos):
        pass

    def addCube(self):
        pass
        

    def draw(self, surface):
        pass


def drawGrid(surface):
    for i in range(ROW):
        pygame.draw.line(surface,(0, 0, 0), (0, SPACE * i), (LENGTH, SPACE * i))
        pygame.draw.line(surface,(0, 0, 0), (SPACE * i, 0), (SPACE * i, LENGTH))
             

def redrawWindow(surface):
    surface.fill((255, 255, 255))
    drawGrid(surface)
    pygame.display.update()


def randomSnack(rows, item):
    pass


def message_box(subject, content):
    pass


def main():
    window = pygame.display.set_mode((LENGTH,LENGTH))
    s = snake((0,255,0), (10,10))
    clock = pygame.time.Clock()
    run = True
    while run:
        pygame.time.delay(50)
        clock.tick(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        redrawWindow(window)       


main()