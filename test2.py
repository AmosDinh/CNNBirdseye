
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

    # get conours in gray image
    contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # draw contours on black image
    black = np.zeros_like(gray)
    #cv2.drawContours(black, contours, -1, (255,255,255), 1)
  
    # for contour in contours:
    #     if len(contour) < 5:
    #         continue
    #     # Fit an ellipse to the contour
    #     ellipse = cv2.fitEllipse(contour)
        
    #     # Extract the angle from the ellipse
    #     angle = ellipse[2]

    #     # Draw the ellipse on the original image
        
    #     cv2.ellipse(img, ellipse, (0, 255, 0), 2)

    #     # Display the angle
    #     print(f"Contour angle: {angle} degrees")
    for contour in contours:
        # Filter out contours with fewer than 5 points
        if len(contour) >= 5:
            # Fit an ellipse to the contour
            ellipse = cv2.fitEllipse(contour)
            
            # Extract ellipse parameters
            center, axes, angle = ellipse
            major_axis, minor_axis = axes

            # Extend contours on both sides of the ellipse angle
            extension_distance = 20  # Adjust the distance as needed

            # Calculate points on the major and minor axes
            major_axis_point = (
                int(center[0] + extension_distance * np.cos(np.radians(angle))),
                int(center[1] + extension_distance * np.sin(np.radians(angle)))
            )
            minor_axis_point = (
                int(center[0] + extension_distance * np.cos(np.radians(angle + 90))),
                int(center[1] + extension_distance * np.sin(np.radians(angle + 90)))
            )

            # Connect the points to create extended contours
            extended_contour = np.array([major_axis_point, minor_axis_point], dtype=np.int32)
            
            # Draw the extended contour on the copy of the original image
            cv2.polylines(img, [extended_contour], isClosed=False, color=(0, 255, 0), thickness=2)

    cv2.destroyAllWindows()

    # side_by_side = np.hstack((img, gray))
    cv2.imshow("Side by Side", img)
    cv2.waitKey(0)
    
trace_walkable_sections('google_maps2.png')