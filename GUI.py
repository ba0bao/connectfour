import copy
import random 
import tkinter as tk

def print_board(board):
    for row in board:
        print("|", end="")
        for cell in row:
            print(cell + "|", end="")
        print()
    print("---------------\n")

def check_winner(board, player):

    for row in range(6):
        for col in range(4):
            if board[row][col] == player and \
               board[row][col+1] == player and \
               board[row][col+2] == player and \
               board[row][col+3] == player:
                return True

    for row in range(3):
        for col in range(7):
            if board[row][col] == player and \
               board[row+1][col] == player and \
               board[row+2][col] == player and \
               board[row+3][col] == player:
                return True

    for row in range(3, 6):
        for col in range(4):
            if board[row][col] == player and \
               board[row-1][col+1] == player and \
               board[row-2][col+2] == player and \
               board[row-3][col+3] == player:
                return True

    for row in range(3):
        for col in range(4):
            if board[row][col] == player and \
               board[row+1][col+1] == player and \
               board[row+2][col+2] == player and \
               board[row+3][col+3] == player:
                return True

    return False

def is_full(board):
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True

def evaluate_window(window, player):
    score = 0
    opponent = 'X' if player == 'O' else 'O'
    if window.count(player) == 4:
        score += 100
    elif window.count(player) == 3 and window.count(' ') == 1:
        score += 5
    elif window.count(player) == 2 and window.count(' ') == 2:
        score += 2

    if window.count(opponent) == 3 and window.count(' ') == 1:
        score -= 4

    return score

def score_position(board, player):
    score = 0
    center_array = [i for i in [col[4] for col in board]]
    center_count = center_array.count(player)
    score += center_count * 3

    for r in range(6):
        row_array = [i for i in board[r]]
        for c in range(4):
            window = row_array[c:c+4]
            score += evaluate_window(window, player)

    for c in range(7):
        col_array = [col[c] for col in board]
        for r in range(3):
            window = col_array[r:r+4]
            score += evaluate_window(window, player)

    # m is+ve
    for r in range(3):
        for c in range(4):
            window = [board[r+i][c+i] for i in range(4)]
            score += evaluate_window(window, player)

    #diag?
    for r in range(3):
        for c in range(4):
            window = [board[r+3-i][c+i] for i in range(4)]
            score += evaluate_window(window, player)

    return score

def minimax(board, depth, maximizing_player):
    valid_locations = [col for col in range(7) if board[0][col] == ' ']
    is_terminal_node = is_full(board) or check_winner(board, 'X') or check_winner(board, 'O')

    if is_terminal_node or depth == 0:
        if is_terminal_node:
            if check_winner(board, 'X'):
                return (None, 100000000000000)
            elif check_winner(board, 'O'):
                return (None, -10000000000000)
            else:
                return (None, 0)
        else:
            return (None, score_position(board, 'X'))

    if maximizing_player:
        value = -10000000000000
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = next_empty_row(board, col)
            temp_board = copy.deepcopy(board)
            drop_piece(temp_board, row, col, 'X')
            new_score = minimax(temp_board, depth-1, False)[1]
            if new_score > value:
                value = new_score
                column = col
        return column, value
    else:
        value = 10000000000000
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = next_empty_row(board, col)
            temp_board = copy.deepcopy(board)
            drop_piece(temp_board, row, col, 'O')
            new_score = minimax(temp_board, depth-1, True)[1]
            if new_score < value:
                value = new_score
                column = col
        return column, value

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def next_empty_row(board, col):
    for r in range(5, -1, -1):
        if board[r][col] == ' ':
            return r

def player_move(board, col):
    row = next_empty_row(board, col)
    if row is not None:
        drop_piece(board, row, col, 'O')
        return True
    return False

def computer_move(board, level):
    valid_locations = [col for col in range(7) if board[0][col] == ' ']
    if level == 'easy':
        col = random.randint(0, (len(valid_locations) - 1))
        col = valid_locations[col]
    elif level == 'medium':
        col, _ = minimax(board, 4, True)
    elif level == 'hard':
        col, _ = minimax(board, 6, True)
    row = next_empty_row(board, col)
    if row is not None:
        drop_piece(board, row, col, 'X')
        return True
    return False

class ConnectFourGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Connect Four")

        self.board = [[' ' for _ in range(7)] for _ in range(6)]
        self.buttons = []

        self.create_buttons()

    def create_buttons(self):
        for i in range(6):
            row_buttons = []
            for j in range(7):
                button = tk.Button(self.master, text=' ', width=4, height=2, command=lambda i=i, j=j: self.button_click(i, j))
                button.grid(row=i, column=j)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

    def button_click(self, row, col):
        if player_move(self.board, col):
            self.update_board()
            if check_winner(self.board, 'O'):
                print("You win!")
                self.disable_buttons()
            elif is_full(self.board):
                print("It's a tie!")

                self.disable_buttons()
            else:
                self.computer_turn('medium')
    def update_board(self):
        for i in range(6):
            for j in range(7):
                self.buttons[i][j].config(text=self.board[i][j])

    def computer_turn(self, level):
        if computer_move(self.board, level):
            self.update_board()
            if check_winner(self.board, 'X'):
                print("Computer wins!")
                self.disable_buttons()
            elif is_full(self.board):
                print("It's a tie!")
                self.disable_buttons()

    def disable_buttons(self):
        for i in range(6):
            for j in range(7):
                self.buttons[i][j].config(state=tk.DISABLED)

def main():
    print("Choose difficulty level:")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")
    choice = input("Enter your choice (1/2/3): ")

    if choice == '1':
        difficulty = 'easy'
    elif choice == '2':
        difficulty = 'medium'
    elif choice == '3':
        difficulty = 'hard'
    else:
        print("Invalid, setting to medium")
        difficulty = 'medium'

    root = tk.Tk()
    game = ConnectFourGUI(root)

    while True:
        game.computer_turn(difficulty)

        root.update()

        player_col = input("Enter column (0-6): ")
        if player_col.isdigit():
            player_col = int(player_col)
            if 0 <= player_col <= 6:
                if game.buttons[0][player_col]['state'] != tk.DISABLED:
                    if player_move(game.board, player_col):
                        game.update_board()
                    else:
                        print("column full!")
                        continue
                else:
                    print("column full!")
                    continue
            else:
                print("Invalid column")
                continue
        else:
            print("Invalid input")
            continue

        if check_winner(game.board, 'O'):
            print("You win!")
            break
        elif is_full(game.board):
            print("Tie!")
            break

        root.update()

    root.mainloop()

if __name__ == "__main__":
    main()
