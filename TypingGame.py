import pygame
import os
from string import ascii_letters, ascii_lowercase, ascii_uppercase
from random import choice, randint
pygame.font.init()
pygame.mixer.init()
# 1 set window to Height = 500, Width = 900
# 2 set window caption to "Typing Game"
# 3 start a message loop, set FPS=60, quit game when receving quit event
# 4 load a space.png as background image

# 5 create an array (list) to store the characters
# 6 add a random character at random x postion into the list for every N frames
# 7 render the character use comicsans font with size = 40
# 8 increase the character images Y postion by VEL for every frame
# 9 remove the character image from the list if the Y postion is larger than the screen height
# 10 draw all the charaters images every frame

# 11 get key pressed list
# 12 remove the character if it is in the key pressed list

# 13 Create a health value, and show it on the top right corner
# 14 Create a level value, and show it on the top left corner
# 15 If the character image reached buttom, health -=1. If health = 0 the game ended.

WIDTH = 900
HEIGHT = 500
FPS = 60

N = 40
VEL = 1

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets','space.png')),(WIDTH,HEIGHT))
WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))

WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)

TYPE_NORMAL = 0
TYPE_KILLER = 1
TYPE_HEALTH = 2

CHARACTER_FONT = pygame.font.SysFont('comicsans',40)
HEALTH_FONT = pygame.font.SysFont('comicsans',50)
WINNER_TEXT = "Game Over"
WIN_FONT = pygame.font.SysFont('comicsans',100)
FINAL_SCORE_FONT = pygame.font.SysFont('comicsans',60)
LEVEL_FONT = pygame.font.SysFont('comicsans',50)
SCORE_FONT = pygame.font.SysFont('comicsans',50)

BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets',"Gun+Silencer.mp3"))
KILLER_SOUND = pygame.mixer.Sound(os.path.join('Assets',"killer.wav"))
HEALTH_SOUND = pygame.mixer.Sound(os.path.join('Assets',"health.wav"))

pygame.display.set_caption("Typing Game")

class GameContext:
    def __init__(self, health, score):
        self.health = health
        self.score = score
        
    def get_level(self):
        return int(self.score / 30) + 1

class DroppingChar:
    def __init__(self, c, x, y, type):
        self.c = c
        self.x = x
        self.y = y
        self.type = type
        if type == TYPE_HEALTH:
            self.color = GREEN
        elif type == TYPE_KILLER:
            self.color = RED
        else:
            self.color = WHITE

class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y           
        self.images = []
        for i in range(9):
            path = os.path.join('Assets','explosion',f'regularExplosion0{i}.png')
            img = pygame.image.load(path)
            img = pygame.transform.scale(img, (50,50))
            self.images.append(img)
        self.index = 0
        self.is_finished = False
        self.time = pygame.time.get_ticks()
    
    def draw(self, screen):
        screen.blit(self.images[self.index], (self.x, self.y))
        if pygame.time.get_ticks() - self.time > 50:
            self.index += 1
            self.time = pygame.time.get_ticks()

        if self.index >= 9:
            self.is_finished = True
       
def get_type():
    num = randint(0,100)
    if num >= 0 and num <= 20:
        return TYPE_KILLER
    if num >= 21 and num <= 30:
        return TYPE_HEALTH
    else:
        return TYPE_NORMAL


def main():
    run = True
    clock = pygame.time.Clock()
    character_list = []
    explosion_list = []
    frame_count =  0
    context = GameContext(5,0)
    while run:
        clock.tick(FPS)
        if frame_count % N == 0:
            c = choice(ascii_uppercase)
            character_list.append(DroppingChar(c, randint(10,WIDTH-50), 0, get_type()))
        key_press = ""
        frame_count += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                key_press = pygame.key.name(event.key)
                key_press = key_press.upper()
        handle_char(character_list, explosion_list, key_press, context)
        draw_window(character_list, explosion_list, context)
        if context.health <= 0:
            winner_text = WIN_FONT.render(WINNER_TEXT,1,WHITE)
            WINDOW.blit(winner_text,(WIDTH/2 - winner_text.get_width()/2, HEIGHT/2 - winner_text.get_height()/2))
            score_text = FINAL_SCORE_FONT.render(f"Your score is {context.score}", 1, WHITE)
            WINDOW.blit(score_text,(WIDTH/2 - score_text.get_width()/2, HEIGHT/2 - score_text.get_height()/2 + 100))
            pygame.display.update()
            pygame.time.delay(5000)
            run = False

def draw_window(character_list, explosion_list,  context):
    WINDOW.blit(SPACE,(0,0))
    health_text = HEALTH_FONT.render("Health:" + str(context.health), 1, WHITE)
    WINDOW.blit(health_text,(WIDTH - health_text.get_width() -10, 10))
    score_text = SCORE_FONT.render("Score:" + str(context.score), 1, WHITE)
    level_text = LEVEL_FONT.render("Level:" + str(context.get_level()), 1, WHITE)
    WINDOW.blit(score_text,((WIDTH - score_text.get_width()) /2 ,10))
    WINDOW.blit(level_text,(10,10))
    for dc in character_list:
        char_image = CHARACTER_FONT.render(dc.c, 1, dc.color)
        WINDOW.blit(char_image, (dc.x, dc.y))
    for e in explosion_list:
        if e.is_finished:
            explosion_list.remove(e)
        else:
            e.draw(WINDOW)

    pygame.display.update()

def handle_char(character_list, explosion_list, key_press, context):
    for dc in character_list:
        if dc.type == TYPE_KILLER:
            dc.y += VEL + context.get_level() * 1.5
        else: 
            dc.y += VEL + context.get_level() * 0.5
        if dc.y > HEIGHT:
            character_list.remove(dc)
            context.health -= 1
        elif dc.c == key_press:
            character_list.remove(dc)
            if dc.type == TYPE_KILLER:
                context.score += 5
                KILLER_SOUND.play()
                explosion_list.append(Explosion(dc.x-20, dc.y-20))
            elif dc.type == TYPE_HEALTH:
                context.health += 1
                HEALTH_SOUND.play()
            else: 
                context.score += 1 
                explosion_list.append(Explosion(dc.x-20, dc.y-20))
                BULLET_FIRE_SOUND.play()

if __name__ == "__main__":
    main()