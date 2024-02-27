import random

def is_safe(board, row, col):
    """
    Check if it's safe to place a knight at position (row, col) on the board.
    """
    directions = [(2, 1), (1, 2), (-1, 2), (-2, 1),
                  (-2, -1), (-1, -2), (1, -2), (2, -1)]

    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < 8 and 0 <= c < 8 and board[r][c] == 'K':
            return False
    return True

def print_board(board):
    for row in board:
        print(' '.join(row))
    print()

def place_knights():
    """
    Place knights randomly on the board until no more knights can be placed.
    """
    board = [['.'] * 8 for _ in range(8)]
    knights_count = 0

    while True:
        available_positions = [(r, c) for r in range(8) for c in range(8) if board[r][c] == '.' and is_safe(board, r, c)]
        if not available_positions:
            break
        row, col = random.choice(available_positions)
        board[row][col] = 'K'
        knights_count += 1

    for row in range(8):
        for col in range(8):
            if board[row][col] == '.':
                board[row][col] = 'X' if not is_safe(board, row, col) else '.'

    return board

if __name__ == "__main__":
    best_board = None
    max_knights = 0


# We run the program 1000 times. This will almost certainly find the actual optimal 32 Knights
# At around 100, or a little higher, tries the program returns the 32 Knights about 50% of the time
    for _ in range(1000):  # Try 1000 attempts
        board = place_knights()
        num_knights = sum(row.count('K') for row in board)

        if num_knights > max_knights:
            max_knights = num_knights
            best_board = board

    print("Maximum number of knights found:", max_knights)
    print("Best Board Found:")
    print_board(best_board)
