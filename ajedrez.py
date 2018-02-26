import random

#################################################################
####################### Global Variables ########################
#################################################################

## Contants
WHITE       = "white"
BLACK       = "black"

WHITE_QUEEN = 'Q'
WHITE_KING  = 'K'
BLACK_KING  = 'k'
BLACK_QUEEN = 'q'

EASY        = '1'
NORMAL      = '2'
HARD        = '3'

EMP= ' '
INITIAL_POS = -1

## Variables
level = EASY           #default
list_pieces = []
player_color = WHITE   #default

# Chess Table (Matrix 8x8)
#         a    b    c    d    e    f    g    h
# col     0    1    2    3    4    5    6    7      # row   #
table = [[EMP, EMP, EMP, EMP, EMP, EMP, EMP, EMP],  # 0     # 8
         [EMP, EMP, EMP, EMP, EMP, EMP, EMP, EMP],  # 1     # 7
         [EMP, EMP, EMP, EMP, EMP, EMP, EMP, EMP],  # 2     # 6
         [EMP, EMP, EMP, EMP, EMP, EMP, EMP, EMP],  # 3     # 5
         [EMP, EMP, EMP, EMP, EMP, EMP, EMP, EMP],  # 4     # 4
         [EMP, EMP, EMP, EMP, EMP, EMP, EMP, EMP],  # 5     # 3
         [EMP, EMP, EMP, EMP, EMP, EMP, EMP, EMP],  # 6     # 2
         [EMP, EMP, EMP, EMP, EMP, EMP, EMP, EMP]]  # 7     # 1

#################################################################
############################ Classes ############################
#################################################################

################ Pieces ##################

class Piece:
    row = INITIAL_POS
    col = INITIAL_POS
    is_attacked = False
    color = ""
    key = ''
    name = ""

    def put_piece_into_table(self):
        global table
        table[self.row][self.col] = self.key

    def init_position(self, row, col):
        self.row = row
        self.col = col


class Queen(Piece):

    # Constructor
    def __init__(self, color, row = INITIAL_POS, col = INITIAL_POS):
        self.color = color
        self.name = color.upper() + " QUEEN"
        self.row = row
        self.col = col
        if color == WHITE:
            self.key = WHITE_QUEEN
        else:
            self.key = BLACK_QUEEN

    def is_valid_movement(self, row, col):
        ret = False
        posible_positions = self.get_all_new_positions()

        for pos in posible_positions:
            if row == pos[0] and col == pos[1]:
                ret = True
                break

        return ret

    def set_positions(self, row, col):
        if self.is_valid_movement(row, col):
            self.row = row
            self.col = col
            return True
        else:
            print("Invalid Position")
            return False

    def get_all_new_positions(self):
        list_positions = []

        #Insert positions of current row
        row = self.row
        col = 0

        while col <= 7:
            if row != self.row or col != self.col:
                list_positions.append([row, col])
            col += 1

        #Insert positions of current column
        col = self.col
        row = 0

        while row <= 7:
            if row != self.row or col != self.col:   # Exclude current positions
                list_positions.append([row, col])
            row += 1

        #Insert diagonals
        row = self.row
        col = self.col

        while row <= 7 and col <= 7:
            if row != self.row or col != self.col:   # Exclude current positions
                list_positions.append([row, col])
            row += 1
            col += 1

        row = self.row
        col = self.col

        while row >= 0 and col >= 0:
            if row != self.row or col != self.col:   # Exclude current positions
                list_positions.append([row, col])
            row -= 1
            col -= 1

        row = self.row
        col = self.col

        while row >= 0 and col <= 7:
            if row != self.row or col != self.col:   # Exclude current positions
                list_positions.append([row, col])
            row -= 1
            col += 1

        row = self.row
        col = self.col

        while row <= 7 and col >= 0:
            if row != self.row or col != self.col:   # Exclude current positions
                list_positions.append([row, col])
            row += 1
            col -= 1

        return list_positions

    def get_atacked_places(self):
        # Since the Queen can attack in all posible positions
        # return the positions
        return self.get_all_new_positions()

class King(Piece):

    # Constructor
    def __init__(self, color, row = INITIAL_POS, col = INITIAL_POS):
        self.color = color
        self.name = color.upper() + " KING"
        self.row = row
        self.col = col
        if color == WHITE:
            self.key = WHITE_KING
        else:
            self.key = BLACK_KING

    def is_valid_movement(self, row, col):
        ret = False
        posible_positions = self.get_all_new_positions()

        for pos in posible_positions:
            if row == pos[0] and col == pos[1]:
                ret = True
                break

        return ret

    def set_positions(self, row, col):
        if self.is_valid_movement(row, col):
            self.row = row
            self.col = col
            return True
        else:
            print("Invalid Position")
            return False

    def get_all_new_positions(self):
        def append_valid_positions(list_positions, row):
            col = self.col - 1
            if col >= 0: list_positions.append([row, col])
            col = self.col
            if row != self.row or col != self.col:
                list_positions.append([row, col])
            col = self.col + 1
            if col <= 7: list_positions.append([row, col])

        list_positions = []

        #Previous row
        row = self.row - 1
        if (row >= 0):
            append_valid_positions(list_positions, row)

        #Current Row
        row = self.row
        append_valid_positions(list_positions, row)

        #Next row
        row = self.row + 1
        if (row <= 7):
            append_valid_positions(list_positions, row)

        return list_positions

    def get_atacked_places(self):
        # Since the king can attack in all posible positions
        # return the positions
        return self.get_all_new_positions()

################ Algorithm ##################

class Node:
    piece = None
    min = 0
    max = 0

class Tree:
    root = None

#################################################################
######################### Procedures ############################
#################################################################

################ Console Utils ##################

def get_console_input(str, list_valid_entries):
    is_invalid = True
    inp = None

    while is_invalid:
        inp = input(str)

        #Search if input is valid
        for value in list_valid_entries:
            if value == inp:
                is_invalid = False        # Valid input, break loops
                break

        if is_invalid:
            print("Invalid entry, Try again")

    return inp

def convet_int_to_index(inp):
    return abs(int(inp) - 8)

def convert_asc_to_index(inp):
    return ord(inp) - ord('a')

def convert_index_to_int(ind):
    return abs(ind - 8)

def convert_index_to_asc(ind):
    return chr(ind + ord('a'))

##################### Draw ######################

def print_table():
    print("  a    b    c    d    e    f    g    h")
    i = 8
    for row in table:
        print(row, "{}".format(i))
        i -= 1

############### Table functions #################

def get_piece_position(piece):
    valid_col = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    valid_row = ['1', '2', '3', '4', '5', '6', '7', '8']

    table_col = get_console_input("Select Column position for {} [a - h]: ".format(piece.name), valid_col)
    table_row = get_console_input("Select Row position for {} [1 - 8]: ".format(piece.name), valid_row)

    row = convet_int_to_index(table_row)
    col = convert_asc_to_index(table_col)

    return row, col

def init_piece_position(piece, row, col):
    piece.init_position(row, col)

def set_piece_positions(piece, row, col):
    global table
    prev_row = piece.row
    prev_col = piece.col

    ret = piece.set_positions(row, col)

    if ret == True:
        # clean prev position in table
        table[prev_row][prev_col] = EMP
        # write new position
        table[row][col] = piece.key

    return ret

def are_positions_equals(piece1, piece2):
    if piece1.row == piece2.row and piece1.col == piece2.col:
        return True
    else:
        return False

def get_initial_positions():
    global list_pieces
    i = 0

    print("Insert Initial positions of pieces\n")

    # get positions of pieces
    while i < len(list_pieces):
        piece = list_pieces[i]
        row, col = get_piece_position(piece)
        init_piece_position(piece, row, col)

        #Verify that the position is free
        j = 0
        is_invalid = False
        while j < len(list_pieces):
            if piece != list_pieces[j] and are_positions_equals(piece, list_pieces[j]):
                print("Invalid position, try again")
                is_invalid = True
                break

            j += 1

        if (is_invalid == False):
            i += 1;

def insert_pieces_into_table():
    for piece in list_pieces:
        piece.put_piece_into_table()

def search_attacked_places():
    white_attacks = {}
    black_attacks = {}

    for piece in list_pieces:
        if piece.color == WHITE:
            # Add list to Dictionary
            white_attacks[piece.key] = piece.get_atacked_places()
        else:     #BLACK
            black_attacks[piece.key] = piece.get_atacked_places()

    return white_attacks, black_attacks

def is_movement_attacked(mov, attacked_places):
    ret = False

    for attack in attacked_places:
        if mov[0] == attack[0] and mov[1] == attack[1]:  # If the place was found
            ret = True
            break

    return ret

def all_movements_are_attacked(movements, attacked_places):
    ret = False
    n = 0

    for mov in movements:
        if is_movement_attacked(mov, attacked_places):
            n += 1       #Increase counter

    if n == len(movements):
        ret = True

    return ret

def is_checkmate():
    white_attacks, black_attacks = search_attacked_places()       #Return a dictionary with the attacked places
    white_attacks_list = []
    black_attacks_list = []
    white_king = get_piece_from_key(WHITE_KING)
    black_king = get_piece_from_key(BLACK_KING)

    movements_white_king = white_king.get_all_new_positions()
    movements_black_king = black_king.get_all_new_positions()

    #Convert Dictionaries in list R1
    for key, value in white_attacks.items():
        #Concatenate list
        white_attacks_list += value

    for key, value in black_attacks.items():
        #Concatenate list
        black_attacks_list += value

    #Add the piece position
    for piece in list_pieces:
        if piece.color == WHITE:
            white_attacks_list.append([piece.row, piece.col])
        else:  #BLACK
            black_attacks_list.append([piece.row, piece.col])
    
    #Check if all movements are attacked
    ret = all_movements_are_attacked(movements_white_king, black_attacks_list)

    if ret == True:
        print("\nCHECKMATE: BLACK WIN")
    else:
        ret = all_movements_are_attacked(movements_black_king, white_attacks_list)
        if ret == True:
            print("\nCHECKMATE: WHITE WIN")

    return ret

def get_not_attacked_places(piece):
    white_attacks, black_attacks = search_attacked_places()
    movements = piece.get_all_new_positions()
    list_attacks = []
    not_attacked_places = []

    # Convert Dictionaries in list R1
    if piece.color == WHITE:
        for key, value in black_attacks.items():
            # Concatenate list
            list_attacks += value
    else:     #BLACK
        for key, value in white_attacks.items():
            # Concatenate list
            list_attacks += value

    for mov in movements:
        if is_movement_attacked(mov, list_attacks) == False:
            not_attacked_places.append(mov)

    return not_attacked_places


################## Algorithm ####################

def minimax(list_of_movements):
    pass

############### Init functions ##################

def create_pieces():
    global list_pieces

    # Create list of pieces
    white_queen = Queen(WHITE)
    white_king = King(WHITE)
    black_king = King(BLACK)

    list_pieces.append(white_queen)
    list_pieces.append(white_king)
    list_pieces.append(black_king)


def init_game():
    global level
    global player_color

    print("********************************************************************************************")
    print("*************************************  CHESS GAME ******************************************")
    print("********************************************************************************************")
    print("\n")
    print("Final stage. Pieces: White Queen, White King, Black King")
    print("\n")
    print_table()
    print("\n")
    level = get_console_input("Select Game Level [1 - Easy, 2 - Normal, 3 - Hard]: ", [EASY, NORMAL, HARD])
    player_color = get_console_input("Select Color [white, black]: ", [WHITE, BLACK])

    create_pieces()
    get_initial_positions()
    insert_pieces_into_table()

    print_table()

############### Play functions ##################

def move_machine_piece(piece):
    movements = get_not_attacked_places(piece)

    #TODO: change this and implement minimax
    pos = random.choice(movements)
    set_piece_positions(piece, pos[0], pos[1])
    print("\nMachine movement [{},{}]\n".format(convert_index_to_asc(pos[1]), convert_index_to_int(pos[0])))

def machine_movement():
    global player_color

    if player_color == WHITE:
        piece = get_piece_from_key(BLACK_KING)
    else:
        #If the color is BLACK the machine always move the WHITE_QUEEN
        #because the king cannot be eaten
        piece = get_piece_from_key(WHITE_QUEEN)

    return move_machine_piece(piece)

def get_piece_from_key(key):
    piece = None

    # Search piece
    for value in list_pieces:
        if value.key == key:
            # Piece found
            piece = value
            break

    return piece

def select_piece_to_move():
    global player_color

    if player_color == WHITE:
        valid_opt = ['K', 'Q']
        key = get_console_input("Select piece to move [K - White King, Q - White Queen]: ", valid_opt)
    else:      #BLACK
        key = BLACK_KING

    return get_piece_from_key(key)


def do_movement():
    piece = select_piece_to_move()
    loop = True

    while loop:
        row, col = get_piece_position(piece)
        is_valid = set_piece_positions(piece, row, col)
        if is_valid == True:
            print("\nMovement [{},{}]\n".format(convert_index_to_asc(col), convert_index_to_int(row)))
            loop = False

def play():
    do_movement()
    print_table()

    machine_movement()
    print_table()

    return is_checkmate() == False

def main():
    init_game()

    while play():       #infinity loop until checkmate
        pass

#When this script is called as main, run the main function
if __name__ == '__main__':
    main()