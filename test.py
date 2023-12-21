
import cv2
import numpy as np

def get_minimap(img):
    #x, y, width, height = 24, 482, 214, 214
    #minimap = img[y:y + height, x:x + width]
    return img

def trace_walkable_sections(image_path):
    # Read the image
    img = cv2.imread(image_path)
    img = get_minimap(img)
    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define lower and upper bounds for blue color (you may need to adjust these values)
    # lower_blue = np.array([76, 49, 168])
    # upper_blue = np.array([98, 246, 247])
    #     cv2.setTrackbarPos('HMax', 'image', 107)
    # cv2.setTrackbarPos('SMax', 'image', 229)
    # cv2.setTrackbarPos('VMax', 'image', 237)
    # cv2.setTrackbarPos('HMin', 'image', 92)
    # cv2.setTrackbarPos('SMin', 'image', 9)
    # cv2.setTrackbarPos('VMin', 'image', 172)
    lower_blue = np.array([92, 9, 172])
    upper_blue = np.array([107, 229, 237])


    # Thresholding to get binary image
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    

    # Optional: Apply morphological operations for noise reduction
    #kernel = np.ones((5, 5), np.uint8)
    #mask = cv2.erode(mask, kernel, iterations=1)
    #mask = cv2.dilate(mask, kernel, iterations=1)

    result = cv2.bitwise_and(img, img, mask=mask)
    result[np.where((result != [0,0,0]).all(axis = 2))] = [255,255,255]
    gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Remove small contours
    contours = [c for c in contours if cv2.contourArea(c) > 200]
    filtered_contours_mask = np.zeros_like(mask)
    cv2.drawContours(filtered_contours_mask, contours, -1, (255), thickness=cv2.FILLED)
    result_gray = cv2.bitwise_and(gray, gray, mask=filtered_contours_mask)


    
    # side_by_side = np.hstack((img, gray))
    cv2.imshow("Side by Side", result_gray)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
trace_walkable_sections('images/20231221093425150346e5b50366-a123-42d3-9653-c34197c025a5_Palo_Alto_CA_bev.png')