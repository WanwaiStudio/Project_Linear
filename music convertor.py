import mido
import numpy as np
import sys
import random
import xlwt

from tkinter import * 
from tkinter import filedialog as file
from tkinter import font
from tkinter import messagebox

root = Tk()
root.title("Music Convertor")
root.geometry("800x500")


#================ Background ====================#
bg = PhotoImage(file="Project_Linear/test3.png")
mylabel = Label(root, image=bg)
mylabel.place(x=0, y=0, relwidth=1, relheight=1)

frame = LabelFrame(root, text="test for this",padx=50)
frame.pack()
#================== INP Field ====================#
e = Entry(frame)
e.pack(padx=10,pady = 20)

path_for_generate = []
run = False
midi_file = ()
tempforpath = ''

def save_as():
    path_save = str(file.asksaveasfile(defaultextension='.mid'))
    check = 0
    index = 0
    global tempforpath
    for i in range(len(path_save)):
        print(i)
        if path_save[i] == '=':
            index = i + 2
            break
    for index in range(index,len(path_save)):
        if path_save[index] == 'm':
            break
        elif path_save[index] != 'm':
            tempforpath += path_save[index]
    tempforpath += "mid"
        
    print("Path is : {} len = {}".format(path_save,len(path_save)))
    print("Path is : {}".format(tempforpath))

def browse_file():
    midi_file = file.askopenfilename()
    if midi_file == '':
        pass
    else:
        path_for_generate.append(midi_file)
    e.insert(0,str(path_for_generate))

def generate():
    run = True
    print("midi file : {}".format(path_for_generate))
    global tempforpath
    if run is True and tempforpath != '' :

        np.set_printoptions(threshold=sys.maxsize) #set full output
        note2 = np.zeros((2304,48)).astype(int) #second markov chain
        note2result = np.zeros((2304,48)).astype(int) #second markov chain of result for similarity
        NOTE_NAMES = {0:"C", 1:"C#", 2:"D", 3:"D#", 4:"E", 5:"F", 6:"F#", 7:"G", 8:"G#", 9:"A", 10:"A#", 11:"B"}
        result =[]
        octave = 5
        #add note from midi to list
        for j in range(len(path_for_generate)):
            mid = mido.MidiFile(path_for_generate[j])
            quatergrid=mid.ticks_per_beat/4
            note = [] #note in 1 midi files
            print(mid)
            for i, track in enumerate(mid.tracks):
                for msg in track:
                    if msg.type=='note_on' or msg.type=='note_off':
                        print(msg)
                        time=int(np.ceil(msg.time/quatergrid))
                        if time!=0:
                            if time>4:
                                time = 4
                            note.append(((msg.note%12)*4+time)-1)
            for i in range(len(note)):
                print(NOTE_NAMES[int(np.floor(note[i]/4))]+str((note[i]%4)+1),end=" ")
            for i in range(len(note)-2):
                prevNote2=note[i]
                prevNote1=note[i+1]
                currentNote=note[i+2]
                note2[prevNote2 * 48 + prevNote1][currentNote] += 1


        wb = xlwt.Workbook()
        ws = wb.add_sheet('second markov')
        for i in range(2304):
            temp=''
            temp=temp+str(NOTE_NAMES[np.floor(i/192)])
            temp=temp+str(int(np.floor(i/48)%4+1))
            temp=temp+str(NOTE_NAMES[np.floor((i/4)%12)])
            temp=temp+str((i%4)+1)
            ws.write(i+1,0,temp)
        for j in range(48):
            temp=''
            temp=temp+str(NOTE_NAMES[np.floor(j/4)])
            temp=temp+str((j%4)+1)
            ws.write(0,j+1,temp)
        for i in range(2304):
            for j in range(48):
                #print(note2[i][j],end=" ")
                ws.write(i+1, j+1, int(note2[i][j]))
            #print("")
        wb.save('second markov.xls')

        #output song
        result.append(0)
        result.append(8)
        for i in range(300):
            prevNote2=result[i]
            prevNote1=result[i+1]
            randomtemp=0
            for j in range(48):
                randomtemp+=note2[prevNote2*48+prevNote1][j]
            randomtemp=randomtemp*random.random()
            for j in range(48):
                if randomtemp-note2[prevNote2*48+prevNote1][j]<0 :
                    break
                randomtemp=randomtemp-note2[prevNote2*48+prevNote1][j]
            result.append(j)
            note2result[prevNote2*48+prevNote1][j]+=1
        #midi
        new = mido.MidiFile(type=1)
        track = mido.MidiTrack()
        settrack=mido.MidiTrack()
        settrack.append(mido.MetaMessage('time_signature',numerator=4,denominator=4,clocks_per_click=24,notated_32nd_notes_per_beat=8,time=0))
        settrack.append(mido.MetaMessage('set_tempo',tempo=500000,time=0))
        settrack.append(mido.MetaMessage('end_of_track',time=0))
        track.append(mido.MetaMessage('track_name',name='SONG',time=0))
        track.append(mido.Message('program_change', program=0, time=0))
        for i in range(len(result)):
            noteresult=int(np.floor(result[i]/4))
            timeresult=(result[i]%4)+1
            print(NOTE_NAMES[noteresult],end="")
            print(timeresult)
            #midi
            track.append(mido.Message('note_on', note=octave*12+noteresult, velocity=50, time=0))
            track.append(mido.Message('note_off', note=octave*12+noteresult, velocity=0, time=timeresult*120))
        new.tracks.append(settrack)
        new.tracks.append(track)
        new.save(str(tempforpath))
        print("path save {}".format(tempforpath))
        #cosine similarity
        note2sim=note2.reshape(110592)
        note2resultsim=note2result.reshape(110592)
        similarity_scores = np.dot(note2sim, note2resultsim)/(np.linalg.norm(note2sim)*np.linalg.norm(note2resultsim))
        print(similarity_scores)
        print("finished build")
        tempforpath = ''
        run = False
        messagebox.showinfo("Notification","Done!")
    if tempforpath == '':
        messagebox.showerror("Error","Plese add save path!")






btn1 = Button(frame, text="Browse",command=browse_file)
btn1.pack(pady=10)

btn2 = Button(frame, text="Saveas",command=save_as)
btn2.pack(pady=10)

btn2 = Button(frame, text="Generate",command=generate)
btn2.pack(pady=10)

btn3 = Button(frame, text="Exit",command=root.quit)
btn3.pack(pady=70)













root.mainloop()

