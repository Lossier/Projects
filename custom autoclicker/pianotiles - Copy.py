import pygame
import sys
import time
import pyautogui
import keyboard
import win32api
import win32con
from pynput.mouse import Listener
from ctypes import windll
import win32gui
import pygame  # import after disabling prompt
from win32api import GetSystemMetrics

print('Width:', GetSystemMetrics(0))
print('Height:', GetSystemMetrics(1))
Xpos = Ypos = 0

def GetMouseInfos(WhatToGet="leaving emety will get you x and y", GetXOnly=False, GetYOnly=False, GetColor=False, Key='Right', OverrideKey=False):#gets color of whats under Key cursor on right click
    #code below is to get all varibles needed
    #---------------------------------------------------------------
    print(WhatToGet)
    if OverrideKey:
        Key_To_click = Key
    if Key == 'Left':
        Key_To_click = 0x01
    if Key == 'Right':
        Key_To_click = 0x02
    if Key == 'Wheel':
        Key_To_click = 0x04
    state_left = win32api.GetKeyState(Key_To_click)  # Left button up = 0 or 1. Button down = -127 or -128
    IsTrue = True
    if IsTrue:
        Key_To_click = 0x01
        a = win32api.GetKeyState(Key_To_click)
        print(win32api.GetKeyState(Key_To_click))
        if a != state_left:  # Button state changed
            state_left = a
            if a < 0:
                global Xpos, Ypos
                Xpos, Ypos = win32api.GetCursorPos()
                x, y = pyautogui.position()
                pixelColor = pyautogui.screenshot().getpixel((x, y))
            else:
                posnowX, posnowY = win32api.GetCursorPos()
                win32api.SetCursorPos((posnowX, posnowY))
                IsTrue = False#remove this for it to keep giving coords on click without it just quitting after 1 click
        time.sleep(0.001)
    if GetXOnly: #Checks if we should get Only X (def options) the command to do this would be GetKeyInfos("Click To get X ONLY", True)
        if GetYOnly:
            return(Xpos , Ypos)
        if GetColor:
            return(Xpos, pixelColor)
        return(Xpos)
    if GetYOnly: #Checks if we should get Only Y (def options) the command to do this would be GetKeyInfos("Click To get X ONLY",False, True)
        if GetXOnly:
            return(Xpos , Ypos)
        #if GetColor:
            #return(Ypos, pixelColor) 
        return(Ypos)
    #if GetColor:
        #return(pixelColor) #Checks 
    return(Xpos, Ypos)


    
pygame.init()

clock = pygame.time.Clock()
editing = ''
FONT = pygame.font.Font(None, 25)

def draw_text(text, x, y, color):
    text_surface = FONT.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)
key = None
clockin = False
editin = ''
destx = 0;desty = 0
custpos = False
multi = False
multipos = []
coordflag = False
hotkeyflag = False
abc = 0
clicktime = looptime = 0.5


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
    elif chr(key) == '.': return '.'
    else: return None
editingct = editinglt = False

ack = []
def select():
    global editing, key, clockin, destx, desty, searching, custpos, multi, multipos, coordflag, hotkeyflag, FONT, clicktime, looptime, editingct, editinglt, ack
    if editing == '' and clockin == False:
        screen.blit(background_image, (0, 0))
        screen.blit(thymother, (0, 20)) if multi == False else None
        screen.blit(settings_image, (143, 0))
        if key != None and multi == False:
            draw_text(str(key), 100, 75, (0,0,0))
        if key != None and multi == True:
            draw_text(str(key) + ' to begin.', 100, 140, (0,0,0))
        if (destx != 0 or desty != 0) and multi == False:
            custpos = True
            draw_text(f'x:{destx}', 60, 100, (0,0,0))
            draw_text(f'y:{desty}', 140, 100, (0,0,0))
        elif multi == True:
            coordflag = True
            custpos = True
            FONT = pygame.font.Font(None, 18)
            pygame.draw.rect(screen, (240,210,250), [5, 16, 110, 20])
            pygame.draw.rect(screen, (0,0,0), [5, 16, 110, 20], 1)
            draw_text('+ custom position', 60, 25, (0,0,0))
            
            pygame.draw.rect(screen, (200,240,250), [120, 16, 60, 20])
            pygame.draw.rect(screen, (0,0,0), [120, 16, 60, 20], 1)
            draw_text('clear', 145, 25, (0,0,0))
            if len(multipos) == 0:
                draw_text(f"No positions.", 45, 50, (0,0,0))
            if len(multipos) > 0:
                draw_text(f"{len(multipos)} position{'s' if len(multipos) > 1 else ''}.", 45, 50, (0,0,0))
            pygame.draw.rect(screen, (255,255,255), [0, 13, 200, 3])
            pygame.draw.rect(screen, (255,255,255), [0, 60, 200, 3])
            pygame.draw.rect(screen, (255,255,255), [0, 125, 200, 3])
            draw_text(f"Time between each click:", 100, 70, (0,0,0))
            draw_text(f"{clicktime} second{'s' if clicktime > 1 or clicktime < 1 else ''}", 100, 85, (0,0,0))
            draw_text(f"Time between each loop:", 100, 100, (0,0,0))
            draw_text(f"{looptime} second{'s' if looptime > 1 or looptime < 1 else ''}", 100, 115, (0,0,0))

            if editingct == True:
                pygame.draw.rect(screen, (220, 220, 220), [0, 80, 200, 10])
                draw_text(f"{''.join(ack)}", 100, 85, (0,0,0))
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN or event.key == 1073741912:
                            clicktime = float(''.join(ack))
                            editingct = False
                            ack = []
                        ack.append(numkeypress(event.key)) if event.key != 1073741912 and numkeypress(event.key) != None else '.'
                        if len(ack) == 4:
                            clicktime = float(''.join(ack))
                            editingct = False
                            ack = []
            if editinglt == True:
                pygame.draw.rect(screen, (220, 220, 220), [0, 110, 200, 10])
                draw_text(f"{''.join(ack)}", 100, 115, (0,0,0))
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN or event.key == 1073741912:
                            looptime = float(''.join(ack))
                            editinglt = False
                            ack = []
                        ack.append(numkeypress(event.key)) if event.key != 1073741912 and numkeypress(event.key) != None else '.'
                        if len(ack) == 4:
                            looptime = float(''.join(ack))
                            editinglt = False
                            ack = []
            FONT = pygame.font.Font(None, 25)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mx, my = pygame.mouse.get_pos()
                    if mx <= 75 and my <= 15:
                        editing = 'hotkey'
                    elif mx <= 77 and my >= 20 and my < 32 and multi == False:
                        coordflag = True
                        editing = 'coords'
                    elif mx >= 5 and mx <= 110 and my >= 20 and my < 32 and multi == True:
                        editing = 'coords'
                    elif mx >= 120 and mx <= 180 and my >= 20 and my < 32 and multi == True:
                        multipos = []
                    elif abs(mx - 100) < 25 and abs(my - 80) < 10 and multi == True and editinglt== False and editingct == False:
                        editingct = True
                    elif abs(mx - 100) < 25 and abs(my - 115) < 10 and multi == True and editinglt== False and editingct == False:
                        editinglt = True
                    elif mx >= 144 and my <= 15:
                        editing = 'settings'
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    elif editing == 'clicktime' and clockin == False:
        return
    elif editing == 'looptime' and clockin == False:
        None
    elif editing == 'hotkey' and clockin == False:
        pygame.draw.rect(screen, (0, 0, 0), [25, 50, 150, 50])
        draw_text(f"{'Press any key'}", 100, 75, (255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                #key = keyboard.on_press(print_state1)
                key = event.key
                if key < 1000:
                    key = str(chr(key))
                if key == 'q': key = None
                #elif key == pygame.KSCAN_KP_0: key = None
                #elif key == pygame.KSCAN_KP_1: key = None
                #elif key == pygame.KSCAN_KP_2: key = None
                #elif key == pygame.KSCAN_KP_3: key = None
                #elif key == pygame.KSCAN_KP_4: key = None
                #elif key == pygame.KSCAN_KP_5: key = None
                #elif key == pygame.KSCAN_KP_6: key = None
                #elif key == pygame.KSCAN_KP_7: key = None
                #elif key == pygame.KSCAN_KP_8: key = None
                #elif key == pygame.KSCAN_KP_9: key = None
                elif key == pygame.K_F1: key = 'F1'
                elif key == pygame.K_F2: key = 'F2'
                elif key == pygame.K_F3: key = 'F3'
                elif key == pygame.K_F4: key = 'F4'
                elif key == pygame.K_F5: key = 'F5'
                elif key == pygame.K_F6: key = 'F6'
                elif key == pygame.K_F7: key = 'F7'
                elif key == pygame.K_F8: key = 'F8'
                elif key == pygame.K_F9: key = 'F9'
                elif key == pygame.K_F10: key = 'F10'
                elif key == pygame.K_F11: key = 'F11'
                elif key == pygame.K_F12: key = 'F12'
                if key is int: key = str(chr(key))
                keyboard.on_release(print_state)
                time.sleep(0.1)
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
    elif editing == 'coords' and clockin == False:
        pos = win32api.GetCursorPos()
        pygame.draw.rect(screen, (0, 0, 0), [25, 25, 150, 100])
        pos = win32api.GetCursorPos()
        FONT = pygame.font.Font(None, 14)
        draw_text("press enter or click to set custom position.", 100, 10, (0, 0, 0))
        FONT = pygame.font.Font(None, 25)
        draw_text('x:', 70, 50, (255,255,255))
        draw_text(f'{pos[0]}', 120, 50, (255,0,0))
        draw_text('y:', 70, 100, (255,255,255))
        draw_text(f'{pos[1]}', 120, 100, (255,0,0))
        Key_To_click = 0x01
        if coordflag == False:
            a = win32api.GetKeyState(Key_To_click)
            if (keyboard.is_pressed('enter')) or (a!= 0 and a!= 1) and multi == False:
                editing = ''
                destx, desty = win32api.GetCursorPos()
            if (keyboard.is_pressed('enter')) or (a!= 0 and a!= 1) and multi == True:
                editing = ''
                multipos.append(win32api.GetCursorPos())
            
        else:
            time.sleep(0.2)
            coordflag = False
    elif editing == 'settings' and clockin == False:
        pygame.draw.rect(screen, (0,0,0), [20, 20, 160, 110])
        FONT = pygame.font.Font(None, 17)
        draw_text('Esc to exit', 30, 10, (200,0,0))
        FONT = pygame.font.Font(None, 24)
        draw_text('Advanced', 90, 50, (255,255,255))
        if multi == False: aa = (255, 0, 0)
        else: aa = (0,255,0)
        draw_text(f"{'X' if multi == False else 'V'}", 160, 50, aa)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mx1,my1 = pygame.mouse.get_pos()
                    if mx1 >= 22 and mx1 <= 175 and my1 >= 40 and my1 <= 50:
                        multi = not multi
            elif event.type == pygame.KEYDOWN:
                if event.key == 27:
                    editing = ''
def print_state1(event):
    global key
    if event.event_type == keyboard.KEY_DOWN:
        return event.name    
def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    time.sleep(0.1) #This pauses the script for 0.1 seconds
    
# Load image assets
background_image = pygame.image.load('kys.png')
settings_image = pygame.image.load('settings.png')
thymother = pygame.image.load('coordinate.png')
# Create the screen
screen = pygame.display.set_mode((200, 150))

# Game loop
done = False

from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame  # import after disabling environ prompt
from win32gui import SetWindowPos
import tkinter as tk


root = tk.Tk()  # create only one instance for Tk()
root.withdraw()  # keep the root window from appearing

screen_w, screen_h = root.winfo_screenwidth(), root.winfo_screenheight()
win_w = 200
win_h = 150

x = round((screen_w - win_w) / 2)
y = round((screen_h - win_h) / 2 * 0.8)  # 80 % of the actual height

# pygame screen parameter for further use in code
screen = pygame.display.set_mode((win_w, win_h))

# Set window position center-screen and on top of other windows
# Here 2nd parameter (-1) is essential for putting window on top
SetWindowPos(pygame.display.get_wm_info()['window'], -1, x, y, 0, 0, 1)
#print(GetMouseInfos())


def print_state(event):
    global editing
    #if event.event_type == keyboard.KEY_DOWN:
        #print(f"{event.name} pressed.")
    if event.event_type == keyboard.KEY_UP and key != None:
        if len(event.name) > 1:
            event.name = (event.name).upper()
        if event.name == key:
            editing = ''

#keyboard.on_press(print_state)

#keyboard.wait()



while not done:
    screen.fill((220, 220, 220))
    select()
    if clockin:
        try:  # used try so that if user pressed other than the given key error will not be shown
            if keyboard.is_pressed('q'):  # if key 'q' is pressed 
                print('aborted')
                clockin = False
        except KeyError:
            break
        finally:
            draw_text('Press q to stop', 100, 100, (0,0,0))
    elif key != None:
        b = str(key)
        try:
            if keyboard.is_pressed(b) and hotkeyflag == False and editing != 'hotkey' and clockin == False:
                print('began')
                clockin = True
        except KeyError:
            break
    if clockin == True and custpos == False and multi == False:
        looptime = 0; clicktime = 0
        pos = win32api.GetCursorPos()
        click(pos[0],pos[1])
    elif clockin == True and custpos == True and multi == False:
        print('b')
        pos = (destx,desty)
        click(pos[0],pos[1])
    elif clockin == True and custpos == False and multi == True:
        print('c')
        pos = win32api.GetCursorPos()
        click(pos[0],pos[1])
        time.sleep(looptime)
    elif clockin == True and custpos ==True and multi == True:
        for pos in multipos:
            if keyboard.is_pressed('q'): clockin = False
            click(pos[0],pos[1])
            time.sleep(clicktime) if clicktime > 0.01 else None
        if keyboard.is_pressed('q'): clockin = False
        time.sleep(looptime) if looptime > 0.01 else None
        if keyboard.is_pressed('q'): clockin = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            
    pygame.display.update()
    clock.tick(60)

pygame.quit()




