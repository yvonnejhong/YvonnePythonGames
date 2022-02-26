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

class Tetrimino:
    def draw(self, surface):
        for block in self.blocks:
            s = create_brick(SPACE, SPACE, self.color)
            surface.blit(s, (GAME_LEFT + block.x * SPACE, GAME_TOP + block.y * SPACE))
            
    def move_down(self, field):
        for block in self.blocks:
            if block.y + 1 >= NUM_ROW or field[block.y + 1][block.x][0] > -1: 
                return False
        for block in self.blocks:    
            block.y += 1
        return True
    
    def move_left_or_right(self, field, direction):
        for block in self.blocks:
            if block.x + direction >= NUM_COLUMN or block.x + direction < 0 or field[block.y][block.x + direction][0] > -1:
                return False
        for block in self.blocks:
            block.x += direction
        return True

class IBlock(Tetrimino):
    def __init__(self):
        self.blocks = [Position(4, 0), Position(4, 1), Position(4, 2), Position(4, 3)]
        self.color = (64, 202, 233)
        
class OBlock(Tetrimino):
    def __init__(self):
        self.blocks = [Position(4, 0), Position(5, 0), Position(4, 1), Position(5, 1)]
        self.color = (255, 215, 0)
        
class JBlock(Tetrimino):
    def __init__(self):
        self.blocks = [Position(5, 0), Position(5, 1), Position(5, 2), Position(4, 2)]
        self.color = (101, 121, 197) 
            
class LBlock(Tetrimino):
    def __init__(self):
        self.blocks = [Position(4, 0), Position(4, 1), Position(4, 2), Position(5, 2)]
        self.color = (255, 179, 38)            
            
class Tetris:
    def __init__(self, surface:pygame.Surface):
        self.surface = surface
        self.field = []
        self.next_queue = []
       
        for _ in range(NUM_ROW):
            row = []
            for _ in range(NUM_COLUMN):
                row.append((-1,-1,-1))
            self.field.append(row)
        self.create_tetrimino() 
        self.move_down_tick = pygame.time.get_ticks()
        self.move_left_or_right_tick = pygame.time.get_ticks()
        

    def create_tetrimino(self):
        if len(self.next_queue) == 0:
            self.next_queue += Tetrimino.__subclasses__()
            self.next_queue += Tetrimino.__subclasses__()
            random.shuffle(self.next_queue)
        self.tetrimino = self.next_queue.pop(0)()

    def drawGrid(self):
        for i in range(NUM_ROW):
            pygame.draw.line(self.surface,(0, 0, 0), (GAME_LEFT, SPACE * i + GAME_TOP), (GAME_LEFT + GAME_WIDTH, SPACE * i + GAME_TOP))

        
        for i in range(NUM_COLUMN):
            pygame.draw.line(self.surface,(0, 0, 0), (GAME_LEFT + SPACE * i, GAME_TOP), (GAME_LEFT + SPACE * i, GAME_HEIGHT + GAME_TOP))

        pygame.draw.rect(self.surface, (0, 0, 0), pygame.Rect(GAME_LEFT, GAME_TOP, GAME_WIDTH, GAME_HEIGHT), 3)

    def update(self):
        # check key press and pass to tetrimino
        
        current_tick = pygame.time.get_ticks()
        if current_tick - self.move_left_or_right_tick > 100:  
            self.handle_left_right_movement()
            self.move_left_or_right_tick = current_tick
    
        if current_tick - self.move_down_tick > 150:   
            self.handle_down_movement()
            self.move_down_tick = current_tick

    def handle_down_movement(self):
        if self.tetrimino.move_down(self.field) == False:
            for block in self.tetrimino.blocks:
                self.field[block.y][block.x] = self.tetrimino.color  
            self.create_tetrimino()

    def handle_left_right_movement(self):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_LEFT]:
            self.tetrimino.move_left_or_right(self.field, -1) 
        elif keys_pressed[pygame.K_RIGHT]:
            self.tetrimino.move_left_or_right(self.field, 1)
            
    def draw(self):
        self.surface.fill((255, 255, 255))
        self.drawGrid()
        for r in range(NUM_ROW):
            for c in range(NUM_COLUMN):
                if self.field[r][c][0] > -1:
                    s = create_brick(SPACE, SPACE, self.field[r][c])
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
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        tetris.update()
        tetris.draw()    

main()