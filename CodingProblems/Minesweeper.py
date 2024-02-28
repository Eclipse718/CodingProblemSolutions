import pygame
import random

# Initialize Pygame
pygame.init()

# Define some colors
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Set the width and height of the screen (width, height)
size = (300, 300)
screen = pygame.display.set_mode(size)

# Set the size of the tiles
tile_size = 20

# Generate the matrix
matrix = [[' ' for _ in range(16)] for _ in range(16)]
visible = [[False for _ in range(16)] for _ in range(16)]  # Add visibility matrix

# Randomly place 40 mines
for _ in range(40):
    x, y = random.randint(0, 15), random.randint(0, 15)
    while matrix[x][y] == 'm':
        x, y = random.randint(0, 15), random.randint(0, 15)
    matrix[x][y] = 'm'

# Calculate the number of mines in adjacent squares
for x in range(16):
    for y in range(16):
        if matrix[x][y] == 'm':
            continue
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= x+i < 16 and 0 <= y+j < 16 and matrix[x+i][y+j] == 'm':
                    count += 1
        matrix[x][y] = str(count)

# Load the mine icon
mine_icon = pygame.image.load("C:/Users/bryce/OneDrive/Desktop/DataAnnotations Code/CodeTests/LeetCodeSolutions/Minesweeper/naval-mine-icon.png")
mine_icon = pygame.transform.scale(mine_icon, (tile_size, tile_size))

# Function to draw the tiles
def draw_tiles():
    for x in range(16):
        for y in range(16):
            rect = pygame.Rect(x*tile_size, y*tile_size, tile_size, tile_size)
            pygame.draw.rect(screen, GREY, rect)
            if visible[x][y] and matrix[x][y] != 'm':  # Check if tile should be revealed
                text = pygame.font.Font(None, 20).render(matrix[x][y], True, BLACK)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)
            elif visible[x][y] and matrix[x][y] == 'm':  # Check if tile is a mine
                screen.blit(mine_icon, rect)

# Function to handle the reveal of a tile
def on_reveal(x, y):
    if not visible[x][y] and matrix[x][y] != 'm':  # Check if tile should be revealed
        visible[x][y] = True  # Mark the tile as visible
        if matrix[x][y] == '0':  # If the tile is a zero, reveal all its neighbors
            for i in range(-1, 2):
                for j in range(-1, 2):
                    nx, ny = x+i, y+j
                    if 0 <= nx < 16 and 0 <= ny < 16 and not visible[nx][ny]:
                        on_reveal(nx, ny)
    elif not visible[x][y] and matrix[x][y] == 'm':  # Check if tile is a mine
        visible[x][y] = True  # Mark the tile as visible
        for x in range(16):
            for y in range(16):
                visible[x][y] = True  # Reveal all tiles

# Function to draw the grid
def draw_grid():
    for x in range(16):
        pygame.draw.line(screen, BLACK, (x*tile_size, 0), (x*tile_size, 300), 1)
        pygame.draw.line(screen, BLACK, (0, x*tile_size), (300, x*tile_size), 1)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            x //= tile_size
            y //= tile_size
            on_reveal(x, y)

    screen.fill(WHITE)
    draw_tiles()
    draw_grid()  # Ensure grid is drawn after tiles for visibility
    pygame.display.flip()

# Quit Pygame
pygame.quit()