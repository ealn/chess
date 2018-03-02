import datetime
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

EMP= '-'
INITIAL_POS = -1

INFINITY_POSITIVE = 1000000
INFINITY_NEGATIVE = -1000000

## Variables
g_difficulty = EASY           #default
g_list_pieces = []
g_player_color = WHITE   #default

# Chess Table (Matrix 8x8)
#            a    b    c    d    e    f    g    h
# col        0    1    2    3    4    5    6    7     # row   #
g_table = [[EMP, EMP, EMP, EMP, EMP, EMP, EMP, EMP],  # 0     # 8
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
    color = ""
    key = ''
    name = ""

    def put_piece_into_table(self):
        global g_table
        g_table[self.row][self.col] = self.key

    def init_position(self, row, col):
        self.row = row
        self.col = col

    def __get_piece_at_position(self, row, col):
        global g_list_pieces
        global g_table
        ret = None

        if g_table[row][col] != EMP:
            # search key
            for piece in g_list_pieces:
                if piece.key == g_table[row][col]:
                    ret = piece
                    break

        return ret
    
    def is_there_piece_same_color(self, row, col):
        ret = False
        piece = self.__get_piece_at_position(row, col)
        
        if piece != None and piece.color == self.color:
            ret = True

        return ret
        
    def is_there_piece_other_color(self, row, col):
        ret = False
        piece = self.__get_piece_at_position(row, col)
        
        if piece != None and piece.color != self.color:
            ret = True

        return ret

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
        possible_positions = self.get_all_new_positions()

        for pos in possible_positions:
            if row == pos[0] and col == pos[1]:
                ret = True
                break

        return ret

    def set_positions(self, row, col, showerror = True):
        if self.is_valid_movement(row, col):
            self.row = row
            self.col = col
            return True
        else:
            if showerror:
                print("Invalid Position")
            return False

    def get_all_new_positions(self, check_entire_line = False):
        def append_position(list_positions, row, col):
            break_loop = False

            if row != self.row or col != self.col:  # Exclude current positions
                if self.is_there_piece_same_color(row, col):
                    break_loop = True

                list_positions.append([row, col])

                if not check_entire_line:
                    if self.is_there_piece_other_color(row, col):
                        break_loop = True

            return break_loop

        def append_row_positions(list_positions):
            # Insert positions of current row
            row = self.row
            col = self.col

            while col <= 7:
                if append_position(list_positions, row, col):
                    break
                col += 1

            row = self.row
            col = self.col

            while col >= 0:
                if append_position(list_positions, row, col):
                    break
                col -= 1

        def append_col_positions(list_positions):
            # Insert positions of current column
            row = self.row
            col = self.col

            while row <= 7:
                if append_position(list_positions, row, col):
                    break
                row += 1

            row = self.row
            col = self.col

            while row >= 0:
                if append_position(list_positions, row, col):
                    break
                row -= 1

        def append_diagonal_positions(list_positions):
            # Insert diagonals
            row = self.row
            col = self.col

            while row <= 7 and col <= 7:
                if append_position(list_positions, row, col):
                    break
                row += 1
                col += 1

            row = self.row
            col = self.col

            while row >= 0 and col >= 0:
                if append_position(list_positions, row, col):
                    break
                row -= 1
                col -= 1

            row = self.row
            col = self.col

            while row >= 0 and col <= 7:
                if append_position(list_positions, row, col):
                    break
                row -= 1
                col += 1

            row = self.row
            col = self.col

            while row <= 7 and col >= 0:
                if append_position(list_positions, row, col):
                    break
                row += 1
                col -= 1

        list_positions = []

        append_row_positions(list_positions)
        append_col_positions(list_positions)
        append_diagonal_positions(list_positions)

        return list_positions

    def get_attacked_places(self):
        # Since the Queen can attack in all posible positions
        # return the positions
        return self.get_all_new_positions(check_entire_line = True)

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
        possible_positions = self.get_all_new_positions()

        for pos in possible_positions:
            if row == pos[0] and col == pos[1]:
                ret = True
                break

        return ret

    def set_positions(self, row, col, showerror = True):
        if self.is_valid_movement(row, col):
            self.row = row
            self.col = col
            return True
        else:
            if showerror:
                print("Invalid Position")
            return False

    def get_all_new_positions(self, check_another_king = True):
        def is_there_another_king(row, col):
            valid = False

            # Get the opposing king
            if self.color == WHITE:
                opposing_king = get_piece_from_key(BLACK_KING)
            else:   #Black
                opposing_king = get_piece_from_key(WHITE_KING)
                
            opposing_king_movements = opposing_king.get_all_new_positions(False)
            
            for position in opposing_king_movements:
                if position[0] == row and position[1] == col:
                    valid = True
            
            return valid
            
        def append_valid_positions(list_positions, row):
            col = self.col - 1
            if col >= 0:
                if not self.is_there_piece_same_color(row, col):
                    if check_another_king:
                        if not is_there_another_king(row,col):
                            list_positions.append([row, col])
                    else:
                        list_positions.append([row, col])

            col = self.col
            if row != self.row or col != self.col:    #Don't add current position
                if not self.is_there_piece_same_color(row, col):
                    if check_another_king:
                        if not is_there_another_king(row,col):
                            list_positions.append([row, col])
                    else:
                        list_positions.append([row, col])

            col = self.col + 1
            if col <= 7:
                if not self.is_there_piece_same_color(row, col):
                    if check_another_king:
                        if not is_there_another_king(row,col):
                            list_positions.append([row, col])
                    else:
                        list_positions.append([row, col])

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

    def get_attacked_places(self):
        # Since the king can attack in all posible positions
        # return the positions
        return self.get_all_new_positions()

################ Algorithm ##################

class Node:
    piece = None
    parent = None
    child = None
    next = None
    prev = None
    level = 1
    minimax_value = 0
    minimax_node = None

    def __init__(self, piece, level = 1):
        self.piece = piece
        self.level = level

class Tree:
    top_node = None

    def __init__(self, top_node):
        self.top_node = top_node


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

def print_debug_file(str):
    try:
        debug_file = open("tree.dbg", 'a')
        date = datetime.datetime.now()

        debug_file.write("{}\t:{}\n".format(date,str))
        debug_file.close()
    except Exception as ex:
        print("Exception: ", ex)
    
##################### Draw ######################

def print_table():
    global g_table

    print("  a    b    c    d    e    f    g    h")
    print_debug_file("  a    b    c    d    e    f    g    h")
    
    i = 8
    for row in g_table:
        print("{} {}".format(row, i))
        print_debug_file("{} {}".format(row, i))
        i -= 1

############### Table functions #################
def eat_piece(key):
    global g_list_pieces

    piece = get_piece_from_key(key)
    g_list_pieces.remove(piece)

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

def set_piece_positions(piece, row, col, show_error = True):
    global g_table
    prev_row = piece.row
    prev_col = piece.col

    ret = piece.set_positions(row, col, show_error)

    if ret:
        # Check if this place contains another piece
        if g_table[row][col] != EMP:
            eat_piece(g_table[row][col])

        # clean prev position in table
        g_table[prev_row][prev_col] = EMP
        # write new position
        g_table[row][col] = piece.key

    return ret

def are_positions_equals(piece1, piece2):
    if piece1.row == piece2.row and piece1.col == piece2.col:
        return True
    else:
        return False

def get_initial_positions():
    global g_list_pieces
    i = 0

    print("Insert Initial positions of pieces\n")

    # get positions of pieces
    while i < len(g_list_pieces):
        piece = g_list_pieces[i]
        row, col = get_piece_position(piece)
        init_piece_position(piece, row, col)

        #Verify that the position is free
        j = 0
        is_invalid = False
        while j < len(g_list_pieces):
            if piece != g_list_pieces[j] and are_positions_equals(piece, g_list_pieces[j]):
                print("Invalid position, try again")
                is_invalid = True
                break

            j += 1

        if (is_invalid == False):
            i += 1

def insert_pieces_into_table():
    global g_list_pieces
    for piece in g_list_pieces:
        piece.put_piece_into_table()

def search_attacked_places():
    global g_list_pieces
    white_attacks = {}
    black_attacks = {}

    for piece in g_list_pieces:
        if piece.color == WHITE:
            # Add list to Dictionary
            white_attacks[piece.key] = piece.get_attacked_places()
        else:     #BLACK
            black_attacks[piece.key] = piece.get_attacked_places()

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

    #Check if all movements are attacked
    ret = all_movements_are_attacked(movements_white_king, black_attacks_list)

    if ret:
        print("\nCHECKMATE: BLACK WIN")
    else:
        ret = all_movements_are_attacked(movements_black_king, white_attacks_list)
        if ret:
            print("\nCHECKMATE: WHITE WIN")

    return ret

def is_draw_game():
    global g_list_pieces
    ret = False

    if len(g_list_pieces) == 2 \
        and (g_list_pieces[0].key == WHITE_KING or g_list_pieces[0].key == BLACK_KING) \
        and (g_list_pieces[1].key == WHITE_KING or g_list_pieces[1].key == BLACK_KING):
        ret = True
        print("\n DRAW GAME")

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
        if not is_movement_attacked(mov, list_attacks):
            not_attacked_places.append(mov)

    return not_attacked_places


################## Algorithm ####################

def print_node(node):
    if node != None:
        tab = '\t'
        tab_space = ''
        level = node.level
        
        while level > 1:
            tab_space += tab
            level -= 1
            
        print_debug_file("{}Name: {} Level: {} [{},{}] minimax value = {}".format(tab_space, node.piece.name, node.level, node.piece.row, node.piece.col, node.minimax_value))

def print_tree(top_node):
    if top_node != None:
        print_node(top_node)
    
        if top_node.child != None:
            print_tree(top_node.child)
        if top_node.next != None:
            print_tree(top_node.next)

def heuristic(node):
    value = 0

    if node != None and node.child == None:  #Verify that this node is a leaf
        if node.level % 2 == 0:    # Min
            value = 1
        else:   # Max, the leaf node is a player movement
            # Player win
            value = INFINITY_NEGATIVE

    return value

def get_max(node):
    max = 0
    max_node = None

    if node != None:
        child = node.child

        #Init values with the first child
        if child != None:
            max = child.minimax_value
            max_node = child

        while child != None:
            if child.minimax_value > max:
                max = child.minimax_value
                max_node = child
            child = child.next

    return max, max_node

def get_min(node):
    min = 0
    min_node = None

    if node != None:
        child = node.child

        # Init values with the first child
        if child != None:
            min = child.minimax_value
            min_node = child

        while child != None:
            if child.minimax_value < min:
                min = child.minimax_value
                min_node = child
            child = child.next

    return min, min_node

def minimax(node):
    if node.child != None:
        if node.level % 2 == 0:    #Min
            minimax_v, minimax_n = get_min(node)

        else:                      #Max
            minimax_v, minimax_n = get_max(node)

        node.minimax_value = minimax_v
        node.minimax_node = minimax_n
    else:
        node.minimax_value = heuristic(node)   #Leaf

def search(node):
    if node != None:
        if node.child != None:
            search(node.child)

        minimax(node)

        if node.next != None:
            search(node.next)

def get_best_movement(top_node):
    search(top_node)

    piece = top_node.minimax_node.piece

    return piece.row, piece.col

def create_list_nodes(parent, level, dic_places):
    list_nodes = []

    # Create a list of nodes
    for key, value in dic_places.items():
        for place in value:
            new_piece = None
            row = place[0]
            col = place[1]
    
            # Create pieces and add to the tree
            if key == WHITE_QUEEN:
                # Create a White Queen
                new_piece = Queen(WHITE, row, col)
            elif key == WHITE_KING:
                # Create a White King
                new_piece = King(WHITE, row, col)
            elif key == BLACK_KING:
                # Create a Black King
                new_piece = King(BLACK, row, col)
    
            if new_piece != None:
                node = Node(new_piece, level)
                list_nodes.append(node)

    # Set prev and next nodes
    for index, node in enumerate(list_nodes):
        if index == 0:  # First element
            # only set the next element and parent
            if len(list_nodes) > 1:
                node.next = list_nodes[index + 1]
            parent.child = node
        elif index == len(list_nodes) - 1:  # Last element
            # only set the prev element
            node.prev = list_nodes[index - 1]
        else:
            node.prev = list_nodes[index - 1]
            node.next = list_nodes[index + 1]
         
        node.parent = parent

    return list_nodes

def get_all_parent_nodes(node):
    list_parent_nodes = []
    
    list_parent_nodes.append(node)
    
    while node.parent != None:
        list_parent_nodes.append(node.parent)
        node = node.parent
    
    return list_parent_nodes[::-1]

def modify_list_pieces(parent):
    global g_list_pieces
    
    list_parent_nodes = get_all_parent_nodes(parent)
    
    for node in list_parent_nodes:
        node_piece = node.piece
        piece = get_piece_from_key(node_piece.key)
        ret = set_piece_positions(piece, node_piece.row, node_piece.col, False)
    
def create_backup():
    global g_list_pieces
    global g_table

    #Create backup
    backup_list_pieces = g_list_pieces
    backup_table = g_table

    #Create copy
    copy_list = []
    copy_table = [[EMP, EMP, EMP, EMP, EMP, EMP, EMP, EMP],
                  [EMP, EMP, EMP, EMP, EMP, EMP, EMP, EMP],
                  [EMP, EMP, EMP, EMP, EMP, EMP, EMP, EMP],
                  [EMP, EMP, EMP, EMP, EMP, EMP, EMP, EMP],
                  [EMP, EMP, EMP, EMP, EMP, EMP, EMP, EMP],
                  [EMP, EMP, EMP, EMP, EMP, EMP, EMP, EMP],
                  [EMP, EMP, EMP, EMP, EMP, EMP, EMP, EMP],
                  [EMP, EMP, EMP, EMP, EMP, EMP, EMP, EMP]]

    for piece in g_list_pieces:
        if piece.key == WHITE_KING:
            copy_piece = King(WHITE, piece.row, piece.col)
        elif piece.key == WHITE_QUEEN:
            copy_piece = Queen(WHITE, piece.row, piece.col)
        else:    #BLACK KING
            copy_piece = King(BLACK, piece.row, piece.col)

        copy_list.append(copy_piece)
        copy_table[piece.row][piece.col] = piece.key

    #Set global with the copy
    g_list_pieces = copy_list
    g_table = copy_table

    return backup_list_pieces, backup_table
    
def restore_backup(backup_list_pieces, backup_table):
    global g_list_pieces
    global g_table

    g_list_pieces = backup_list_pieces
    g_table = backup_table

def create_computer_answer(node, level, use_prev_pos = False):
    backup_list_pieces, backup_table = create_backup()
    dic = {}
    
    modify_list_pieces(node)

    if use_prev_pos:
        dic[node.parent.piece.key] = node.parent.piece.get_all_new_positions()
    else:
        dic[node.piece.key] = node.piece.get_all_new_positions()

    list_nodes = create_list_nodes(node, level, dic)
    
    restore_backup(backup_list_pieces, backup_table)

    return list_nodes
    
def create_player_answer(node, level):
    global g_player_color
    backup_list_pieces, backup_table = create_backup()
    
    modify_list_pieces(node)

    white_attacks, black_attacks = search_attacked_places()

    if g_player_color == WHITE:
        dic = white_attacks
    else:
        dic = black_attacks

    list_nodes = create_list_nodes(node, level, dic)

    restore_backup(backup_list_pieces, backup_table)

    return list_nodes

def create_level_computer_answer(parent, level, list_list_nodes):
    def is_there_another_valid_movement(player_node):
        ret = True

        if player_node != None:
            computer_node = player_node.parent
            white_attacks, black_attacks = search_attacked_places()

            if g_player_color == WHITE:
                dic = white_attacks
            else:
                dic = black_attacks

            #If place is attacked
            for key, value in dic.items():
                for place in value:
                    if place[0] == computer_node.piece.row and place[1] == computer_node.piece.col:
                        ret = False
                        break
                if ret == False:
                    break

        return ret

    list_list_computer_nodes = []

    if list_list_nodes == None:
        if parent != None:
            list_computer_nodes = create_computer_answer(parent, level)
            list_list_computer_nodes.append(list_computer_nodes)
    else:
        for list_nodes in list_list_nodes:
            for node in list_nodes:
                if is_there_another_valid_movement(node):
                    list_computer_nodes = create_computer_answer(node, level, True)
                    list_list_computer_nodes.append(list_computer_nodes)

    return list_list_computer_nodes


def create_level_player_answer(parent, level, list_list_nodes):
    list_list_player_nodes = []

    if list_list_nodes == None:
        if parent != None:
            list_player_nodes = create_player_answer(parent, level)
            list_list_player_nodes.append(list_player_nodes)
    else:
        for list_nodes in list_list_nodes:
            for node in list_nodes:
                list_player_nodes = create_player_answer(node, level)
                list_list_player_nodes.append(list_player_nodes)

    return list_list_player_nodes

def create_tree(piece):
    global g_difficulty

    top_node = Node(piece)
    tree = Tree(top_node)

    #Create first level of answers
    list_list_computer_nodes = create_level_computer_answer(top_node, 2, None)

    list_list_player_nodes = create_level_player_answer(None, 3, list_list_computer_nodes)
    list_list_computer_nodes = create_level_computer_answer(None, 4, list_list_player_nodes)

    if g_difficulty >= NORMAL:
        #Create second level
        list_list_player_nodes = create_level_player_answer(None, 5, list_list_computer_nodes)
        list_list_computer_nodes = create_level_computer_answer(None, 6, list_list_player_nodes)

        if g_difficulty >= HARD:
            #Create third level
            list_list_player_nodes = create_level_player_answer(None, 7, list_list_computer_nodes)
            list_list_computer_nodes = create_level_computer_answer(None, 8, list_list_player_nodes)

    return tree

############### Init functions ##################

def create_pieces():
    global g_list_pieces

    # Create list of pieces
    white_queen = Queen(WHITE)
    white_king = King(WHITE)
    black_king = King(BLACK)

    g_list_pieces.append(white_queen)
    g_list_pieces.append(white_king)
    g_list_pieces.append(black_king)


def init_game():
    global g_difficulty
    global g_player_color

    print("********************************************************************************************")
    print("*************************************  CHESS GAME ******************************************")
    print("********************************************************************************************")
    print("\n")
    print("Final stage. Pieces: White Queen, White King, Black King")
    print("\n")
    print_debug_file("********************************************************************************************")
    print_table()
    print("\n")
    g_difficulty = get_console_input("Select Game Level [1 - Easy, 2 - Normal, 3 - Hard]: ", [EASY, NORMAL, HARD])
    g_player_color = get_console_input("Select Color [white, black]: ", [WHITE, BLACK])

    create_pieces()
    get_initial_positions()
    insert_pieces_into_table()

    print_debug_file("Init Game level: {} color: {}".format(g_difficulty, g_player_color))

    print_table()

############### Play functions ##################

def move_machine_piece(piece):
    tree = create_tree(piece)
    row, col = get_best_movement(tree.top_node)
    print_tree(tree.top_node)

    is_valid = set_piece_positions(piece, row, col)
    
    if is_valid:
        print("\nMachine movement: {} to [{},{}]\n".format(piece.name, convert_index_to_asc(col), convert_index_to_int(row)))
        print_debug_file("Machine movement: {} to [{},{}]".format(piece.name, convert_index_to_asc(col), convert_index_to_int(row)))

def machine_movement():
    global g_player_color

    if g_player_color == WHITE:
        piece = get_piece_from_key(BLACK_KING)
    else:
        #Get random the piece to move
        key = random.choice([WHITE_QUEEN, WHITE_KING])
        piece = get_piece_from_key(key)

    return move_machine_piece(piece)

def get_piece_from_key(key):
    global g_list_pieces
    piece = None

    # Search piece
    for value in g_list_pieces:
        if value.key == key:
            # Piece found
            piece = value
            break

    return piece

def select_piece_to_move():
    global g_player_color

    if g_player_color == WHITE:
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
        if is_valid:
            print("\nMovement {} to [{},{}]\n".format(piece.name, convert_index_to_asc(col), convert_index_to_int(row)))
            print_debug_file("Movement {} to [{},{}]".format(piece.name, convert_index_to_asc(col), convert_index_to_int(row)))
            loop = False

def is_valid_another_movement():
    ret = True
    
    if is_checkmate() or is_draw_game():
        ret = False
    
    return ret
            
           
def play():
    loop = True

    while loop:    #infinity loop until checkmate or draw game
        loop = is_valid_another_movement()
        
        if loop:
            do_movement()
            print_table()
        
            loop = is_valid_another_movement()
            
            if loop:
                machine_movement()
                print_table()

    return loop

def main():
    init_game()
    play()

#When this script is called as main, run the main function
if __name__ == '__main__':
    main()