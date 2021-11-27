import pygame
import os
from random import randint
pygame.init()
WIDTH = 1280
HEIGHT = 780
FPS = 60 
BRICK_HEIGHT = 30
BRICK_WIDTH = 50
CITY = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'background','city.jpg')),(WIDTH,HEIGHT))

def adjust_brightness(color, value):
    #color = (r,g,b)
    r = max(min(color[0] + value, 255), 0)
    g = max(min(color[1] + value, 255), 0)
    b = max(min(color[2] + value, 255), 0)


    return (r, g, b)
    

class Brick(pygame.sprite.Sprite):
    def __init__(self, pos, color, health) -> None:
        super().__init__()
        self.pos = pos
        self.color = color
        self.health = health
        surface = pygame.Surface((BRICK_WIDTH, BRICK_HEIGHT))
        self.draw_brick(surface)
        self.image = surface
        self.rect = pygame.Rect(pos[0], pos[1], BRICK_WIDTH, BRICK_HEIGHT)
        
    def draw_brick(self, surface):  
        surface.fill(self.color)
        pygame.draw.line(surface, adjust_brightness(self.color, 100), (0, 0), (BRICK_WIDTH, 0), 5)
        pygame.draw.line(surface, adjust_brightness(self.color, 100), (0, 0), (0, BRICK_HEIGHT), 5)
        pygame.draw.line(surface, adjust_brightness(self.color, -100), (BRICK_WIDTH, 0), (BRICK_WIDTH, BRICK_HEIGHT), 5)
        pygame.draw.line(surface, adjust_brightness(self.color, -100), (0, BRICK_HEIGHT), (BRICK_WIDTH, BRICK_HEIGHT), 5)
    
pygame.display.set_caption("Brick Breaker Game")
brickGroup = pygame.sprite.Group()        

def draw_window(surface:pygame.Surface):
    surface.blit(CITY,(0,0))
    brickGroup.draw(surface)
    pygame.display.update()
    
def main():
    window = pygame.display.set_mode((WIDTH,HEIGHT))
    clock = pygame.time.Clock()
    run = True
    for r in range(7):
        color = (randint(0, 255), randint(0, 255), randint(0, 255))
        for i in range(22):
            brickGroup.add(Brick((100 + BRICK_WIDTH * i, 100 + BRICK_HEIGHT * r), color, 2))
    while run:
        clock.tick(FPS)
        brickGroup.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        draw_window(window)
    
if __name__ == "__main__":
    main()                
