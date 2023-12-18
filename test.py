import cv2
import numpy as np
import random

def draw_random_white_curves(image_size, num_curves, max_curve_length, max_curve_angle, curve_thickness, black_noise_intensity):
    # Create a blank black image
    img = np.zeros((image_size[1], image_size[0], 3), dtype=np.uint8)
    num_curves = random.randint(num_curves[0], num_curves[1])
    for _ in range(num_curves):
        # Generate random number of points for the curve
        num_points = random.randint(3, max_curve_length)
        
        # Generate random starting angle for the curve
        start_angle = random.uniform(0, 2 * np.pi)

        # Generate random segment lengths and angles
        segments = []
        for _ in range(num_points):
            segment_length = random.randint(30, 40)  # Adjust the range as needed
            segment_angle = random.uniform(-max_curve_angle, max_curve_angle)
            segments.append((segment_length, segment_angle))

        # Calculate curve points
        points = []
        current_point = (random.randint(0, image_size[0]), random.randint(0, image_size[1]))
        points.append(current_point)

        for length, angle in segments:
            x, y = current_point
            x += length * np.cos(start_angle + angle)
            y += length * np.sin(start_angle + angle)
            current_point = (int(x), int(y))
            points.append(current_point)

        # Draw the curve in white color
        color = (255, 255, 255)
        is_closed = False  # Set to True if you want to close the 
        thickness = np.random.randint(curve_thickness[0], curve_thickness[1])
        cv2.polylines(img, [np.array(points)], isClosed=is_closed, color=color, thickness=thickness)

    
    black_spots_intensity = 0.02  # Adjust the intensity of the black spots
    max_spot_radius = 20  # Adjust the maximum radius of the spots
    num_clusters = 9  # Adjust the number of clusters
    max_cluster_size =6000  # Adjust the maximum size of each cluster
    cluster_intensity = 10  # Adjust the intensity of clustering

    # Add black noise
    cluster_positions = [(random.randint(0, img.shape[1]), random.randint(0, img.shape[0])) for _ in range(num_clusters)]
    img_original = img.copy()
    for cluster_center in cluster_positions:
        # Generate points within each cluster
        cluster_points = []
        for _ in range(random.randint(max_cluster_size//3, max_cluster_size)):
            x_offset = int(np.random.normal(0, cluster_intensity))
            y_offset = int(np.random.normal(0, cluster_intensity))
            x = min(max(0, cluster_center[0] + x_offset), img.shape[1] - 1)
            y = min(max(0, cluster_center[1] + y_offset), img.shape[0] - 1)
            cluster_points.append((x, y))

        # Add points to the image
        for point in cluster_points:
            img[point[1], point[0]] = (0, 0, 0)

    return img_original, img

# Image size
image_size = (214, 214)

# Number of curves, maximum curve length, maximum curve angle, curve thickness, and black noise intensity
num_curves = (2,6)
max_curve_length = 210
max_curve_angle = np.pi / 2  # 45 degrees
curve_thickness = (3,9)
black_noise_intensity = 0.02  # Adjust the intensity of the black noise

# Create an image with random white curves and black noise
original, random_curves_with_black_noise = draw_random_white_curves(image_size, num_curves, max_curve_length, max_curve_angle, curve_thickness, black_noise_intensity)

# Display the result
cv2.imshow('Random Curves with Black Noise', random_curves_with_black_noise)
cv2.waitKey(0)
cv2.destroyAllWindows()
