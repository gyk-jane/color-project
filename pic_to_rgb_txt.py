import itertools
import csv
import cv2
import webcolors
import pandas as pd
import numpy as np
from scipy import spatial

# creation of text file of rgb codes of the art
# ******VERY IMPORTANT - CV2 PROCESSES PIXELS AS (B,G,R)*******
def picture_to_rgb_text(filepath, art_name):
    # Input image
    input_img = cv2.imread(filepath)
    # Get input_img size
    height, width = input_img.shape[:2]

    # Desired "pixelated" size
    w, h = (32, 32)

    # Resize input_img to "pixelated" size
    temp = cv2.resize(input_img, (w, h), interpolation=cv2.INTER_NEAREST)

    # Initialize output image
    # pixelated image of the art 
    output = cv2.resize(temp, (width, height), interpolation=cv2.INTER_NEAREST)

    rows,cols = temp.shape[:2]
    flatten = list()
    for i in range(rows):
        for j in range(cols):
            bgr = temp[i,j]
            flatten.append(list([bgr[2], bgr[1], bgr[0]]))

    with open(art_name + '.txt', "w") as out:
        for i in flatten:
            out.write(str(i) + '\n')
    
    # cv2.imwrite('starry_night_pixelated.jpg', output)

picture_to_rgb_text('artists/munch/the scream.jpg', "the_scream")