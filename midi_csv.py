import music21 as m
import pandas as pd
import re

# return a list of all the notes, chords, and rests in the midi file
def midi_list(midi_file):
    zippedList = []
    cdl = m.converter.parse(midi_file)
    # creating a dataframe of all notes, chords, and rests for analysis
    col_names = ['type', 'note(s)', 'duration_type', 'duration_quarterLength', 'offset', 'quarterLength']
    type_list = []
    notes_list = []
    duration_list = []
    duration_qLength = []
    offset = []
    for x in cdl.recurse().notesAndRests:
        if (x.isNote):
            type_list.append('note')
            notes_list.append(str(x.pitch).replace('-', ''))
            duration_list.append(x.duration.type)
            duration_qLength.append(x.quarterLength)
            offset.append(x.offset)
        if (x.isChord):
            type_list.append('chord')
            
            # take only the notes which make up the chord
            temp_str = str(x).replace('<music21.chord.Chord ', '')
            temp_str = temp_str.replace('>', '')
            temp_str = temp_str.replace('-', '')
            x_str = temp_str.replace(' ', ',')
            notes_list.append(x_str)

            duration_list.append(x.duration.type)
            duration_qLength.append(x.duration.quarterLength)
            offset.append(x.offset)
        if (x.isRest):
            type_list.append('rest')
            notes_list.append('')
            duration_list.append(x.duration.type)
            duration_qLength.append(x.duration.quarterLength)
            offset.append(x.offset)
    zippedList =  list(zip(type_list, notes_list, duration_list, duration_qLength, offset))
    return zippedList

# output a csv and html file of the all note, chords, and rests in the midi file
def get_csv(final_list, song_name):
    col_names = ['type', 'note(s)', 'duration_type', 'duration_quarterLength', 'offset']
    df_orgNotes = pd.DataFrame(final_list, columns = col_names) 
    df_orgNotes.to_html(song_name+'.html', index=False)
    df_orgNotes.to_csv(song_name+'.csv', index=False)

get_csv(midi_list('etc/Beethoven_Symphony_No._5_1st_movement_Piano_solo.mid'), 'Beethoven_Symphony_No._5_1st_movement_Piano_solo')