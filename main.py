import random
import os
import time
from sets import *

running = True


def clear():
    os.system('cls')


def banner():
    print("=" * 64)


def error_input():
    print("=" * 14)
    clear()
    print("Invalid input...")
    time.sleep(1)
    clear()


def random_pieces(pieces, n, equal=False):
    out = random.sample(pieces, n)
    if equal is False:
        for x in ["k", "K"]:
            out.append(x)
    else:
        out.append("k")
    return out


def generate_fen(pieces_old):
    pawns = []
    pieces = []
    check = True
    random.shuffle(pieces_old)
    for i in range(len(pieces_old)):
        if pieces_old[i] in ("p", "P"):
            pawns.append(pieces_old[i])
        else:
            pieces.append(pieces_old[i])
    while check is True:
        check = False
        random_squares = random.sample(range(1, 65), len(pieces))
        random_squares_pawns = random.sample(range(9, 57), len(pawns))
        random_squares.sort()
        random_squares_pawns.sort()
        check = any(item in random_squares for item in random_squares_pawns)

    pieces_dict = {random_squares[i]: pieces[i] for i in range(len(pieces))}
    pawns_dict = {random_squares_pawns[i]: pawns[i] for i in range(len(pawns))}
    pieces_dict.update(pawns_dict)
    print(pieces_dict)
    placed = []
    temp = []
    final = []
    visual = []
    for i in range(1, 65):
        if i in pieces_dict.keys():
            placed.append(pieces_dict[i])
        else:
            placed.append(1)
    row_len = 0
    odd = True
    for square in placed:
        row_len += 1
        if type(square) == int:
            temp.append(square)
            if odd is True:
                if len(visual) % 2 == 0:
                    visual.append("•")
                else:
                    visual.append("◦")
            else:
                if len(visual) % 2 == 0:
                    visual.append("◦")
                else:
                    visual.append("•")
            if row_len == 8:
                odd = not odd
                row_len = 0
                final.append(sum(temp))
                final.append("/")
                temp = []
            else:
                sum(temp)

        elif type(square) is str:
            if len(temp) > 0:
                final.append(sum(temp))
                temp = []
            final.append(square)
            visual.append(square)
            if row_len == 8:
                odd = not odd
                row_len = 0
                final.append("/")
    del final[-1]
    final = ''.join([str(elem) for elem in final])
    return final, visual


def print_menu():
    print("Select Mode:")
    print("1 = input pieces")
    print("2 = random pieces")
    print("3 = equal input pieces")
    print("4 = equal random pieces")
    print("5 = use preset")


def print_naming(equal=False):
    banner()
    print("Please follow the FEN naming conventions:")
    print("\nWhite pieces are capitalized, while black pieces are lowercase.")
    print("P/p = pawn")
    print("Q/q = queen")
    print("B/b = bishop")
    print("N/n = knight")
    print("R/r = rook\n")
    print("Please note that Kings will be added automatically.")
    print("To stop the input type <s>")
    if equal is True:
        print("\nInput ONLY the pieces for one side.")
    banner()


def choose_preset():
    while True:
        clear()
        banner()
        print("Here's a list of presets to choose from\n")
        print("1 = King and Pawn endgame")
        print("2 = Rook endgame")
        print("3 = Pawns and Kings")
        print("4 = Only pieces")
        print("5 = Bishop and Knight vs Rook")
        print("6 = Queen vs Two Rooks")
        print("7 = Queen vs Two Knights and Bishop")
        print("8 = Queen vs Two Bishops and Knight")
        while True:
            choice = input("\n> ").strip()
            if choice in menu_dic.keys():
                return menu_dic[choice]
            else:
                banner()
                clear()
                print("Invalid input...")
                time.sleep(1)


def main():
    clear()
    banner()
    print("Welcome to RandomFEN generator 1.0!\n")
    print_menu()
    choice = input("> ").strip()
    pieces = []
    white_move = True
    retry = "0"
    while choice not in ["1", "2", "3", "4", "5"]:
        banner()
        clear()
        print("Invalid input...")
        time.sleep(1)
        clear()
        print_menu()
        choice = input("> ")

    # ==={INPUT PIECES}===
    if choice == "1":
        piece = ""
        while piece not in ("s", "S"):
            clear()
            print_naming()
            if len(pieces) > 0:
                for x in pieces:
                    print(x, end=" ")
            piece = input("> ").strip()
            if len(pieces) > 0:
                for x in pieces:
                    print(x, end=" ")
            if piece in all_pieces:
                pieces.append(piece)
            elif piece not in ("s", "S"):
                banner()
                clear()
                print("Invalid input...")
                time.sleep(1)
        for king in ("k", "K"):
            pieces.append(king)

    # ==={RANDOM PIECES}===
    elif choice == "2":
        n = ""
        while n.isdecimal() is False:
            clear()
            print("How many random pieces would you like to generate, Kings excluded?")
            n = input("> ").strip()
            if n.isdecimal() is True:
                if int(n) > 32:
                    n = ""
                    print("\nYou can't generate more than the standard 32 pieces")
                    time.sleep(1.5)
                else:
                    pieces = random_pieces(all_pieces, int(n))
            else:
                clear()
                banner()
                print("Invalid input...")
                time.sleep(1)

    # ==={INPUT PIECES EQUAL}===
    elif choice == "3":
        pieces_black = []
        while True:
            clear()
            print_naming(equal=True)
            if len(pieces_black) > 0:
                for x in pieces_black:
                    print(x, end=" ")
            piece = input("> ").strip().lower()
            if piece == "s":
                break
            elif piece in all_pieces:
                pieces_black.append(piece)
            else:
                banner()
                clear()
                print("Invalid input...")
                time.sleep(1)
        for i in pieces_black:
            pieces.append(i)
            pieces.append(i.upper())
        for king in ("k", "K"):
            pieces.append(king)

    # ==={RANDOM PIECES EQUAL}===
    elif choice == "4":
        pieces_b = []
        n = ""
        while n.isdecimal() is False:
            clear()
            print("How many random pieces PER SIDE would you like to generate, Kings excluded?")
            print("(High numbers will most likely result in an invalid position)")
            n = input("> ").strip()
            if n.isdecimal() is True:
                if int(n) > 16:
                    n = ""
                    print("\nYou can't generate more than the standard 16 pieces per side")
                    time.sleep(1.5)
                else:
                    pieces_b = random_pieces(all_pieces_b, int(n), equal=True)
            else:
                clear()
                banner()
                print("Invalid input...")
                time.sleep(1)
        for x in pieces_b:
            pieces.append(x)
            pieces.append(x.upper())

    # ==={PRESET}===
    if choice == "5":
        pieces = choose_preset()

    # ===[COLOR SELECTION]===
    who_moves = ""
    while who_moves not in ("0", "1"):
        clear()
        print("Whose turn is it?")
        print("0 = white")
        print("1 = black")
        who_moves = input("> ")
        if who_moves == "0":
            white_move = True
        elif who_moves == "1":
            white_move = False
        else:
            banner()
            clear()
            print("Invalid input...")
            time.sleep(1)
            clear()
    while retry == "0":
        clear()
        print("Generating...")
        time.sleep(1)
        clear()
        fen, visual = generate_fen(pieces)
        print("Generation successful:")
        print(fen, end=" ")
        if white_move is True:
            print("w - - 0 1\n")
        else:
            print("b - - 0 1\n")
        retry = ""
        x = 0
        y = 0
        print("Preview: ")
        for lit in ("a", "b", "c", "d", "e", "f", "g", "h"):
            print("  " + lit, end="")
        print("")
        for i in range(64):
            if x == 7:
                print("  " + visual[i] + f"  {y + 1}")
                x = 0
                y += 1
            else:
                print("  " + visual[i], end="")
                x += 1

        while retry not in ("0", "1", "2"):
            print("\nGenerate again?")
            print("0 = same pieces")
            print("1 = restart")
            print("2 = exit")
            retry = input("> ")
            if retry == "2":
                run_script = False
                return run_script
            elif retry == "1":
                run_script = True
                return run_script
            elif retry == "0":
                clear()
                pass
            else:
                error_input()


while running is True:
    clear()
    running = main()
