from tkinter import * 
from tkinter import filedialog as file
from tkinter import font

root = Tk()
root.title("Music Convertor")
root.geometry("800x500")


#================ Background ====================#
bg = PhotoImage(file="Project_Linear/test3.png")
mylabel = Label(root, image=bg)
mylabel.place(x=0, y=0, relwidth=1, relheight=1)

frame = LabelFrame(root, text="test for this",padx=50, pady=50)
frame.pack()
#================== INP Field ====================#
e = Entry(frame)
e.pack(padx=10)

path_for_generate = []
path_saveas = []

def save_as():
    path_save = file.asksaveasfilename()
    path_saveas.append(path_save)

def browse_file():
    midi_file = file.askopenfilename()
    if midi_file == '':
        pass
    else:
        path_for_generate.append(midi_file)
    e.insert(0,str(midi_file))

def display_directory():
    print(path_for_generate)






btn1 = Button(frame, text="Browse",command=display_directory)
btn1.pack(pady=10)

btn2 = Button(frame, text="Generate",command=browse_file)
btn2.pack(pady=10)

btn2 = Button(frame, text="Saveas",command=browse_file)
btn2.pack(pady=10)









root.mainloop()