import random
import pygame
import os

WIDTH = 960
HEIGHT = 720
SPACE = 30
VERTICAL_ROW = 10
HORIZONTAL_ROW = 20



def draw(self, surface):
    rect = pygame.Rect(self.pos.x * SPACE + 1, self.pos.y * SPACE + 1, SPACE - 1, SPACE -1)
    pygame.draw.rect(surface, self.color, rect)
    if self.eyes:
        eye_rect = pygame.Rect(self.pos.x * SPACE + 1 + 5, self.pos.y * SPACE + 1 + 8, 4, 4)
        pygame.draw.rect(surface, (0,0,0), eye_rect)
        eye_rect = pygame.Rect(self.pos.x * SPACE + 1 + 13, self.pos.y * SPACE + 1 + 8, 4, 4)
        pygame.draw.rect(surface, (0,0,0), eye_rect)

def drawGrid(surface):
    for i in range(HORIZONTAL_ROW):
        pygame.draw.line(surface,(0, 0, 0), (0, SPACE * i), (HEIGHT, SPACE * i))
        #pygame.draw.line(surface,(0, 0, 0), (SPACE * i, 0), (SPACE * i, HEIGHT))

    for i in range(VERTICAL_ROW):
        #pygame.draw.line(surface,(0, 0, 0), (0, SPACE * i), (WIDTH, SPACE * i))
        pygame.draw.line(surface,(0, 0, 0), (SPACE * i, 0), (SPACE * i, WIDTH))

def redrawWindow(surface):
    surface.fill((255, 255, 255))
    drawGrid(surface)
    pygame.display.update()            

def main():
    pygame.display.set_caption("Tetris")
    window = pygame.display.set_mode((WIDTH, HEIGHT))
   
    clock = pygame.time.Clock()
    run = True
    while run:
        #pygame.time.delay(100)
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        redrawWindow(window)      
        
main()