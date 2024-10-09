import chess
import time
import random

#Pruning Alg
def evaluate_board(board):
    eval = 0
    for piece in board.piece_map().values():
        if piece.color == chess.WHITE:
            eval += piece_value(piece)
        else:
            eval -= piece_value(piece)
    return eval

def piece_value(piece):
    if piece.piece_type == chess.PAWN:
        return 1
    elif piece.piece_type == chess.KNIGHT or piece.piece_type == chess.BISHOP:
        return 3
    elif piece.piece_type == chess.ROOK:
        return 5
    elif piece.piece_type == chess.QUEEN:
        return 9
    return 0

def alpha_beta(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    if maximizing_player:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval = alpha_beta(board, depth-1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = alpha_beta(board, depth-1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def best_move(board, depth):
    best_moves = []
    best_value = float('-inf')
    for move in board.legal_moves:
        board.push(move)
        board_value = alpha_beta(board, depth-1, float('-inf'), float('inf'), False)
        board.pop()
        if board_value > best_value:
            best_value = board_value
            best_moves = [move]
        elif board_value == best_value:
            best_moves.append(move)
    return random.choice(best_moves) if best_moves else None

def evaluate_game(board):
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return -1000
        else:
            return 1000
    elif board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves() or board.is_fivefold_repetition():
        return 0
    else:
        return evaluate_board(board)

def play_game():
    board = chess.Board()
    move_times = []
    game_moves = []

    while not board.is_game_over():
        start_time = time.time()
        move = best_move(board, 3)
        end_time = time.time()
        move_times.append(end_time - start_time)
        game_moves.append(board.san(move))
        board.push(move)

    final_score = evaluate_game(board)
    print("Game Over")
    print(board)
    print("\n")
    print("Move times:", move_times)
    average_move_time = sum(move_times) / len(move_times)
    print("Average move time:", average_move_time)
    print("Game notation:", " ".join(game_moves))
    print("Final score:", final_score)

if __name__ == "__main__":
    for i in range(20):
      play_game()

#Minimax alg
def evaluate_board(board):
    eval = 0
    for piece in board.piece_map().values():
        if piece.color == chess.WHITE:
            eval += piece_value(piece)
        else:
            eval -= piece_value(piece)
    return eval

def piece_value(piece):
    if piece.piece_type == chess.PAWN:
        return 1
    elif piece.piece_type == chess.KNIGHT or piece.piece_type == chess.BISHOP:
        return 3
    elif piece.piece_type == chess.ROOK:
        return 5
    elif piece.piece_type == chess.QUEEN:
        return 9
    return 0

def minimax(board, depth, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    if maximizing_player:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth-1, False)
            board.pop()
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth-1, True)
            board.pop()
            min_eval = min(min_eval, eval)
        return min_eval

def best_move(board, depth):
    best_moves = []
    best_value = float('-inf')
    for move in board.legal_moves:
        board.push(move)
        board_value = minimax(board, depth-1, False)
        board.pop()
        if board_value > best_value:
            best_value = board_value
            best_moves = [move]
        elif board_value == best_value:
            best_moves.append(move)
    return random.choice(best_moves) if best_moves else None

def play_game():
    board = chess.Board()
    move_times = []
    game_moves = []

    while not board.is_game_over():
        start_time = time.time()
        move = best_move(board, 3)
        end_time = time.time()
        move_times.append(end_time - start_time)
        game_moves.append(board.san(move))
        board.push(move)

    final_score = evaluate_game(board)
    print("Game Over")
    print(board)
    print("\n")
    print("Move times:", move_times)
    average_move_time = sum(move_times) / len(move_times)
    print("Average move time:", average_move_time)
    print("Game notation:", " ".join(game_moves))
    print("Final score:", final_score)

if __name__ == "__main__":
    for i in range(20):
      play_game()

#Eval alg
import chess
import chess.engine
import chess.polyglot

def evaluate_board(board):
    eval = 0
    piece_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9
    }
    
    for piece_type in piece_values:
        eval += len(board.pieces(piece_type, chess.WHITE)) * piece_values[piece_type]
        eval -= len(board.pieces(piece_type, chess.BLACK)) * piece_values[piece_type]
    
    return eval

def parse_moves(game_string):
    return game_string.split()

def evaluate_move(board, move):
    board.push_san(move)
    move_eval = evaluate_board(board)
    board.pop()

    best_move = None
    best_move_eval = float('-inf') if board.turn == chess.WHITE else float('inf')

    for legal_move in board.legal_moves:
        board.push(legal_move)
        eval = evaluate_board(board)
        board.pop()
        if board.turn == chess.WHITE:
            if eval > best_move_eval:
                best_move_eval = eval
                best_move = legal_move
        else:
            if eval < best_move_eval:
                best_move_eval = eval
                best_move = legal_move

    return best_move_eval, move_eval

def calculate_accuracy(game_string):
    board = chess.Board()
    moves = parse_moves(game_string)
    accuracy = 0
    move_count = 0

    for move in moves:
        best_move_eval, move_eval = evaluate_move(board, move)
        accuracy += abs(move_eval - best_move_eval)
        board.push_san(move)
        move_count += 1

    if move_count == 0:
        return 0

    return accuracy / move_count

game_string = "insert game notation here"
accuracy_score = calculate_accuracy(game_string)
print(f"Accuracy Score: {accuracy_score}")
