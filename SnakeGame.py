import random
import pygame
from tkinter import messagebox

LENGTH = 500
ROW = 20
SPACE = LENGTH // ROW

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y     
        
    def clone(self):
        return Position(self.x, self.y)

    def equals(self, other):
        return self.x == other.x and self.y == other.y

class Cube:
    def __init__(self, pos, color = (0, 175, 0), eyes=False):
        self.pos = pos
        self.color = color      
        self.eyes = eyes

    def draw(self, surface):
        rect = pygame.Rect(self.pos.x * SPACE + 1, self.pos.y * SPACE + 1, SPACE - 1, SPACE -1)
        pygame.draw.rect(surface, self.color, rect)
        if self.eyes:
            eye_rect = pygame.Rect(self.pos.x * SPACE + 1 + 5, self.pos.y * SPACE + 1 + 8, 4, 4)
            pygame.draw.rect(surface, (0,0,0), eye_rect)
            eye_rect = pygame.Rect(self.pos.x * SPACE + 1 + 13, self.pos.y * SPACE + 1 + 8, 4, 4)
            pygame.draw.rect(surface, (0,0,0), eye_rect)

class Apple(Cube):
    def __init__(self):
        super().__init__(Position(0,0), color=(255, 0, 0), eyes = False)
        self.pick_location()
    
    def pick_location(self):
        x = random.randint(0,ROW-1)
        y = random.randint(0,ROW-1)
        self.pos = Position(x,y)

class Snake:
    def __init__(self, color, pos):
        self.body = []
        self.body.append(Cube(pos.clone(), eyes=True))
        #for i in range(50):
            #self.body.append(Cube(pos.clone()))
        self.dirnx = 1
        self.dirny = 0

    def move(self, keys_pressed, apple):
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
        for i in range(len(self.body)-1, 0, -1):
            self.body[i].pos.x = self.body[i - 1].pos.x
            self.body[i].pos.y = self.body[i - 1].pos.y
            
        head = self.body[0].pos.clone()
        head.x += self.dirnx
        head.y += self.dirny

        if self.check_hit(head):
            return False

        if head.equals(apple.pos):
            self.body.append(Cube(self.body[-1].pos.clone()))
            apple.pick_location()

        self.body[0].pos = head
        if head.x >= ROW:
            head.x  = 0
        if head.x < 0:
            head.x = ROW
        if head.y >= ROW:
            head.y  = 0
        if head.y < 0:
            head.y = ROW

        return True
            
    def check_hit(self, pos):
        for cube in self.body:
            if cube.pos.equals(pos):
                return True
                
        return False

        
    def draw(self, surface):
        for cube in self.body:
            cube.draw(surface)
        
def drawGrid(surface):
    for i in range(ROW):
        pygame.draw.line(surface,(0, 0, 0), (0, SPACE * i), (LENGTH, SPACE * i))
        pygame.draw.line(surface,(0, 0, 0), (SPACE * i, 0), (SPACE * i, LENGTH))
             

def redrawWindow(surface, snake, apple):
    surface.fill((255, 255, 255))
    drawGrid(surface)
    snake.draw(surface)
    apple.draw(surface)
    pygame.display.update()


def message_box(snake):
    messagebox.showwarning('Game Over.', f'You died. Total length = {len(snake.body)}')

def main():
    pygame.display.set_caption("Snake Game")
    window = pygame.display.set_mode((LENGTH,LENGTH))
    s = Snake((0,255,0), Position(10,10))
    a = Apple()
    clock = pygame.time.Clock()
    run = True
    while run:
        #pygame.time.delay(100)
        clock.tick(15)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        keys_pressed = pygame.key.get_pressed()
        if not s.move(keys_pressed, a):
            message_box(s)
            run = False
        redrawWindow(window, s, a)       

main()