import pygame
import copy
import random
import os
import sys
import json
flaggiewaggie = False
extra1 = True
#try:
#    with open('board.json', 'r') as file:
#        data = json.load(file)
#        if data[0] == True:
#            anton = data[1]
#            board = data[2]
#            curplay = data[3]
#            p1time = data[4]
#            p2time = data[5]
            #flaggiewaggie = True
            #sadge
#            raise FileNotFoundError
#except FileNotFoundError:
#    None
# Initialize Pygame
pygame.init()

# Set up the screen
screen_width, screen_height = 800, 825
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Chess")
started = False
# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
LIGHT_SQUARE = (234, 235, 200)
#former LS LIGHT_SQUARE = (232, 235, 239)
DARK_SQUARE = (100, 134, 68)
#former DS DARK_SQUARE = (125, 135, 150)
SELECTED_COLOR = (0, 255, 0)
FONT = pygame.font.Font(None, 45)
timefont = pygame.font.Font(None, 25)


king_pos = None
RONALDO = None
players = ['w','b']
curplay = 0 if flaggiewaggie != True else curplay
game_over = False
# Load chess piece images
pieces = {}
for color in ["w", "b"]: #made by chatgpt because apparently my checkers draw_pieces function was inefficient
    for piece in ["K", "Q", "R", "B", "N", "P"]:
        img = pygame.image.load(f"assets/{color}{piece}.png")
        pieces[color + piece] = pygame.transform.scale(img, (80, 80)) #i know how on earth this works
rooks_moved = [False, False, False, False] #TL, TR, BL, BR
kings_moved = [False, False] #wK, bK
inpro = False
timerfont = False
# Define the chess board
board = [
    ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
    ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
    ["",    "",   "",   "",   "",   "",   "",   ""],
    ["",    "",   "",   "",   "",   "",   "",   ""],
    ["",    "",   "",   "",   "",   "",   "",   ""],
    ["",    "",   "",   "",   "",   "",   "",   ""],
    ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
    ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
] if flaggiewaggie != True else board

board2 = [
    ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
    ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
    ["",    "",   "",   "",   "",   "",   "",   ""],
    ["",    "",   "",   "",   "",   "",   "",   ""],
    ["",    "",   "",   "",   "",   "",   "",   ""],
    ["",    "",   "",   "",   "",   "",   "",   ""],
    ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
    ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
]
possibles = []
selected_piece = None # start game without a piece selected


clock = pygame.time.Clock() #reminder: make turn timer

def draw_text(text, x, y, color):
    if timerfont == False:
        text_surface = FONT.render(text, True, color)
    else: text_surface = timefont.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)
    
abc = []
bruh = []

def numkeypress(key):
    if key == pygame.K_KP_0 or key == pygame.K_0: return '0'
    elif key == pygame.K_KP_1 or key == pygame.K_1: return '1'
    elif key == pygame.K_KP_2 or key == pygame.K_2: return '2'
    elif key == pygame.K_KP_3 or key == pygame.K_3: return '3'
    elif key == pygame.K_KP_4 or key == pygame.K_4: return '4'
    elif key == pygame.K_KP_5 or key == pygame.K_5: return '5'
    elif key == pygame.K_KP_6 or key == pygame.K_6: return '6'
    elif key == pygame.K_KP_7 or key == pygame.K_7: return '7'
    elif key == pygame.K_KP_8 or key == pygame.K_8: return '8'
    elif key == pygame.K_KP_9 or key == pygame.K_9: return '9'
    else: return None
    
anton = 0 if flaggiewaggie != True else anton
editing = 'None'
edi = []
finedit = False
treset = False
shouffle = False
testtime = 0
brah = 0
def custom():
    global editing, anton, edi, p1time, p2time, finedit, treset, testtime, curplay, kings_moved, shouffle, extra1, brah
    clock.tick(60)
    mx = my = 0
    pygame.draw.rect(screen, WHITE, [0, 450, 800, 5]); pygame.draw.rect(screen, WHITE, [0, 300, 800, 5]); pygame.draw.rect(screen, WHITE, [0, 100, 800, 5]); pygame.draw.rect(screen, WHITE, [500, 0, 5, 100])
    draw_text(f'Esc to exit to main menu.', 225, 50, (255, 255, 0))
    draw_text(f'Click to begin.', 660, 50, (40, 200, 40))
    
    draw_text(f'Starting timer:', 140, 350, WHITE)
    draw_text(f'{p1time}', 360, 350, RED)
    draw_text(f'Seconds.', 550, 350, WHITE)
    
    draw_text(f"Timer resets after player's turn ends?:", 315, 420, WHITE)
    draw_text(f'{treset}', 650, 420, RED)
    
    draw_text(f"Beginning player:", 150, 150, WHITE)
    draw_text(f"{'white' if players[curplay] == 'w' else 'black'}", 340, 150, RED)

    draw_text(f"Shuffle mode:", 120, 240, WHITE)
    draw_text(f"{shouffle}", 275, 240, RED)

    draw_text(f"Piece movement Mode:", 190, 520, WHITE)
    draw_text(f"{(['Simple Click.', 'Click n Drag'])[brah]}", 500, 520, RED)



    if editing == 'BT':
        pygame.draw.rect(screen, BLACK, [320, 330, 50, 40])
        if len(edi) > 0: draw_text(f'{int(''.join(edi))}', 360, 350, RED)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if len(edi) == 4: p1time = int(''.join(edi)); editing = 'None'
                if numkeypress(event.key) != None: edi.append(numkeypress(event.key))
                if event.key == pygame.K_RETURN:
                    if len(edi) == 0:edi = ['0']
                    p1time = int(''.join(edi))
                    editing = 'None'
                    
    if editing == 'None':
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mx, my = pygame.mouse.get_pos()
                    if abs(mx - 337) < 100 and abs(my - 346) < 10: #start timer
                        p1time = 0
                        edi = []
                        editing = 'BT'
                    elif abs(mx - 650) < 25 and abs(my - 420) < 25: #timer reset
                        treset = not treset
                    elif abs(mx - 340) < 25 and abs(my - 150) < 25: #starting player
                        curplay = 1 - curplay
                    elif abs(mx - 275) < 25 and abs(my - 240) < 25: #shuffle mode
                        shouffle = not shouffle
                    elif abs(mx - 500) < 100 and abs(my - 520) < 20: #piece mm mode
                        brah = 1 - brah
                    elif abs(mx - 700) < 100 and abs(my - 50) < 10:
                        if shouffle: random.shuffle(board[0]); random.shuffle(board[7])
                        extra1 = False if brah == 1 else True
                        testtime = copy.copy(p1time)
                        p2time = copy.copy(p1time)
                        finedit = True
                        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    anton = 0
                        
                    
                    

selboa = False
def selection():
    global anton, p1time, p2time, selboa, FONT, finedit
    selboa = True
    draw_board()
    selboa = False
    pygame.draw.rect(screen, BLACK, [0, 300, 400, 200])
    pygame.draw.rect(screen, BLACK, [400, 300, 400, 200])
    pygame.draw.rect(screen, BLACK, [200, 500, 400, 200])
    pygame.draw.rect(screen, WHITE, [397, 300, 5, 200])
    pygame.draw.rect(screen, WHITE, [0, 500, 800, 5])
    draw_text('Bullet.', 200, 350, RED)
    draw_text('Standard.', 600, 350, RED)
    draw_text('Custom.', 400, 600, RED)
    FONT = pygame.font.Font(None, 25)
    draw_text('+ extras.', 400, 650, WHITE)
    draw_text('- 30 second timer.', 200, 400, WHITE)
    draw_text('- Timer resets after your move.', 200, 450, WHITE)
    draw_text('- 10 min for each player.', 600, 400, WHITE)
    draw_text('- Timer only counts down on your turn.', 600, 450, WHITE)
    FONT = pygame.font.Font(None, 45)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mx, my = pygame.mouse.get_pos()
                if abs(mx - 200) < 50 and abs(my - 400) < 100:
                    anton = 1
                    p1time = 30
                    p2time = 30

                if abs(mx - 600) < 50 and abs(my - 400) < 100:
                    anton = 2
                    p1time = 600
                    p2time = 600

                if abs(mx - 400) < 50 and abs(my - 600) < 100:
                    anton = 3
                    finedit = False
                    p1time = 600
                    p2time = 0

piece_clicked = False
def handle_events(): #click n drag
    global selected_piece, curplay, running, RONALDO, board, king_pos, abc, p1time,p2time, bruh, piece_clicked, game_over
    promo()
    if is_king_in_check(board, players[curplay]) or is_king_in_check(board, players[1 - curplay]) and inpro == False and game_over == False:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    None
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                row, col = mouse_y // 100, mouse_x // 100
                if selected_piece is not None:
                    if valid_move(selected_piece, row, col, board) and 'K' not in board[row][col]:
                        temp_board = copy.deepcopy(board)
                        temp_board[row][col] = temp_board[selected_piece[0]][selected_piece[1]]
                        temp_board[selected_piece[0]][selected_piece[1]] = ""
                        if not is_king_in_check(temp_board, players[curplay]):
                            board = copy.deepcopy(temp_board)
                            selected_piece = None
                            piece_clicked = False
                            curplay = 1 - curplay
                            savetest([started, anton, board, curplay, p1time, p2time])
                            if anton == 1:
                                p1time = 30
                                p2time = 30
                            if treset == True and finedit == True:
                                p1time = copy.copy(testtime)
                                p2time = copy.copy(testtime)
                            RONALDO = None
                        else:
                            selected_piece = None
                    else:
                        selected_piece = None
                        piece_clicked = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if mouse_y > 800:
                        return
                    row = mouse_y // 100
                    col = mouse_x // 100
                    if selected_piece is None and players[curplay] in board[row][col]:
                        bruh = []
                        selected_piece = (row, col)
                        piece_clicked = True
                        for rowa in range(len(board)):
                            for cola in range(len(board[rowa])):
                                if players[curplay] not in board[rowa][cola]:
                                    if valid_move(selected_piece, rowa, cola, board):
                                        tempo = copy.deepcopy(board); tempo[rowa][cola] = tempo[selected_piece[0]][selected_piece[1]];tempo[selected_piece[0]][selected_piece[1]] = ""
                                        if not is_king_in_check(tempo, players[curplay]):
                                            bruh.append([rowa,cola])
                    elif selected_piece is not None:
                        selected_row, selected_col = selected_piece
                        if (row, col) != (selected_row, selected_col) and players[curplay] in board[row][col]:
                            selected_piece = (row, col)
                            bruh = []
                            for rowa in range(len(board)):
                                for cola in range(len(board[rowa])):
                                    if players[curplay] not in board[rowa][cola]:
                                        if valid_move(selected_piece, rowa, cola, board):
                                            tempo = copy.deepcopy(board); tempo[rowa][cola] = tempo[selected_piece[0]][selected_piece[1]];tempo[selected_piece[0]][selected_piece[1]] = ""
                                            if not is_king_in_check(tempo, players[curplay]):
                                                bruh.append([rowa,cola])
                        elif valid_move(selected_piece, row, col, board):
                            temp_board = copy.deepcopy(board)
                            temp_board[row][col] = temp_board[selected_row][selected_col]
                            temp_board[selected_row][selected_col] = ""
                            if is_king_in_check(temp_board, players[curplay]):
                                #Invalid move: King still in check
                                selected_piece = None
                            elif not is_king_in_check(temp_board, players[curplay]) and 'K' not in board[row][col]:
                                abc = []
                                # Valid move: Update the actual board and switch players
                                RONALDO = None
                                board = copy.deepcopy(temp_board)
                                selected_piece = None
                                if anton == 1:
                                    p1time = 30
                                    p2time = 30
                                if treset == True and finedit == True:
                                    p1time = copy.copy(testtime)
                                    p2time = copy.copy(testtime)
                                curplay = 1 - curplay
                                piece_clicked = False
                                savetest([started, anton, board, curplay, p1time, p2time])

    else:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    None
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                row, col = mouse_y // 100, mouse_x // 100
                if selected_piece is not None:
                    if valid_move(selected_piece, row, col, board) and 'K' not in board[row][col]:
                        temp_board = copy.deepcopy(board)
                        temp_board[row][col] = temp_board[selected_piece[0]][selected_piece[1]]
                        temp_board[selected_piece[0]][selected_piece[1]] = ""
                        if not is_king_in_check(temp_board, players[curplay]):
                            board = copy.deepcopy(temp_board)
                            selected_piece = None
                            piece_clicked = False
                            curplay = 1 - curplay
                            savetest([started, anton, board, curplay, p1time, p2time])
                            if anton == 1:
                                p1time = 30
                                p2time = 30
                            if treset == True and finedit == True:
                                p1time = copy.copy(testtime)
                                p2time = copy.copy(testtime)
                            RONALDO = None
                        else:
                            selected_piece = None
                    else:
                        selected_piece = None
                        piece_clicked = False
            if event.type == pygame.MOUSEBUTTONDOWN and inpro == False and game_over == False:
                if event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if mouse_y > 800: return
                    row = mouse_y // 100
                    col = mouse_x // 100
                    if selected_piece is None and players[curplay] in board[row][col]:
                        bruh = []
                        selected_piece = (row, col)
                        piece_clicked = True
                        for rowa in range(len(board)):
                            for cola in range(len(board[rowa])):
                                if players[curplay] not in board[rowa][cola]:
                                    if valid_move(selected_piece, rowa, cola, board):
                                        tempo = copy.deepcopy(board); tempo[rowa][cola] = tempo[selected_piece[0]][selected_piece[1]];tempo[selected_piece[0]][selected_piece[1]] = ""
                                        if not is_king_in_check(tempo, players[curplay]):
                                            bruh.append([rowa,cola])
                    elif selected_piece is not None:
                        selected_row, selected_col = selected_piece
                        if (row, col) != (selected_row, selected_col) and players[curplay] in board[row][col]:
                            selected_piece = (row, col)
                            piece_clicked = True
                            bruh = []
                            for rowa in range(len(board)):
                                for cola in range(len(board[rowa])):
                                    if players[curplay] not in board[rowa][cola]:
                                        if valid_move(selected_piece, rowa, cola, board):
                                            tempo = copy.deepcopy(board); tempo[rowa][cola] = tempo[selected_piece[0]][selected_piece[1]];tempo[selected_piece[0]][selected_piece[1]] = ""
                                            if not is_king_in_check(tempo, players[curplay]):
                                                bruh.append([rowa,cola])
                        elif valid_move(selected_piece, row, col, board) and 'K' not in board[row][col]:
                            temp_board = copy.deepcopy(board)
                            temp_board[row][col] = temp_board[selected_row][selected_col]
                            temp_board[selected_row][selected_col] = ""
                            if not is_king_in_check(temp_board, players[curplay]):
                                board = copy.deepcopy(temp_board)
                                selected_piece = None
                                piece_clicked = False
                                curplay = 1 - curplay
                                savetest([started, anton, board, curplay, p1time, p2time])
                                if anton == 1:
                                    p1time = 30
                                    p2time = 30
                                if treset == True and finedit == True:
                                    p1time = copy.copy(testtime)
                                    p2time = copy.copy(testtime)
                                RONALDO = None
                            else:
                                selected_piece = None
#handle_events 2 is an absolute redundancy but i don't have the knowledge nor mood to redefine handle_events to properly change to conform to piece movement move
def handle_events2(): #simple click
        global selected_piece, curplay, running, RONALDO, board, king_pos, abc, p1time, p2time, bruh, piece_clicked, game_over, anton
        promo()
        if is_king_in_check(board, players[curplay]) or is_king_in_check(board, players[
            1 - curplay]) and inpro == False and game_over == False:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_over = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        if mouse_y > 800:
                            return
                        row = mouse_y // 100
                        col = mouse_x // 100
                        if selected_piece is None and players[curplay] in board[row][col]:
                            bruh = []
                            selected_piece = (row, col)
                            piece_clicked = True
                            for rowa in range(len(board)):
                                for cola in range(len(board[rowa])):
                                    if players[curplay] not in board[rowa][cola]:
                                        if valid_move(selected_piece, rowa, cola, board):
                                            tempo = copy.deepcopy(board);
                                            tempo[rowa][cola] = tempo[selected_piece[0]][selected_piece[1]];
                                            tempo[selected_piece[0]][selected_piece[1]] = ""
                                            if not is_king_in_check(tempo, players[curplay]):
                                                bruh.append([rowa, cola])
                        elif selected_piece is not None:
                            selected_row, selected_col = selected_piece
                            if (row, col) != (selected_row, selected_col) and players[curplay] in board[row][col]:
                                selected_piece = (row, col)
                                bruh = []
                                for rowa in range(len(board)):
                                    for cola in range(len(board[rowa])):
                                        if players[curplay] not in board[rowa][cola]:
                                            allowcastle = False
                                            if valid_move(selected_piece, rowa, cola, board):
                                                tempo = copy.deepcopy(board);
                                                tempo[rowa][cola] = tempo[selected_piece[0]][selected_piece[1]];
                                                tempo[selected_piece[0]][selected_piece[1]] = ""
                                                if not is_king_in_check(tempo, players[curplay]):
                                                    bruh.append([rowa, cola])
                            elif valid_move(selected_piece, row, col, board):
                                temp_board = copy.deepcopy(board)
                                temp_board[row][col] = temp_board[selected_row][selected_col]
                                temp_board[selected_row][selected_col] = ""
                                if is_king_in_check(temp_board, players[curplay]):
                                    # Invalid move: King still in check
                                    selected_piece = None
                                elif not is_king_in_check(temp_board, players[curplay]) and 'K' not in board[row][col]:
                                    abc = []
                                    # Valid move: Update the actual board and switch players
                                    RONALDO = None
                                    board = copy.deepcopy(temp_board)
                                    selected_piece = None
                                    if anton == 1:
                                        p1time = 30
                                        p2time = 30
                                    if treset == True and finedit == True:
                                        p1time = copy.copy(testtime)
                                        p2time = copy.copy(testtime)
                                    curplay = 1 - curplay
                                    piece_clicked = False
                                    savetest([started, anton, board, curplay, p1time, p2time])

        else:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_over = True

                if event.type == pygame.MOUSEBUTTONDOWN and inpro == False and game_over == False:
                    if event.button == 1:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        if mouse_y > 800: return
                        row = mouse_y // 100
                        col = mouse_x // 100
                        if selected_piece is None and players[curplay] in board[row][col]:
                            bruh = []
                            selected_piece = (row, col)
                            piece_clicked = True
                            for rowa in range(len(board)):
                                for cola in range(len(board[rowa])):
                                    if players[curplay] not in board[rowa][cola]:
                                        if valid_move(selected_piece, rowa, cola, board):
                                            tempo = copy.deepcopy(board);
                                            tempo[rowa][cola] = tempo[selected_piece[0]][selected_piece[1]];
                                            tempo[selected_piece[0]][selected_piece[1]] = ""
                                            if not is_king_in_check(tempo, players[curplay]):
                                                bruh.append([rowa, cola])
                        elif selected_piece is not None:
                            selected_row, selected_col = selected_piece
                            if (row, col) != (selected_row, selected_col) and players[curplay] in board[row][col]:
                                selected_piece = (row, col)
                                piece_clicked = True
                                bruh = []

                                for rowa in range(len(board)):
                                    for cola in range(len(board[rowa])):
                                        if players[curplay] not in board[rowa][cola]:
                                            if valid_move(selected_piece, rowa, cola, board):
                                                tempo = copy.deepcopy(board);
                                                tempo[rowa][cola] = tempo[selected_piece[0]][selected_piece[1]];
                                                tempo[selected_piece[0]][selected_piece[1]] = ""
                                                if not is_king_in_check(tempo, players[curplay]):
                                                    bruh.append([rowa, cola])
                            elif valid_move(selected_piece, row, col, board) and 'K' not in board[row][col]:
                                temp_board = copy.deepcopy(board)
                                temp_board[row][col] = temp_board[selected_row][selected_col]
                                temp_board[selected_row][selected_col] = ""
                                if not is_king_in_check(temp_board, players[curplay]):
                                    board = copy.deepcopy(temp_board)
                                    selected_piece = None
                                    piece_clicked = False
                                    curplay = 1 - curplay
                                    savetest([started, anton, board, curplay, p1time, p2time])
                                    if anton == 1:
                                        p1time = 30
                                        p2time = 30
                                    if treset == True and finedit == True:
                                        p1time = copy.copy(testtime)
                                        p2time = copy.copy(testtime)
                                    RONALDO = None
                                else:
                                    selected_piece = None



def  dragyopiece():
    global piece_clicked
    if selected_piece != None:
        mou1, mou2 = (pygame.mouse.get_pos())[0], (pygame.mouse.get_pos())[1]
        color, piece = board[selected_piece[0]][selected_piece[1]]
        img = pygame.image.load(f"assets/{color}{piece}.png")
        img = pygame.transform.scale(img, (80, 80))
        img.set_alpha(80)
        screen.blit(img, [mou1 - 40, mou2 - 25])
        screen.blit(img, [selected_piece[1] * 100 + 4, selected_piece[0] * 100 + 11])
        pygame.mouse.set_visible(False)

    else:
        pygame.mouse.set_visible(True)


testcheck = False
def is_king_in_check(board, player):
    global RONALDO, king_pos, abc, testcheck, allowcastle
    abc = []
    allowcastle = False
    opponent = "w" if player == "b" else "b"
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == player + 'K':
                king_pos = (row,col)
    for row in range(len(board)):
        for col in range(len(board[row])):
            if opponent in board[row][col]:
                if valid_move((row,col), king_pos[0], king_pos[1], board):
                    RONALDO = (row,col)
                    abc.append(RONALDO)
    allowcastle = True
    if len(abc) != 0:
        hlsp()
        return True
    return False

def savetest(data):
    with open("board.json", "w") as file:
        json.dump(data, file)



def matte(player, board):
    global possibles, testcheck, allowcastle
    possibles = []
    allowcastle = False
    for prow in range(len(board)):
        for pcol in range(len(board[prow])):
            if player in board[prow][pcol]:
                selp = (prow, pcol)
                for trow in range(len(board)):
                    for tcol in range(len(board[trow])):
                        if player not in board[trow][tcol]:
                            testcheck = True
                            if valid_move(selp, trow, tcol, board):
                                temp_board = copy.deepcopy(board)
                                temp_board[trow][tcol] = temp_board[prow][pcol]
                                temp_board[prow][pcol] = ""
                                if is_king_in_check(temp_board, players[curplay]):
                                    #not a move that gets out of check
                                    None
                                elif not is_king_in_check(temp_board, players[curplay]):
                                    #a move that gets the king out of check exists
                                    possibles.append([prow,pcol])
    allowcastle = True
    testcheck = False
    if len(possibles) > 0:
        return True
    return False
                                    
                                
            
    

def promo():
    global inpro
    for row in range(len(board)):
        for col in range(len(board[row])): #i know this can be optimized, however, i am lazy and it was the very final thing to code.
            if 'P' in board[0][col]:
                inpro = True
                pygame.draw.rect(screen, (40,40,40), [45, 20, 130, 160])
                pygame.draw.rect(screen, (40,40,40), [240, 20, 130, 160])
                pygame.draw.rect(screen, (40,40,40), [440, 20, 130, 160])
                pygame.draw.rect(screen, (40,40,40), [645, 20, 130, 160])
                
                aa = pygame.image.load('assets/wQ.png')
                aa = pygame.transform.scale(aa, (125, 150))
                screen.blit(aa, [50, 20])
                pygame.draw.rect(screen, (100,25,200), [45, 20, 130, 160], 5)
                
                aa = pygame.image.load('assets/wR.png')
                aa = pygame.transform.scale(aa, (125, 150))
                screen.blit(aa, [245, 20])
                pygame.draw.rect(screen, (100,25,200), [240, 20, 130, 160], 5)
                
                aa = pygame.image.load('assets/wN.png')
                aa = pygame.transform.scale(aa, (125, 150))
                screen.blit(aa, [445, 20])
                pygame.draw.rect(screen, (100,25,200), [440, 20, 130, 160], 5)
                
                aa = pygame.image.load('assets/wB.png')
                aa = pygame.transform.scale(aa, (125, 150))
                screen.blit(aa, [650, 20])
                pygame.draw.rect(screen, (100,25,200), [645, 20, 130, 160], 5)
            if 'P' in board[7][col]:
                inpro = True
                pygame.draw.rect(screen, (200,200,200), [45, 610, 130, 180])
                pygame.draw.rect(screen, (200,200,200), [240, 610, 130, 180])
                pygame.draw.rect(screen, (200,200,200), [440, 610, 130, 180])
                pygame.draw.rect(screen, (200,200,200), [645, 610, 130, 180])
                
                aa = pygame.image.load('assets/bQ.png')
                aa = pygame.transform.scale(aa, (125, 150))
                screen.blit(aa, [47, 625])
                pygame.draw.rect(screen, (100,25,200), [45, 610, 130, 180], 5)
                
                aa = pygame.image.load('assets/bR.png')
                aa = pygame.transform.scale(aa, (125, 150))
                screen.blit(aa, [243, 625])
                pygame.draw.rect(screen, (100,25,200), [240, 610, 130, 180], 5)
                
                aa = pygame.image.load('assets/bN.png')
                aa = pygame.transform.scale(aa, (125, 150))
                screen.blit(aa, [443, 625])
                pygame.draw.rect(screen, (100,25,200), [440, 610, 130, 180], 5)
                
                aa = pygame.image.load('assets/bB.png')
                aa = pygame.transform.scale(aa, (125, 150))
                screen.blit(aa, [647, 625])
                pygame.draw.rect(screen, (100,25,200), [645, 610, 130, 180], 5)
            if inpro == True:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1 and curplay == 1:
                            if (pygame.mouse.get_pos())[0] > 45 and pygame.mouse.get_pos()[0] < 175 and pygame.mouse.get_pos()[1] < 180:board[0][col] = 'wQ'
                            elif (pygame.mouse.get_pos())[0] > 240 and pygame.mouse.get_pos()[0] < 365 and pygame.mouse.get_pos()[1] < 180:board[0][col] = 'wR'
                            elif (pygame.mouse.get_pos())[0] > 440 and pygame.mouse.get_pos()[0] < 565 and pygame.mouse.get_pos()[1] < 180:board[0][col] = 'wN'
                            elif (pygame.mouse.get_pos())[0] > 645 and pygame.mouse.get_pos()[0] < 775 and pygame.mouse.get_pos()[1] < 180:board[0][col] = 'wB'
                        if event.button == 1 and curplay == 0:
                            if (pygame.mouse.get_pos())[0] > 45 and pygame.mouse.get_pos()[0] < 175 and pygame.mouse.get_pos()[1] > 620:board[7][col] = 'bQ'
                            elif (pygame.mouse.get_pos())[0] > 240 and pygame.mouse.get_pos()[0] < 365 and pygame.mouse.get_pos()[1] > 620:board[7][col] = 'bR'
                            elif (pygame.mouse.get_pos())[0] > 440 and pygame.mouse.get_pos()[0] < 565 and pygame.mouse.get_pos()[1] > 620:board[7][col] = 'bN'
                            elif (pygame.mouse.get_pos())[0] > 650 and pygame.mouse.get_pos()[0] < 775 and pygame.mouse.get_pos()[1] > 620:board[7][col] = 'bB'
                inpro = False

wcastle = False
bcastle = False
castled = [0,0] #wK, bK
def valid_move(selected_piece, row, col, board): #made by chatGPT because i could not be bothered to have to do math
    global kings_moved, rooks_moved, castled
    piece = board[selected_piece[0]][selected_piece[1]]
    piece_color = piece[0];piece_type = piece[1]
    # Check if the selected piece is a pawn
    if piece_type == 'P':
        # White pawns can only move forward
        if piece_color == 'w':
            if row == selected_piece[0] - 1 and col == selected_piece[1] and board[row][col] == '':
                return True
            elif row == selected_piece[0] - 2 and col == selected_piece[1] and board[row][col] == '' and selected_piece[0] == 6 and board[row + 1][selected_piece[1]] == '' : #twice on start
                return True
            elif row == selected_piece[0] - 1 and (col == selected_piece[1] - 1 or col == selected_piece[1] + 1) and board[row][col] != '': #takes pieces that are directly diagnol by one
                return True
        # Black pawns can only move forward
        else:
            if row == selected_piece[0] + 1 and col == selected_piece[1] and board[row][col] == '':
                return True
            elif row == selected_piece[0] + 2 and col == selected_piece[1] and board[row][col] == '' and selected_piece[0] == 1 and board[row - 1][selected_piece[1]] == '':
                return True
            elif row == selected_piece[0] + 1 and (col == selected_piece[1] - 1 or col == selected_piece[1] + 1) and board[row][col] != '':
                return True

    # Check if the selected piece is a rook
    if piece_type == 'R':
        # Check if the move is horizontal or vertical
        if row == selected_piece[0] or col == selected_piece[1]:
            # Check if there are any pieces obstructing the path
            if row == selected_piece[0]:
                start = min(col, selected_piece[1]) + 1
                end = max(col, selected_piece[1])
                for c in range(start, end):
                    if board[row][c] != '':
                        return False
            else:
                start = min(row, selected_piece[0]) + 1
                end = max(row, selected_piece[0])
                for r in range(start, end):
                    if board[r][col] != '':
                        return False
            # Check if the destination square is empty or occupied by an opponent's piece
            if board[row][col] == '' or board[row][col][0] != piece_color:
                if selected_piece == (0,0) and rooks_moved[0] == False:rooks_moved[0] = True
                if selected_piece == (0,7) and rooks_moved[1] == False:rooks_moved[1] = True
                if selected_piece == (7,0) and rooks_moved[2] == False:rooks_moved[2] = True
                if selected_piece == (7,7) and rooks_moved[3] == False:rooks_moved[3] = True

                return True

    # Check if the selected piece is a knight
    if piece_type == 'N':
        # Check if the move is a valid knight's move
        if abs(row - selected_piece[0]) == 2 and abs(col - selected_piece[1]) == 1:
            return True
        elif abs(row - selected_piece[0]) == 1 and abs(col - selected_piece[1]) == 2:
            return True

    # Check if the selected piece is a bishop
    if piece_type == 'B':
        if abs(row - selected_piece[0]) == abs(col - selected_piece[1]):
            # Check if there are any pieces obstructing the path
            start_row = selected_piece[0] + 1 #bottom right diagonal path
            start_col = selected_piece[1] + 1 
            while start_row < row and start_col < col: 
                if board[start_row][start_col] != '':
                    return False
                start_row += 1
                start_col += 1
                        
            start_row = selected_piece[0] + 1 #bottom left diagonal path
            start_col = selected_piece[1] - 1 
            while start_row < row and start_col > col: 
                if board[start_row][start_col] != '':
                    return False
                start_row += 1
                start_col -= 1
                        
            start_row = selected_piece[0] - 1#top left diaganol path
            start_col = selected_piece[1] - 1
            while start_row > row and start_col > col:
                if board[start_row][start_col] != '':
                    return False
                start_row -= 1
                start_col -= 1
                        
            start_row = selected_piece[0] - 1 # top right diaganol path
            start_col = selected_piece[1] + 1
            while start_row > row and start_col < col:
                if board[start_row][start_col] != '':
                    return False
                start_row -= 1
                start_col += 1
            # Check if the destination square is empty or occupied by an opponent's piece
            if board[row][col] == '' or board[row][col][0] != piece_color:
                return True

    # Check if the selected piece is a queen
    if piece_type == 'Q':
        # Check if the move is along a straight line (horizontal, vertical, or diagonal)
        if row == selected_piece[0] or col == selected_piece[1] or abs(row - selected_piece[0]) == abs(col - selected_piece[1]):
            # Check if there are any pieces obstructing the path
            if row == selected_piece[0]:
                start = min(col, selected_piece[1]) + 1
                end = max(col, selected_piece[1])
                for c in range(start, end):
                    if board[row][c] != '':
                        return False
            elif col == selected_piece[1]:
                start = min(row, selected_piece[0]) + 1
                end = max(row, selected_piece[0])
                for r in range(start, end):
                    if board[r][col] != '':
                        return False
            else:
                if abs(row - selected_piece[0]) == abs(col - selected_piece[1]): #if diaganol
                    # Check if there are any pieces obstructing the path
                    start_row = selected_piece[0] + 1 #bottom right diagonal path
                    start_col = selected_piece[1] + 1 
                    while start_row < row and start_col < col: 
                        if board[start_row][start_col] != '':
                            return False
                        start_row += 1
                        start_col += 1
                        
                    start_row = selected_piece[0] + 1 #bottom left diagonal path
                    start_col = selected_piece[1] - 1 
                    while start_row < row and start_col > col: 
                        if board[start_row][start_col] != '':
                            return False
                        start_row += 1
                        start_col -= 1
                        
                    start_row = selected_piece[0] - 1#top left diaganol path
                    start_col = selected_piece[1] - 1
                    while start_row > row and start_col > col:
                        if board[start_row][start_col] != '':
                            return False
                        start_row -= 1
                        start_col -= 1
                        
                    start_row = selected_piece[0] - 1 # top right diaganol path
                    start_col = selected_piece[1] + 1
                    while start_row > row and start_col < col:
                        if board[start_row][start_col] != '':
                            return False
                        start_row -= 1
                        start_col += 1
    
            # Check if the destination square is empty or occupied by an opponent's piece
            if board[row][col] == '' or board[row][col][0] != piece_color:
                return True

    # Check if the selected piece is a king
    if piece_type == 'K':
        if piece_color == 'w' and kings_moved[0] == False and wcastle == False and testcheck == False and (row,col) == (7,2) and board[7][1] == "" and board[7][2] == "" and board[7][3] == "" and rooks_moved[2] == False: castled[0] = 1; return True#bottom left castling
        if piece_color == 'w' and kings_moved[0] == False and wcastle == False and testcheck == False and (row,col) == (7,6) and board[7][6] == "" and board[7][5] == "" and rooks_moved[3] == False: castled[0] = 2; return True #bottom right castling
        if piece_color == 'b' and kings_moved[1] == False and bcastle == False and testcheck == False and (row,col) == (0,2) and board[0][1] == "" and board[0][2] == "" and board[0][2] == "" and rooks_moved[0] == False: castled[1] = 1;return True #top left
        if piece_color == 'b' and kings_moved[1] == False and bcastle == False and testcheck == False and (row,col) == (0,6) and board[0][6] == "" and board[0][5] == "" and rooks_moved[1] == False: castled[1] = 2; return True #top right
        
        #if piece_color == 'w' and kings_moved[0] == False and testcheck == False and (row,col) == (7,2) and board[7][1] == "" and board[7][2] == "" and board[7][3] == "" and rooks_moved[2] == False: board[7][0] = ''; board[7][3] = 'wR'; kings_moved[0] = True;return True; #bottom left castling
        #if piece_color == 'w' and kings_moved[0] == False and testcheck == False and (row,col) == (7,6) and board[7][6] == "" and board[7][5] == "" and rooks_moved[3] == False: board[7][7] = ''; board[7][5] = 'wR'; kings_moved[0] = True;return True; #bottom right castling
        #if piece_color == 'b' and kings_moved[1] == False and testcheck == False and (row,col) == (0,2) and board[0][1] == "" and board[0][2] == "" and board[0][2] == "" and rooks_moved[0] == False: board[0][0] = ''; board[0][3] = 'bR'; kings_moved[1] = True;return True; #top left
        #if piece_color == 'b' and kings_moved[1] == False and testcheck == False and (row,col) == (0,6) and board[0][6] == "" and board[0][5] == "" and rooks_moved[1] == False: board[0][7] = ''; board[0][5] = 'bR'; kings_moved[1] = True;return True; #top right

        # Check if the move is within one square in any direction
        if abs(row - selected_piece[0]) <= 1 and abs(col - selected_piece[1]) <= 1:
            # Check if the destination square is empty or occupied by an opponent's piece
            if board[row][col] == '' or board[row][col][0] != piece_color:
                return True

    return False

def draw_board():
    for row in range(8):
        for col in range(8):
            if (row + col) % 2 == 0:
                color = LIGHT_SQUARE
            else:
                color = DARK_SQUARE
            pygame.draw.rect(screen, color, (col * 100, row * 100, 100, 100))
            piece = board[row][col]
            if piece != "" and selboa == False:
                screen.blit(pieces[piece], (col * 100 + 10, row * 100 + 10))

    # Add numbering and lettering
    for i in range(8):
        # Draw numbers
        number_font = pygame.font.Font(None, 24)
        if i % 2 == 0:
            number_text = number_font.render(str(8 - i), True, WHITE)
        else:
            number_text = number_font.render(str(8 - i), True, BLACK)
        screen.blit(number_text, (790, i * 100))

        letterkey = ['a','b','c','d','e','f','g','h']
        if i % 2 == 0:
            letter_text = number_font.render(letterkey[i], True, WHITE)
        else:
            letter_text = number_font.render(letterkey[i], True, BLACK)
        screen.blit(letter_text, (100 * i, 785))

import time
def hlsp(): #i need it to see the piece :widepeepohappy:
    global bruh
    if len(abc) > 0:
        for x in abc:
            pygame.draw.rect(screen, RED, (x[1] * 100, x[0] * 100, 100, 100), 4)
    if selected_piece is not None:
        #print(selected_piece)
        #time.sleep(0.3)
        if len(bruh) > 0:
            for x in bruh:
                pygame.draw.rect(screen, (0,0,100), (x[1] * 100, x[0] * 100, 100, 100), 4)
        if selected_piece == (7,4):
            if castled[0] == 0 and board[7][1] == "" and board[7][2] == "" and board[7][3] == "" and rooks_moved[2] == False:
                pygame.draw.rect(screen, (255,255,255), (2 * 100, 7 * 100, 100, 100), 4);
            if castled[0] == 0 and board[7][6] == "" and board[7][5] == "" and rooks_moved[3] == False:
                pygame.draw.rect(screen, (255,255,255), (6 * 100, 7 * 100, 100, 100), 4);
        if selected_piece == (0,4):
            if castled[1] == 0 and board[0][1] == "" and board[0][2] == "" and board[0][3] == "" and rooks_moved[0] == False:
                pygame.draw.rect(screen, (255,255,255), (2 * 100, 0 * 100, 100, 100), 4);
            if castled[1] == 0 and board[0][6] == "" and board[0][5] == "" and rooks_moved[1] == False:
                pygame.draw.rect(screen, (255,255,255), (6 * 100, 0 * 100, 100, 100), 4);
        selected_row, selected_col = selected_piece
        pygame.draw.rect(screen, (0,0,255), (selected_col * 100, selected_row * 100, 100, 100), 4)
    else: bruh = []



def castleforrealthistime():
    global castled, board, kings_moved, wcastle, bcastle
    if castled[0] == 1:
        if board[7][2] == 'wK':
            board[7][3] = 'wR'
            board[7][0] = ''
            wcastle = True
    if castled[0] == 2:
        if board[7][6] == 'wK':
            board[7][5] = 'wR'
            board[7][7] = ''
            wcastle = True
    if castled[1] == 1:
        if board[0][6] == 'bK':
            board[0][5] = 'bR'
            board[0][7] = ''
            bcastle = True   
    if castled[1] == 2:
        if board[0][6] == 'bK':
            board[0][5] = 'bR'
            board[0][7] = ''
            bcastle = True



timer = 0
def turn_timer():

    global p1time, timer, p2time, timerfont
    timer += 1
    savetest([started, anton, board, curplay, p1time, p2time])
    if curplay == 0:
        if timer == 60:
            timer = 0
            p1time -= 1
    if curplay == 1: 
        if timer == 60:
            timer = 0
            p2time -= 1
    timerfont = True

    hours = '0' + str(p1time // 3600); hours2 = '0' + str(p2time // 3600)
    minu = str(p1time // 60 - (p1time // 3600 * 60)); minu2 = str(p2time // 60 - (p2time // 3600 * 60))
    hb1 = ':';hb2 = ':'; sec1 = p1time % 60; sec2 = p2time % 60
    if hours[-1] == '0': hours = ''; hb1 = ''; mb1 = ''
    if hours2[-1] == '0': hours2 = '';hb2 = ''; mb2 = ''
    aasa ='0' if len(str(minu)) == 1 else ''
    bbsa = '0' if len(str(minu2)) == 1 else ''
    test1 = ':' if aasa + minu != '' or hours != '' else ''
    test2 = ':' if bbsa + minu2 != '' or hours2 != '' else ''
    draw_text(f"White:    {hours}{hb1}{aasa + minu if aasa + minu != '00' else ''}{test1 if aasa + minu != '00' else ''}{'0' if len(str(sec1)) == 1 else ''}{sec1}", 100, 810, WHITE)
    draw_text(f"Black:    {hours2}{hb2}{bbsa + minu2 if bbsa + minu2 != '00' else ''}{test2 if bbsa + minu2 != '00' else ''}{'0' if len(str(sec2)) == 1 else ''}{sec2}", 700, 810, WHITE)
    draw_text(f"{'Black' if players[curplay] == 'b' else 'White'}'s turn.", 400, 810, RED)
    timerfont = False
    


redefflag = False
def choss():
    global game_over, timer, timerfont, board, anton, curplay, redefflag, treset, shouffle
    screen.fill(BLACK)
    draw_board()     
    hlsp()
    if extra1 == False:
        handle_events()
        dragyopiece()
    if extra1 == True:
        handle_events2()
    if not game_over:
        turn_timer()
        savetest([started, anton, board, curplay, p1time, p2time])
    if p1time == 0: draw_text('Black', 400, 400, BLACK); draw_text('Wins.', 490, 400, RED); selected_piece = None;piece_clicked = False; timer = 0; game_over = True
    if p2time == 0: draw_text('White', 400, 400, BLACK); draw_text('Wins.', 490, 400, RED); selected_piece = None;piece_clicked = False; timer = 0; game_over = True
    elif is_king_in_check(board, players[curplay]) or is_king_in_check(board, players[1 - curplay]):
        draw_text('Check.', 400, 400, RED)
        if not matte(players[curplay], board):
            draw_text('Mate.', 482, 400, BLACK)
            selected_piece = None
            piece_clicked = False
            game_over = True
            timer = 0

    if game_over:
        wcastle = False
        
        bcastle = False
        treset = False
        shouffle = False
        timerfont = True
        draw_text('Esc to return to Main Menu', 400, 813, (255,255, 0))
        timerfont = False
        timer = 0
        clock.tick(60); pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                 if event.key == pygame.K_ESCAPE:
                    anton = 0
                    curplay = 0
                    board = copy.copy(board2)
                    game_over = False
                
    promo()
    castleforrealthistime()
    pygame.display.flip()
    clock.tick(60)
    
running = True 
while running:
    try:
        ack = pygame.image.load("assets/fish.jpg") #loadbearing fish
    except:
        running = False
    screen.fill(BLACK)
    if anton == 0: selection(); started = False
    elif anton == 1 or anton == 2:
        choss()
    elif anton == 3 and finedit == False:
        custom()
    elif anton == 3 and finedit == True:
        choss()
    if anton != 0: started = True
    pygame.display.flip()

