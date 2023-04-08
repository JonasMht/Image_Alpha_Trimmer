### Image resizing

import sys
import cv2
import os
import numpy as np


# function to load all the images with transparency and their filename in a directory using OpenCV
def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename), cv2.IMREAD_UNCHANGED)
        if img is not None:
            images.append([img, filename])
    return images

# Function to keep only the part of the image that is not transparent using alpha channel using OpenCV
def remove_alpha_edges_from_images(images):
    for i in range(len(images)):
        # Get alpha channel
        alpha = images[i][0][:, :, 3]
        # Get the indices of the non-zero elements
        indices = np.where(alpha > 0)
        # Get the bounding box of the non-zero elements
        x1, y1 = np.min(indices[0]), np.min(indices[1])
        x2, y2 = np.max(indices[0]), np.max(indices[1])
        # Crop the image
        images[i][0] = images[i][0][x1:x2, y1:y2]
    return images


# Function to resize images using openCV
def resize_images(images, size):
    for i in range(len(images)):
        ## Interpolation methods of cv2.resize():
        # INTER_NEAREST: nearest neighbor interpolation technique
        # INTER_LINEAR: bilinear interpolation (default)
        # INTER_LINEAR_EXACT
        # INTER_AREA: resampling using pixel area relation
        # INTER_CUBIC: bicubic interpolation over 4 x 4 pixel neighborhood
        # INTER_LANCZOS4: Lanczos interpolation over 8 x 8 pixel neighborhood
        # INTER_NEAREST_EXACT
        # INTER_MAX
        # WARP_FILL_OUTLIERS
        # WARP_INVERSE_MAP
        images[i][0] = cv2.resize(images[i][0], size, interpolation = cv2.INTER_LANCZOS4)
    return images

# Function that resizes images and then removes the alpha edges using OpenCV
def resize_and_remove_alpha_edges(images, size):
    images = resize_images(images, size)
    images = remove_alpha_edges_from_images(images)
    return images

# Function to save images to a directory using OpenCV
def save_images_to_folder(path, images):
    if not os.path.exists(path):
        os.makedirs(path)
        print("Created folder ", path)
    for image in images:
        cv2.imwrite(os.path.join(path, image[1]), image[0])

# function to save images to a directory using OpenCV keeping transparency
def save_images_to_folder_with_alpha(path, images):
    if not os.path.exists(path):
        os.makedirs(path)
        print("Created folder ", path)
    for image in images:
        cv2.imwrite(os.path.join(path, image[1]), image[0], [cv2.IMWRITE_PNG_COMPRESSION, 0])


src_path = ""
dst_path = ""
size = 0

if len(sys.argv) != 4:
    print("Usage: python resize-images.py <src_path> <dst_path> <size>")
    exit()
else:
    src_path = sys.argv[1]
    dst_path = sys.argv[2]
    size = int(sys.argv[3])

if not os.path.exists(src_path):
    print("Source folder does not exist")
    exit()

if not os.path.exists(dst_path):
    os.makedirs(dst_path)
    print("Created folder ", dst_path)

# Resize

images = load_images_from_folder(src_path)
images = resize_and_remove_alpha_edges(images, (size, size))

save_images_to_folder(dst_path, images)