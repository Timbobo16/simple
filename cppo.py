
# coding: utf-8

# In[7]:


import subprocess
from subprocess import Popen,CREATE_NEW_CONSOLE,PIPE
import win32com.client as comclt
import pyautogui
import time
import sys
import chess
import random

def send(s, w=0):
    wsh.AppActivate("C:\Windows\System32\cmd.exe") # select another application
    wsh.SendKeys(s) # send the keys you want
    pyautogui.press('enter')
    if w!=0:
        time.sleep(w)

def random_move():
    return list(board.legal_moves)[random.randint(0, board.legal_moves.count()-1)].uci()

def get_move():
    output = open(r"..\SIMPLE\app\out.txt","r")
    move = int_to_uci(int(output.read()))
    output.close()
    return move

def int_to_square(i):
    if i%8 == 0:
        first = "a"
    elif i%8 == 1:
        first = "b"
    elif i%8 == 2:
        first = "c"
    elif i%8 == 3:
        first = "d"
    elif i%8 == 4:
        first = "e"
    elif i%8 == 5:
        first = "f"
    elif i%8 == 6:
        first = "g"
    elif i%8 == 7:
        first = "h"
    second = str((i//8)+1)
    return first + second

def int_to_uci(i):
    if i >= 4096:
        if i%4 == 0:
            last = "n"
        elif i%4 == 1:
            last = "b"
        elif i%4 == 2:
            last = "r"
        elif i%4 == 3:
            last = "q"
        if i < 4100:
            first = "a7a8"
        elif i < 4104:
            first = "b7b8"
        elif i < 4108:
            first = "c7c8"
        elif i < 4112:
            first = "d7d8"
        elif i < 4116:
            first = "e7e8"
        elif i < 4120:
            first = "f7f8"
        elif i < 4124:
            first = "g7g8"
        elif i < 4128:
            first = "h7h8"
        elif i < 4132:
            first = "a2a1"
        elif i < 4136:
            first = "b2b1"
        elif i < 4140:
            first = "c2c1"
        elif i < 4144:
            first = "d2d1"
        elif i < 4148:
            first = "e2e1"
        elif i < 4152:
            first = "f2f1"
        elif i < 4156:
            first = "g2g1"
        elif i < 4160:
            first = "h2h1"
        return first + last
    first = int_to_square(i//64)
    second = int_to_square(i%64)
    return first + second

def uci_to_int(uci):
    if len(uci) == 5:
        if uci[:2] == "a7":
            result = 4096
        elif uci[:2] == "b7":
            result = 4100
        elif uci[:2] == "c7":
            result = 4104
        elif uci[:2] == "d7":
            result = 4108
        elif uci[:2] == "e7":
            result = 4112
        elif uci[:2] == "f7":
            result = 4116
        elif uci[:2] == "g7":
            result = 4120
        elif uci[:2] == "h7":
            result = 4124
        elif uci[:2] == "a2":
            result = 4128
        elif uci[:2] == "b2":
            result = 4132
        elif uci[:2] == "c2":
            result = 4136
        elif uci[:2] == "d2":
            result = 4140
        elif uci[:2] == "e2":
            result = 4144
        elif uci[:2] == "f2":
            result = 4148
        elif uci[:2] == "g2":
            result = 4152
        elif uci[:2] == "h2":
            result = 4156
        if uci[4] == "n":
            result += 0
        elif uci[4] == "b":
            result += 1
        elif uci[4] == "r":
            result += 2
        elif uci[4] == "q":
            result += 3
        return result
    result = 0
    if uci[0] == "a":
        result += 0
    elif uci[0] == "b":
        result += 64
    elif uci[0] == "c":
        result += 128
    elif uci[0] == "d":
        result += 192
    elif uci[0] == "e":
        result += 256
    elif uci[0] == "f":
        result += 320
    elif uci[0] == "g":
        result += 384
    elif uci[0] == "h":
        result += 448
    if uci[1] == "1":
        result += 0
    elif uci[1] == "2":
        result += 512
    elif uci[1] == "3":
        result += 1024
    elif uci[1] == "4":
        result += 1536
    elif uci[1] == "5":
        result += 2048
    elif uci[1] == "6":
        result += 2560
    elif uci[1] == "7":
        result += 3072
    elif uci[1] == "8":
        result += 3584
    if uci[2] == "a":
        result += 0
    elif uci[2] == "b":
        result += 1
    elif uci[2] == "c":
        result += 2
    elif uci[2] == "d":
        result += 3
    elif uci[2] == "e":
        result += 4
    elif uci[2] == "f":
        result += 5
    elif uci[2] == "g":
        result += 6
    elif uci[2] == "h":
        result += 7
    if uci[3] == "1":
        result += 0
    elif uci[3] == "2":
        result += 8
    elif uci[3] == "3":
        result += 16
    elif uci[3] == "4":
        result += 24
    elif uci[3] == "5":
        result += 32
    elif uci[3] == "6":
        result += 40
    elif uci[3] == "7":
        result += 48
    elif uci[3] == "8":
        result += 56
    return result

def write_board(board):
    board_file = open(r"..\SIMPLE\app\board.txt","w")
    board_file.write(board.fen())
    board_file.close()


# In[8]:


#SET BOARD
board = chess.Board()

#/K option tells cmd to run the command and keep the command window from closing. You may use /C instead to close the command window after the 
#START CHSS
command='start'
proc=Popen(command,creationflags=CREATE_NEW_CONSOLE,stdout=PIPE, stdin=PIPE, stderr=PIPE, shell = True)
time.sleep(3)
wsh= comclt.Dispatch("WScript.Shell")

docker_start_command = "docker-compose exec app python3 testnet.py -d -g 1 -a best_model human -e connect5"
send("cd ..", w=1)
send("cd SIMPLE", w=1)
send(docker_start_command, w=15)

#READ INPUT
while True:
    line = input()
    print()
    line_split = line.split(" ")
    if line == "uci":
        print("id name CPPO 0.1") 
        print("id author tcw74")
        print("option name OwnBook type check default true")
        print("uciok")
    elif line == "quit":
        wsh.AppActivate("C:\Windows\System32\cmd.exe")
        #wsh.Close()
        break
    elif line == "isready":
        print("readyok")
    elif line_split[0] == "position":
        if line_split[1] == "startpos":
            board = chess.Board()
        else:
            board = chess.Board(line_split[2] + " " + line_split[3] + " " + line_split[4] + " " + line_split[5] + " " + line_split[6] + " " + line_split[7])
        if "moves" in line_split:
            for uci_move in line_split[line_split.index("moves")+1:]:
                board.push_uci(uci_move)
        board_file = open(r"..\SIMPLE\app\board.txt","w")
        board_file.write(board.fen())
        board_file.close()
        send("0000")
    elif line_split[0] == "go":
        if len(line_split) > 1:
            if line_split[1] == "infinite":
                while True:
                    line = input()
                    if line == "quit":
                        sys.exit()
                    elif line == "stop":
                        print("bestmove " + get_move())
                        break
                    else: 
                        continue
            elif line_split[1] == "ponder":
                while True:
                    line = input()
                    if line == "quit":
                        sys.exit()
                    elif line == "ponderhit":
                        print("bestmove " + get_move())
                        break
                    else: 
                        continue
            else:
                print("bestmove " + get_move())
                continue
        else:
            print("bestmove " + get_move())
            continue
    else:
        pass

#output = open(r"SIMPLE\app\out.txt","r")
#output.read()
#output.close()

#send("3")

