import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH = 250
HEIGHT = 300
SQUARE_SIZE = 50

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set up the font
font = pygame.font.SysFont('Arial', 30)

# Create a 5x6 matrix of empty strings
grid = [['' for _ in range(5)] for _ in range(6)]

# Keep track of each letter's color
color_grid = [[(0, 0, 0) for _ in range(5)] for _ in range(6)]  # Default color is black

# Set up the wordle word
wordle_words = ['hedge', 'dazed', 'gyoza', 'proxy', 'djinn', 'kazoo', 'dizzy', 'foxes', 'foggy', 'squid', 'finch', 'apple', 'house', 'above', 'acids', 'admin', 'after', 'agent', 'agony', 'again', 'agile', 'ahead', 'aglow',  'aegis', 'adopt', 'acute', 'badge', 'basis', 'baths', 'basic', 'began', 'beast', 'beams', 'begin', 'cabal', 'cabin', 'canal', 'cello', 'chair', 'chalk', 'canon', 'camel', 'candy', 'calls', 'cache', 'dealt', 'decoy', 'delay', 'depot', 'desks', 'devil', 'death', 'eagle', 'enjoy', 'enter', 'elves', 'elder', 'edits', 'eaten', 'table', 'tabby', 'tacos', 'taboo', 'tapir', 'tenet', 'happy', 'hasty', 'ghoul', 'glare', 'oxide', 'ovens', 'otter', 'orbit', 'olive', 'onion']
wordle_word = random.choice(wordle_words)

# Set up the current row and column
current_row = 0
current_col = 0

# Flag to track if the word has been guessed correctly
word_guessed = False

def handle_keydown(event):
    global current_row, current_col, grid, color_grid, word_guessed
    if event.key == pygame.K_BACKSPACE:
        if current_col > 0 and not word_guessed:
            current_col -= 1
            grid[current_row][current_col] = ''
            color_grid[current_row][current_col] = (0, 0, 0)  # Reset color to black
    elif event.key == pygame.K_RETURN:
        if current_col == 5 and not word_guessed:
            # Check and color the row
            check_and_color_row(current_row)
            if grid[current_row] == list(wordle_word):  # Check if the word was guessed correctly
                word_guessed = True
            elif current_row == 5:  # Check if we're on the last row
                print("Sorry, the word was", wordle_word)
                running = False  # End the game
            if current_row < 5:  # Ensure we don't go beyond the grid
                current_row += 1
            current_col = 0
    elif event.key >= pygame.K_a and event.key <= pygame.K_z and not word_guessed:
        if current_col < 5:
            grid[current_row][current_col] = chr(event.key)
            # Do not color the letter here; it will be colored when the row is checked
            current_col += 1

def check_and_color_row(row):
    global wordle_word, grid, color_grid
    user_word = ''.join(grid[row])
    for i in range(5):
        if user_word[i] == wordle_word[i]:
            color_grid[row][i] = (0, 255, 0)  # Green for correct position
        elif user_word[i] in wordle_word:
            color_grid[row][i] = (255, 165, 0)  # Orange for correct letter, wrong position
        else:
            color_grid[row][i] = (255, 0, 0)  # Red for incorrect letter

# Set up the event loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            handle_keydown(event)

    # Draw the grid
    screen.fill((255, 255, 255))
    for i in range(6):
        for j in range(5):
            letter = grid[i][j]
            color = color_grid[i][j]  # Use the color from the color grid
            text = font.render(letter.upper() if letter else '_', True, color)
            text_rect = text.get_rect(center=(j * SQUARE_SIZE + SQUARE_SIZE // 2, i * SQUARE_SIZE + SQUARE_SIZE // 2))
            screen.blit(text, text_rect)
            pygame.draw.rect(screen, (0, 0, 0), (j * SQUARE_SIZE, i * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 2)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()