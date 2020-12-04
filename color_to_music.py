import ast
import itertools
import csv
import webcolors
import pandas as pd
import numpy as np
from scipy import spatial
import matplotlib.pyplot as plt
import music21 as m
import random

# color = ast.literal_eval(art_rgb.readlines())
print('start')
def color_to_music(textfile, art_name):
    with open(textfile) as f:
        color = f.read().splitlines()

    with open('color data/color_combos.txt') as f:
        color_combos = f.read().splitlines()

    # list of rgb of 32x32 pixelated image
    color = list(map(lambda x: ast.literal_eval(x), color))
    # list of rgb color combos from ryb -> circle of fifths
    color_combos = list(map(lambda x: ast.literal_eval(x), color_combos))

    # match to predetermined color dataset 
    def find_nearest(a, a0):
        array = np.asarray(a)
        "Element in nd array `a` closest to the scalar value `a0`"
        idx = np.abs(array - a0).argmin()
        return array[idx]

    tree = spatial.cKDTree(color_combos)

    match_with_tree = list(map(lambda x: tree.query(x), color))
    diff = list(map(lambda x: x[0], match_with_tree))
    matched_idx = list(map(lambda x: x[1], match_with_tree))


    matched_color = list(map(lambda x: color_combos[x], matched_idx))
    to_hex = list(map(lambda x: webcolors.rgb_to_hex(x), matched_color))

    matched_color_hex = np.array(to_hex)
    matched_color_show = matched_color_hex.reshape(32,32)


    # get matched colors (what colors  make up chord)
    with open('color data/color_combos_dict.txt') as f:
        color_combos_dict = f.read()
    color_combos_dict = ast.literal_eval(color_combos_dict)

    def key_in_dict(k,d):
        if k in d:
            return d[k]

    resulting_notes = list(map(key_in_dict, matched_color, itertools.repeat(color_combos_dict, len(matched_color))))

    # match the resulting colors to the notes
    colors_by_notes = []
    with open('color data/color_chart_rgb.csv') as file:
        reader = csv.reader(file, lineterminator = '\n')
        colors_by_notes = list(reader)
    df_colors = pd.DataFrame(colors_by_notes[1:], columns=colors_by_notes[0])

    # df_colors[df_colors == "#93c76f"].stack().index.tolist()
    # matched_color_hex
    # list(map(lambda x: df_colors[df_colors == str(x)].stack().index.tolist(), matched_color_hex))
    to_note = [list(map(lambda x: df_colors[df_colors == str(x)].stack().index.tolist()[0], x)) for x in resulting_notes]

    a = (1, 'D#')
    str(a[1]+str(a[0]+1))

    final_notes = list()
    for notes in to_note:
        temp = list()
        for note in notes:
            temp.append(str(note[1]+str(note[0]+1)))
        final_notes.append(temp)


    final_output = list()
    offset_range = np.arange(1,7)/2.0
    offset_rand = 0
    offset = 0
    for notes in final_notes:
        if len(notes)==1:
            new_note = m.note.Note(notes)
            new_note.storedInstrument = m.instrument.Piano()
            new_note.offset = offset
            final_output.append(new_note)
        else:
            new_chord = m.chord.Chord(notes)
            new_chord.offset = offset
            final_output.append(new_chord)
        offset += 0.5
        # offset_rand += random.choice(offset_range)

    midi_stream = m.stream.Stream(final_output)
    midi_stream.write('midi', fp=art_name + '.mid')
print('done')
