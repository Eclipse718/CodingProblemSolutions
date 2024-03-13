import random
import numpy as np
import matplotlib.pyplot as plt

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
        return [(row + 1, col - 1), (row + 1, col + 1)]
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
            update_board_for_piece(board, valid_positions, piece_type, row, col)
            pieces_placed += 1

        max_pieces_list.append(pieces_placed)

        if pieces_placed > overall_max_pieces:
            overall_max_pieces = pieces_placed
            best_board = board.copy()

    return overall_max_pieces, best_board, max_pieces_list


def create_bar_chart(max_pieces_list):
    max_value = max(max_pieces_list)
    values, counts = np.unique(max_pieces_list, return_counts=True)
    max_iterations = 1.2 * counts.max()
    color_intensity = counts / counts.max()

    # Adjusting color intensity for darker shades
    color_intensity = 0.5 + (color_intensity * 0.5)  # Shift and scale to make colors darker

    plt.bar(values, counts, color=plt.cm.BuPu(color_intensity))
    plt.xlabel('Maximum Pieces')
    plt.ylabel('Instances')
    plt.title('Distribution of Maximum Pieces Placed')
    plt.xlim(0, max_value + 1)  # Adjusted to be one greater than the maximum number of pieces
    plt.ylim(0, max_iterations)
    plt.show()

max_queens, best_board_queens, max_pieces_list = place_chess_pieces('queen', 1000)
create_bar_chart(max_pieces_list)
