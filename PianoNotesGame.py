import pygame
import os
import random
from pygame import image
import pygame.midi

pygame.init()
pygame.fastevent.init()
event_get = pygame.fastevent.get
event_post = pygame.fastevent.post
pygame.midi.init()

WIDTH = 1200
HEIGHT = 760
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255,0, 0)

MUSICLINE_HEIGHT = 200
MUSICLINE_WIDTH = 1000

CLEF_WIDTH, CLEF_HEIGHT = 50, 100
MUSICNOTE_WIDTH, MUSICNOTE_HEIGHT = 25, 75

FONT = pygame.font.SysFont('comicsans',80)
SCORE_FONT = pygame.font.SysFont('comicsans',40)
BG = pygame.transform.scale(pygame.image.load(os.path.join('Assets','background','city.jpg')),(WIDTH,HEIGHT))


music_line_group = pygame.sprite.Group()
treble_notes_group = pygame.sprite.Group()
bass_notes_group = pygame.sprite.Group()
text_group = pygame.sprite.Group()

class GameContext:
    def __init__(self) -> None:
        self.success = 0
        self.missed = 0
        self.error = 0
        self.continues_success = 0
        self.continues_fail = 0
        self.note_speed = 0.5

    def increase_success(self):
        self.success += 1
        self.continues_success += 1
        self.continues_fail = 0

    def increase_miss(self):
        self.missed += 1
        self.continues_success = 0
        self.continues_fail += 1

    def increase_error(self):
        self.error += 1
        self.continues_success = 0
        self.continues_fail += 1

context = GameContext()

def number_to_note(number):
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    return notes[number%12]

class NoteText(pygame.sprite.Sprite):
    def __init__(self, note, correct=True) -> None:
        super().__init__()
        self.note = note
        if correct:
            self.image = FONT.render(note, True, GREEN)
        else:
            self.image = FONT.render(note, True, RED)

        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, 400)
        self.count = 50

    def update(self):
        self.count -= 1
        if self.count <= 0:
            self.kill()



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
            surface.blit(clef, (10, 40))
        else:
            clef = pygame.transform.scale(
                pygame.image.load(os.path.join('Assets','music_notes','Bass_Clef.png')).convert_alpha(),(CLEF_WIDTH,CLEF_WIDTH))
            surface.blit(clef, (10, 70))

        
        self.image_staff = surface
        self.image = surface
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        
    def update(self):
        self.notes.update()
        self.image = self.image_staff.copy()
        self.notes.draw(self.image)


class MusicNote(pygame.sprite.Sprite):
    def __init__(self, pos_x, note = 'E', octave = 0, is_treble = True) -> None:
        super().__init__()
        self.image = pygame.Surface((MUSICNOTE_WIDTH + 20, MUSICNOTE_HEIGHT), pygame.SRCALPHA)
        note_image = pygame.transform.scale(
                pygame.image.load(os.path.join('Assets','music_notes','music-notes-transparent-41.png')).convert_alpha(),(MUSICNOTE_WIDTH, MUSICNOTE_HEIGHT))
        self.image.blit(note_image, (10, 0))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.note = note
        self.is_treble = is_treble
        self.octave = octave
        self.adjust_position()
        self.frame_count = 0
    
    def adjust_octave0_treble(self):
        if self.note == 'E':
            self.rect.bottom = 143
        elif self.note == 'D':
            self.rect.bottom = 153
        elif self.note == 'F':
            self.rect.bottom = 133
        elif self.note == 'G':
            self.rect.bottom = 123            
        elif self.note == 'A':
            self.rect.bottom = 113            
        elif self.note == 'B':
            self.rect.bottom = 103            
        elif self.note == 'C':
            pygame.draw.line(self.image, BLACK, (0, MUSICNOTE_HEIGHT - 12), (MUSICNOTE_WIDTH + 20, MUSICNOTE_HEIGHT - 12), width=2)
            self.rect.bottom = 163

    def adjust_octave1_treble(self):
        self.image = pygame.transform.flip(self.image, True, True)
        if self.note == 'C':
            self.rect.top = 70
        elif self.note == 'D':
            self.rect.top = 60
        elif self.note == 'E':
            self.rect.top = 50
        elif self.note == 'F':
            self.rect.top = 40
        elif self.note == 'G':
            self.rect.top = 30            
        elif self.note == 'A':
            pygame.draw.line(self.image, BLACK, (0, 10), (MUSICNOTE_WIDTH + 20, 10), width=2)
            self.rect.top = 20            
        elif self.note == 'B':
            pygame.draw.line(self.image, BLACK, (0, 20), (MUSICNOTE_WIDTH + 20, 20), width=2)
            self.rect.top = 10            


    def adjust_octave0_bass(self):
        if self.note == 'D':
            self.rect.bottom = 103
        elif self.note == 'E':
            self.rect.bottom = 163
            pygame.draw.line(self.image, BLACK, (0, MUSICNOTE_HEIGHT - 12), (MUSICNOTE_WIDTH + 20, MUSICNOTE_HEIGHT - 12), width=2)
        elif self.note == 'F':
            self.rect.bottom = 153
        elif self.note == 'G':
            self.rect.bottom = 143            
        elif self.note == 'A':
            self.rect.bottom = 133            
        elif self.note == 'B':
            self.rect.bottom = 123            
        elif self.note == 'C':
            self.rect.bottom = 113

    def adjust_octave1_bass(self):
        self.image = pygame.transform.flip(self.image, True, True)
        if self.note == 'C':
            self.rect.top = 20
            pygame.draw.line(self.image, BLACK, (0, 10), (MUSICNOTE_WIDTH + 20, 10), width=2)
        elif self.note == 'D':
            self.rect.top = 10
            pygame.draw.line(self.image, BLACK, (0, 20), (MUSICNOTE_WIDTH + 20, 20), width=2)
        elif self.note == 'E':
            self.rect.top = 70
        elif self.note == 'F':
            self.rect.top = 60
        elif self.note == 'G':
            self.rect.top = 50            
        elif self.note == 'A':
            self.rect.top = 40            
        elif self.note == 'B':
            self.rect.top = 30   

    def adjust_position(self):
        if self.is_treble:
            if self.octave == 0:
                self.adjust_octave0_treble()
            elif self.octave == 1:
                self.adjust_octave1_treble()
        else:
            if self.octave == 0:
                self.adjust_octave0_bass()
            elif self.octave == 1:
                self.adjust_octave1_bass()

            


    def update(self):
        if context.note_speed >= 1:
            self.rect.x -= context.note_speed
        else:
            frame_needed = 1.0 / context.note_speed
            self.frame_count += 1
            if self.frame_count > frame_needed:
                self.rect.x -= 1
                self.frame_count = 0
        if self.rect.x < 50:
            self.kill()
            context.increase_miss()

def draw_window(surface:pygame.Surface):
    surface.blit(BG, (0,0))
    music_line_group.draw(surface)
    text_group.draw(surface)
    score = SCORE_FONT.render(f"Success:{context.success}  Missed:{context.missed}  Error:{context.error} C_S:{context.continues_success} C_F:{context.continues_fail}", 1, WHITE)
    surface.blit(score, (WIDTH/2 - score.get_width()/2, 700))

    pygame.display.flip()

def adjust_level():
    if context.continues_fail > 10:
        context.note_speed *= 0.8
        context.continues_fail = 0
    elif context.continues_success > 10:
        context.note_speed *= 1.2
        context.continues_success = 0

def update():
    adjust_level()
    music_line_group.update()
    text_group.update()


def main():
    input_id = pygame.midi.get_default_input_id()
    if input_id < 0:
        print("Please connect a midi keyboard to play. Quit")
        return
    
    pygame.display.set_caption("Piano Game")
    window = pygame.display.set_mode((WIDTH,HEIGHT))
    clock = pygame.time.Clock()
    run = True

    midi_input = pygame.midi.Input(input_id)
    midi_output = pygame.midi.Output(pygame.midi.get_default_output_id())

    music_line_group.add(MusicLine((100, 100), treble_notes_group))

    music_line_group.add(MusicLine((100, 400), bass_notes_group, is_treble=False))

    frame = 0
    notes = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    #notes = ['F']


    while run:
        clock.tick(FPS)
        frame += 1
        if frame > 100/context.note_speed:
            frame = 0
            treble_notes_group.add(MusicNote(1000, random.choice(notes), random.randint(0,1)))
            bass_notes_group.add(MusicNote(1000, random.choice(notes), random.randint(0,1), is_treble=False))
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
            if e.type == pygame.midi.MIDIIN:
                if e.status == 144:
                    midi_output.note_on(e.data1, e.data2)
                    note = number_to_note(e.data1)
                    if len(treble_notes_group) > 0:
                        first_note_sprite = bass_notes_group.sprites()[0]
                        if note == first_note_sprite.note:
                            text_group.add(NoteText(note))
                            first_note_sprite.kill()
                            context.increase_success()
                        else:
                            text_group.add(NoteText(note, False))
                            context.increase_error()

                if e.status == 128:
                    midi_output.note_off(e.data1, e.data2)
        
        if midi_input.poll():
            midi_events = midi_input.read(10)
            # convert them into pygame events.
            midi_evs = pygame.midi.midis2events(midi_events, midi_input.device_id)

            for m_e in midi_evs:
                event_post(m_e)

        update()
        draw_window(window)       

if __name__ == "__main__":
    main()