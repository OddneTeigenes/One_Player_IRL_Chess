# import the necessary packages
import numpy as np
import cv2
import os
# load the image
image = cv2.imread("SPLITIMG\Wraped.jpg")

# define the list of boundaries
boundaries = [
	#([17, 15, 100], [50, 56, 200]),
	#([0, 85, 0], [100, 255, 100]),
	#([25, 146, 190], [62, 174, 250]),
	#([25, 100, 180], [45, 180, 255]),
	#([22, 93, 0], [45, 255, 255])
	([80, 230, 230], [170, 255, 255]),
	([45, 90 , 0], [110, 250, 102])
]


# loop over the boundaries

numrow = 1
while numrow <= 8:
	numplace = 1
	while numplace <= 8:
		string = str("_0" + str(numrow) + "_0" + str(numplace))
		img = "SPLITIMG\Wraped"  + string + ".png" #.jpg"# + string + ".png"
		for (lower, upper) in boundaries:
			image = cv2.imread(img)
			# create NumPy arrays from the boundaries
			lower = np.array(lower, dtype = "uint8")
			upper = np.array(upper, dtype = "uint8")
			# find the colors within the specified boundaries and apply
			# the mask
			mask = cv2.inRange(image, lower, upper)
			output = cv2.bitwise_and(image, image, mask = mask)
			# show the images
			print(np.transpose(mask.nonzero()).size)
			print(string)
			cv2.imshow("images", np.hstack([image, output]))
			cv2.waitKey(0)
		numplace += 1
	numrow += 1