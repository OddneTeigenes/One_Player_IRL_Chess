# import the necessary packages
import numpy as np
import cv2
#image = cv2.imread('4blue2.jpg')
vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)
while True:
    image = vid.read()[1]
    lower = [86, 31, 4]
    upper = [220, 88, 50]
    # create NumPy arrays from the boundaries
    lower = np.array(lower, dtype = "uint8")
    upper = np.array(upper, dtype = "uint8")
    # find the colors within the specified boundaries and apply
    # the mask
    mask = cv2.inRange(image, lower, upper)
    output = cv2.bitwise_and(image, image, mask = mask)
    # show the images

    cv2.imshow("images", np.hstack([image, output]))
    cv2.waitKey(0)
    cv2.imshow("images", image)
    cv2.waitKey(0)

    #print(cv2.countNonZero(mask))
    #print(np.transpose(mask.nonzero()))


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
            return avrgpos1, avrgpos2
        except:
            avrgpos1 = 0
            avrgpos2 = 0
            return avrgpos1, avrgpos2

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
        #print(int(pos[0]))
        cv2.circle(image,(int(pos[1]),int(pos[0])), 18, (0,0,255), -1)
        print(pos[0])
        print(pos[1])

    cv2.imshow("images", image)
    cv2.waitKey(0)
































'''# import the necessary packages
import numpy as np
import argparse
import cv2
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image")
args = vars(ap.parse_args())
# load the image
image = cv2.imread(args["image"])

# define the list of boundaries
boundaries = [
	([86, 31, 4], [220, 88, 50]),
]

# loop over the boundaries
for (lower, upper) in boundaries:
	# create NumPy arrays from the boundaries
	lower = np.array(lower, dtype = "uint8")
	upper = np.array(upper, dtype = "uint8")
	# find the colors within the specified boundaries and apply
	# the mask
	mask = cv2.inRange(image, lower, upper)
	output = cv2.bitwise_and(image, image, mask = mask)
	# show the images
	cv2.imshow("images", np.hstack([image, output]))
	cv2.waitKey(0)
'''