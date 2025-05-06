# Chess Engine

import chess

positions_evaluated = 0

def initialize_board():
    return chess.Board()

def choose_player_color():
    # Prompts the player to select their color and returns True if they choose white, False if black.
    while True:
        color = input("Choose your color (white/black): ").strip().lower()
        if color in ['white', 'black']:
            is_player_white = (color == 'white')
            break
        else:
            print("Invalid choice. Please choose 'white' or 'black'.")
    
    print("You have chosen to play as", "White" if is_player_white else "Black")
    return is_player_white

def get_player_move(board):
    while True:
        player_move = input("Enter your move (e.g., e2e4): ").strip()
        try:
            move = chess.Move.from_uci(player_move)
            if move in board.legal_moves:
                return move
            else:
                print("Illegal move. Please try again.")
        except ValueError:
            print("Invalid input format. Please enter moves in UCI format (e.g., 'e2e4').")

def engine_move(board):
    """
    Finds the best move for the current player and returns that move.
    
    Parameters:
    - board (chess.Board): The current board state.
    - depth (int): The maximum depth of the search. 
    
    Returns:
    - chess.Move: The best move for the current player.
    """
    remaining_pieces = len(board.piece_map())

    if remaining_pieces >= 25:
        depth = 4
    elif remaining_pieces >= 14:
        depth = 5
    elif remaining_pieces >= 10:
        depth = 6
    else: 
        depth = 7

    # Determine if the current player is maximizing (white) or minimizing (black)
    is_maximizing = board.turn  # True for white, False for black
    
    # Call find_best_move with adjusted parameters for color
    best_move, _ = alpha_beta_search(board, depth, is_maximizing)

    global positions_evaluated

    print(positions_evaluated)

    positions_evaluated = 0

    return best_move

def main_game_loop():
    board = initialize_board()
    player_is_white = choose_player_color()
    
    # Start the game loop
    while not board.is_game_over():
        print(board)  # Display the current board state
        
        if board.turn == player_is_white:  # Player's turn
            move = get_player_move(board)
            board.push(move)
        else:  # Engine's turn
            
            move = engine_move(board)
            if move:  # Only push if engine_move returns a valid move
                print(move)
                board.push(move)
            else:
                print("Engine has no move (placeholder).")

        # Check if the game has ended
        if board.is_checkmate():
            print("Checkmate!", "You win!" if board.turn != player_is_white else "Engine wins!")
            break
        elif board.is_stalemate():
            print("Stalemate. The game is a draw.")
            break
        elif board.is_insufficient_material():
            print("Draw due to insufficient material.")
            break

##############################################################################################################

def is_endgame(board):
    total_pieces = len(board.piece_map())
    return total_pieces <= 14  # Endgame if there are 14 or fewer pieces on the board

def evaluate_board(board):
    """
    Evaluates the board based on material values and positional bonuses for each side, 
    using different positional tables for midgame and endgame phases.
    
    Parameters:
    - board (chess.Board): The current board state.
    
    Returns:
    - int: The evaluation score, positive if white is better, negative if black is better.
    """
    # Fixed piece values
    piece_values = {
        chess.PAWN: 100,
        chess.KNIGHT: 320,
        chess.BISHOP: 330,
        chess.ROOK: 500,
        chess.QUEEN: 910,
    }
    
    # Midgame and Endgame Positional Tables for Each Piece
    mg_pawn_table = [
         0,   0,   0,   0,   0,   0,  0,   0,
        98, 134,  61,  95,  68, 126, 34, -11,
        -6,   7,  26,  31,  65,  56, 25, -20,
       -14,  13,   6,  21,  23,  12, 17, -23,
       -27,  -2,  -5,  12,  17,   6, 10, -25,
       -26,  -4,  -4, -10,   3,   3, 33, -12,
       -35,  -1, -20, -23, -15,  24, 38, -22,
         0,   0,   0,   0,   0,   0,  0,   0,
    ]

    eg_pawn_table = [
         0,   0,   0,   0,   0,   0,   0,   0,
       178, 173, 158, 134, 147, 132, 165, 187,
        94, 100,  85,  67,  56,  53,  82,  84,
        32,  24,  13,   5,  -2,   4,  17,  17,
        13,   9,  -3,  -7,  -7,  -8,   3,  -1,
         4,   7,  -6,   1,   0,  -5,  -1,  -8,
        13,   8,   8,  10,  13,   0,   2,  -7,
         0,   0,   0,   0,   0,   0,   0,   0,
    ]

    mg_knight_table = [
       -167, -89, -34, -49,  61, -97, -15, -107,
        -73, -41,  72,  36,  23,  62,   7,  -17,
        -47,  60,  37,  65,  84, 129,  73,   44,
         -9,  17,  19,  53,  37,  69,  18,   22,
        -13,   4,  16,  13,  28,  19,  21,   -8,
        -23,  -9,  12,  10,  19,  17,  25,  -16,
        -29, -53, -12,  -3,  -1,  18, -14,  -19,
       -105, -21, -58, -33, -17, -28, -19,  -23,
    ]

    eg_knight_table = [
        -58, -38, -13, -28, -31, -27, -63, -99,
        -25,  -8, -25,  -2,  -9, -25, -24, -52,
        -24, -20,  10,   9,  -1,  -9, -19, -41,
        -17,   3,  22,  22,  22,  11,   8, -18,
        -18,  -6,  16,  25,  16,  17,   4, -18,
        -23,  -3,  -1,  15,  10,  -3, -20, -22,
        -42, -20, -10,  -5,  -2, -20, -23, -44,
        -29, -51, -23, -15, -22, -18, -50, -64,
    ]

    mg_bishop_table = [
        -29,   4, -82, -37, -25, -42,   7,  -8,
        -26,  16, -18, -13,  30,  59,  18, -47,
        -16,  37,  43,  40,  35,  50,  37,  -2,
         -4,   5,  19,  50,  37,  37,   7,  -2,
         -6,  13,  13,  26,  34,  12,  10,   4,
          0,  15,  15,  15,  14,  27,  18,  10,
          4,  15,  16,   0,   7,  21,  33,   1,
        -33,  -3, -14, -21, -13, -12, -39, -21,
    ]

    eg_bishop_table = [
        -14, -21, -11,  -8, -7,  -9, -17, -24,
         -8,  -4,   7, -12, -3, -13,  -4, -14,
          2,  -8,   0,  -1, -2,   6,   0,   4,
         -3,   9,  12,   9, 14,  10,   3,   2,
         -6,   3,  13,  19,  7,  10,  -3,  -9,
        -12,  -3,   8,  10, 13,   3,  -7, -15,
        -14, -18,  -7,  -1,  4,  -9, -15, -27,
        -23,  -9, -23,  -5, -9, -16,  -5, -17,
    ]

    mg_rook_table = [
         32,  42,  32,  51, 63,  9,  31,  43,
         27,  32,  58,  62, 80, 67,  26,  44,
         -5,  19,  26,  36, 17, 45,  61,  16,
        -24, -11,   7,  26, 24, 35,  -8, -20,
        -36, -26, -12,  -1,  9, -7,   6, -23,
        -45, -25, -16, -17,  3,  0,  -5, -33,
        -44, -16, -20,  -9, -1, 11,  -6, -71,
        -19, -13,   1,  17, 16,  7, -37, -26,
    ]

    eg_rook_table = [
        13, 10, 18, 15, 12,  12,   8,   5,
        11, 13, 13, 11, -3,   3,   8,   3,
         7,  7,  7,  5,  4,  -3,  -5,  -3,
         4,  3, 13,  1,  2,   1,  -1,   2,
         3,  5,  8,  4, -5,  -6,  -8, -11,
        -4,  0, -5, -1, -7, -12,  -8, -16,
        -6, -6,  0,  2, -9,  -9, -11,  -3,
        -9,  2,  3, -1, -5, -13,   4, -20,
    ]

    mg_queen_table = [
       -28,   0,  29,  12,  59,  44,  43,  45,
       -24, -39,  -5,   1, -16,  57,  28,  54,
       -13, -17,   7,   8,  29,  56,  47,  57,
       -27, -27, -16, -16,  -1,  17,  -2,   1,
        -9, -26,  -9, -10,  -2,  -4,   3,  -3,
       -14,   2, -11,  -2,  -5,   2,  14,   5,
       -35,  -8,  11,   2,   8,  15,  -3,   1,
        -1, -18,  -9,  10, -15, -25, -31, -50,
    ]
    eg_queen_table = [
         -9,  22,  22,  27,  27,  19,  10,  20,
        -17,  20,  32,  41,  58,  25,  30,   0,
        -20,   6,   9,  49,  47,  35,  19,   9,
          3,  22,  24,  45,  57,  40,  57,  36,
        -18,  28,  19,  47,  31,  34,  39,  23,
        -16, -27,  15,   6,   9,  17,  10,   5,
        -22, -23, -30, -16, -16, -23, -36, -32,
        -33, -28, -22, -43,  -5, -32, -20, -41,
    ]

    mg_king_table = [
       -65,  23,  16, -15, -56, -34,   2,  13,
        29,  -1, -20,  -7,  -8,  -4, -38, -29,
        -9,  24,   2, -16, -20,   6,  22, -22,
       -17, -20, -12, -27, -30, -25, -14, -36,
       -49,  -1, -27, -39, -46, -44, -33, -51,
       -14, -14, -22, -46, -44, -30, -15, -27,
         1,   7,  -8, -64, -43, -16,   9,   8,
       -15,  36,  12, -54,   8, -28,  24,  14,
    ]

    eg_king_table = [
       -74, -35, -18, -18, -11,  15,   4, -17,
       -12,  17,  14,  17,  17,  38,  23,  11,
        10,  17,  23,  15,  20,  45,  44,  13,
        -8,  22,  24,  27,  26,  33,  26,   3,
       -18,  -4,  21,  24,  27,  23,   9, -11,
       -19,  -3,  11,  21,  23,  16,   7,  -9,
       -27, -11,   4,  13,  14,   4,  -5, -17,
       -53, -34, -21, -11, -28, -14, -24, -43,
    ]

    mg_tables = {
        chess.PAWN: mg_pawn_table,
        chess.KNIGHT: mg_knight_table,
        chess.BISHOP: mg_bishop_table,
        chess.ROOK: mg_rook_table,
        chess.QUEEN: mg_queen_table,
        chess.KING: mg_king_table,
    }
    
    eg_tables = {
        chess.PAWN: eg_pawn_table,
        chess.KNIGHT: eg_knight_table,
        chess.BISHOP: eg_bishop_table,
        chess.ROOK: eg_rook_table,
        chess.QUEEN: eg_queen_table,
        chess.KING: eg_king_table,
    }

    # Check if the game is in the endgame phase
    in_endgame = is_endgame(board)
    tables = eg_tables if in_endgame else mg_tables
    
    # Initialize material scores
    white_score = 0
    black_score = 0
    
    # Calculate material and positional score for each piece type
    for piece_type, material_value in piece_values.items():
        # Fetch the appropriate positional table based on game phase
        position_table = tables.get(piece_type, None)
        
        for square in board.pieces(piece_type, chess.WHITE):
            white_score += material_value
            if position_table:
                white_score += position_table[square]
        
        for square in board.pieces(piece_type, chess.BLACK):
            black_score += material_value
            if position_table:
                black_score += position_table[chess.square_mirror(square)]  # Mirror for black
    
    board_eval = white_score - black_score
    board_eval += calculate_undefended_pieces(board)
    if len(board.piece_map()) >= 14:
        board_eval += calculate_king_safety(board)
    board_eval += calculate_rook_placement(board)
    board_eval += calculate_bishop_placement(board)
    board_eval += calculate_knight_placement(board)
    board_eval += calculate_pawn_placement(board)

    # Return the difference: positive if white has an advantage, negative if black does
    return board_eval

################################################################################################################

def calculate_pawn_placement(board):
    """
    Evaluate pawn placement by scoring diagonal support and penalizing for pawns in the same column.
    """
    white_score = 0
    black_score = 0
    
    # Iterate over each square that contains a pawn
    for square in board.pieces(chess.PAWN, chess.WHITE) | board.pieces(chess.PAWN, chess.BLACK):
        pawn = board.piece_at(square)
        pawn_color = pawn.color
        score = 0
        
        # Calculate diagonal support score
        file = chess.square_file(square)
        rank = chess.square_rank(square)
        
        # Check the two diagonal squares for friendly pawns
        diagonal_squares = [
            chess.square(file + 1, rank + (1 if pawn_color == chess.WHITE else -1)),
            chess.square(file - 1, rank + (1 if pawn_color == chess.WHITE else -1))
        ]
        
        for diag_square in diagonal_squares:
            # Validate if the diagonal square is within bounds (0-63)
            if 0 <= diag_square < 64 and board.piece_at(diag_square):
                diag_piece = board.piece_at(diag_square)
                if diag_piece.piece_type == chess.PAWN and diag_piece.color == pawn_color:
                    score += 3
        
        # Check for pawns in the same column
        for rank_check in range(8):
            if rank_check != rank:
                same_column_square = chess.square(file, rank_check)
                if board.piece_at(same_column_square):
                    same_column_piece = board.piece_at(same_column_square)
                    if same_column_piece.piece_type == chess.PAWN and same_column_piece.color == pawn_color:
                        score -= 9
        
        # Add the calculated score to the appropriate color's score
        if pawn_color == chess.WHITE:
            white_score += score
        else:
            black_score += score
    
    # Return the difference between white and black pawn placement scores
    return white_score - black_score

def calculate_knight_placement(board):

    white_score = 0
    black_score = 0
    
    # Iterate over each square that contains a knight
    for square in board.pieces(chess.KNIGHT, chess.WHITE) | board.pieces(chess.KNIGHT, chess.BLACK):
        knight = board.piece_at(square)
        knight_color = knight.color
        score = 0
        
        # Calculate mobility score for each possible knight move
        for target_square in chess.SQUARES:
            if chess.square_distance(square, target_square) == 1:
                # Check if the square is either open or occupied by an enemy piece
                if board.is_legal(chess.Move(square, target_square)):
                    score += 2
        
        # Check if the knight is defended by a pawn
        pawn_defended = any(
            board.piece_at(defender_square)
            and board.piece_at(defender_square).piece_type == chess.PAWN
            and board.piece_at(defender_square).color == knight_color
            for defender_square in board.attackers(knight_color, square)
        )
        
        if pawn_defended:
            score += 5
        
        # Add the calculated score to the appropriate color's score
        if knight_color == chess.WHITE:
            white_score += score
        else:
            black_score += score
    
    # Return the difference between white and black knight placement scores
    return white_score - black_score

def calculate_bishop_placement(board):

    white_score = 0
    black_score = 0
    
    directions = [chess.square(1, 1), chess.square(1, -1), chess.square(-1, 1), chess.square(-1, -1)]  # Diagonal directions
    
    # Center squares for bishop control
    center_squares = {chess.D4, chess.D5, chess.E4, chess.E5}
    
    # Enemy king squares within 1 space
    white_king_square = board.king(chess.WHITE)
    black_king_square = board.king(chess.BLACK)
    white_king_zone = {square for square in chess.SQUARES if chess.square_distance(white_king_square, square) == 1}
    black_king_zone = {square for square in chess.SQUARES if chess.square_distance(black_king_square, square) == 1}
    
    # Iterate over each square that contains a bishop
    for square in board.pieces(chess.BISHOP, chess.WHITE) | board.pieces(chess.BISHOP, chess.BLACK):
        bishop = board.piece_at(square)
        bishop_color = bishop.color
        score = 0
        
        # Determine the enemy king zone based on bishop's color
        enemy_king_zone = black_king_zone if bishop_color == chess.WHITE else white_king_zone
        
        # Calculate bishop score based on its line of sight
        for direction in directions:
            current_square = square
            
            while True:
                current_square = chess.square_mirror(current_square + direction)
                
                # If current square is out of bounds, break the loop
                if current_square < 0 or current_square >= 64:
                    break
                
                # Check if the square is empty or occupied
                piece = board.piece_at(current_square)
                
                if piece is None:
                    # Add +1 for each open space the bishop "sees"
                    score += 1
                    # Add +2 if the space is within one space of the enemy king
                    if current_square in enemy_king_zone:
                        score += 2
                    # Add +3 if the square is one of the central squares
                    if current_square in center_squares:
                        score += 3
                else:
                    # Stop line of sight as the bishop is blocked by another piece
                    break
        
        # Add the calculated score to the appropriate color's score
        if bishop_color == chess.WHITE:
            white_score += score
        else:
            black_score += score
    
    # Return the difference between white and black bishop placement scores
    return white_score - black_score

def calculate_rook_placement(board):

    white_score = 0
    black_score = 0
    
    directions = [chess.square(0, 1), chess.square(0, -1), chess.square(1, 0), chess.square(-1, 0)]  # Right, Left, Up, Down
    
    # Iterate over each square that contains a rook
    for square in board.pieces(chess.ROOK, chess.WHITE) | board.pieces(chess.ROOK, chess.BLACK):
        rook = board.piece_at(square)
        rook_color = rook.color
        score = 0
        
        for direction in directions:
            current_square = square
            
            while True:
                current_square = chess.square_mirror(current_square + direction)
                
                # If current square is out of bounds, break the loop
                if current_square < 0 or current_square >= 64:
                    break
                
                # Check the piece on the current square
                piece = board.piece_at(current_square)
                
                if piece is None:
                    # Add +1 for each open space the rook "sees"
                    score += 2
                else:
                    # If the piece is a rook or queen of the same color, add +2
                    if piece.color == rook_color and piece.piece_type in {chess.ROOK, chess.QUEEN}:
                        score += 4
                    # Stop the line of sight as the rook is blocked by another piece
                    break
        
        # Add the calculated score to the appropriate color's score
        if rook_color == chess.WHITE:
            white_score += score
        else:
            black_score += score
    
    # Return the difference between white and black rook placement scores
    return white_score - black_score


def calculate_king_safety(board):

    scores = {
        (chess.PAWN, 'friendly'): 6,
        (chess.KNIGHT, 'friendly'): 1,
        (chess.BISHOP, 'friendly'): 3,
        (chess.ROOK, 'friendly'): 1,
        (chess.QUEEN, 'friendly'): -2,
        (chess.PAWN, 'enemy'): -8,
        (chess.KNIGHT, 'enemy'): -9,
        (chess.BISHOP, 'enemy'): -4,
        (chess.ROOK, 'enemy'): -2,
        (chess.QUEEN, 'enemy'): -25
    }
    
    def get_king_zone(king_square):
        """Returns a set of squares within two spaces of the given king's square."""
        king_zone = set()
        rank, file = chess.square_rank(king_square), chess.square_file(king_square)
        
        # Iterate through the 5x5 area around the king (3x3 square centered on the king)
        for dr in range(-2, 3):  # Row distance from king
            for df in range(-2, 3):  # File distance from king
                nearby_square = chess.square(file + df, rank + dr)
                if 0 <= nearby_square < 64:  # Ensure the square is within board bounds
                    king_zone.add(nearby_square)
        
        return king_zone
    
    # Get king positions
    white_king_square = board.king(chess.WHITE)
    black_king_square = board.king(chess.BLACK)
    
    white_king_zone = get_king_zone(white_king_square)
    black_king_zone = get_king_zone(black_king_square)
    
    white_score = 0
    black_score = 0

    for square in white_king_zone:
        piece = board.piece_at(square)
        if piece:  # Ensure there's a piece on this square
            piece_type = piece.piece_type
            piece_color = 'friendly' if piece.color == chess.WHITE else 'enemy'
            white_score += scores.get((piece_type, piece_color), 0)  # Default to 0 if no score found
    
    # Calculate black king safety score
    for square in black_king_zone:
        piece = board.piece_at(square)
        if piece:  # Ensure there's a piece on this square
            piece_type = piece.piece_type
            piece_color = 'friendly' if piece.color == chess.BLACK else 'enemy'
            black_score += scores.get((piece_type, piece_color), 0)  # Default to 0 if no score found
    
    # Return the difference between white and black king safety scores
    return white_score - black_score

def calculate_undefended_pieces(board):
    """
    Calculate the difference in undefended pieces between black and white.
    
    Parameters:
    - board: A `chess.Board` object representing the current board state.
    
    Returns:
    - int: (Number of black undefended pieces - Number of white undefended pieces) * 2
    """
    def is_defended(square, color):
        """Check if a square is defended by any piece of the given color."""
        return any(board.is_attacked_by(color, defender_square) for defender_square in chess.SQUARES if board.piece_at(defender_square) and board.piece_at(defender_square).color == color)
    
    # Initialize undefended piece counts
    white_undefended = 0
    black_undefended = 0
    
    # Define all piece types to check
    piece_types = [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN]
    
    # Check undefended pieces for each piece type
    for piece_type in piece_types:
        # Check undefended pieces for white
        for square in board.pieces(piece_type, chess.WHITE):
            if not is_defended(square, chess.WHITE):
                white_undefended += 1

        # Check undefended pieces for black
        for square in board.pieces(piece_type, chess.BLACK):
            if not is_defended(square, chess.BLACK):
                black_undefended += 1
    
    # Calculate the final result
    return (black_undefended - white_undefended) * 2

##############################################################################################################

def alpha_beta_search(board, depth, is_maximizing, alpha=float('-inf'), beta=float('inf')):
    """
    Finds the best move for the current player using minimax with alpha-beta pruning.
    It accounts for checkmate situations, avoiding self-checkmate and prioritizing opponent checkmates.

    Parameters:
    - board (chess.Board): The current board state.
    - depth (int): The maximum depth of the search.
    - is_maximizing (bool): True if the current turn is for the maximizing player (white), False otherwise.
    - alpha (float): The best score for the maximizing player along the path.
    - beta (float): The best score for the minimizing player along the path.

    Returns:
    - tuple: (best_move, best_score) where best_move is the chess.Move and best_score is the evaluation score.
    """

    global positions_evaluated

    # Base case: if we reach depth 0 or the game is over, return the evaluation of the board
    if depth == 0 or board.is_game_over():
        if board.is_checkmate():
            # If the board is in checkmate, return a large negative score if the current player is losing
            # and a large positive score if the current player has won.
            return None, float('-inf') if is_maximizing else float('inf')
        # Otherwise, return the evaluation score of the board
        positions_evaluated += 1
        return None, evaluate_board(board)

    best_move = None

    if is_maximizing:  # Maximizing player (white)
        best_score = float('-inf')
        
        for move in board.legal_moves:
            board.push(move)
            if board.is_checkmate():
                score = float('inf')  # Checkmate for the opponent is ideal
            else:
                _, score = alpha_beta_search(board, depth - 1, not is_maximizing, alpha, beta)
            board.pop()

            # Update best score and best move if found a better option
            if score > best_score:
                best_score = score
                best_move = move

            # Alpha-beta pruning
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break  # Prune the remaining moves

    else:  # Minimizing player (black)
        best_score = float('inf')
        
        for move in board.legal_moves:
            board.push(move)
            if board.is_checkmate():
                score = float('-inf')  # Avoid self-checkmate at all costs
            else:
                _, score = alpha_beta_search(board, depth - 1, not is_maximizing, alpha, beta)
            board.pop()

            # Update best score and best move if found a better option
            if score < best_score:
                best_score = score
                best_move = move

            # Alpha-beta pruning
            beta = min(beta, best_score)
            if beta <= alpha:
                break  # Prune the remaining moves

    return best_move, best_score

# Run the main game loop
main_game_loop()
