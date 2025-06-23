


def create_board():
    board = [
        ["r", "n", "b", "q", "k", "b", "n", "r"],
        ["p"] * 8,
        ["."] * 8,
        ["."] * 8,
        ["."] * 8,
        ["."] * 8,
        ["P"] * 8,
        ["R", "N", "B", "Q", "K", "B", "N", "R"]
            ]
    return  board

def print_board(board):
    WHITE = '\033[97m'
    BLACK = '\033[90m'
    RESET = '\033[0m'
    BG1 = '\033[47m'
    BG2 = '\033[100m'
    print("     a   b   c   d   e   f   g   h")
    print("    ------------------------------")
    for i in range(8):
        print(str(8-i), end= " | ")
        for j in range(8):
            piece = board[i][j]
            bg = BG1 if (i+j) % 2 == 0 else BG2
            if piece == ".":
                display = "   "
            elif piece.isupper():
                display = WHITE + " " + piece + " "
            else:
                display = BLACK +  " " + piece + " "
            print(bg + display + RESET + " ", end="")
        print("| " + str(8-i))
    print("    ------------------------------")
    print("     a   b   c   d   e   f   g   h")

def parse_move(move):
    try:
        start_col = ord(move[0].lower()) - ord("a") #column
        start_row = 8 - int(move[1]) # row
        end_col = ord(move[3].lower()) - ord("a")
        end_row = 8 - int(move[4])
        return (start_row, start_col), (end_row, end_col)
    except:
        return None, None
def apply_move(board, start, end):
    sr, sc = start 
    er, ec = end
    board[er][ec] = board[sr][sc]
    board[sr][sc] = "."

def main():
    board = create_board()
    turn = True
    while True:
        print_board(board)
        print(f"{'White' if turn else 'Black'}'s move (e.g., e2 e4), or  'q' to quit:")
        move = input("  >")
        if move.lower() == 'q':
            print("Game exited.")
            break
        start, end = parse_move(move)
        if start is None or end is None:
            print("Invalid move format")
            continue
        sr, sc = start
        piece = board[sr][sc]
        if piece == ".":
            print("No piece selected")
            continue
        if ((turn and piece.isupper()) or (not turn and piece.islower())):
            apply_move(board, start,end)
            turn = not turn
        else:
            print("Not your piece silly goose")


main()
