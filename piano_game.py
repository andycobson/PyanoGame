import pygame
import random
import mido
import threading

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Musical Side Scroller")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Font
font = pygame.font.Font(None, 36)

# Notes
NOTES = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
NOTE_TO_MIDI = {note: 60 + i for i, note in enumerate(NOTES)}

# Note class
class Note:
    def __init__(self, note, x):
        self.note = note
        self.x = x
        self.y = HEIGHT // 2 + (NOTES.index(note) - 3) * 20

    def move(self, speed):
        self.x -= speed

    def draw(self):
        text = font.render(self.note, True, BLACK)
        screen.blit(text, (self.x, self.y))

# Game variables
notes = []
score = 0
speed = 2
last_pressed_note = None

# MIDI input handling
def handle_midi_input():
    global last_pressed_note
    with mido.open_input() as inport:
        for msg in inport:
            if msg.type == 'note_on':
                midi_note = msg.note
                for note, midi_value in NOTE_TO_MIDI.items():
                    if midi_value % 12 == midi_note % 12:
                        last_pressed_note = note
                        break

# Start MIDI input thread
midi_thread = threading.Thread(target=handle_midi_input, daemon=True)
midi_thread.start()

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Check for correct note press
    if notes and last_pressed_note:
        if notes[0].note == last_pressed_note:
            score += 1
            notes.pop(0)
        else:
            score -= 1
        last_pressed_note = None

    # Generate new notes
    if len(notes) < 5 and random.random() < 0.02:
        new_note = Note(random.choice(NOTES), WIDTH)
        notes.append(new_note)

    # Move notes
    for note in notes:
        note.move(speed)

    # Remove off-screen notes
    notes = [note for note in notes if note.x > 0]

    # Draw everything
    screen.fill(WHITE)
    
    # Draw staff lines
    for i in range(5):
        pygame.draw.line(screen, BLACK, (0, HEIGHT // 2 + (i - 2) * 20), (WIDTH, HEIGHT // 2 + (i - 2) * 20))

    for note in notes:
        note.draw()

    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

# Clean up
pygame.quit()