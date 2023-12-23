import PIL 
from PIL import Image
import cv2
import os
count = 0
total_count = 0
from tqdm.auto import tqdm
from trace_walkable_sections import trace_walkable_sections

resize_width = 256
resize_height = 144

dataset_folder = 'images_preprocessed'

# batches
images = os.listdir('images')

# key images:
bev_images = [image for image in images if '_bev' in image]
# only if bev exists, the batch of 5 images is useful
for bev_image in tqdm(bev_images):
    img = cv2.imread('images/' + bev_image)
    grayscale = trace_walkable_sections(img, False)

    # resize
    grayscale = cv2.resize(grayscale, (resize_width, resize_height), interpolation=cv2.INTER_AREA)
    img = cv2.resize(img, (resize_width, resize_height), interpolation=cv2.INTER_AREA)
    
    # save
    cv2.imwrite(dataset_folder+'/' + bev_image, img)
    cv2.imwrite(dataset_folder+'/' + bev_image.replace('_bev', '_grayscale'), grayscale)
    
    for direction in ['north', 'south', 'east', 'west']:
        direction_image = bev_image.replace('_bev', '_'+direction)
        if direction_image in images:
            img = cv2.imread('images/' + direction_image)
            img = cv2.resize(img, (resize_width, resize_height), interpolation=cv2.INTER_AREA)
            cv2.imwrite(dataset_folder+'/' + direction_image, img)