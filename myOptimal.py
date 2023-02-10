from tkinter import *
import tkinter.messagebox
from tkinter.filedialog import *
from tkinter import ttk
import csv
import os

csvInput = []

# main page
myWindow = Tk()
myWindow.title("Optimal")
myWindow.geometry("500x170+100+100")


# check input files
def checkInput():
    filePath = fileOpen.get()
    name, extension = os.path.splitext(filePath)

    if extension != '.csv':
        if filePath == '':
            tkinter.messagebox.showerror('Error', 'Your file is empty!')
            myWindow.destroy()
        else:
            tkinter.messagebox.showerror(
                'Error', 'Please select only .csv file!')
            myWindow.destroy()

    if extension == '.csv':
        myWindow.destroy()
        msg = txt.get()
        n = int(msg)
        f = filePath
        readText(n, f)


def readText(n, f):
    root = Tk()
    root.title("Optimal")
    root.geometry("800x500+100+100")

    mainFrame = Frame(root)
    mainFrame.pack(fill=BOTH, expand=1)

    myCanvas = Canvas(mainFrame)
    myCanvas.pack(side=LEFT, fill=BOTH, expand=1)

    myScroll = ttk.Scrollbar(
        mainFrame, orient=VERTICAL, command=myCanvas.yview)
    myScroll.pack(side=RIGHT, fill=Y)

    myCanvas.configure(yscrollcommand=myScroll.set)
    myCanvas.bind('<Configure>', lambda e: myCanvas.configure(
        scrollregion=myCanvas.bbox("all")))

    secondFrame = Frame(myCanvas)

    myCanvas.create_window((0, 0), window=secondFrame, anchor='nw')

    userFrame = int(n)
    pageStatus = ''
    faultCount = 0
    rowCount = 0
    myFrame = []
    priorityList = []

    with open(f) as file:  # file path
        data = csv.reader(file)
        for row in data:
            csvInput.append("{}".format(row[0]))
        refString = [eval(i) for i in csvInput]
        totalRequest = len(refString)
    myLabel1 = Label(secondFrame, text="|  Page  |", fg=('black'),
                     font='Helvetica 14 bold', bg='pink').grid(row=0, column=0)

    for i in range(userFrame):
        label = Label(secondFrame, font='Helvetica 14 bold',
                      text=str(i), bg='#e08dad').grid(row=0, column=i+1)
    label = Label(secondFrame, font='Helvetica 14 bold',
                  text=' |  Page Fault Status', bg='pink').grid(row=0, column=n+1)

    for i in range(userFrame):
        priorityList.append(None)

    for i in range(len(refString)):
        if refString[i] in myFrame:
            pageStatus = 'Page Hit'
            rowCount += 1
        else:
            if len(myFrame) < userFrame:
                myFrame.append(refString[i])
            else:
                for j in range(len(myFrame)):
                    if myFrame[j] not in refString[i+1:]:
                        myFrame[j] = refString[i]
                        break
                    else:
                        priorityList[j] = refString[i+1:].index(myFrame[j])
                else:
                    myFrame[priorityList.index(
                        max(priorityList))] = refString[i]
            faultCount += 1
            rowCount += 1
            pageStatus = 'Page Fault'

        label = Label(secondFrame, font='Helvetica 10 bold',
                      text="%d" % refString[i]).grid(row=i+1, column=0,)

        copyF = myFrame.copy()
        for i in range(len(myFrame)):
            pageVal = copyF.pop(0)
            label = Label(secondFrame, font='Helvetica 9 bold',
                          text=pageVal).grid(row=rowCount, column=i+1,)

        if pageStatus == 'Page Hit':

            label = Label(secondFrame, font='Helvetica 10 bold', fg='green',
                          text=" %s" % pageStatus).grid(row=rowCount, column=userFrame + 1)

        else:

            label = Label(secondFrame, font='Helvetica 10 bold', fg='red',
                          text=" %s" % pageStatus).grid(row=rowCount, column=userFrame + 1)

    faultRate = (faultCount/len(refString))*100

    label = Label(secondFrame, font='Helvetica 10 bold',
                  text='').grid(row=rowCount+2, column=0)
    label = Label(secondFrame, font='Helvetica 15 bold',
                  text='Total requests: %d' % totalRequest, bg='#a9e5e5').grid(row=rowCount+3, column=userFrame + 3, sticky='w')
    label = Label(secondFrame, font='Helvetica 15 bold', text="Total Page Faults: %d" %
                  faultCount, bg='#a9e5e5').grid(row=rowCount+4, column=userFrame+3, sticky='w')
    label = Label(secondFrame, font='Helvetica 15 bold', text='Fault Rate: %0.2f%%' %
                  faultRate, bg='#a9e5e5').grid(row=rowCount+5, column=userFrame + 3, sticky='w')
    root.mainloop()

# input frame form user


def frameInput():
    msg = txt.get()
    if msg != '':
        if msg.isdigit():
            checkInput()
        else:
            tkinter.messagebox.showerror('Error', 'Integer only!')
            pass
    else:
        tkinter.messagebox.showerror('Error', 'Your frame input is empty!')


# file selection
def selectFile():
    fileOpen = askopenfilename()
    os.path.normpath(fileOpen)
    et.insert(0, fileOpen)


# input frame form user
fileOpen = StringVar()
txt = StringVar()
frame = Entry(myWindow, width=20, font=30, textvariable=txt).place(x=250, y=6)
et = Entry(width=20, font=30, textvariable=fileOpen)
et.place(x=250, y=57)

# Label 'Enter number of frames'
Label(text='   Enter number of frames  ',
      font='Helvetica 14 bold',).grid(row=0)
Label(text='').grid(row=1, column=0)

# frame select button
btn1 = Button(myWindow, text='         Chose File         ',
              font='Helvetica 14 bold', bg='dark gray', command=selectFile).grid(row=2)
# Next button
btn2 = Button(myWindow, text='               Next               ',
              font='Helvetica 14 bold', bg='pink', command=frameInput).place(x=20, y=110)

myWindow.mainloop()
