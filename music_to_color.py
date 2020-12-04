import csv
import pandas as pd 
import re
from math import sqrt
import matplotlib
from matplotlib import pyplot as plt
import numpy as np 
import ast
from PIL import Image
from PIL import ImageFilter

# extract default color <--> note relationship data from csv file into dataframe
df_colors = pd.read_csv('color data/color_chart_RGB.csv')


# @param string type: name of the csv file which contains all the notes of the music in a disgestable format
# @return the final chart which shows the "picture" of the note -> color conversion (basically, shows the final product)
def get_chart(csv_file):
    all_notes = []
    with open(csv_file) as file:
        reader = csv.reader(file, lineterminator = '\n')
        all_notes = list(reader)

    all_beats_to_colors = list()
    for row in all_notes:
        if row[0] == 'type':
            continue
        elif row[0] == 'note':
            all_beats_to_colors.append(note_to_color(row[1]))
        elif row[0] == 'chord':
            all_beats_to_colors.append(chord_to_color(row[1]))
        else:
            all_beats_to_colors.append([255,255,255])

    perf_square_colorlist = modified_list(all_beats_to_colors)
    even_list = np.array_split(perf_square_colorlist, sqrt(len(perf_square_colorlist)))

    # img = Image.fromarray(even_list)
    # img.show()
    matplotlib.rc('axes',edgecolor='w')
    plt.imshow(even_list, interpolation = 'nearest')
    plt.show()
    

# @param string type: is one of the three, "note", "rest", or "chord"
# @param string or list
# @return one RGB code corresponding to the note or lackthereof (rest) in which the returned RGB code is white [255,255,255]; type: numpy array
def note_to_color(beat):
    letter_only = ''.join(re.findall('[A-Z#]', str(beat)))
    octave = ''.join(re.findall('[1-7]', str(beat)))
    rgb_code = df_colors[letter_only][int(octave)-1]
    return ast.literal_eval(rgb_code)

# @param string type containing 2 or more notes
# @return one RGB code which represents a mix of the notes which make up the chord
def chord_to_color(beat):
    notes_list = str(beat).split(',')
    rgb_list = []
    for idx in range(len(notes_list)):
        rgb_list.append(note_to_color(notes_list[idx]))
    
    # mix RGB codes
    chord_length = len(rgb_list)
    RED = 0
    GREEN = 0
    BLUE = 0
    for rgb in rgb_list:
        RED = RED + rgb[0]
        GREEN = GREEN + rgb[1]
        BLUE = BLUE + rgb[2]

    rgb_array = [int(RED/chord_length), int(GREEN/chord_length), int(BLUE/chord_length)]
    return rgb_array

def modified_list(rgb_list):
    new_list = rgb_list
    counter = 0
    len_add_white = next_square(len(rgb_list))-len(rgb_list)
    while counter != len_add_white:
        new_list.append([255,255,255])
        counter = counter + 1
    return new_list

def next_square(n):
    next_num = int(sqrt(n)) + 1
    return next_num*next_num

get_chart('output/waltz for debby.csv')                                                                
