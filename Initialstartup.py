# import the necessary packages
import cv2
import numpy as np
import time as t
#image = cv2.imread('4blue2.jpg')
from image_slicer import slice

def StartupFunc(): # Må sjekke at posisjonene er gyldig før man godkjenner checken
    def CalibratePosOfBoard():
        isittrue = 0
        while(isittrue == 0):
            image = cv2.imread(r"SPLITIMG\rawimg.png")

            lower = [86, 31, 4]
            upper = [220, 88, 50]
            # create NumPy arrays from the boundaries
            lower = np.array(lower, dtype = "uint8")
            upper = np.array(upper, dtype = "uint8")
            # find the colors within the specified boundaries and apply
            # the mask
            mask = cv2.inRange(image, lower, upper)

            # alt over er for å få tak i alle blå prikker i hjørnene

            def getcornerpos(listofpos):
                totalpos1 = 0
                totalpos2 = 0
                i = 0
                try:
                    for pos in listofpos:
                        totalpos1 += pos[0]
                        totalpos2 += pos[1]
                        i += 1
                    avrgpos1 = totalpos1/i
                    avrgpos2 = totalpos2/i
                    return avrgpos1, avrgpos2, "Worked"
                except:
                    avrgpos1 = 0
                    avrgpos2 = 0
                    return avrgpos1, avrgpos2, "Failed"

            UPLEFT = []
            LOLEFT = []
            UPRIGH = []
            LORIGH = []


            for value in np.transpose(mask.nonzero()):
                if value[0] < image.shape[0]/2 and value[1] < image.shape[1]/2: #Upper left corner i think
                    UPLEFT.append(value)
                if value[0] > image.shape[0]/2 and value[1] < image.shape[1]/2: #Lower left corner i think
                    LOLEFT.append(value)
                if value[0] < image.shape[0]/2 and value[1] > image.shape[1]/2: #Upper right corner i think
                    UPRIGH.append(value)
                if value[0] > image.shape[0]/2 and value[1] > image.shape[1]/2: # Lower Right
                    LORIGH.append(value)

            ValUPLEFT = getcornerpos(UPLEFT)
            ValLOLEFT = getcornerpos(LOLEFT)
            ValUPRIGH = getcornerpos(UPRIGH)
            ValLORIGH = getcornerpos(LORIGH)


            listofpos = [ValUPLEFT, ValLOLEFT, ValUPRIGH, ValLORIGH]

            for pos in listofpos:
                if pos[2] == "Failed":
                    isittrue = 0
                else:
                    return [[int(ValUPLEFT[1]), int(ValUPLEFT[0])], [int(ValLOLEFT[1]), int(ValLOLEFT[0])], [int(ValUPRIGH[1]), int(ValUPRIGH[0])], [int(ValLORIGH[1]), int(ValLORIGH[0])]]
                #cv2.circle(image,(int(pos[1]),int(pos[0])), 18, (0,0,255), -1)


    Positisons = CalibratePosOfBoard()
    while Positisons[0][0] == 0 or Positisons[1][0] == 0 or Positisons[2][0] == 0 or Positisons[3][0] == 0:
        Positisons = CalibratePosOfBoard()
        t.sleep(2)
        print(Positisons)
        cv2.destroyAllWindows()
        cv2.imwrite(r"SPLITIMG\rawimg.png", cv2.VideoCapture(0, cv2.CAP_DSHOW).read()[1])


    img = cv2.imread(r"SPLITIMG\rawimg.png") #image 
    # specify desired output size 

    width = 400
    height = 400

    # specify conjugate x,y coordinates (not y,x)
    input = np.float32([Positisons[0], Positisons[1], Positisons[3], Positisons[2]])
    output = np.float32([[0,0], [width-1,0], [width-1,height-1], [0,height-1]])

    # compute perspective matrix
    matrix = cv2.getPerspectiveTransform(input,output)
    # do perspective transformation setting area outside input to black
    imgOutput = cv2.warpPerspective(img, matrix, (width,height), cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0))

    # save the warped output
    cv2.imwrite("SPLITIMG\Wraped.jpg", imgOutput)

    slice("SPLITIMG\Wraped.jpg", 64)
    #return Positisons