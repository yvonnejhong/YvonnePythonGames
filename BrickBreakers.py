# Monkeys Spinning Monkeys Kevin MacLeod (incompetech.com)
# Licensed under Creative Commons: By Attribution 3.0 License
# http://creativecommons.org/licenses/by/3.0/
# Music promoted by https://www.chosic.com/free-music/all/

# Fast Feel Banana Peel by Alexander Nakarada | https://www.serpentsoundstudios.com
# Music promoted on https://www.chosic.com/free-music/all/
# Creative Commons Attribution 4.0 International (CC BY 4.0)
# https://creativecommons.org/licenses/by/4.0/

# Music: Happy Clappy Ukulele by Shane Ivers - https://www.silvermansound.com
# Licensed under Creative Commons Attribution 4.0 International License
# https://creativecommons.org/licenses/by/4.0/
# Music promoted by https://www.chosic.com/free-music/all/


import pygame
import os
import random

pygame.init()

WIDTH = 1200
HEIGHT = 760
FPS = 120

BRICK_WIDTH, BRICK_HEIGHT = 50, 30
BAR_WIDTH = 120
BAR_HEIGHT = 20
RED = (255, 0, 0)
BLUE = (0, 0, 255)

BAR_VELOCITY = 5
BALL_VELOCITY = 3
TIME_UNIT = 1
bar_moving = 0

game_start = False

BG = pygame.transform.scale(pygame.image.load(os.path.join('Assets','background','city.jpg')),(WIDTH,HEIGHT))
DING = pygame.mixer.Sound(os.path.join('Assets',"ding.mp3"))
DING2 = pygame.mixer.Sound(os.path.join('Assets',"ding2.mp3"))
DANG = pygame.mixer.Sound(os.path.join('Assets',"dang.mp3"))
BGM = [
    pygame.mixer.Sound(os.path.join('Assets','bgm',"Monkeys-Spinning-Monkeys.mp3")),
    pygame.mixer.Sound(os.path.join('Assets','bgm',"FastFeelBananaPeel-320bit.mp3")),
    pygame.mixer.Sound(os.path.join('Assets','bgm',"happy-clappy-ukulele.mp3"))
]

def adjustBrightness(color, value):
    r = max(0, min(255, color[0] + value))
    g = max(0, min(255, color[1] + value))
    b = max(0, min(255, color[2] + value))

    return (r, g, b)

class Brick(pygame.sprite.Sprite):
    def __init__(self, pos, color, health):
        super().__init__()
        self.pos = pos
        self.color = color
        self.health = health
        brickSurface = pygame.Surface((BRICK_WIDTH, BRICK_HEIGHT))
        self.image = self.drawBrick(brickSurface)
        self.rect = pygame.Rect(pos[0], pos[1], BRICK_WIDTH, BRICK_HEIGHT)


    def drawBrick(self, surface):
        surface.fill(self.color)
        highlight = adjustBrightness(self.color, 150)
        pygame.draw.line(surface, highlight, (0,0), (0, BRICK_HEIGHT), 5)
        pygame.draw.line(surface, highlight, (0,0), (BRICK_WIDTH, 0), 5)
        shadow = adjustBrightness(self.color, -150)
        pygame.draw.line(surface, shadow, (0, BRICK_HEIGHT), (BRICK_WIDTH, BRICK_HEIGHT), 5)
        pygame.draw.line(surface, shadow, (BRICK_WIDTH, 0), (BRICK_WIDTH, BRICK_HEIGHT), 5)
        return surface


class Ball(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load(os.path.join('Assets', 'Blue_ball.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.x_speed = BALL_VELOCITY
        self.y_speed = -BALL_VELOCITY

    def update(self):
        if not game_start:
            dx = bar_moving * BAR_VELOCITY
            bar = barGroup.sprites()[0]
            if dx != 0 and bar.rect.right + dx > WIDTH or bar.rect.left + dx < 0:
                dx = 0
            self.rect = self.rect.move(dx, 0)            
        else:
            dx = self.x_speed * TIME_UNIT
            dy = self.y_speed * TIME_UNIT
            if self.rect.top + dy < 0:          
                self.y_speed = -self.y_speed 
            if self.rect.left + dx < 0 or self.rect.right + dx > WIDTH:                 
                self.x_speed = -self.x_speed

            targetRect = self.rect.move(dx, dy)
            brick = pygame.sprite.spritecollideany(self, brickGroup)
            if brick != None:
                brick.health -= 1
                if brick.health <= 0:
                    brick.kill()
                    DING2.play()
                else:
                    DING.play()
                    
                if (self.x_speed > 0 and brick.rect.collidepoint(targetRect.midright)) or (self.x_speed < 0 and brick.rect.collidepoint(targetRect.midleft)): # left/right
                    self.x_speed = -self.x_speed 
                    self.y_speed = self.y_speed * (1 + (random.random()-0.5)*0.1)
                if (self.y_speed > 0 and brick.rect.collidepoint(targetRect.midbottom)) or (self.y_speed < 0 and brick.rect.collidepoint(targetRect.midtop)): # up/down
                    self.x_speed = self.x_speed * (1 + (random.random()-0.5)*0.1)
                    self.y_speed = -self.y_speed
                       
            
            for bar in barGroup:
                if targetRect.colliderect(bar):
                    self.x_speed = self.x_speed * (1 + (random.random()-0.5)*0.1)
                    self.y_speed = -self.y_speed
                    DANG.play()

            if self.rect.bottom + dy > HEIGHT:
                self.kill()
                if len(ballGroup) == 0:
                    lose()

            dx = self.x_speed * TIME_UNIT
            dy = self.y_speed * TIME_UNIT    
            self.rect = self.rect.move(dx, dy)

class Bar(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.color = (200, 200, 200)
        barSurface = pygame.Surface((BAR_WIDTH, BAR_HEIGHT))
        self.image = self.drawBar(barSurface)
        self.rect = pygame.Rect(pos[0], pos[1], BAR_WIDTH, BAR_HEIGHT)
        self.rect.center = pos

    def drawBar(self, surface):
        surface.fill(self.color)
        highlight = adjustBrightness(self.color, 150)
        pygame.draw.line(surface, highlight, (0,0), (0, BAR_HEIGHT), 5)
        pygame.draw.line(surface, highlight, (0,0), (BAR_WIDTH, 0), 5)
        shadow = adjustBrightness(self.color, -150)
        pygame.draw.line(surface, shadow, (0, BAR_HEIGHT), (BAR_WIDTH, BAR_HEIGHT), 5)
        pygame.draw.line(surface, shadow, (BAR_WIDTH, 0), (BAR_WIDTH, BAR_HEIGHT), 5)
        return surface
    
    def update(self):
        dx = bar_moving * BAR_VELOCITY
        if dx != 0 and self.rect.right + dx > WIDTH or self.rect.left + dx < 0:
            dx = 0
        self.rect = self.rect.move(dx, 0)

brickGroup = pygame.sprite.Group()    
ballGroup = pygame.sprite.Group()    
barGroup = pygame.sprite.Group()

def redrawWindow(surface:pygame.surface.Surface):
    surface.blit(BG, (0,0))
    brickGroup.draw(surface)
    ballGroup.draw(surface)
    barGroup.draw(surface)
    pygame.display.update()

def lose():
    # lost one life
    global game_start
    game_start = False
    barGroup.empty()
    ballGroup.add(Ball((600, 650)))
    barGroup.add(Bar((600, 675)))

def update(key_pressed):

    global bar_moving
    if key_pressed[pygame.K_LEFT]:
        bar_moving = -1
    elif key_pressed[pygame.K_RIGHT]:
        bar_moving = 1
    else:
        bar_moving = 0

    brickGroup.update()
    ballGroup.update()
    barGroup.update()


def main():
    global game_start
    pygame.display.set_caption("Brick Breaker")
    window = pygame.display.set_mode((WIDTH,HEIGHT))
    clock = pygame.time.Clock()
    run = True
    for j in range(7):
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) 
        for i in range(1, 21):
            brickGroup.add(Brick((50*i + 50, 100+j*30), color, 2))
    ballGroup.add(Ball((600, 650)))
    barGroup.add(Bar((600, 675)))
    BGM[random.randint(0, len(BGM)-1)].play(-1)
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_SPACE]:
            game_start = True

        update(keys_pressed)
        redrawWindow(window)       

if __name__ == "__main__":
    main()