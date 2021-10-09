import pygame
import os

pygame.font.init()
pygame.mixer.init()
WIDTH = 900
HEIGHT = 500
WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))
COLOR = (255,255,255)
BLACK = (0,0,0)
YELLOW = (255,255,0)
RED = (255,0,0)
FPS = 60
BULLET_VEL = 7
VEL = 5
MAX_BULLET = 4
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets',"Grenade+1.mp3"))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets',"Gun+Silencer.mp3"))
BGM = pygame.mixer.Sound(os.path.join('Assets',"bgm.mp3"))
BORDER = pygame.Rect(WIDTH/2-5,0,10,HEIGHT)
HEALTH_FONT = pygame.font.SysFont('comicsans',40)
WINNER_FONT = pygame.font.SysFont('comicsans',100)
SPACESHIP_WIDTH,SPACESHIP_HEIGHT = (55,40)
YELLOW_SPACESHIP_IMAGE = pygame.transform.rotate(pygame.image.load(
    os.path.join('Assets','spaceship_yellow.png')), 90)
YELLOW_SPACESHIP = pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT))
RED_SPACESHIP_IMAGE = pygame.transform.rotate(pygame.image.load(
    os.path.join('Assets','spaceship_red.png')),270)
RED_SPACESHIP = pygame.transform.scale(
    RED_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT))    
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets','space.png')),(WIDTH,HEIGHT))

pygame.display.set_caption("Spaceship Game")

def handle_bullet(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            yellow_bullets.remove(bullet)
            pygame.event.post(pygame.event.Event(RED_HIT))
        if bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            red_bullets.remove(bullet)
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
        if bullet.x < 0:
            red_bullets.remove(bullet)

def handle_yellow_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL < BORDER.x - SPACESHIP_WIDTH: 
        yellow.x += VEL
 
    if keys_pressed[pygame.K_s] and yellow.y + VEL < HEIGHT - SPACESHIP_HEIGHT:
        yellow.y += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:
        yellow.y -= VEL

def handle_red_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL < WIDTH - SPACESHIP_WIDTH:
        red.x += VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL < HEIGHT - SPACESHIP_HEIGHT:
        red.y += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:
        red.y -= VEL

def draw_window(red, yellow, yellow_bullets, red_bullets, yellow_health, red_health):
    WINDOW.blit(SPACE,(0,0))
    pygame.draw.rect(WINDOW,BLACK,BORDER)
    red_health_text = HEALTH_FONT.render("Health:" + str(red_health), 1, COLOR)
    yellow_health_text = HEALTH_FONT.render("Health:" + str(yellow_health), 1, COLOR)
    WINDOW.blit(yellow_health_text,(10,10))
    WINDOW.blit(red_health_text,(WIDTH - red_health_text.get_width() -10, 10))
    WINDOW.blit(YELLOW_SPACESHIP,(yellow.x,yellow.y))
    WINDOW.blit(RED_SPACESHIP,(red.x,red.y))
    for bullet in yellow_bullets:
        pygame.draw.rect(WINDOW,YELLOW,bullet)
    for bullet in red_bullets:
        pygame.draw.rect(WINDOW,RED,bullet)
    pygame.display.update()

def display_winner(winner_msg):
    winner_text = WINNER_FONT.render(winner_msg,1,COLOR)
    WINDOW.blit(winner_text,(WIDTH/2 - winner_text.get_width()/2, HEIGHT/2 - winner_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    red = pygame.Rect(700,300,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100,300,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    run = True
    red_bullets = []
    yellow_bullets = []
    red_health = 10
    yellow_health = 10
    clock = pygame.time.Clock()
    BGM.play()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) <= MAX_BULLET:
                    bullet = pygame.Rect(yellow.x + SPACESHIP_WIDTH, yellow.y + SPACESHIP_HEIGHT/2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and len(red_bullets) <= MAX_BULLET:
                    bullet = pygame.Rect(red.x - 10, red.y + SPACESHIP_HEIGHT/2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()
        winner_msg = ""
        if red_health <= 0:
            winner_msg = "Yellow wins!"
        if yellow_health <= 0:
            winner_msg = "Red wins!"
        if winner_msg != "":
            display_winner(winner_msg)
            break 

        keys_pressed = pygame.key.get_pressed()
        handle_bullet(yellow_bullets, red_bullets,yellow,red)

        handle_yellow_movement(keys_pressed, yellow)
        handle_red_movement(keys_pressed, red)
        draw_window(red,yellow,yellow_bullets,red_bullets,yellow_health,red_health)
    main()

if __name__ == "__main__":
    main()