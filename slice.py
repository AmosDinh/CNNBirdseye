# find possible directions to move

import cv2
import numpy as np

def get_minimap(img):
    x, y, width, height = 24, 482, 214, 214
    minimap = img[y:y + height, x:x + width]
    return minimap

def trace_walkable_sections(image_path):
    # Read the image
    img = cv2.imread(image_path)
    img = get_minimap(img)
    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define lower and upper bounds for blue color (you may need to adjust these values)
    lower_blue = np.array([76, 49, 168])
    upper_blue = np.array([98, 246, 247])

    # Thresholding to get binary image
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    

    # Optional: Apply morphological operations for noise reduction
    #kernel = np.ones((5, 5), np.uint8)
    #mask = cv2.erode(mask, kernel, iterations=1)
    #mask = cv2.dilate(mask, kernel, iterations=1)

    # Find contours
    #contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw contours on a blank image
    #result = np.zeros_like(img)
    result = cv2.bitwise_and(img, img, mask=mask)
    result[np.where((result != [0,0,0]).all(axis = 2))] = [255,255,255]
    gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)


    
    # side_by_side = np.hstack((img, gray))
    cv2.imshow("Side by Side", gray)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
trace_walkable_sections('google_maps2.png')