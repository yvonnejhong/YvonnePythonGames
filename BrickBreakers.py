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

from threading import Timer
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
WHITE = (255, 255, 255)

BAR_VELOCITY = 5
BALL_VELOCITY = 3.0
TIME_UNIT = 1
bar_moving = 0

game_start = False

in_power_mode = False
power_mode_timer = None

BG = pygame.transform.scale(pygame.image.load(os.path.join('Assets','background','city.jpg')),(WIDTH,HEIGHT))
DING = pygame.mixer.Sound(os.path.join('Assets',"ding.mp3"))
DING2 = pygame.mixer.Sound(os.path.join('Assets',"ding2.mp3"))
DANG = pygame.mixer.Sound(os.path.join('Assets',"dang.mp3"))
BGM = [
    pygame.mixer.Sound(os.path.join('Assets','bgm',"Monkeys-Spinning-Monkeys.mp3")),
    pygame.mixer.Sound(os.path.join('Assets','bgm',"FastFeelBananaPeel-320bit.mp3")),
    pygame.mixer.Sound(os.path.join('Assets','bgm',"happy-clappy-ukulele.mp3"))
]

prize_font = pygame.font.SysFont(None, 25)

def adjustBrightness(color, value):
    r = max(0, min(255, color[0] + value))
    g = max(0, min(255, color[1] + value))
    b = max(0, min(255, color[2] + value))

    return (r, g, b)

brickGroup = pygame.sprite.Group()    
ballGroup = pygame.sprite.Group()    
barGroup = pygame.sprite.Group()
prizeGroup = pygame.sprite.Group()

class Prize(pygame.sprite.Sprite):
    def __init__(self, pos, color, text) -> None:
        super().__init__()
        self.color = color
        self.text = text
        
        self.rect = pygame.Rect(pos[0], pos[1], BRICK_WIDTH, BRICK_HEIGHT)
        self.image = self.drawPrize()

    
    def drawPrize(self):
        s1 = pygame.Surface((BRICK_WIDTH, BRICK_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(s1, self.color, pygame.Rect(0,0, BRICK_WIDTH, BRICK_HEIGHT), border_radius=15)
        highlight = adjustBrightness(self.color, 150)
        pygame.draw.circle(s1, highlight, (15, 15), 15, 5, False, True, False, False)
        pygame.draw.line(s1, highlight, (15,0), (BRICK_WIDTH-12, 0), 7)
        shadow = adjustBrightness(self.color, -150)
        pygame.draw.circle(s1, shadow, (BRICK_WIDTH - 15, 15), 15, 3, False, False, False, True)
        pygame.draw.line(s1, shadow, (12,BRICK_HEIGHT), (BRICK_WIDTH-15, BRICK_HEIGHT), 5)
        text = prize_font.render(self.text, 1, WHITE)
        center_x = (BRICK_WIDTH - text.get_width()) / 2
        center_y = (BRICK_HEIGHT - text.get_height()) /2
        s1.blit(text, (center_x, center_y))

        s1 =  pygame.transform.scale(s1, (BRICK_WIDTH-5, BRICK_HEIGHT-5))

        s2 = pygame.Surface((BRICK_WIDTH, BRICK_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(s2, (150,150,150), s1.get_rect().move(3,3), border_radius=15)
        s2.blit(s1, (0,0))
        return s2
    
    def update(self):
        self.rect = self.rect.move(0, 2)
        if self.rect.top > HEIGHT:
            self.kill()
        bar = pygame.sprite.spritecollideany(self, barGroup)
        if bar != None:
            self.kill()
            self.handle_effect()

    def handle_effect(self):
        if self.text == "M":
            for ball in ballGroup:
                b1 = Ball(ball.rect.center, x_speed=BALL_VELOCITY - 0.5, y_speed=ball.y_speed)
                b1.change_color('Yellow')
                ballGroup.add(b1)
                b2 = Ball(ball.rect.center, x_speed=BALL_VELOCITY + 0.5, y_speed=ball.y_speed)
                b2.change_color('Yellow')

                ballGroup.add(b2)
        elif self.text == "P":
            global in_power_mode, power_mode_timer
            in_power_mode = True    
            def timeout():
                global in_power_mode
                in_power_mode = False
            if power_mode_timer != None:
                power_mode_timer.cancel()
            power_mode_timer = Timer(10, timeout)
            power_mode_timer.start()       
                   
                   
        

class Brick(pygame.sprite.Sprite):
    def __init__(self, pos, color, health):
        super().__init__()
        self.pos = pos
        self.color = color
        self.health = health
        brickSurface = pygame.Surface((BRICK_WIDTH, BRICK_HEIGHT))
        self.image = self.drawBrick(brickSurface)
        self.rect = pygame.Rect(pos[0], pos[1], BRICK_WIDTH, BRICK_HEIGHT)
        self.is_breakable = True


    def drawBrick(self, surface):
        surface.fill(self.color)
        highlight = adjustBrightness(self.color, 150)
        pygame.draw.line(surface, highlight, (0,0), (0, BRICK_HEIGHT), 5)
        pygame.draw.line(surface, highlight, (0,0), (BRICK_WIDTH, 0), 5)
        shadow = adjustBrightness(self.color, -150)
        pygame.draw.line(surface, shadow, (0, BRICK_HEIGHT), (BRICK_WIDTH, BRICK_HEIGHT), 5)
        pygame.draw.line(surface, shadow, (BRICK_WIDTH, 0), (BRICK_WIDTH, BRICK_HEIGHT), 5)
        return surface

class NonBreakableBrick(Brick):
    def __init__(self, pos):
        super().__init__(pos, (100,100,100), 100)
        self.is_breakable = False

class Ball(pygame.sprite.Sprite):
    def __init__(self, pos, x_speed = BALL_VELOCITY, y_speed = -BALL_VELOCITY):
        super().__init__()
        self.image = pygame.image.load(os.path.join('Assets', 'Blue_ball.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.color = "Blue"
    def update(self):
        if not game_start:
            dx = bar_moving * BAR_VELOCITY
            bar = barGroup.sprites()[0]
            if dx != 0 and bar.rect.right + dx > WIDTH or bar.rect.left + dx < 0:
                dx = 0
            self.rect = self.rect.move(dx, 0)            
        else:
            if in_power_mode:
                self.change_color("Red")
            else:
                self.change_color("Blue")
            dx = self.x_speed * TIME_UNIT
            dy = self.y_speed * TIME_UNIT
            if self.rect.top + dy < 0:          
                self.y_speed = -self.y_speed 
            if self.rect.left + dx < 0 or self.rect.right + dx > WIDTH:                 
                self.x_speed = -self.x_speed
                            
            targetRect = self.rect.move(dx, dy)
            brick = pygame.sprite.spritecollideany(self, brickGroup)
            if brick != None:
                if in_power_mode:
                    brick.health = 0
                else:    
                    brick.health -= 1
                if brick.health <= 0:
                    if random.randint(0,100) < 5 and len(ballGroup) < 3 and not in_power_mode: # dropping prize
                        prizeGroup.add(Prize((brick.rect.left, brick.rect.top), RED, "P"))
                    elif random.randint(0,100) < 10 and len(ballGroup) < 5 and not in_power_mode : # dropping prize
                        prizeGroup.add(Prize((brick.rect.left, brick.rect.top), BLUE, "M"))
                    brick.kill()
                    DING2.play()
                                           
                    if not any([x for x in brickGroup if x.is_breakable]):
                        next_level()

                else:
                    DING.play()
                if not in_power_mode:    
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

    def change_color(self, color):
        if self.color == color:
            return 
        else:
            self.image = pygame.image.load(os.path.join('Assets', f'{color}_ball.png')).convert_alpha()
            self.image = pygame.transform.scale(self.image, (30, 30))
            self.color = color        

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


def redrawWindow(surface:pygame.surface.Surface):
    surface.blit(BG, (0,0))
    brickGroup.draw(surface)
    prizeGroup.draw(surface)
    ballGroup.draw(surface)
    barGroup.draw(surface)
    pygame.display.update()

def lose():
    # lost one life
    global game_start, in_power_mode
    game_start = False
    barGroup.empty()
    if power_mode_timer != None:
        power_mode_timer.cancel()
    in_power_mode = False
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
    prizeGroup.update()
    barGroup.update()

def setup_stage(level):
    if level == 0:
        for j in range(9):
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) 
            for i in range(0, 22):
                brickGroup.add(Brick((50*i + 50, 100+j*30), color, 2))
    elif level == 1:
        for j in range(9):
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) 
            for i in range(0, 22):
                if i == 11:
                    continue
                if j == 8:
                    brickGroup.add(NonBreakableBrick((50*i + 50, 100+j*30)))
                else:    
                    brickGroup.add(Brick((50*i + 50, 100+j*30), color, 2))
    elif level == 2:
        for j in range(11):
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) 
            for i in range(0, 22):
                if i == 5 or i == 15:
                    continue
                if j == 4 or j == 8:
                    brickGroup.add(NonBreakableBrick((50*i + 50, 100+j*30)))
                else:    
                    brickGroup.add(Brick((50*i + 50, 100+j*30), color, 1))

TOTAL_LEVEL = 3
def next_level():
    global level, bgm

    brickGroup.empty()
    ballGroup.empty()
    barGroup.empty()
    level = (level + 1) % TOTAL_LEVEL
    setup_stage(level)
    global game_start
    game_start = False
    ballGroup.add(Ball((600, 650)))
    barGroup.add(Bar((600, 675)))
    bgm.stop()
    bgm = BGM[random.randint(0, len(BGM)-1)]
    bgm.play(-1)

def main():
    global game_start, level, bgm
    pygame.display.set_caption("Brick Breaker")
    window = pygame.display.set_mode((WIDTH,HEIGHT))
    clock = pygame.time.Clock()
    run = True

    level = 2
    setup_stage(level)

    ballGroup.add(Ball((600, 650)))
    barGroup.add(Bar((600, 675)))

    bgm = BGM[random.randint(0, len(BGM)-1)]
    bgm.play(-1)
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if power_mode_timer != None:
                    power_mode_timer.cancel()
                run = False
        
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_SPACE]:
            game_start = True

        update(keys_pressed)
        redrawWindow(window)       

if __name__ == "__main__":
    main()