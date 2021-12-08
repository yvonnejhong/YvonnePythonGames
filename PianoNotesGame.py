import pygame
import os
import random
from pygame import image
import pygame.midi

pygame.init()

WIDTH = 1200
HEIGHT = 760
FPS = 120
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

MUSICLINE_HEIGHT = 200
MUSICLINE_WIDTH = 1000

CLEF_WIDTH, CLEF_HEIGHT = 50, 100
MUSICNOTE_WIDTH, MUSICNOTE_HEIGHT = 25, 75

note_speed = 1
music_line_group = pygame.sprite.Group()
notes_group = pygame.sprite.Group()
class MusicLine(pygame.sprite.Sprite):
    def __init__(self, pos, notes_group, is_treble = True) -> None:
        super().__init__()
        surface = pygame.Surface((MUSICLINE_WIDTH, MUSICLINE_HEIGHT), pygame.SRCALPHA)
        self.notes = notes_group
        for i in range(5):
            pygame.draw.line(surface, BLACK, (0, 50+i*20), (MUSICLINE_WIDTH, 50+i*20))

        if is_treble:
            clef = pygame.transform.scale(
                pygame.image.load(os.path.join('Assets','music_notes','treble_Clef.png')).convert_alpha(),(CLEF_WIDTH,CLEF_HEIGHT))
        else:
            clef = pygame.transform.scale(
                pygame.image.load(os.path.join('Assets','music_notes','Bass_Clef.png')).convert_alpha(),(CLEF_WIDTH,CLEF_HEIGHT))

        surface.blit(clef, (10, 40))
        self.image_staff = surface
        self.image = surface
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        
    def update(self):
        self.notes.update()
        self.image = self.image_staff.copy()
        self.notes.draw(self.image)


class MusicNote(pygame.sprite.Sprite):
    def __init__(self, pos_x, note = 'E', is_treble = True) -> None:
        super().__init__()
        self.image = pygame.Surface((MUSICNOTE_WIDTH + 20, MUSICNOTE_HEIGHT), pygame.SRCALPHA)
        note_image = pygame.transform.scale(
                pygame.image.load(os.path.join('Assets','music_notes','music-notes-transparent-41.png')).convert_alpha(),(MUSICNOTE_WIDTH, MUSICNOTE_HEIGHT))
        self.image.blit(note_image, (10, 0))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.note = note
        self.is_treble = is_treble
        self.adjust_position()
    
    def adjust_position(self):
        if self.note == 'E':
            self.rect.bottom = 143
        elif self.note == 'D':
            self.rect.bottom = 133
        elif self.note == 'F':
            self.rect.bottom = 153
        elif self.note == 'G':
            self.rect.bottom = 123            
        elif self.note == 'A':
            self.rect.bottom = 113            
        elif self.note == 'B':
            self.rect.bottom = 103            
        elif self.note == 'C':
            pygame.draw.line(self.image, BLACK, (0, MUSICNOTE_HEIGHT - 12), (MUSICNOTE_WIDTH + 20, MUSICNOTE_HEIGHT - 12), width=2)
            self.rect.bottom = 163
            


    def update(self):
        global note_speed
        self.rect.x -= note_speed
        if self.rect.x < 50:
            self.kill()

def draw_window(surface):
    surface.fill(WHITE)
    music_line_group.draw(surface)
    
    pygame.display.flip()

def update():
    music_line_group.update()



def main():
    
    pygame.display.set_caption("Piano Game")
    window = pygame.display.set_mode((WIDTH,HEIGHT))
    clock = pygame.time.Clock()
    run = True

    music_line_group.add(MusicLine((100, 100), notes_group))
    notes_group.add(MusicNote(850, 'C'))
    notes_group.add(MusicNote(900, 'E'))
    notes_group.add(MusicNote(940, 'D'))
    notes_group.add(MusicNote(980, 'F'))
    notes_group.add(MusicNote(820, 'G'))
    notes_group.add(MusicNote(780, 'A'))
    notes_group.add(MusicNote(740, 'B'))
    level = 2

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        

        update()
        draw_window(window)       

if __name__ == "__main__":
    main()