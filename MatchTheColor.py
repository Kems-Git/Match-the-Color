import cv2
import pandas as pd
import numpy as np
import argparse

# Take an image from the user
ap = argparse.ArgumentParser()

# --i and --image are what is used to signal to add an image followed by the image file
ap.add_argument('-i', '--image', required=True, help='Image Path')

# Parse the command line arguments. Use Vars to turn into a python dictionary
args = vars(ap.parse_args())

# Place image file into this variable
img_path = args['image']

# Reading image with opencv
img = cv2.imread(img_path)

# Declare global var
clicked = False
ypos = 0
xpos = 0
b = g = r = 0

# Read the CSV file
# Reading csv file and giving names to each column
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('data\colors.csv', names=index, header=None)

# Create Draw_function
def draw_function (event, x, y, flags, param):
    # If user double clicks, then set values
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, xpos, ypos, clicked
        clicked = True
        ypos = y
        xpos = x
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)

def getColorName(R, G, B):
    minimum = 10000
    # For each row in colors.csv file
    for i in range(len(csv)):
        # Parameter = image color, csv.loc calls color values for red, green, and blue
        distance = abs(R-int(csv.loc[i, 'R'])) + abs(G-int(csv.loc[i, 'G'])) + abs(B-int(csv.loc[i, 'B']))
        # The closer the numbers, the closer to zero
        # Example: R = 255 - csv.loc[R] = 255 = 0
        # The closer to te actual color
        if distance <= minimum:
            minimum = distance
            # Keep the closest to 0 in this variable
            cname = csv.loc[i, 'color_name']
    return cname


# Set a mouse callback event on a window
cv2.namedWindow('image')
# Named the window image above and call to the draw_function() whenever a mouse event occurs
cv2.setMouseCallback('image', draw_function)

# Display image on window
while(1):

    cv2.imshow('image', img)
    if (clicked):
        # cv2.rectangle(image, startpoint, endpoint, color, thickness) -1 thickness fills rectangle entirely
        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)

        # A string to get and display the color name and RGB values
        text = getColorName(r, g, b)

        # cv2.putText(img,text,start,font(0-7), fontScale, color, thickness, lineType, (optional bottomLeft bool) )
        # Default way to show text
        cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        #For very light colours we will display text in black colour
        if(r+g+b>=600):
            cv2.putText(img, text,(50,50),2,0.8,(0,0,0),2,cv2.LINE_AA)

            clicked = False

    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()


