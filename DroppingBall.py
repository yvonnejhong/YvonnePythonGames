import pygame
import random
import os
WIDTH = 800
HEIGHT = 600
BALL_SIZE = 70

GRAVITY = 1
TIME_UNIT = 0.25

def rot_center(image, angle, x, y):
    
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)

    return rotated_image, new_rect

class Ball(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load(os.path.join('Assets', 'football.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (BALL_SIZE, BALL_SIZE))
        self.original = self.image
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.angle = 0
        self.x_speed = random.randint(-20,20)
        self.y_speed = 0

    def update(self):

        self.angle = (self.angle + 2) % 360
        self.image, self.rect = rot_center(self.original, self.angle, self.rect.center[0], self.rect.center[1]) 

        self.y_speed += GRAVITY * TIME_UNIT

        dy = self.y_speed * TIME_UNIT
        dx = self.x_speed * TIME_UNIT

        if self.rect.right + dx > WIDTH or self.rect.left + dx < 0:
            self.x_speed = -self.x_speed * 0.9

        if self.rect.bottom + dy > HEIGHT:
            self.y_speed = -self.y_speed * 0.9

        dy = self.y_speed * TIME_UNIT
        dx = self.x_speed * TIME_UNIT

        self.rect = self.rect.move(dx, dy)
        


    

spriteGroup = pygame.sprite.Group()        

def redrawWindow(surface:pygame.Surface):
    surface.fill((150,150,150))
    spriteGroup.draw(surface)
    pygame.display.update()
    



def main():
    
    pygame.display.set_caption("Dropping Ball")
    window = pygame.display.set_mode((WIDTH,HEIGHT))
    clock = pygame.time.Clock()
    run = True
    spriteGroup.add(Ball((100,100)))
    while run:
        clock.tick(120)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        spriteGroup.update()
        redrawWindow(window)       

main()