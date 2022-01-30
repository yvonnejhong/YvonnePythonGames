import random
import pygame
import os

WIDTH = 960
HEIGHT = 720
SPACE = 30
NUM_COLUMN = 10
NUM_ROW = 20
GAME_WIDTH = SPACE * NUM_COLUMN
GAME_HEIGHT = SPACE * NUM_ROW
GAME_TOP = (HEIGHT - GAME_HEIGHT)/2
GAME_LEFT = (WIDTH - GAME_WIDTH)/2

class Tetris:
    def __init__(self, surface):
        self.surface = surface
        self.field = []
        for _ in range(NUM_ROW):
            row = []
            for _ in range(NUM_COLUMN):
                row.append(-1)
            self.field.append(row)
            
        self.field[4][3] = 1
        self.field[4][4] = 1
        

    def drawGrid(self):
        for i in range(NUM_ROW):
            pygame.draw.line(self.surface,(0, 0, 0), (GAME_LEFT, SPACE * i + GAME_TOP), (GAME_LEFT + GAME_WIDTH, SPACE * i + GAME_TOP))

        for i in range(NUM_COLUMN):
            pygame.draw.line(self.surface,(0, 0, 0), (GAME_LEFT + SPACE * i, GAME_TOP), (GAME_LEFT + SPACE * i, GAME_HEIGHT + GAME_TOP))

        pygame.draw.rect(self.surface, (0, 0, 0), pygame.Rect(GAME_LEFT, GAME_TOP, GAME_WIDTH, GAME_HEIGHT), 3)
        
    def draw(self):
        self.surface.fill((255, 255, 255))
        self.drawGrid()
        for i in range(NUM_ROW):
            for j in range(NUM_COLUMN):
                if self.field[i][j] > -1:
                    pygame.draw.rect(self.surface, (255,0,0), pygame.Rect(GAME_LEFT + j * SPACE, GAME_TOP + i * SPACE, SPACE, SPACE))
        pygame.display.update()            

def main():
    pygame.display.set_caption("Tetris")
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    tetris = Tetris(window)
    clock = pygame.time.Clock()
    run = True
    while run:
        #pygame.time.delay(100)
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        tetris.draw()    
        
main()