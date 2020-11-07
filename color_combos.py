# %%
import cv2
import csv

# ******VERY IMPORTANT - CV2 PROCESSES PIXELS AS (B,G,R)*******

# Input image
input = cv2.imread('starry night.png')

# Get input size
height, width = input.shape[:2]

# Desired "pixelated" size
w, h = (32, 32)

# Resize input to "pixelated" size
temp = cv2.resize(input, (w, h), interpolation=cv2.INTER_NEAREST)

# Initialize output image
output = cv2.resize(temp, (width, height), interpolation=cv2.INTER_NEAREST)


rows,cols = temp.shape[:2]
flatten = list()
for i in range(rows):
      for j in range(cols):
        bgr = temp[i,j]
        flatten.append(list([bgr[2], bgr[1], bgr[0]]))

with open("starry_night_rgb.txt", "w") as out:
    for i in flatten:
        out.write(str(i) + '\n')

# cv2.imwrite('the_kiss.jpg', output)
# cv2.imshow('Input', input)
# cv2.imshow('Resized', temp)
# cv2.imshow('Output', output)
# cv2.waitKey(0)


#%%
import itertools
import csv
import webcolors
import pandas as pd
import numpy as np
from scipy import spatial

colors_by_notes = []
with open('color_chart.csv') as file:
    reader = csv.reader(file, lineterminator = '\n')
    colors_by_notes = list(reader)
df_colors = pd.DataFrame(colors_by_notes[1:], columns=colors_by_notes[0])    
flatten = itertools.chain.from_iterable(colors_by_notes[1:])
to_rgb = []
for i in flatten:
    temp = webcolors.hex_to_rgb(i)
    to_rgb.append((temp[0], temp[1], temp[2]))

two_notes = list(itertools.combinations(to_rgb, 2))
three_notes = list(itertools.combinations(to_rgb, 3))

two_notes = [list(map(list, i)) for i in two_notes]
three_notes = [list(map(list, i)) for i in three_notes]

def mix_colors(color_combos_list, length):
    final_list = list()
    final_dict = dict()
    for i in color_combos_list:
        total_red = 0
        total_green = 0
        total_blue = 0
        for j in i:
            total_red = total_red + j[0]
            total_green = total_green + j[1]
            total_blue = total_blue + j[2]
        final_dict.update({(int(total_red/length), int(total_green/length), int(total_blue/length)):i})
        final_list.append((int(total_red/length), int(total_green/length), int(total_blue/length)))
    final = [final_list, final_dict]
    return final

mixed_list_2, mixed_dict_2 = mix_colors(two_notes, 2)
mixed_list_3, mixed_dict_3 = mix_colors(three_notes, 3)

# create "dummy" dict for the basic colors
to_rgb_dict = dict()
for i in to_rgb:
    to_rgb_dict.update({i:i})

# creating the final list and dict
# combining mixed lists 2, 3 and the all to_rgb colors
final_list = mixed_list_2 + mixed_list_3 + to_rgb
final_dict = {**to_rgb_dict, **mixed_dict_2, **mixed_dict_3}

with open("color_combos.txt", "w") as output:
    for i in final_list:
        output.write(str(i) + '\n')

with open("color_combos_dict.txt", "w") as output:
    output.write(str(final_dict))

# %%
