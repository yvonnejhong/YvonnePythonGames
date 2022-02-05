import random
import pygame
import os
from position import *
from beautiful_brick import *

WIDTH = 960
HEIGHT = 720
SPACE = 30
NUM_COLUMN = 10
NUM_ROW = 20
GAME_WIDTH = SPACE * NUM_COLUMN
GAME_HEIGHT = SPACE * NUM_ROW
GAME_TOP = (HEIGHT - GAME_HEIGHT)/2
GAME_LEFT = (WIDTH - GAME_WIDTH)/2

class OBlock:
    def __init__(self):
        self.blocks = [Position(4, 0), Position(5, 0), Position(4, 1), Position(5, 1)]
        self.color = (255, 215, 0)
        
    def draw(self, surface):
        for block in self.blocks:
            s = create_brick(SPACE, SPACE, self.color)
            surface.blit(s, (GAME_LEFT + block.x * SPACE, GAME_TOP + block.y * SPACE))
            
    def move_down(self):
        for block in self.blocks:
            block.y += 1
                    
class Tetris:
    def __init__(self, surface:pygame.Surface):
        self.surface = surface
        self.field = []
        for _ in range(NUM_ROW):
            row = []
            for _ in range(NUM_COLUMN):
                row.append(-1)
            self.field.append(row)
            
        self.tetrimino = OBlock()
        

    def drawGrid(self):
        for i in range(NUM_ROW):
            pygame.draw.line(self.surface,(0, 0, 0), (GAME_LEFT, SPACE * i + GAME_TOP), (GAME_LEFT + GAME_WIDTH, SPACE * i + GAME_TOP))

        
        for i in range(NUM_COLUMN):
            pygame.draw.line(self.surface,(0, 0, 0), (GAME_LEFT + SPACE * i, GAME_TOP), (GAME_LEFT + SPACE * i, GAME_HEIGHT + GAME_TOP))

        pygame.draw.rect(self.surface, (0, 0, 0), pygame.Rect(GAME_LEFT, GAME_TOP, GAME_WIDTH, GAME_HEIGHT), 3)

    def update(self):
        self.tetrimino.move_down()
                
    def draw(self):
        self.surface.fill((255, 255, 255))
        self.drawGrid()
        for r in range(NUM_ROW):
            for c in range(NUM_COLUMN):
                if self.field[r][c] > -1:
                    s = create_brick(SPACE, SPACE, (255, 0, 0))
                    self.surface.blit(s, (GAME_LEFT + c * SPACE, GAME_TOP + r * SPACE))
        self.tetrimino.draw(self.surface)
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
        tetris.update()
        tetris.draw()    
        
main()