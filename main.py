# Importing Libraries

import numpy as np
import cv2
import time

# Object for Capuring the video from camera

vcap = cv2.VideoCapture(0)

# Setting up webcam

time.sleep(2)

background = 0

# Capturing the background multiple times

for i in range(30):
    
    ret, background = vcap.read()

while(vcap.isOpened()):
    
    ret, img = vcap.read()
    
    if not ret:
        break
    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# HSV values
    lower_white = np.array([0,120, 70])
    upper_white = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_white, upper_white) #Cloak Partition
    
    lower_white = np.array([170, 120, 70])
    upper_white = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_white, upper_white)
    
    mask1 = mask1 + mask2 # Operator overloading for OR logic
    
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=2) #Noise Removal
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8), iterations=1) #Improve smoothness
    
    mask2 = cv2.bitwise_not(mask1)
    
    result1 = cv2.bitwise_and(background, background, mask = mask1) # Colour Segmentation
    
    result2 = cv2.bitwise_and(img, img, mask = mask2) # Remove cloak
    
    final_outcome = cv2.addWeighted(result1, 1, result2, 1, 0)
    
    cv2.imshow("Harry Potter", final_outcome)
    
    x = cv2.waitKey(10)
    if x == 27:
        break

vcap.release()
cv2.destroyAllWindows()

    