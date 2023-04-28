### Image resizing

import cv2
import os
import numpy as np
import sys

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
def resize_images(images, factor):
    for i in range(len(images)):
        # Get the size of the image
        height, width = images[i][0].shape[:2]
        # Resize the image
        size = (int(width * factor), int(height * factor))

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
def resize_and_remove_alpha_edges(images, factor):
    images = resize_images(images, factor)
    images = remove_alpha_edges_from_images(images)
    return images

# Function to save images to a directory using OpenCV
def save_images_to_folder(folder, images):
    if not os.path.exists(folder):
        os.makedirs(folder)
        print("Created folder ", folder)
    for image in images:
        cv2.imwrite(os.path.join(folder, image[1]), image[0])

# function to save images to a directory using OpenCV keeping transparency
def save_images_to_folder_with_alpha(folder, images):
    if not os.path.exists(folder):
        os.makedirs(folder)
        print("Created folder ", folder)
    for image in images:
        cv2.imwrite(os.path.join(folder, image[1]), image[0], [cv2.IMWRITE_PNG_COMPRESSION, 0])

src = ""
dst = ""
factor = 1.0

# get src dst and factor from user python input
if len(sys.argv) > 1:
    src = sys.argv[1]
    dst = sys.argv[2]
    factor = float(sys.argv[3])

if src == "" or dst == "":
    print("Please provide src and dst folder")
    sys.exit()

# If folder does not exist create it
if not os.path.exists(dst):
    os.makedirs(dst)
    print("Created folder ", dst)

# Resize

images = load_images_from_folder(src)
images = resize_and_remove_alpha_edges(images, factor)
save_images_to_folder(dst, images)
