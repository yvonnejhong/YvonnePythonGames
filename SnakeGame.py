#Snake Tutorial Python

import math
import random
from tkinter.constants import S
import pygame
import tkinter as tk
from tkinter import messagebox
LENGTH = 500
ROW = 20
SPACE = LENGTH // ROW

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y        

class Cube:
    def __init__(self, pos, color = (0, 175, 0)):
        self.pos = pos
        self.color = color      

    def draw(self, surface, eyes=False):
        rect = pygame.Rect(self.pos.x * SPACE + 1, self.pos.y * SPACE + 1, SPACE - 1, SPACE -1)
        pygame.draw.rect(surface, self.color, rect)

class Snake:
    def __init__(self, color, pos):
        self.body = []
        self.body.append(Cube(pos))
        self.dirnx = 1
        self.dirny = 0

    def move(self, keys_pressed):
        if keys_pressed[pygame.K_LEFT]:
            self.dirnx = -1
            self.dirny = 0
        elif keys_pressed[pygame.K_RIGHT]:
            self.dirnx = 1
            self.dirny = 0
        elif keys_pressed[pygame.K_DOWN]:
            self.dirnx = 0
            self.dirny = 1
        elif keys_pressed[pygame.K_UP]: 
            self.dirnx = 0
            self.dirny = -1

        head = self.body[0].pos
        head.x += self.dirnx
        head.y += self.dirny
        if head.x > ROW:
            head.x  = 0
        if head.x < 0:
            head.x = ROW
        if head.y > ROW:
            head.y  = 0
        if head.y < 0:
            head.y = ROW
            

        
    def reset(self, pos):
        pass

    def addCube(self):
        pass
        

    def draw(self, surface):
        for cube in self.body:
            cube.draw(surface)
        


def drawGrid(surface):
    for i in range(ROW):
        pygame.draw.line(surface,(0, 0, 0), (0, SPACE * i), (LENGTH, SPACE * i))
        pygame.draw.line(surface,(0, 0, 0), (SPACE * i, 0), (SPACE * i, LENGTH))
             

def redrawWindow(surface, snake):
    surface.fill((255, 255, 255))
    drawGrid(surface)
    snake.draw(surface)
    pygame.display.update()

def randomSnack(rows, item):
    pass


def message_box(subject, content):
    pass


def main():
    window = pygame.display.set_mode((LENGTH,LENGTH))
    s = Snake((0,255,0), Position(10,10))
    clock = pygame.time.Clock()
    run = True
    while run:
        #pygame.time.delay(100)
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        keys_pressed = pygame.key.get_pressed()
        s.move(keys_pressed)
        redrawWindow(window, s)       


main()