from numpy import transpose
from random import randint
from copy import deepcopy
from math import inf

MODES = {'user', 'easy', 'medium', 'hard'}


def new_game():
    commands = input('Input command: ').split()
    while not check_command(*commands):
        print('Bad parameters!')
        commands = input('Input command: ').split()
    return commands, [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]


def start_cell(start):
    cells.append(start[0:3])
    cells.append(start[3:6])
    cells.append(start[6:9])


def draw():
    print("---------")
    print(f"| {cells[0][0]} {cells[0][1]} {cells[0][2]} |")
    print(f"| {cells[1][0]} {cells[1][1]} {cells[1][2]} |")
    print(f"| {cells[2][0]} {cells[2][1]} {cells[2][2]} |")
    print("---------")


def check_occupation(y, x):
    if cells[y - 1][x - 1] == ' ':
        return True
    else:
        return False


def check_coord(coord):
    try:
        y = int(coord[0])
    except ValueError:
        print('You should enter numbers!')
        return False
    try:
        x = int(coord[1])
    except ValueError:
        print('You should enter numbers!')
        return False
    try:
        cells[y - 1][x - 1]
    except IndexError:
        print('Coordinates should be from 1 to 3!')
        return False
    if check_occupation(y, x):
        return True
    else:
        print('This cell is occupied! Choose another one!')
        return False


def check_stage(board):
    for row in board:
        if "O" not in row and " " not in row:
            return "X wins"
        if "X" not in row and " " not in row:
            return "O wins"
    t_cells = deepcopy(board)
    t_cells = transpose(t_cells)
    for row in t_cells:
        if "O" not in row and " " not in row:
            return "X wins"
        if "X" not in row and " " not in row:
            return "O wins"
    if board[0][0] == board[1][1] == board[2][2]:
        if board[0][0] == "X":
            return "X wins"
        if board[0][0] == "O":
            return "O wins"
    if board[0][2] == board[1][1] == board[2][0]:
        if board[1][1] == "X":
            return "X wins"
        if board[1][1] == "O":
            return "O wins"
    for row in board:
        if " " in row:
            return "Game not finished"
    return "Draw"


def which_sign():
    x_num = 0
    o_num = 0
    for row in cells:
        x_num += row.count('X')
        o_num += row.count('O')
    if x_num == o_num:
        return 'X'
    return 'O'


def make_random_move():
    y = randint(0, 2)
    x = randint(0, 2)
    while not check_occupation(y + 1, x + 1):
        y = randint(0, 2)
        x = randint(0, 2)
    cells[y][x] = which_sign()


def computer_move_easy():
    make_random_move()
    print('Making move level "easy"')


def check_possible_win(sign):
    for y in range(len(cells)):
        if cells[y].count(sign) == 2 and ' ' in cells[y]:
            x = cells[y].index(' ')
            cells[y][x] = which_sign()
            return False
    t_cells = deepcopy(cells)
    t_cells = transpose(t_cells).tolist()
    for x in range(len(t_cells)):
        if t_cells[x].count(sign) == 2 and ' ' in t_cells[x]:
            y = t_cells[x].index(' ')
            cells[y][x] = which_sign()
            return False
    # first d
    if cells[0][0] == cells[1][1] == sign and cells[2][2] == ' ':
        cells[2][2] = which_sign()
        return False
    if cells[0][0] == cells[2][2] == sign and cells[1][1] == ' ':
        cells[1][1] = which_sign()
        return False
    if cells[1][1] == cells[2][2] == sign and cells[0][0] == ' ':
        cells[0][0] = which_sign()
        return False
    # second d
    if cells[2][0] == cells[1][1] == sign and cells[0][2] == ' ':
        cells[0][2] = which_sign()
        return False
    if cells[0][2] == cells[1][1] == sign and cells[2][0] == ' ':
        cells[2][0] = which_sign()
        return False
    if cells[0][2] == cells[2][0] == sign and cells[1][1] == ' ':
        cells[1][1] = which_sign()
        return False
    return True


def computer_move_medium():
    if check_possible_win(which_sign()):
        if which_sign() == 'O':
            another_side = 'X'
        else:
            another_side = 'O'
        if check_possible_win(another_side):
            make_random_move()
    print('Making move level "medium"')


def empty_cells(board):
    empty = []
    for y in range(len(board)):
        for x in range(len(board)):
            if board[y][x] == ' ':
                empty.append([y, x])
    return empty


def minimax(me, sign, back_up):
    if me:
        best = [-1, -1, -inf]
    else:
        best = [-1, -1, +inf]

    if sign == 'X':
        another_sign = 'O'
    else:
        another_sign = 'X'

    if check_stage(back_up) != 'Game not finished':
        if check_stage(back_up) == f'{which_sign()} wins':
            return [-1, -1, +1]
        elif check_stage(back_up) == 'Draw':
            return [-1, -1, 0]
        else:
            return [-1, -1, -1]

    for cell in empty_cells(back_up):
        y, x = cell[0], cell[1]
        back_up[y][x] = sign
        score = minimax(not me, another_sign, deepcopy(back_up))
        back_up[y][x] = ' '
        score[0], score[1] = y, x
        if me:
            if score[2] > best[2]:
                best = score
        else:
            if score[2] < best[2]:
                best = score
    return best


def computer_move_hard():
    print('Making move level "hard"')
    back_up_board = deepcopy(cells)
    if len(empty_cells(cells)) == 9:
        cells[1][0] = 'X'
    else:
        res = minimax(True, which_sign(), back_up_board)
        cells[res[0]][res[1]] = which_sign()


def new_move():
    coord = list(input('Enter the coordinates: ').split())
    while not check_coord(coord):
        coord = list(input('Enter the coordinates: ').split())
    cells[int(coord[0]) - 1][int(coord[1]) - 1] = which_sign()


def check_command(*commands):
    if len(commands) < 1:
        return False
    if commands[0] == 'start' and len(commands) == 3:
        if commands[1] in MODES and commands[1] in MODES:
            return True
    if commands[0] == 'exit' and len(commands) == 1:
        return True
    return False


command, cells = new_game()
while command[0] != 'exit':
    draw()
    player = 1
    while check_stage(cells) == 'Game not finished':
        if command[player] == 'user':
            new_move()
        elif command[player] == 'easy':
            computer_move_easy()
        elif command[player] == 'medium':
            computer_move_medium()
        else:
            computer_move_hard()
        draw()
        if player == 1:
            player = 2
        else:
            player = 1
    print(check_stage(cells))
    print()
    command, cells = new_game()
