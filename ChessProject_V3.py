# import the necessary packages
import cv2
import Initialstartup
import string
import numpy as np
import time as t
import os
from stockfish import Stockfish

#
#Improvements left:
#Make it dynamically get range for color
#Make it able to detect check mate
#

#Download stockfish engine and link it here:
stockfish = Stockfish("stockfish_14_win_x64_avx2\stockfish_14_x64_avx2.exe")

#Set values for green and yellow upper and lower limits of color
lower = np.array([45, 90 , 0], dtype = "uint8") #[30, 75, 0], dtype = "uint8")
upper = np.array([110, 250, 102], dtype = "uint8") #[120, 255, 102], dtype = "uint8")
lowerYellow = np.array([80, 230, 230], dtype = "uint8")
upperYellow = np.array([170, 255, 255], dtype = "uint8")

#closes all windows
cv2.destroyAllWindows()
#takes a picture (might need to change the 0 in VideoCapture depending on how many cameras are connected)
cv2.imwrite(r"SPLITIMG\rawimg.png", cv2.VideoCapture(0, cv2.CAP_DSHOW).read()[1])

#This function finds the corners, 
#Cuts it to a just have the chessboard in frame,
#Flattens the image, 
#Splits it to 64 pictures
#and puts it in the SPLITIMG folder 
Initialstartup.StartupFunc()

Elo_Rating = input("Set elo rating of your oponent: ")
stockfish.set_elo_rating(Elo_Rating)
Color_of_Pieces = input("Choose witch color to play with, white or black, type 'w' or 'b': ")

Boardmem = [ # 1=2=Pawn, 3=4=Rook, 5=6=Horse, 7=8=Bishop, 9=10=queen, 11=12=king, even = white, odd = black
        [3,5,7,9,11,7,5,3],
        [1,1,1,1,1,1,1,1 ],
        [0,0,0,0,0,0,0,0 ],
        [0,0,0,0,0,0,0,0 ],
        [0,0,0,0,0,0,0,0 ],
        [0,0,0,0,0,0,0,0 ],
        [2,2,2,2,2,2,2,2 ],
        [4,6,8,10,12,8,6,4],
    ]

def renderboard():
    '''print("========================")
    for row in Boardmem:
        print(row)
    print("========================")'''
    os.system('cls')
    print("Hello, have a good game :D")
    print('')
    print(stockfish.get_board_visual())
    print('')
    print('current eval: ' + str(stockfish.get_evaluation()))

#Stockfish makes a move
def stockfishmove():
    global Boardmem
    l1 = [8,7,6,5,4,3,2,1,0]
    Stockmove = stockfish.get_best_move()
    stockfish.make_moves_from_current_position([Stockmove])
    Boardmem[l1[int(Stockmove[3])]][int(string.ascii_lowercase.index(Stockmove[2]))] = Boardmem[l1[int(Stockmove[1])]][int(string.ascii_lowercase.index(Stockmove[0]))]
    Boardmem[l1[int(Stockmove[1])]][int(string.ascii_lowercase.index(Stockmove[0]))] = 0
    renderboard()

def updateboard(oldpos, newpos):
    global Boardmem 
    oldlist = oldpos.split('_0')
    newlist = newpos[0].split('_0')
    l1 = [8,7,6,5,4,3,2,1,0]
    Boardmem[int(newlist[1])-1][int(l1[int(newlist[2])])] = Boardmem[int(oldlist[1])-1][int(l1[int(oldlist[2])])]
    Boardmem[int(oldlist[1])-1][int(l1[int(oldlist[2])])] = 0
    renderboard()

def ismovelegal(oldpos, newpos):
    oldlist = oldpos.split('_0')
    newlist = newpos[0].split('_0')
    l1 = ['0','8','7','6','5','4','3','2','1']
    l2 = ['0','h','g','f','e','d','c','b','a']
    move =  l2[int(oldlist[2])] + l1[int(oldlist[1])] + l2[int(newlist[2])] + l1[int(newlist[1])]
    legalornot = stockfish.is_move_correct(move)
    if legalornot == True:
        pass
    else:
        print(move + " is an illegal move")
    return legalornot, move

def wherearepices():
    global Boardmem
    whiteishere = []
    blackishere = []
    emptyishere  = []
    whiterooksarehere = []
    blackrooksarehere = []
    l1 = [8,7,6,5,4,3,2,1]
    numrow = 1
    for row in Boardmem:
        numplace = 0
        for piece in row:
            if piece == 12:
                whitekingishere = str("_0" + str(numrow) + "_0" + str(l1[numplace]))
                whiteishere.append(string)
            elif piece == 11: #må få kameraet til å alltid sjekke kongen først
                blackkingishere = str("_0" + str(numrow) + "_0" + str(l1[numplace]))
                blackishere.append(string)
            elif piece == 4: 
                string = str("_0" + str(numrow) + "_0" + str(l1[numplace]))
                whiterooksarehere.append(string)
                whiteishere.append(string)
            elif piece == 3: 
                string = str("_0" + str(numrow) + "_0" + str(l1[numplace]))
                blackrooksarehere.append(string)
                blackishere.append(string)
            elif piece == 0:
                string = str("_0" + str(numrow) + "_0" + str(l1[numplace]))
                emptyishere.append(string)
            elif (piece % 2) == 0:
                string = str("_0" + str(numrow) + "_0" + str(l1[numplace]))
                whiteishere.append(string) #White
            else:
                string = str("_0" + str(numrow) + "_0" + str(l1[numplace]))
                blackishere.append(string) #black
            numplace += 1
        numrow += 1
    return whiteishere, blackishere, emptyishere, whitekingishere, blackkingishere, whiterooksarehere, blackrooksarehere



if Color_of_Pieces == 'w':
    renderboard()
    while True:
        cv2.destroyAllWindows()
        cv2.imwrite(r"SPLITIMG\rawimg.png", cv2.VideoCapture(0, cv2.CAP_DSHOW).read()[1])
        Initialstartup.StartupFunc() #Could make this better by not having it find the corners each time... but thats a mission for another day ... kinda disagree now but eh, maybe
        listofpiecepos = wherearepices()
        #print(listofpiecepos)
        missing = []
        image = cv2.imread('SPLITIMG\Wraped' + listofpiecepos[3] + '.png') #sjekker kongen først
        mask = cv2.inRange(image, lower, upper)
        if np.transpose(mask.nonzero()).size <= 10:
            print("missing piece is: " + listofpiecepos[3])
            missing.append(listofpiecepos[3])
            t.sleep(1)
            cv2.destroyAllWindows()
            cv2.imwrite(r"SPLITIMG\rawimg.png", cv2.VideoCapture(0, cv2.CAP_DSHOW).read()[1])
            Initialstartup.StartupFunc()
            image = cv2.imread('SPLITIMG\\Wraped' + missing[0] + '.png')
            mask = cv2.inRange(image, lower, upper)
            if np.transpose(mask.nonzero()).size <= 15:
                print("piece is confirmed missing: " + missing[0] )
                t.sleep(1)
                cv2.destroyAllWindows()
                cv2.imwrite(r"SPLITIMG\rawimg.png", cv2.VideoCapture(0, cv2.CAP_DSHOW).read()[1])
                Initialstartup.StartupFunc()
                for piece in listofpiecepos[5]:
                    image = cv2.imread('SPLITIMG\Wraped' + piece + '.png')
                    mask = cv2.inRange(image, lower, upper)
                    if np.transpose(mask.nonzero()).size <= 20:
                        print("missing piece is: " + piece)
                        missing.append(piece)
                if len(missing) >= 2:
                    num = missing[1].split('_0')
                    if int(num[2]) >= 4:
                        updateboard("_08_04", ["_08_06"]) #flytter kongen
                        updateboard("_08_08", ["_08_05"]) #flytter tårnet
                        stockfish.make_moves_from_current_position([ismovelegal("_08_04", ["_08_06"])[1]])
                        stockfishmove()
                    else:
                        updateboard("_08_04", ["_08_02"])
                        updateboard("_08_01", ["_08_03"])
                        stockfish.make_moves_from_current_position([ismovelegal("_08_04", ["_08_02"])[1]])
                        stockfishmove()

        else:
            for piece in listofpiecepos[0]:
                image = cv2.imread('SPLITIMG\Wraped' + piece + '.png')
                mask = cv2.inRange(image, lower, upper)
                if np.transpose(mask.nonzero()).size <= 10:
                    print("missing piece is: " + piece)
                    missing.append(piece)
            if len(missing) != 0:
                t.sleep(1)
                cv2.destroyAllWindows()
                cv2.imwrite(r"SPLITIMG\rawimg.png", cv2.VideoCapture(0, cv2.CAP_DSHOW).read()[1])
                Initialstartup.StartupFunc()
                image = cv2.imread('SPLITIMG\\Wraped' + missing[0] + '.png')
                mask = cv2.inRange(image, lower, upper)
                if np.transpose(mask.nonzero()).size <= 15:
                    print("piece is confirmed missing: " + missing[0] )
                    thereuare = []
                    while len(thereuare) == 0:
                        for foundyou in listofpiecepos[2]:
                            image = cv2.imread('SPLITIMG\\Wraped' + foundyou + '.png')
                            mask = cv2.inRange(image, lower, upper)
                            if np.transpose(mask.nonzero()).size >= 15:
                                thereuare.append(foundyou)
                        if len(thereuare) == 0:
                            for foundyou in listofpiecepos[1]:
                                image = cv2.imread('SPLITIMG\\Wraped' + foundyou + '.png')
                                mask = cv2.inRange(image, lower, upper)
                                if np.transpose(mask.nonzero()).size >= 15:
                                    thereuare.append(foundyou)
                            if len(thereuare) == 0:
                                cv2.imwrite(r"SPLITIMG\rawimg.png", cv2.VideoCapture(0, cv2.CAP_DSHOW).read()[1])
                                Initialstartup.StartupFunc()
                                t.sleep(1)
                                print("Sorry but i cant find the piece")
                    if ismovelegal(missing[0], thereuare)[0] == True:
                        print(ismovelegal(missing[0], thereuare)[1] + " is a legal move")
                        stockfish.make_moves_from_current_position([ismovelegal(missing[0], thereuare)[1]])
                        updateboard(missing[0], thereuare)
                        stockfishmove()
                    else:
                        print("please move piece back too original position")
        t.sleep(2)

else:
    stockfishmove()
    while True:
        renderboard()
        cv2.destroyAllWindows()
        cv2.imwrite(r"SPLITIMG\rawimg.png", cv2.VideoCapture(0, cv2.CAP_DSHOW).read()[1])
        Initialstartup.StartupFunc()
        listofpiecepos = wherearepices()
        missing = []
        image = cv2.imread('SPLITIMG\Wraped' + listofpiecepos[4] + '.png') #sjekker kongen først
        mask = cv2.inRange(image, lowerYellow, upperYellow)
        if np.transpose(mask.nonzero()).size <= 10:
            print("missing piece is: " + listofpiecepos[4])
            missing.append(listofpiecepos[4])
            t.sleep(1)
            cv2.destroyAllWindows()
            cv2.imwrite(r"SPLITIMG\rawimg.png", cv2.VideoCapture(0, cv2.CAP_DSHOW).read()[1])
            Initialstartup.StartupFunc()
            image = cv2.imread('SPLITIMG\\Wraped' + missing[0] + '.png')
            mask = cv2.inRange(image,lowerYellow, upperYellow)
            if np.transpose(mask.nonzero()).size <= 15:
                print("piece is confirmed missing: " + missing[0] )
                t.sleep(1)
                cv2.destroyAllWindows()
                cv2.imwrite(r"SPLITIMG\rawimg.png", cv2.VideoCapture(0, cv2.CAP_DSHOW).read()[1])
                Initialstartup.StartupFunc()
                for piece in listofpiecepos[6]:
                    image = cv2.imread('SPLITIMG\Wraped' + piece + '.png')
                    mask = cv2.inRange(image, lowerYellow, upperYellow)
                    if np.transpose(mask.nonzero()).size <= 20:
                        print("missing piece is: " + piece)
                        missing.append(piece)
                if len(missing) >= 2:
                    num = missing[1].split('_0')
                    if int(num[2]) >= 4:
                        updateboard("_01_04", ["_01_06"]) #flytter kongen
                        updateboard("_01_08", ["_01_05"]) #flytter tårnet
                        stockfish.make_moves_from_current_position([ismovelegal("_01_04", ["_01_06"])[1]])
                        stockfishmove()
                    else:
                        updateboard("_01_04", ["_01_02"])
                        updateboard("_01_01", ["_01_03"])
                        stockfish.make_moves_from_current_position([ismovelegal("_01_04", ["_01_02"])[1]])
                        stockfishmove()

        else:
            for piece in listofpiecepos[1]:
                image = cv2.imread('SPLITIMG\Wraped' + piece + '.png')
                mask = cv2.inRange(image, lowerYellow, upperYellow)
                if np.transpose(mask.nonzero()).size >= 10:
                    pass
                else:
                    print("missing piece is: " + piece)
                    missing.append(piece)
            if len(missing) != 0:
                t.sleep(1)
                cv2.destroyAllWindows()
                cv2.imwrite(r"SPLITIMG\rawimg.png", cv2.VideoCapture(0, cv2.CAP_DSHOW).read()[1])
                Initialstartup.StartupFunc()
                for piece in missing: #Assuming only one piece is moved
                    image = cv2.imread('SPLITIMG\\Wraped' + piece + '.png')
                    mask = cv2.inRange(image, lowerYellow, upperYellow)
                    if np.transpose(mask.nonzero()).size <= 15:
                        print("piece is confirmed missing: " + piece )
                        #findpiece, and update board
                        thereuare = []
                        while len(thereuare) == 0:
                            for foundyou in listofpiecepos[2]:
                                image = cv2.imread('SPLITIMG\\Wraped' + foundyou + '.png')
                                mask = cv2.inRange(image, lowerYellow, upperYellow)
                                if np.transpose(mask.nonzero()).size >= 15:
                                    thereuare.append(foundyou)
                            if len(thereuare) == 0:
                                for foundyou in listofpiecepos[0]:
                                    image = cv2.imread('SPLITIMG\\Wraped' + foundyou + '.png')
                                    mask = cv2.inRange(image, lowerYellow, upperYellow)
                                    if np.transpose(mask.nonzero()).size >= 15:
                                        thereuare.append(foundyou)
                                if len(thereuare) == 0:
                                    t.sleep(1)
                                    print("Sorry but i cant find the piece")
                        if ismovelegal(piece, thereuare)[0] == True:
                            stockfish.make_moves_from_current_position([ismovelegal(piece, thereuare)[1]])
                            updateboard(piece, thereuare)
                            stockfishmove()
                        else:
                            print("please move piece back too original position")
        t.sleep(2)
