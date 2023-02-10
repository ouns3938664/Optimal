from tkinter import *
import tkinter.messagebox
from tkinter.filedialog import *

root = Tk()
root.title("Optimal")
root.geometry("500x500+100+100")


def selectFile():
    fileOpen = askopenfilename()
    fileContent = open(fileOpen)
    #myLabel1 = Label(text=fileContent.read()).pack()
    myLabel1 = Label(text=fileOpen).pack()


btn1 = Button(root, text='Chose File', fg=('red'), font=30,
              bg='pink', command=selectFile).grid()

root.mainloop()
