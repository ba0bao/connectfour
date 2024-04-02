import copy 

def main():
    columns = 7
    rows = 6
    connect4 = 4
    again = True
    while again:
        print("Choose difficulty level(depth) from 1 to 10 ")
        depth = int(input())

        board = [['0' for c in range(columns)] for r in range(rows)]
        print("Who would you like to go first? 1 for computer (Red) or 2 for you (Blue)")
        Turn = int(input())

        while (Turn > 2 or Turn < 1):
            print("Enter 1 for Computer or 2 for Player\nEnter new number:")
            Turn = int(input())

        if Turn == 1:
            computerTurn = True
        else:
            computerTurn = False

        selected_column = None  
        while not game_over(board, columns, rows, connect4):
            if computerTurn:
                alpha = -float('inf')
                beta = float('inf')
                best_move, _ = minimax(board, depth, True, alpha, beta, columns, rows, connect4)
                board = best_move
                printboard(board, columns, rows)
            else:
                while selected_column is None or not (0 <= selected_column < columns and valid_move(board, selected_column, columns, rows)):
                    selected_column = int(input("Enter column to drop your piece (1-7): ")) - 1  
                    if not (0 <= selected_column < columns):
                        print("Invalid column. Please choose a valid column.")
                        selected_column = None
                board = drop_piece(board, selected_column, 'B')  

            computerTurn = not computerTurn


        print("Play again? y/n")
        playagain = input()
        again = playagain == 'y'

def minimax(board, depth, is_maximizing_player, alpha, beta, columns, rows, connect4):
    if depth == 0 or game_over(board, columns, rows, connect4):
        return None, evaluate(board, columns, rows, connect4)

    if is_maximizing_player:
        max_eval = -float('inf')
        best_move = None
        for col in range(columns):
            if valid_move(board, col, columns, rows):
                new_board = drop_piece(board, col, 'R')
                _, eval = minimax(new_board, depth - 1, False, alpha, beta, columns, rows, connect4)
                if eval > max_eval:
                    max_eval = eval
                    best_move = new_board
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
        return best_move, max_eval
    else:
        min_eval = float('inf')
        best_move = None
        for col in range(columns):
            if valid_move(board, col, columns, rows):
                new_board = drop_piece(board, col, 'B')
                _, eval = minimax(new_board, depth - 1, True, alpha, beta, columns, rows, connect4)
                if eval < min_eval:
                    min_eval = eval
                    best_move = new_board
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return best_move, min_eval

def game_over(board, columns, rows, connect4):
    if check_winner(board, columns, rows, connect4):
        return True
    return isfull(board, columns, rows)

def check_winner(board, columns, rows, connect4):
    
    for i in range(rows):
        for j in range(columns - connect4 + 1):
            if board[i][j] != '0':
                if all(board[i][j] == board[i][j+k] for k in range(1, connect4)):
                    return True
    
    for i in range(rows - connect4 + 1):
        for j in range(columns):
            if board[i][j] != '0':
                if all(board[i][j] == board[i+k][j] for k in range(1, connect4)):
                    return True
    
    for i in range(rows - connect4 + 1):
        for j in range(columns - connect4 + 1):
            if board[i][j] != '0':
                if all(board[i][j] == board[i+k][j+k] for k in range(1, connect4)):
                    return True
                
    for i in range(connect4 - 1, rows):
        for j in range(columns - connect4 + 1):
            if board[i][j] != '0':
                if all(board[i][j] == board[i-k][j+k] for k in range(1, connect4)):
                    return True
    return False

def isfull(board, columns, rows):
    for i in range(rows):
        for c in range(columns):
            if board[i][c] == '0':
                return False
    return True

def valid_move(board, col, columns, rows):
    return board[0][col] == '0'

def drop_piece(board, col, piece):
    new_board = copy.deepcopy(board)
    for i in range(len(new_board) - 1, -1, -1):
        if new_board[i][col] == '0':
            new_board[i][col] = piece
            break
    return new_board

def evaluate(board, columns, rows, connect4):
    score = 0
    return score

def printboard(board, columns, rows):
    print(" 1 | 2 | 3 | 4 | 5 | 6 | 7 |\n")
    for i in range(rows):
        for c in range(columns):
            print(' %s |' % board[i][c], end='')
        print("\n")

if __name__ == "__main__":
    main()
