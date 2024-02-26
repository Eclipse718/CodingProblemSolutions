import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 540, 540
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
FONT = pygame.font.Font(None, 36)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Sudoku board to display
board = [
    ["5", "3", ".", ".", "7", ".", ".", ".", "."],
    ["6", ".", ".", "1", "9", "5", ".", ".", "."],
    [".", "9", "8", ".", ".", ".", ".", "6", "."],
    ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
    ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
    ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
    [".", "6", ".", ".", ".", ".", "2", "8", "."],
    [".", ".", ".", "4", "1", "9", ".", ".", "5"],
    [".", ".", ".", ".", "8", ".", ".", "7", "9"]
]

# Keep track of the original numbers
original_numbers = [[(i, j) for j in range(9) if board[i][j] != "."] for i in range(9)]

def valid(board, num, pos):
    # Check row
    for i in range(len(board[0])):
        if board[pos[0]][i] == str(num) and pos[1] != i:
            return False

    # Check column
    for i in range(len(board)):
        if board[i][pos[1]] == str(num) and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if board[i][j] == str(num) and (i,j) != pos:
                return False

    return True

def find_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == ".":
                return (i, j)  # row, col
    return None

def draw_line(x1, y1, x2, y2, color, thickness):
    pygame.draw.line(screen, color, (x1, y1), (x2, y2), thickness)

def draw_number(x, y, number, color):
    text = FONT.render(number, True, color)
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)

def draw_board():
    screen.fill(WHITE)
    for i in range(1, 9):
        draw_line(i*60, 0, i*60, HEIGHT, BLACK, 2)
        draw_line(0, i*60, WIDTH, i*60, BLACK, 2)
    draw_line(180, 0, 180, HEIGHT, BLACK, 4)
    draw_line(360, 0, 360, HEIGHT, BLACK, 4)
    draw_line(0, 180, WIDTH, 180, BLACK, 4)
    draw_line(0, 360, WIDTH, 360, BLACK, 4)
    for i in range(9):
        for j in range(9):
            number = board[i][j]
            if number != ".":
                color = BLACK if (i, j) in original_numbers[i] else RED
                draw_number(j*60+30, i*60+30, number, color)
    pygame.display.flip()

def solve_sudoku(board):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    find = find_empty(board)
    if not find:
        for i in range(9):
            for j in range(9):
                if board[i][j] != ".":
                    draw_number(j*60+30, i*60+30, board[i][j], BLACK)  # Redraw all numbers in black
        return True
    else:
        row, col = find

    for i in range(1, 10):
        if valid(board, i, (row, col)):
            board[row][col] = str(i)
            draw_board()
            pygame.time.delay(10)  # Delay for visual effect
            if solve_sudoku(board):
                return True
            board[row][col] = "."
            draw_board()
    return False

# Main game loop
while True:
    draw_board()
    solve_sudoku(board)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
