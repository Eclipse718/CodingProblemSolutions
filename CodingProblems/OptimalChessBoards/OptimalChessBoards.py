import pygame
import sys
import os
from pygame_gui.elements import UIButton, UIHorizontalSlider, UILabel
from pygame_gui import UIManager
import random
import numpy as np
import matplotlib.pyplot as plt
import pygame_chart as pc

os.chdir(os.path.dirname(os.path.abspath(__file__)))

pygame.init()

WIDTH, HEIGHT = 600, 400
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)

global max_pieces
max_pieces = 0

global data_or_board
data_or_board = False

global max_pieces_list
max_pieces_list = []

best_board = np.full((8, 8), '', dtype=object)

screen = pygame.display.set_mode((WIDTH, HEIGHT))


images = {
    "Pawn": pygame.transform.scale(pygame.image.load("Pawn.png"), (50, 50)),
    "Knight": pygame.transform.scale(pygame.image.load("Knight.png"), (50, 50)),
    "Bishop": pygame.transform.scale(pygame.image.load("Bishop.png"), (50, 50)),
    "Rook": pygame.transform.scale(pygame.image.load("Rook.png"), (50, 50)),
    "Queen": pygame.transform.scale(pygame.image.load("Queen.png"), (50, 50)),
    "King": pygame.transform.scale(pygame.image.load("King.png"), (50, 50))
}

image_locations = {
    "King": (60, 175),
    "Queen": (170, 175),
    "Rook": (280, 175),
    "Knight": (400, 175),
    "Pawn": (500, 175)
}

image_names = {
    "Pawn": "Pawn",
    "Knight": "Knight",
    "Bishop": "Bishop",
    "Rook": "Rook",
    "Queen": "Queen",
    "King": "King"
}

RedX = pygame.transform.scale(pygame.image.load("RedX.png"), (35, 35))

font = pygame.font.SysFont('Times New Roman', 40)
slider_font = pygame.font.SysFont('Arial', 20)
title_surface = font.render("Maximum Pieces Calculator", True, BLACK)
board_surface = pygame.Surface((WIDTH, HEIGHT))
smaller_board_surface = pygame.Surface((WIDTH-50, HEIGHT-50))
back_arrow_surface = pygame.image.load("BackArrow.png")
manager = UIManager((WIDTH, HEIGHT))

start_button = pygame.Rect(458, 165, 85, 35) 
data_button = pygame.Rect(468, 275, 65, 25) 
slider_x = 430 
slider_y = 120
slider_width, slider_height = 140, 22
slider = UIHorizontalSlider(relative_rect=pygame.Rect((slider_x, slider_y), (slider_width, slider_height)), 
                            start_value=1, 
                            value_range=(1, 2000), 
                            manager=manager)

def draw_label(text, rect, manager, object_id, text_colour):
    return UILabel(relative_rect=rect,
                   text=text,
                   manager=manager,
                   object_id=object_id,
                   text_colour=text_colour) 


def draw_homescreen():
    screen.fill(WHITE)
    screen.blit(title_surface, (75, 40))
    for image, location in image_locations.items():
        screen.blit(images[image], location)
    pygame.display.flip()

def get_attack_patterns(piece, row, col):
    if piece == 'knight':
        return [(row + x, col + y) for x, y in [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]]
    elif piece == 'bishop':
        return [(row + x, col + y) for x in range(-7, 8) for y in range(-7, 8) if abs(x) == abs(y) and (x, y) != (0, 0)]
    elif piece == 'rook':
        return [(row + x, col + y) for x in range(-7, 8) for y in range(-7, 8) if (x == 0 or y == 0) and (x, y) != (0, 0)]
    elif piece == 'queen':
        return [(row + x, col + y) for x in range(-7, 8) for y in range(-7, 8) if (x == 0 or y == 0 or abs(x) == abs(y)) and (x, y) != (0, 0)]
    elif piece == 'king':
        return [(row + x, col + y) for x in [-1, 0, 1] for y in [-1, 0, 1] if (x, y) != (0, 0)]
    elif piece == 'pawn': 
        return [(row - 1, col + 1), (row - 1, col - 1), (row + 1, col + 1), (row + 1, col - 1)]
    return []

def update_board_for_piece(board, valid_positions, piece, row, col):
    board[row, col] = piece[0].upper()  
    attack_positions = get_attack_patterns(piece, row, col)
    
    for attack_row, attack_col in attack_positions:
        if 0 <= attack_row < 8 and 0 <= attack_col < 8:
            board[attack_row, attack_col] = 'X'
            if (attack_row, attack_col) in valid_positions:
                valid_positions.remove((attack_row, attack_col))
    if (row, col) in valid_positions:
        valid_positions.remove((row, col))

def place_chess_pieces(piece_type, n_iterations):
    overall_max_pieces = 0
    best_board = None
    max_pieces_list = []

    for _ in range(n_iterations):
        board = np.full((8, 8), '', dtype=object)
        valid_positions = [(row, col) for row in range(8) for col in range(8)]
        pieces_placed = 0
        
        while valid_positions:
            row, col = random.choice(valid_positions)
            if board[row, col] == '':
                update_board_for_piece(board, valid_positions, piece_type, row, col)
                pieces_placed += 1
            else:
                valid_positions.remove((row, col))  


        max_pieces_list.append(pieces_placed)

        if pieces_placed > overall_max_pieces:
            overall_max_pieces = pieces_placed
            best_board = board.copy()

    return overall_max_pieces, best_board, max_pieces_list

def draw_board(clicked_image):
    global data_or_board
    
    screen.fill(WHITE)
    board_surface.fill(WHITE)
    if(not data_or_board):
        for i in range(8):
                for j in range(8):
                    if (i+j) % 2 == 0:
                        pygame.draw.rect(board_surface, GRAY, (i*50, j*50, 50, 50))
                    else:
                        pygame.draw.rect(board_surface, WHITE, (i*50, j*50, 50, 50))
    screen.blit(board_surface, (0, 0))
    screen.blit(images[clicked_image], (WIDTH - 60, 10))
    screen.blit(pygame.transform.scale(back_arrow_surface, (50, 50)), (WIDTH - 55, HEIGHT - 50))
    
    manager.draw_ui(screen)
    
    font = pygame.font.SysFont('Times New Roman', 40)
    
    pygame.draw.rect(screen, BLACK, start_button, 2)
    start_text = font.render("Start", True, BLACK)
    screen.blit(start_text, (start_button.x+start_button.width//2-start_text.get_width()//2, start_button.y+start_button.height//2-start_text.get_height()//2))
    
    
        
    font = pygame.font.SysFont('Times New Roman', 18)
    
    iterations_text = font.render("Iterations", True, BLACK)
    screen.blit(iterations_text, (slider_x+35, slider_y - 20))
    
    font = pygame.font.SysFont('Times New Roman', 16)
    max_pieces_text_1 = font.render(f"Maximum number of", True, BLACK)
    max_pieces_text_2 = font.render(f"{clicked_image} pieces:", True, BLACK)
    max_pieces_text_3 = font.render(f"{max_pieces}", True, BLACK)
    screen.blit(max_pieces_text_1, (slider_x, slider_y + 85))
    screen.blit(max_pieces_text_2, (slider_x+31, slider_y + 105))
    screen.blit(max_pieces_text_3, (slider_x+65, slider_y + 125))

    slider_value = str(slider.get_current_value())
    slider_value_text = font.render(slider_value, True, BLACK)
    slider_value_text_rect = slider_value_text.get_rect(center=(slider_x + slider_width // 2, slider_y + 30))
    screen.blit(slider_value_text, slider_value_text_rect.topleft)
    
    if(not data_or_board):
        for i in range(8):
            for j in range(8):
                if best_board[i, j] != 'X' and best_board[i, j] != '':
                    screen.blit(images[clicked_image], (j*50, i*50))
                elif best_board[i, j] == 'X':
                    screen.blit(RedX, (j*50+8, i*50+8))
        
        pygame.draw.rect(screen, BLACK, data_button, 2)           
        data_font = pygame.font.SysFont('Times New Roman', 23)
        data_text = data_font.render("Graph", True, BLACK)
        screen.blit(data_text, (data_button.x + (data_button.width - data_text.get_width()) / 2, data_button.y + (data_button.height - data_text.get_height()) / 2))
    else:
        pygame.draw.rect(screen, BLACK, data_button, 2)
        data_font = pygame.font.SysFont('Times New Roman', 25)
        data_text = data_font.render("Board", True, BLACK)
        screen.blit(data_text, (data_button.x + (data_button.width - data_text.get_width()) / 2, data_button.y + (data_button.height - data_text.get_height()) / 2))

    if len(max_pieces_list) > 2 and data_or_board:
        values, counts = np.unique(max_pieces_list, return_counts=True)

        # Scaling down the chart dimensions
        chart_width = 375
        chart_height = 380
        chart_surface = pygame.Surface((chart_width, chart_height))
        chart_surface.fill(WHITE)

        max_height = max(counts)
        base_y = chart_height - 45  # Adjusted base position to leave space for labels at the bottom
        axis_margin_left = 50
        label_space = 0  # Space for 'Instances' label

        num_values = len(values)
        total_spacing = 5 * (num_values - 1)
        available_width = chart_width - axis_margin_left - label_space - total_spacing
        bar_width = available_width / num_values
        bar_width = max(5, min(bar_width, 20))  # Ensure bar width is reasonable

        # Dynamic font size based on space availability
        font_size = min(max(int(bar_width), 10), 15)
        value_font = pygame.font.SysFont('Arial', font_size)
        label_font = pygame.font.SysFont('Arial', 12)

        start_x = axis_margin_left + label_space

        # Y-axis ticks and labels configuration
        num_ticks = 5
        tick_length = 5
        tick_spacing = (base_y - 20) / (num_ticks - 1)
        tick_value_increment = max_height / (num_ticks - 1)
        max_tick_value = tick_value_increment * (num_ticks - 1)

        label_font = pygame.font.SysFont('Arial', 14)


        # Y-axis ticks and labels configuration
        num_ticks = 5
        tick_length = 5
        tick_spacing = (base_y - 20) / (num_ticks - 1)
        tick_value_increment = max_height / (num_ticks - 1)
        max_tick_value = tick_value_increment * (num_ticks - 1)

        if num_values <= 5:
            total_bars_width = num_values * bar_width + (num_values - 1) * 5  # Width of all bars including spacing
            start_x = (chart_width - total_bars_width) / 2  # Adjust to center the bars
            for i, (value, count) in enumerate(zip(values, counts)):
                bar_x = start_x + i * (bar_width+5)
                bar_height = (count / max_tick_value) * (base_y - 20)  # Adjusted scaling
                pygame.draw.rect(chart_surface, BLACK, [bar_x, base_y - bar_height, bar_width, bar_height])
        else:
            for i, (value, count) in enumerate(zip(values, counts)):
                bar_x = start_x + i * (bar_width + 5)
                bar_height = (count / max_tick_value) * (base_y - 20)  # Adjusted scaling
                pygame.draw.rect(chart_surface, BLACK, [bar_x, base_y - bar_height, bar_width, bar_height])

        # Draw x-axis labels
        for i, value in enumerate(values):
            bar_x = start_x + i * (bar_width + 5)
            if num_values <= 5:
                bar_x = start_x + i * (bar_width+5)
            value_label = value_font.render(str(value), True, BLACK)
            chart_surface.blit(value_label, (bar_x + (bar_width - value_label.get_width()) / 2, base_y + 5))

        label_font = pygame.font.SysFont('Arial', 14)  # You can adjust the font and size as needed

        instances_label = label_font.render("Instances", True, BLACK)
        instances_label_rotated = pygame.transform.rotate(instances_label, 90)
        chart_surface.blit(instances_label_rotated, (8, chart_height / 2 - instances_label_rotated.get_height() / 2))
        
        num_ticks = 5  # Number of ticks on the y-axis
        tick_length = 5  # Length of each tick mark

        # Calculate the spacing and value of each tick
        tick_spacing = (base_y - 20) / (num_ticks - 1)
        tick_value_increment = max_height / (num_ticks - 1)

        # Draw ticks and labels
        for i in range(num_ticks):
            tick_value = i * tick_value_increment
            tick_y = base_y - i * tick_spacing

            # Draw the tick line
            pygame.draw.line(chart_surface, BLACK, (axis_margin_left - tick_length, tick_y), (axis_margin_left, tick_y))

            # Create and draw the tick label
            tick_label = label_font.render(f"{int(tick_value)}", True, BLACK)
            chart_surface.blit(tick_label, (axis_margin_left - tick_length - tick_label.get_width() - 2, tick_y - tick_label.get_height() / 2))


        # Draw 'Number of [piece]s placed' label at the bottom
        title_text = f'Number of {clicked_image}s placed'
        title_label = label_font.render(title_text, True, BLACK)
        chart_surface.blit(title_label, (chart_width / 2 - title_label.get_width() / 2, chart_height - 20))

        # Blit the chart surface onto the main screen surface
        screen.blit(chart_surface, (10, 10))

    elif (data_or_board):
        no_data_font = pygame.font.SysFont('Times New Roman', 17)
        no_data_text = no_data_font.render("Too Little Data,", True, BLACK)
        screen.blit(no_data_text, (25, 75))
        no_data_text = no_data_font.render("Increase the Number of Iterations and Press Start", True, BLACK)
        screen.blit(no_data_text, (27, 95))
        
    pygame.display.flip()

def start_button_clicked(pos):
    if start_button.collidepoint(pos):
        piece_type = clicked_image.lower()
        n_iterations = slider.get_current_value()
        global max_pieces
        global best_board
        global max_pieces_list
        max_pieces_list = [] 
        max_pieces, best_board, max_pieces_list = place_chess_pieces(piece_type, n_iterations)

def data_button_clicked(pos):
    if data_button.collidepoint(pos):
        global data_or_board
        data_or_board = not data_or_board

homescreen = True
running = True
clicked_image = None
while running:
    if homescreen:
        draw_homescreen()
    else:
        draw_board(clicked_image)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if homescreen:
                for image, location in image_locations.items():
                    if location[0] <= mouse_pos[0] <= location[0] + 60 and location[1] <= mouse_pos[1] <= location[1] + 60:
                        clicked_image = image
                        homescreen = False
            else:
                if WIDTH - 55 <= mouse_pos[0] <= WIDTH - 3 and HEIGHT - 50 <= mouse_pos[1] <= HEIGHT - 3:
                    homescreen = True
                    clicked_image = None
                    max_pieces = 0
                    best_board = np.full((8, 8), '', dtype=object)
                    max_pieces_list = []
                else:
                    start_button_clicked(mouse_pos)
                    data_button_clicked(mouse_pos)

    manager.process_events(event)
    manager.update(time_delta=1/60)

pygame.quit()
sys.exit()
