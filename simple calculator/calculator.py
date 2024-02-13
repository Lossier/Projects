import pygame
import copy
pygame.init()
screen = pygame.display.set_mode([500,500])
BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (150,150,155)
font = pygame.font.Font(None, 40)
balls = '0'
digits = False
anton = ''

def draw_buttons():
    pygame.draw.rect(screen, BLACK, [0,100, 500,400])
    pygame.draw.line(screen, WHITE,[100, 100], [100, 450], width=1)
    pygame.draw.line(screen, WHITE,[200, 100], [200, 500], width=1)
    pygame.draw.line(screen, WHITE,[300, 100], [300, 500], width=1)
    
    pygame.draw.line(screen, WHITE,[300, 170], [500, 170], width=1)
    pygame.draw.line(screen, WHITE,[300, 250], [500, 250], width=1)
    pygame.draw.line(screen, WHITE,[400, 170], [400, 334], width=1)

    pygame.draw.line(screen, WHITE,[0, 217], [300, 217], width=1)
    pygame.draw.line(screen, WHITE,[0, 334], [500, 334], width=1)
    pygame.draw.line(screen, WHITE,[0, 450], [300, 450], width=1)
    draw_text('c', 385, 110, WHITE)
    
    draw_text('7', 40, 150, WHITE)
    draw_text('8', 140, 150, WHITE)
    draw_text('9', 240, 150, WHITE)
    draw_text('4', 40, 270, WHITE)
    draw_text('5', 140, 270, WHITE)
    draw_text('6', 240, 270, WHITE)
    draw_text('1', 40, 390, WHITE)
    draw_text('2', 140, 390, WHITE)
    draw_text('3', 240, 390, WHITE)
    draw_text('0', 95, 465, WHITE)
    draw_text('.', 243, 438, WHITE)
    draw_text('=', 370, 370, WHITE)
    
    draw_text('+', 330, 265, WHITE)
    draw_text('-', 340, 185, WHITE)
    draw_text('x', 430, 190, WHITE)
    draw_text('/', 450, 270, WHITE)
    font = pygame.font.Font(None, 40)


def digitstuff(cred, bruh):
    global balls
    if balls == '0':
        balls = cred
    elif bruh == None and balls != '0'  and len(balls) < 13:
        balls += cred
def draw_text(txt, x, y, color):
    global font
    if txt in ['.','+','-','x', '/', 'c']:
        font = pygame.font.Font(None, 80)
    elif txt == '=':
        font = pygame.font.Font(None, 140)
    elif digits == True:
        font = pygame.font.Font(None, 80)
    else:
        font = pygame.font.Font(None, 40)
    text = font.render(txt, True, color)
    screen.blit(text, (x,y))
    
sub = False
add = False
mult = False
div = False
ente = False
def handle_events():
    global balls, anton, sub, add, mult, div, ente
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            x,y = pygame.mouse.get_pos()
            if x < 300 and x > 200 and y > 100 and y < 210:
                digitstuff('9', None)
            elif x < 200 and x > 100 and y > 100 and y < 210:
                digitstuff('8', None)
            elif x < 100 and y > 100 and y < 210:
                digitstuff('7', None)
                
            elif x < 300 and x > 200 and y > 180 and y < 300:
                digitstuff('6', None)
            elif x < 200 and x > 100 and y > 180 and y < 300:
                digitstuff('5', None)
            elif x < 100 and y > 100 and y > 180 and y < 300:
                digitstuff('4', None)
                
            elif x < 300 and x > 200 and y > 330 and y < 450:
                digitstuff('3', None)
            elif x < 200 and x > 100 and y > 330 and y < 450:
                digitstuff('2', None)
            elif x < 100 and y > 100 and y > 330 and y < 450:
                digitstuff('1', None)
                
            elif x < 200 and y > 450:
                digitstuff('0', None)
            elif x > 200 and x < 300 and y > 200 and '.' not in balls:
                digitstuff('.', None)
            elif x > 300 and y < 170 and y > 100:
                balls = '0'
                anton = ''
                add, sub, div, mult = False, False, False, False
            elif x > 300 and x < 400 and y > 150 and y < 245:
                anton = copy.deepcopy(balls)
                balls = '0'
                sub = True
            elif x > 400 and y > 150 and y < 245:
                anton = copy.deepcopy(balls)
                balls = '0'
                mult = True
            elif x > 300 and x < 400 and y > 245 and y < 333:
                anton = copy.deepcopy(balls)
                balls = '0'
                add = True
            elif x > 400 and y > 245 and y < 333:
                anton = copy.deepcopy(balls)
                balls = '0'
                div = True
            elif x > 300 and y > 333 and anton != '' and anton != '.' and balls != '.':
                ente = True
                
            
            
def maths():
    global balls, ente, sub, add, div, mult
    if sub == True and ente == True:
        balls = str(float(anton) - float(balls))
        ente = False
        sub = False
    if div == True and ente == True:
        if float(balls) != 0:
            balls = str(round(float(anton) /float(balls), 5))
            ente = False
            div = False
        else:
            div = False
            balls = '0'
    if add == True and ente == True:
        balls = str(float(anton) + float(balls))
        ente = False
        add = False
    if mult == True and ente == True:
        balls = str(round(float(anton) * float(balls), 5))
        ente = False
        mult = False


from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame  # import after disabling environ prompt
from win32gui import SetWindowPos
import tkinter as tk


root = tk.Tk()  # create only one instance for Tk()
root.withdraw()  # keep the root window from appearing

screen_w, screen_h = root.winfo_screenwidth(), root.winfo_screenheight()
win_w = 500
win_h = 500

x = round((screen_w - win_w) / 2)
y = round((screen_h - win_h) / 2 * 0.8)  # 80 % of the actual height

# pygame screen parameter for further use in code
screen = pygame.display.set_mode((win_w, win_h))

# Set window position center-screen and on top of other windows
# Here 2nd parameter (-1) is essential for putting window on top
SetWindowPos(pygame.display.get_wm_info()['window'], -1, x, y, 0, 0, 1)

    
running = True
while running:
    screen.fill(GREY)
    draw_buttons()
    handle_events()
    digits = True
    draw_text(balls, 10, 20, BLACK)
    digits = False
    maths()
    pygame.display.flip()
