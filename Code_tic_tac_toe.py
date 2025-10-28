# tic_tac_toe.py
# Simple Tic-Tac-Toe game with Human vs Human and Human vs Computer (Minimax).
# Works in Python 3.6+



from typing import List, Optional, Tuple
import math
import random

# Board positions: indices 0..8
# Display positions to user as 1..9

def print_board(board: List[str]) -> None:
    """Print the current board in a friendly 3x3 layout."""
    display = [c if c != ' ' else str(i+1) for i, c in enumerate(board)]
    print()
    print(f" {display[0]} | {display[1]} | {display[2]} ")
    print("---+---+---")
    print(f" {display[3]} | {display[4]} | {display[5]} ")
    print("---+---+---")
    print(f" {display[6]} | {display[7]} | {display[8]} ")
    print()

def check_winner(board: List[str]) -> Optional[str]:
    """Return 'X' or 'O' if there's a winner, 'Tie' if tie, or None if game ongoing."""
    wins = [
        (0,1,2), (3,4,5), (6,7,8),  # rows
        (0,3,6), (1,4,7), (2,5,8),  # cols
        (0,4,8), (2,4,6)            # diagonals
    ]
    for a,b,c in wins:
        if board[a] == board[b] == board[c] and board[a] != ' ':
            return board[a]
    if ' ' not in board:
        return 'Tie'
    return None

def available_moves(board: List[str]) -> List[int]:
    return [i for i, c in enumerate(board) if c == ' ']

def minimax(board: List[str], depth: int, is_maximizing: bool, player: str, opponent: str) -> int:
    """Minimax algorithm.
    Returns score: +10 - depth for player win, -10 + depth for opponent win, 0 for tie.
    Depth used to prefer faster wins / slower losses.
    """
    result = check_winner(board)
    if result == player:
        return 10 - depth
    elif result == opponent:
        return -10 + depth
    elif result == 'Tie':
        return 0

    if is_maximizing:
        best_score = -math.inf
        for move in available_moves(board):
            board[move] = player
            score = minimax(board, depth+1, False, player, opponent)
            board[move] = ' '
            best_score = max(best_score, score)
        return best_score
    else:
        best_score = math.inf
        for move in available_moves(board):
            board[move] = opponent
            score = minimax(board, depth+1, True, player, opponent)
            board[move] = ' '
            best_score = min(best_score, score)
        return best_score

def best_move_for_computer(board: List[str], comp: str, human: str) -> int:
    """Return the best move index for the computer using minimax."""
    best_score = -math.inf
    candidates = []
    for move in available_moves(board):
        board[move] = comp
        score = minimax(board, 0, False, comp, human)
        board[move] = ' '
        if score > best_score:
            best_score = score
            candidates = [move]
        elif score == best_score:
            candidates.append(move)
    # if multiple equally best moves, pick randomly among them
    return random.choice(candidates)

def human_turn(board: List[str], symbol: str) -> None:
    while True:
        try:
            choice = input(f"Player {symbol}, enter position (1-9): ").strip()
            if choice.lower() in ('q', 'quit', 'exit'):
                print("Exiting game. Goodbye!")
                exit(0)
            pos = int(choice) - 1
            if pos < 0 or pos > 8:
                print("Invalid position. Choose 1 through 9.")
                continue
            if board[pos] != ' ':
                print("That cell is already taken. Choose another.")
                continue
            board[pos] = symbol
            break
        except ValueError:
            print("Please enter a number 1-9 (or 'q' to quit).")

def play_game(vs_computer: bool) -> None:
    board = [' '] * 9
    # Decide symbols and who goes first
    human_symbol = 'X'
    comp_symbol = 'O'
    current = 'X'  # X always goes first

    if vs_computer:
        # Ask player preference: choose X or O
        while True:
            s = input("Do you want to be X (goes first) or O (goes second)? [X/O]: ").strip().upper()
            if s in ('X','O'):
                human_symbol = s
                comp_symbol = 'O' if s == 'X' else 'X'
                break
            print("Please type X or O.")
        print(f"You are {human_symbol}. Computer is {comp_symbol}.")
        current = 'X'  # X always starts

    else:
        print("2-player mode. Player X goes first.")

    print_board(board)

    while True:
        if vs_computer and current == comp_symbol:
            print("Computer's turn...")
            move = best_move_for_computer(board, comp_symbol, human_symbol)
            board[move] = comp_symbol
        else:
            # human move (if vs_computer and it's human_symbol's turn, or in 2-player both are human)
            human_turn(board, current)

        print_board(board)
        result = check_winner(board)
        if result is not None:
            if result == 'Tie':
                print("It's a tie!")
            else:
                if vs_computer:
                    if result == human_symbol:
                        print("Congratulations — you win!")
                    elif result == comp_symbol:
                        print("Computer wins. Better luck next time!")
                    else:
                        # shouldn't hit
                        print(f"{result} wins!")
                else:
                    print(f"Player {result} wins!")
            break

        # switch player
        current = 'O' if current == 'X' else 'X'

def main() -> None:
    print("Welcome to Tic-Tac-Toe!")
    print("Modes:")
    print(" 1. 2-player (human vs human)")
    print(" 2. Play vs computer (unbeatable)")
    while True:
        choice = input("Choose mode 1 or 2 (or 'q' to quit): ").strip()
        if choice == '1':
            play_game(vs_computer=False)
            break
        elif choice == '2':
            play_game(vs_computer=True)
            break
        elif choice.lower() in ('q','quit','exit'):
            print("Goodbye!")
            return
        else:
            print("Invalid choice. Enter 1 or 2.")

    # ask to replay
    while True:
        again = input("Play again? (y/n): ").strip().lower()
        if again == 'y':
            main()
            return
        elif again == 'n':
            print("Thanks for playing!")
            return
        else:
            print("Enter y or n.")

if __name__ == "__main__":
    main()
