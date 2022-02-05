from dataclasses import field
import random
import pygame
import os

WIDTH = 960
HEIGHT = 720
SPACE = 30
NUM_COLUMN = 10
NUM_ROW = 20

GAME_WIDTH = NUM_COLUMN * SPACE
GAME_HEIGHT = NUM_ROW * SPACE

GAME_LEFT = (WIDTH - GAME_WIDTH) / 2
GAME_TOP = (HEIGHT - GAME_HEIGHT) / 2

OPERATION_TICK = 150

COLOR_GRID = (200, 200, 200)
COLOR_BOARD = (0, 0, 0)

def adjustBrightness(color, value):
    r = max(0, min(255, color[0] + value))
    g = max(0, min(255, color[1] + value))
    b = max(0, min(255, color[2] + value))

    return (r, g, b)

def createCell(color):
    surface = pygame.Surface((SPACE, SPACE))
    surface.fill(color)
    highlight = adjustBrightness(color, 100)
    pygame.draw.line(surface, highlight, (0,0), (0, SPACE), 3)
    pygame.draw.line(surface, highlight, (0,0), (SPACE, 0), 3)
    shadow = adjustBrightness(color, -100)
    pygame.draw.line(surface, shadow, (0, SPACE), (SPACE, SPACE), 3)
    pygame.draw.line(surface, shadow, (SPACE, 0), (SPACE, SPACE), 3)
    return surface

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y     
        
    def clone(self):
        return Position(self.x, self.y)

    def equals(self, other):
        return self.x == other.x and self.y == other.y

class Tetromino():
    def __init__(self, color):
        self.center = Position(5,0)
        self.color = color
        self.activeForm = 0


    def get_blocks(self):
        return self.forms[self.activeForm].blocks
    
    def draw(self, surface:pygame.Surface):
        form = self.forms[self.activeForm]
        for block in form.blocks:
            cell = createCell(self.color)
            surface.blit(cell,  (GAME_LEFT + block.x*SPACE, GAME_TOP+block.y*SPACE))

    
    def move_down(self, field):
        form = self.forms[self.activeForm]
        success = form.move_down(field)
        if not success:
            return False
        for index,form in enumerate(self.forms):
            if index != self.activeForm:
                form.move_down(None)
        return True

    def move_left_right(self, field, direction):
        form = self.forms[self.activeForm]
        success = form.move_left_right(field, direction)
        if not success:
            return False
        for index,form in enumerate(self.forms):
            if index != self.activeForm:
                form.move_left_right(None, direction)
        return True

    def rotate(self, field):
        newForm = (self.activeForm + 1) % len(self.forms)
        form = self.forms[newForm]
        if form.move_left_right(field, 0):
            self.activeForm = newForm
            return True
        return False
class Form:
    def __init__(self, center:Position, block1:Position, block2:Position, block3:Position) -> None:
        self.blocks = [center, block1, block2, block3]

    def move_down(self, field):
        
        for block in self.blocks:
            if block.y + 1 >= NUM_ROW:
                return False
            if field != None:
                if block.x >= 0 and block.y > 0 and field[block.x][block.y + 1] >= 0:
                    return False

        for block in self.blocks:
            block.y += 1
        
        return True

    def move_left_right(self, field, direction = 1):
        
        for block in self.blocks:
            if field != None:
                newX = block.x + direction

                if newX >=0 and newX < NUM_COLUMN and field[newX][block.y] >= 0:
                    return False
            if block.x + direction >= NUM_COLUMN or block.x + direction < 0:
                return False

        for block in self.blocks:
            block.x += direction
        
        return True


class LBlock(Tetromino):
    def __init__(self, color):
        super().__init__(color)
        c = self.center
        self.forms = [
            Form(self.center.clone(), Position(c.x+1, c.y), Position(c.x, c.y-1), Position(c.x, c.y-2)),
            Form(self.center.clone(), Position(c.x, c.y+1), Position(c.x+1, c.y), Position(c.x+2, c.y)),
            Form(self.center.clone(), Position(c.x, c.y+1), Position(c.x, c.y+2), Position(c.x-1, c.y)),
            Form(self.center.clone(), Position(c.x, c.y-1), Position(c.x-1, c.y), Position(c.x-2, c.y)),
        ]

class IBlock(Tetromino):
    def __init__(self, color):
        super().__init__(color)
        c = self.center
        self.forms = [
            Form(self.center.clone(), Position(c.x, c.y+1), Position(c.x, c.y-1), Position(c.x, c.y-2)),
            Form(self.center.clone(), Position(c.x-1, c.y), Position(c.x+1, c.y), Position(c.x+2, c.y))
        ]

class LBlock(Tetromino):
    def __init__(self, color):
        super().__init__(color)
        c = self.center
        self.forms = [
            Form(self.center.clone(), Position(c.x-1, c.y), Position(c.x, c.y-1), Position(c.x, c.y-2)),
            Form(self.center.clone(), Position(c.x, c.y-1), Position(c.x+1, c.y), Position(c.x+2, c.y)),
            Form(self.center.clone(), Position(c.x, c.y+1), Position(c.x, c.y+2), Position(c.x+1, c.y)),
            Form(self.center.clone(), Position(c.x, c.y+1), Position(c.x-1, c.y), Position(c.x-2, c.y)),
        ]

class OBlock(Tetromino):
    def __init__(self, color):
        super().__init__(color)
        c = self.center
        self.forms = [
            Form(self.center.clone(), Position(c.x-1, c.y), Position(c.x-1, c.y-1), Position(c.x, c.y-1))
        ]

class SBlock(Tetromino):
    def __init__(self, color):
        super().__init__(color)
        c = self.center
        self.forms = [
            Form(self.center.clone(), Position(c.x, c.y-1), Position(c.x-1, c.y), Position(c.x+1, c.y-1)),
            Form(self.center.clone(), Position(c.x, c.y-1), Position(c.x+1, c.y), Position(c.x+1, c.y+1))
        ]

class ZBlock(Tetromino):
    def __init__(self, color):
        super().__init__(color)
        c = self.center
        self.forms = [
            Form(self.center.clone(), Position(c.x, c.y-1), Position(c.x-1, c.y-1), Position(c.x+1, c.y)),
            Form(self.center.clone(), Position(c.x, c.y-1), Position(c.x-1, c.y), Position(c.x-1, c.y+1))
        ]

class TBlock(Tetromino):
    def __init__(self, color):
        super().__init__(color)
        c = self.center
        self.forms = [
            Form(self.center.clone(), Position(c.x-1, c.y), Position(c.x+1, c.y), Position(c.x, c.y-1)),
            Form(self.center.clone(), Position(c.x, c.y-1), Position(c.x, c.y+1), Position(c.x+1, c.y)),
            Form(self.center.clone(), Position(c.x, c.y+1), Position(c.x-1, c.y), Position(c.x+1, c.y)),
            Form(self.center.clone(), Position(c.x, c.y+1), Position(c.x, c.y-1), Position(c.x-1, c.y)),
        ]

class Tetris:
    def __init__(self, surface:pygame.Surface):
        self.surface = surface
        self.field = []
        for i in range(NUM_COLUMN):
            self.field.append([-1]*NUM_ROW)
        
        self.init_random_list()
        self.tetromino = self.create_new_tetromino()

        self.drop_tick = pygame.time.get_ticks()
        self.operation_tick = pygame.time.get_ticks()
        self.rotate_tick = pygame.time.get_ticks()
        self.weld_timeout = 3
        self.last_fast_drop = 0

    def init_random_list(self):
        # although people wants random tetromino, their intention is actually slighly different.
        # The real random value has repetition number by nature while people actually expect 
        # some random number with less repetition

        # let's hack here
        self.items = []
        for _ in range(3):
            self.items += Tetromino.__subclasses__()
        
        random.shuffle(self.items)
        # in this case, we will have max repetition of same object 3 times.

        self.item_index = 0

    def create_new_tetromino(self):
        klass = self.items[self.item_index]
        self.item_index += 1
        if self.item_index == len(self.items):
            self.init_random_list()
        return klass((0, 0, 255))

    def update(self):
        new_ticks = pygame.time.get_ticks()
        if new_ticks - self.drop_tick > 300:
            if not self.tetromino.move_down(self.field):
                self.weld_tetromino()
            self.drop_tick = new_ticks
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_LEFT]:
            if new_ticks - self.operation_tick > OPERATION_TICK:
                self.tetromino.move_left_right(self.field, -1)
                self.operation_tick = new_ticks
        if keys_pressed[pygame.K_RIGHT]:
            if new_ticks - self.operation_tick > OPERATION_TICK:
                self.tetromino.move_left_right(self.field, 1)
                self.operation_tick = new_ticks
        if keys_pressed[pygame.K_SPACE]:
            if new_ticks - self.rotate_tick > OPERATION_TICK:
                self.tetromino.rotate(self.field)
                self.rotate_tick = new_ticks
        if keys_pressed[pygame.K_DOWN]:
            if new_ticks - self.operation_tick > OPERATION_TICK / 3:
                self.drop_tick = 1
                self.operation_tick = new_ticks
        if keys_pressed[pygame.K_UP]:
            if new_ticks - self.operation_tick > OPERATION_TICK and new_ticks - self.last_fast_drop > OPERATION_TICK * 5:
                while self.tetromino.move_down(self.field):
                    pass
                self.weld_timeout = 0
                self.weld_tetromino()
                self.operation_tick = new_ticks
                self.last_fast_drop = new_ticks

    def weld_tetromino(self):
        if self.weld_timeout <= 0:
            for block in self.tetromino.get_blocks():
                if block.x >=0 and block.y >= 0:
                    self.field[block.x][block.y] = 1
            self.remove_full_line()
            self.tetromino = self.create_new_tetromino()
            self.weld_timeout = 3
        else:
            self.weld_timeout -= 1

    def remove_full_line(self):
        remove_lines = 0
        for row in range(NUM_ROW):
            count = 0
            for j in range(NUM_COLUMN):
                if self.field[j][row] >= 0:
                    count += 1
            if count == NUM_COLUMN: # a full line, remove the line
                remove_lines += 1
                for i in range(row, 0, -1):
                    for j in range(NUM_COLUMN):
                        self.field[j][i] = self.field[j][i-1]
                for j in range(NUM_COLUMN):
                    self.field[j][0] = -1        
        return remove_lines



    def draw(self):
        self.surface.fill((255, 255, 255))
        self.drawGrid()
        self.tetromino.draw(self.surface)
        pygame.display.update()     

    def drawGrid(self):
        for i in range(NUM_ROW):
            pygame.draw.line(self.surface, COLOR_GRID, (GAME_LEFT, GAME_TOP + SPACE * i), (GAME_LEFT + GAME_WIDTH, GAME_TOP + SPACE * i))
        for i in range(NUM_COLUMN):
            pygame.draw.line(self.surface, COLOR_GRID, (GAME_LEFT + SPACE * i, GAME_TOP), (GAME_LEFT + SPACE * i, GAME_TOP + GAME_HEIGHT))

        pygame.draw.rect(self.surface, COLOR_BOARD, pygame.Rect(GAME_LEFT,GAME_TOP, GAME_WIDTH, GAME_HEIGHT), 3)

        for i in range(NUM_COLUMN):
            for j in range(NUM_ROW):
                color = self.field[i][j]
                if color >= 0:
                    s = createCell(self.getColor(color))
                    self.surface.blit(s, (GAME_LEFT + i*SPACE, GAME_TOP+j*SPACE))
                    
    def getColor(self, color):
        return (255, 0, 0)



def main():
    pygame.display.set_caption("Tetris")
    window = pygame.display.set_mode((WIDTH, HEIGHT))
   
    clock = pygame.time.Clock()
    tetris = Tetris(window)
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