import random
import pygame
import os
from position import *
from beautiful_brick import *

pygame.font.init()
pygame.mixer.init()
WIDTH = 960
HEIGHT = 720
SPACE = 30
NUM_COLUMN = 10
NUM_ROW = 20
GAME_WIDTH = SPACE * NUM_COLUMN
GAME_HEIGHT = SPACE * NUM_ROW
GAME_TOP = (HEIGHT - GAME_HEIGHT)/2
GAME_LEFT = (WIDTH - GAME_WIDTH)/2
BGM = pygame.mixer.Sound(os.path.join('Assets',"bgm","Tetris Music.mp3"))
SPACE_BG = pygame.transform.scale(pygame.image.load(os.path.join('Assets','tetris.jpg')),(WIDTH,HEIGHT))

NEXT_FONT = pygame.font.SysFont('comicsans',30)
LOSE_FONT = pygame.font.SysFont('comicsans', 100)

COLOR = (210, 210, 210)

class Tetrimino:
    def __init__(self) -> None:
        self.TOP_OFFSET = 15
        self.LEFT_OFFSET = 222
        
    def draw(self, surface):
        for block in self.blocks:
            s = create_brick(SPACE, SPACE, self.color)
            surface.blit(s, (GAME_LEFT + block.x * SPACE, GAME_TOP + block.y * SPACE))
    
    def draw_on_right(self, surface):
        for block in self.blocks:
            s = create_brick(SPACE, SPACE, self.color)
            surface.blit(s, (GAME_LEFT + self.LEFT_OFFSET + block.x * SPACE, GAME_TOP + block.y * SPACE + self.TOP_OFFSET))
               
    def draw_on_left(self, surface):
        for block in self.blocks:
            s = create_brick(SPACE, SPACE, self.color)
            surface.blit(s, (GAME_LEFT + self.LEFT_OFFSET + block.x * SPACE - GAME_WIDTH - 50 - 135, GAME_TOP + block.y * SPACE + self.TOP_OFFSET))                    
    
    def reset(self):
        self.__init__()
        
    def move_down(self, field):
        for block in self.blocks:
            if block.y + 1 >= NUM_ROW or field[block.y + 1][block.x][0] > -1: 
                return False
        for block in self.blocks:    
            block.y += 1
        return True

    def is_movable(self, field):
        for block in self.blocks:
            if block.y + 1 >= NUM_ROW or field[block.y + 1][block.x][0] > -1: 
                return False
        return True
    def move_left_or_right(self, field, direction):
        for block in self.blocks:
            if block.x + direction >= NUM_COLUMN or block.x + direction < 0 or field[block.y][block.x + direction][0] > -1:
                return False
        for block in self.blocks:
            block.x += direction
        return True
    
    def rotate(self,field):
        center = self.blocks[1]
        for block in self.blocks:
            # Step 1: move to center
            newx = block.x-center.x
            newy = block.y-center.y
       
            # Step 2: rotate
            newx2 = -newy 
            newy2 = newx
            # Step 3: move back
            newx3 = newx2 + center.x
            newy3 = newy2 + center.y
            
            if newx3 >= NUM_COLUMN or newx3 < 0  or newy3 >= NUM_ROW or \
            field[newy3][newx3][0] > -1:
                return False
        for block in self.blocks:
            # Step 1: move to center
            newx = block.x-center.x
            newy = block.y-center.y
            
            # Step 2: rotate
            #rotation matrix
            #|cosA -sinA| |x| = |xcosA - ysinA|
            #|sinA  cosA| |y|   |xsinA + ycosA|
            # when A=90 the rotation matrix becomes:
            # (x,y) => (-y, x)
            newx2 = -newy 
            newy2 = newx
            # Step 3: move back
            block.x = newx2 + center.x
            block.y = newy2 + center.y
        
            
class IBlock(Tetrimino):
    def __init__(self):
        super().__init__()
        self.blocks = [Position(4, 0), Position(4, 1), Position(4, 2), Position(4, 3)]
        self.color = (64, 202, 233)
        self.LEFT_OFFSET += 34
        self.TOP_OFFSET += 24        
class OBlock(Tetrimino):
    def __init__(self):
        super().__init__()
        self.blocks = [Position(4, 0), Position(5, 0), Position(4, 1), Position(5, 1)]
        self.color = (255, 215, 0)
        self.LEFT_OFFSET += 22
        self.TOP_OFFSET += 50
class JBlock(Tetrimino):
    def __init__(self):
        super().__init__()
        self.blocks = [Position(5, 0), Position(5, 1), Position(5, 2), Position(4, 2)]
        self.color = (101, 121, 197) 
        self.LEFT_OFFSET += 22
        self.TOP_OFFSET += 40
                    
class LBlock(Tetrimino):
    def __init__(self):
        super().__init__()
        self.blocks = [Position(4, 1), Position(4, 2), Position(4, 3), Position(5, 3)]
        self.color = (255, 179, 38)            
        self.LEFT_OFFSET += 22
        self.TOP_OFFSET += 10
                    
class SBlock(Tetrimino):
    def __init__(self):
        super().__init__()
        self.blocks = [Position(5, 0), Position(6, 0), Position(4, 1), Position(5, 1)]
        self.color = (63, 182, 62)       
        self.LEFT_OFFSET += 4
        self.TOP_OFFSET += 52
        
class ZBlock(Tetrimino):
    def __init__(self):
        super().__init__()
        self.blocks = [Position(4, 0), Position(5, 0), Position(5, 1), Position(6, 1)]
        self.color = (236, 32, 42)
        self.LEFT_OFFSET += 4
        self.TOP_OFFSET += 52
class TBlock(Tetrimino):
    def __init__(self):
        super().__init__()
        self.blocks = [Position(4, 0), Position(5, 0), Position(6, 0), Position(5, 1)]
        self.color = (181, 81, 162)
        self.LEFT_OFFSET += 6
        self.TOP_OFFSET += 54
                            
class Tetris:
    def __init__(self, surface:pygame.Surface):
        self.surface = surface
        self.field = []
        self.next_queue = []
        self.score = 0
        self.level = 0

        for _ in range(NUM_ROW):
            row = []
            for _ in range(NUM_COLUMN):
                row.append((-1,-1,-1))
            self.field.append(row)
        self.create_tetrimino() 
        self.move_down_tick = pygame.time.get_ticks()
        self.move_left_or_right_tick = pygame.time.get_ticks()
        self.rotate_tick = pygame.time.get_ticks()
        self.hard_drop_tick = pygame.time.get_ticks()
        self.fast_move_down_tick = pygame.time.get_ticks()
        self.hold_tick = pygame.time.get_ticks()
        self.hold = None
        self.swapped = False
        self.died = False 
        self.level = 0
        
    def create_tetrimino(self):
        if len(self.next_queue) < 10:
            self.next_queue += Tetrimino.__subclasses__()
            self.next_queue += Tetrimino.__subclasses__()
            random.shuffle(self.next_queue)
        self.tetrimino = self.next_queue.pop(0)()
        if self.tetrimino.is_movable(self.field) == False:
            self.died = True
        self.next_on_the_right = self.next_queue[0]()
        self.swapped = False
        
    def drawGrid(self):
        for i in range(NUM_ROW):
            pygame.draw.line(self.surface,COLOR, (GAME_LEFT, SPACE * i + GAME_TOP), (GAME_LEFT + GAME_WIDTH, SPACE * i + GAME_TOP))
        
        for i in range(NUM_COLUMN):
            pygame.draw.line(self.surface,COLOR, (GAME_LEFT + SPACE * i, GAME_TOP), (GAME_LEFT + SPACE * i, GAME_HEIGHT + GAME_TOP))

        pygame.draw.rect(self.surface, COLOR, pygame.Rect(GAME_LEFT, GAME_TOP, GAME_WIDTH, GAME_HEIGHT), 3)
        

    def update(self):
        # check key press and pass to tetrimino
        if self.died:
            return
        current_tick = pygame.time.get_ticks()
        keys_pressed = pygame.key.get_pressed()

        if current_tick - self.move_left_or_right_tick > 150:  
            self.handle_left_right_movement(keys_pressed)
            self.move_left_or_right_tick = pygame.time.get_ticks()
    
        if current_tick - self.move_down_tick > max(100, 1000 - self.level * 100):   
            self.handle_down_movement(keys_pressed)
            self.move_down_tick = pygame.time.get_ticks()
            
        if current_tick - self.rotate_tick > 125:  
            self.handle_rotate(keys_pressed)
            self.rotate_tick = pygame.time.get_ticks()
            
        if current_tick - self.hard_drop_tick > 200:  
            self.handle_hard_drop(keys_pressed)
            self.hard_drop_tick = pygame.time.get_ticks()
        
        if current_tick - self.fast_move_down_tick > 50:  
            self.handle_fast_move_down(keys_pressed)
            self.fast_move_down_tick = pygame.time.get_ticks()

        if current_tick - self.hold_tick > 100:  
            self.handle_hold(keys_pressed)
            self.hold_tick = pygame.time.get_ticks()
            
    def handle_hold(self, keys_pressed):
        if keys_pressed[pygame.K_LCTRL]:
            if self.swapped == True:
                return
            if self.hold == None:
                self.hold = self.tetrimino
                self.create_tetrimino()            
            else:
                temp = self.tetrimino
                self.tetrimino = self.hold
                self.hold = temp
            self.hold.reset()
            self.tetrimino.reset()
            self.swapped = True
        
    def handle_down_movement(self, keys_pressed):
        if self.tetrimino.move_down(self.field) == False:
            self.connect()

    def remove_lines(self):
        count = 0
        for _ in range(4):
            for i in range(NUM_ROW-1, 0, -1):
                if self.is_full_line(self.field[i]):
                    count +=1
                    self.copy_rows_above(i)
        return count
                
    def copy_rows_above(self, start_line):
        for i in range(start_line, 0, -1): 
            self.copy_one_row_above(i)
        self.initialize_first_row()
        
    def copy_one_row_above(self, i):
        for c in range(NUM_COLUMN):
            self.field[i][c] = self.field[i-1][c]
            
    def is_full_line(self, row):
        for cell in row:
            if cell == (-1, -1, -1):
                return False
        return True 
    
    def initialize_first_row(self):
        for a in range(NUM_COLUMN):
            self.field[0][a] = (-1, -1, -1)
            
    def handle_left_right_movement(self, keys_pressed):
        if keys_pressed[pygame.K_LEFT]:
            self.tetrimino.move_left_or_right(self.field, -1) 
        elif keys_pressed[pygame.K_RIGHT]:
            self.tetrimino.move_left_or_right(self.field, 1)
            
    def handle_rotate(self, keys_pressed):
        if keys_pressed[pygame.K_SPACE]:
            self.tetrimino.rotate(self.field) 
               
    def handle_hard_drop(self, keys_pressed):
        if keys_pressed[pygame.K_UP]:
            while self.tetrimino.move_down(self.field):
                pass
            self.connect()
            
    def handle_fast_move_down(self, keys_pressed):
        if keys_pressed[pygame.K_DOWN]:
           self.tetrimino.move_down(self.field)


    def connect(self):
        for block in self.tetrimino.blocks:
            self.field[block.y][block.x] = self.tetrimino.color
        count = self.remove_lines()  
        self.score += count
        self.level = self.score / 30
        self.create_tetrimino()
        
    def draw(self):
        self.surface.blit(SPACE_BG,(0,0))
        self.drawGrid()
        next_word = NEXT_FONT.render("Next:", 1, COLOR)
        self.surface.blit(next_word,(GAME_LEFT + GAME_WIDTH + 25, GAME_TOP - 15))
        hold_word = NEXT_FONT.render("Hold:", 1, COLOR)
        self.surface.blit(hold_word,(GAME_LEFT - 160,GAME_TOP - 15))
        score_word = NEXT_FONT.render("Score:" + str(self.score),  1, COLOR)
        self.surface.blit(score_word,(GAME_LEFT - 160,GAME_HEIGHT + GAME_TOP - 45 ))
        for r in range(NUM_ROW):
            for c in range(NUM_COLUMN):
                if self.field[r][c][0] > -1:
                    s = create_brick(SPACE, SPACE, self.field[r][c])
                    self.surface.blit(s, (GAME_LEFT + c * SPACE, GAME_TOP + r * SPACE))
        self.tetrimino.draw(self.surface)
        pygame.draw.rect(self.surface, COLOR, pygame.Rect(GAME_LEFT + GAME_WIDTH + 25, GAME_TOP + 30 , 135, 135), 3)
        pygame.draw.rect(self.surface, COLOR, pygame.Rect(GAME_LEFT - 160, GAME_TOP + 30 , 135, 135), 3)
        self.next_on_the_right.draw_on_right(self.surface)
        if self.hold != None:
            self.hold.draw_on_left(self.surface)
        if self.died: 
            dead_word = LOSE_FONT.render("You Died.", 1, COLOR)
            self.surface.blit(dead_word,(WIDTH/2 - dead_word.get_width()/2, HEIGHT/2 - dead_word.get_height()/2))
            BGM.stop()
        pygame.display.update()            

def main():
    pygame.display.set_caption("Tetris")
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    tetris = Tetris(window)
    clock = pygame.time.Clock()
    run = True
    BGM.play()
    while run:
        #pygame.time.delay(100)
        clock.tick(120)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        tetris.update()
        tetris.draw()    

main()