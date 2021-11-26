import pygame
import random
import os
import math
WIDTH = 1000
HEIGHT = 600
BALL_SIZE = 70

GRAVITY = 1
TIME_UNIT = 0.5

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets','Bg.jpg')),(WIDTH,HEIGHT))

def dist(pos1, pos2):
    # pos1 = (2,1)
    # pos2 = (6,4)
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)
    
    

class Ball(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load(os.path.join('Assets', 'football.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (BALL_SIZE, BALL_SIZE))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.x_speed = 3.0
        self.y_speed = 4.0
         
              
    def update(self):
        gravity = GRAVITY
        if HEIGHT - self.rect.bottom < 5:
            gravity = 0 
        dy_speed = gravity * TIME_UNIT 
        self.y_speed += dy_speed
        dx = self.x_speed * TIME_UNIT
        dy = self.y_speed * TIME_UNIT
        if self.rect.bottom + dy > HEIGHT or self.rect.top + dy < 0:          
            self.y_speed = -self.y_speed * 0.90
        if self.rect.left + dx < 0 or self.rect.right + dx > WIDTH:                 
            self.x_speed = -self.x_speed * 0.8

        dx = self.x_speed * TIME_UNIT
        dy = self.y_speed * TIME_UNIT    
        self.rect = self.rect.move(dx, dy)


spriteGroup = pygame.sprite.Group()        

def main():
    
    pygame.display.set_caption("Dropping Ball")
    window = pygame.display.set_mode((WIDTH,HEIGHT))
    clock = pygame.time.Clock()
    run = True
    spriteGroup.add(Ball((800,50)))
    spriteGroup.add(Ball((700,40)))
    spriteGroup.add(Ball((600,78)))
    spriteGroup.add(Ball((500,39)))
    spriteGroup.add(Ball((400,42)))
    
    while run:
        clock.tick(120)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        spriteGroup.update()
        window.blit(SPACE,(0,0))
        spriteGroup.draw(window)
        pygame.display.update()    

main()