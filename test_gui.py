from tkinter import * 
from PIL import ImageTk,Image
root = Tk()
#title program
root.title('Music Convertor')
root.geometry("1280x720")
bg = PhotoImage(file="Project_Linear/test2.png")
img = ImageTk.PhotoImage(Image.open("Project_Linear/test2.png"))
#input field
e = Entry(root)
e.pack()

#create widget
#myLabel = Label(bg=Image.open("Project_Linear/test2.png"))
#myLabel = Label(image=img,height=480, width=1080)
#myLabel = Label(root, text="Hello world!", width=40, height=20)
#show on screen
#myLabel.pack()
#================================ Button command =========================================#
def save():
    myLabe3 = Label(root, text=e.get())
    myLabe3.pack()

def clicked():
    myLabe2 = Label(root, text="Clicked yeah boiiiiiii")
    myLabe2.pack()

def clear():
    e.delete(0, END)
    a = e.get()
#============================== Button ===============================================#
#create button
myButton1 = Button(root, text="Name", command=save)
#show on screen
myButton1.pack()

myButton2 = Button(root, text="Click!", command=clicked)
myButton2.pack()

myButton3 = Button(root, text="Clear", command=clear)
myButton3.pack()

button_quit = Button(root, text="Exit", command=root.quit)
button_quit.pack()

root.mainloop()

