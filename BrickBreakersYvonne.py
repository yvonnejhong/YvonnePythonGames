import pygame
import os
from random import randint

pygame.init()
WIDTH = 1280
HEIGHT = 760
FPS = 120 
BRICK_HEIGHT = 30
BRICK_WIDTH = 50
BALL_SIZE = 30
BAR_WIDTH = 120
BAR_HEIGHT = 20
TIME_UNIT = 0.7
BAR_VELOCITY = 6
CITY = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'background','city.jpg')),(WIDTH,HEIGHT))
bar_moving_direction = 0
pygame.display.set_caption("Brick Breaker Game")
brickGroup = pygame.sprite.Group()  
ballGroup = pygame.sprite.Group()   
barGroup = pygame.sprite.Group()  
ball_moving = False

def adjust_brightness(color, value):
    #color = (r,g,b)
    r = max(min(color[0] + value, 255), 0)
    g = max(min(color[1] + value, 255), 0)
    b = max(min(color[2] + value, 255), 0)

    return (r, g, b)

class Bar(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.color = (200, 200, 200)
        self.pos = pos
        surface = pygame.Surface((BAR_WIDTH, BAR_HEIGHT))
        self.draw_bar(surface)
        self.image = surface
        self.rect = pygame.Rect(pos[0], pos[1], BAR_WIDTH, BAR_HEIGHT)
        self.rect.center = pos
        

    def draw_bar(self, surface):  
        surface.fill(self.color)
        pygame.draw.line(surface, adjust_brightness(self.color, 100), (0, 0), (BAR_WIDTH, 0), 5)
        pygame.draw.line(surface, adjust_brightness(self.color, 100), (0, 0), (0, BAR_HEIGHT), 5)
        pygame.draw.line(surface, adjust_brightness(self.color, -100), (BAR_WIDTH, 0), (BAR_WIDTH, BAR_HEIGHT), 5)
        pygame.draw.line(surface, adjust_brightness(self.color, -100), (0, BAR_HEIGHT), (BAR_WIDTH, BAR_HEIGHT), 5)
    def update(self):
        dx =  bar_moving_direction * BAR_VELOCITY * TIME_UNIT
        if self.rect.left + dx > 0 and self.rect.right + dx < WIDTH:
           self.rect.x += dx
           
class Ball(pygame.sprite.Sprite):
    def __init__(self, pos, x_speed, y_speed):
        super().__init__()    
        self.pos = pos
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.image = pygame.image.load(os.path.join('Assets', 'blue_ball.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (BALL_SIZE, BALL_SIZE))
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def update(self):
        if ball_moving == False:
            dx =  bar_moving_direction * BAR_VELOCITY * TIME_UNIT
            if self.rect.left + dx > 0 and self.rect.right + dx < WIDTH:
                self.rect.x += dx
            return
        dx = self.x_speed * TIME_UNIT
        dy = self.y_speed * TIME_UNIT
        new_rect = self.rect.move(dx, dy)
        for bar in barGroup:
            if new_rect.colliderect(bar.rect):
                self.y_speed = - self.y_speed
                break
        for brick in brickGroup:
            if new_rect.colliderect(brick.rect):
                if brick.rect.collidepoint(new_rect.midtop):
                    self.y_speed *= -1
                if brick.rect.collidepoint(new_rect.midbottom):
                    self.y_speed *= -1
                if brick.rect.collidepoint(new_rect.midleft):
                    self.x_speed *= -1
                if brick.rect.collidepoint(new_rect.midright):
                    self.x_speed *= -1
                brick.health -= 1
                if brick.health <= 0:
                    brick.kill()
                break
        if self.rect.bottom + dy > HEIGHT or self.rect.top + dy < 0:          
            self.y_speed = -self.y_speed
        if self.rect.left + dx < 0 or self.rect.right + dx > WIDTH:                 
            self.x_speed = -self.x_speed 
            
        dx = self.x_speed * TIME_UNIT
        dy = self.y_speed * TIME_UNIT    
        self.rect = self.rect.move(dx, dy)

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
    
def draw_window(surface:pygame.Surface):
    surface.blit(CITY,(0,0))
    brickGroup.draw(surface)
    ballGroup.draw(surface)
    barGroup.draw(surface)
    pygame.display.update()
    
def main():
    window = pygame.display.set_mode((WIDTH,HEIGHT))
    clock = pygame.time.Clock()
    run = True
    for r in range(7):
        color = (randint(0, 255), randint(0, 255), randint(0, 255))
        for i in range(22):
            brickGroup.add(Brick((100 + BRICK_WIDTH * i, 100 + BRICK_HEIGHT * r), color, 1))
    ballGroup.add(Ball((650, 650),3, -3))
    barGroup.add(Bar((650, 675)))
    while run:
        clock.tick(FPS)
        brickGroup.update()
        barGroup.update()
        ballGroup.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        draw_window(window)
        keys_pressed = pygame.key.get_pressed()  
        global bar_moving_direction, ball_moving         
        if keys_pressed[pygame.K_LEFT]:
            bar_moving_direction = -1
        elif keys_pressed[pygame.K_RIGHT]: 
            bar_moving_direction = 1
        else:
            bar_moving_direction = 0
        if keys_pressed[pygame.K_SPACE]:
            ball_moving = True
        
if __name__ == "__main__":
    main()                
