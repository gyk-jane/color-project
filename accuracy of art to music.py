# seeing if the colors are "accurate" - recreating the song. of course, the rythym is completely disregarded

notes = []
with open('Vincent_Starry_Starry_Night.csv') as file:
    reader = csv.reader(file, lineterminator = '\n')
    notes = list(reader)
 
# convert all fraction to float
for (idx, i) in enumerate(notes):
    if i[0] == 'type':
        continue
    else:
        try:
            i[3] = float(i[3])
        except ValueError:
            nums_length = i[3].split('/')
            i[3] = float(float(nums_length[0])/float(nums_length[1]))
        try:
            i[4] = float(i[4])
        except ValueError:
            nums_offset = i[4].split('/')
            i[4] = float(float(nums_offset[0])/float(nums_offset[1]))
            
# stream (from csv) to midi 
new_stream = m.stream.Stream()
for i in notes:
    if i[0] == 'type':
        continue
    elif i[0] == 'note':
        new_stream.append(m.note.Note(i[1], quarterLength=float(i[3]), offset=float(i[4])))
    elif i[0] == 'chord':
        new_stream.append(m.chord.Chord(i[1].split(','), quarterLength=float(i[3]), offset=float(i[4])))
    else:
        new_stream.append(m.note.Rest(quarterLength=float(i[3]), offset=float(i[4])))

new_stream.write('midi')